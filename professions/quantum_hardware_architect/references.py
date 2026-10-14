"""Quantum Hardware, Microwave Pulse Shaping & Qubit Control Standards.

Author: Dr. Alistair 'The Flux' Vance
Status: Production Reference Standard
"""

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# Physical & Engineering Constants
MIN_SINGLE_QUBIT_FIDELITY: float = 0.999
MIN_TWO_QUBIT_FIDELITY: float = 0.995
MIN_T1_RELAXATION_US: float = 50.0
MIN_T2_DEPHASING_US: float = 30.0
DEFAULT_ANHARMONICITY_MHZ: float = -300.0
AWG_SAMPLE_RATE_GSPS: float = 2.4  # 2.4 Giga-samples/sec
MAX_CIRCUIT_COHERENCE_RATIO: float = 0.05
DEFAULT_DISPERSIVE_SHIFT_CHI_MHZ: float = -1.5


@dataclass(frozen=True)
class QubitCoherenceProfile:
    """Represents the physical decoherence parameters of a superconducting transmon."""
    qubit_id: int
    t1_us: float
    t2_us: float
    frequency_ghz: float
    anharmonicity_mhz: float = DEFAULT_ANHARMONICITY_MHZ

    def relaxation_rate_khz(self) -> float:
        """Compute longitudinal relaxation rate Gamma_1 = 1 / T_1 in kHz."""
        if self.t1_us <= 0.0:
            return float("inf")
        return 1000.0 / self.t1_us

    def dephasing_rate_khz(self) -> float:
        """Compute transverse dephasing rate Gamma_2 = 1 / T_2* in kHz."""
        if self.t2_us <= 0.0:
            return float("inf")
        return 1000.0 / self.t2_us

    def is_physically_sound(self) -> Tuple[bool, List[str]]:
        """Validate transmon parameters against physical limits (e.g. T2 <= 2*T1)."""
        reasons = []
        if self.t1_us < MIN_T1_RELAXATION_US:
            reasons.append(f"T1 relaxation too low: {self.t1_us:.1f}us < {MIN_T1_RELAXATION_US}us")
        if self.t2_us < MIN_T2_DEPHASING_US:
            reasons.append(f"T2* dephasing too low: {self.t2_us:.1f}us < {MIN_T2_DEPHASING_US}us")
        # Physical thermodynamic limit: T2 <= 2*T1
        if self.t2_us > 2.0 * self.t1_us:
            reasons.append(f"Unphysical dephasing: T2 ({self.t2_us:.1f}us) > 2*T1 ({2*self.t1_us:.1f}us)")
        if self.anharmonicity_mhz >= 0.0:
            reasons.append(f"Transmons must have negative anharmonicity (alpha < 0): got {self.anharmonicity_mhz}MHz")
        return len(reasons) == 0, reasons


@dataclass
class DragPulse:
    """Derivative Removal by Adiabatic Gate (DRAG) microwave pulse waveform."""
    duration_ns: float
    amplitude: float
    sigma_ns: float
    beta_drag: float
    phase_rad: float = 0.0

    def generate_waveform(self, sample_rate_gsps: float = AWG_SAMPLE_RATE_GSPS) -> Tuple[List[float], List[float]]:
        """Generate in-phase I(t) and quadrature Q(t) samples discretized on the AWG clock."""
        num_samples = int(round(self.duration_ns * sample_rate_gsps))
        dt = 1.0 / sample_rate_gsps  # ns per sample
        t0 = self.duration_ns / 2.0

        i_samples = []
        q_samples = []

        for idx in range(num_samples):
            t = (idx + 0.5) * dt - t0
            # Gaussian envelope I(t)
            gauss = self.amplitude * math.exp(-(t ** 2) / (2.0 * (self.sigma_ns ** 2)))
            # DRAG correction: Q(t) proportional to -dI/dt
            # dI/dt = - (t / sigma^2) * I(t)
            # Q(t) = - beta * dI/dt = + beta * (t / sigma^2) * I(t)
            deriv = -(t / (self.sigma_ns ** 2)) * gauss
            drag_q = -self.beta_drag * deriv

            # Apply carrier phase rotation
            i_rot = gauss * math.cos(self.phase_rad) - drag_q * math.sin(self.phase_rad)
            q_rot = gauss * math.sin(self.phase_rad) + drag_q * math.cos(self.phase_rad)

            i_samples.append(i_rot)
            q_samples.append(q_rot)

        return i_samples, q_samples

    def validate(self) -> Tuple[bool, List[str]]:
        """Verify pulse parameters against physical control constraints."""
        errors = []
        if self.duration_ns <= 0.0:
            errors.append(f"Invalid duration: {self.duration_ns}ns must be positive")
        if self.amplitude <= 0.0 or self.amplitude > 1.0:
            errors.append(f"Amplitude out of DAC range (0.0, 1.0]: got {self.amplitude}")
        if self.sigma_ns <= 0.0 or (4.0 * self.sigma_ns > self.duration_ns):
            errors.append(f"Gaussian truncation error: duration ({self.duration_ns}ns) must exceed 4*sigma ({4*self.sigma_ns}ns)")
        return len(errors) == 0, errors


@dataclass
class ReadoutResonator:
    """Dispersive readout resonator coupled to a superconducting transmon."""
    qubit_id: int
    bare_frequency_ghz: float
    dispersive_shift_chi_mhz: float = DEFAULT_DISPERSIVE_SHIFT_CHI_MHZ
    integration_window_ns: float = 1000.0

    def ground_state_frequency_ghz(self) -> float:
        """Resonator frequency when transmon is in |0> state."""
        return self.bare_frequency_ghz + (self.dispersive_shift_chi_mhz / 1000.0)

    def excited_state_frequency_ghz(self) -> float:
        """Resonator frequency when transmon is in |1> state."""
        return self.bare_frequency_ghz - (self.dispersive_shift_chi_mhz / 1000.0)

    def frequency_separation_mhz(self) -> float:
        """Peak-to-peak frequency separation 2*|chi| between |0> and |1> states."""
        return 2.0 * abs(self.dispersive_shift_chi_mhz)


@dataclass
class QuantumGatePulse:
    """Calibrated quantum control gate with duration, DRAG pulse shape, and fidelity."""
    name: str
    target_qubits: List[int]
    pulse: DragPulse
    fidelity: float

    def is_certified(self) -> bool:
        """Verify whether gate meets state-of-the-art quantum volume threshold."""
        threshold = MIN_TWO_QUBIT_FIDELITY if len(self.target_qubits) >= 2 else MIN_SINGLE_QUBIT_FIDELITY
        return self.fidelity >= threshold


@dataclass
class QuantumCircuitSchedule:
    """Validated timeline of quantum microwave control pulses across multiqubit chip."""
    qubits: List[QubitCoherenceProfile]
    gates: List[QuantumGatePulse] = field(default_factory=list)

    def total_duration_ns(self) -> float:
        """Total execution time of the scheduled pulse sequence."""
        return sum(gate.pulse.duration_ns for gate in self.gates)

    def validate_coherence_budget(self) -> Tuple[bool, List[str]]:
        """Ensure total pulse circuit time does not exceed coherence decoherence budget."""
        reasons = []
        circuit_time_us = self.total_duration_ns() / 1000.0

        for q in self.qubits:
            budget_us = MAX_CIRCUIT_COHERENCE_RATIO * min(q.t1_us, q.t2_us)
            if circuit_time_us > budget_us:
                reasons.append(
                    f"Qubit {q.qubit_id}: circuit duration {circuit_time_us:.3f}us exceeds 5% coherence budget ({budget_us:.3f}us)"
                )
        return len(reasons) == 0, reasons


class QuantumHardwareReferenceLibrary:
    """Canonical repository of superconducting transmon & microwave pulse engineering."""

    @staticmethod
    def get_benchmarks() -> Dict[str, Any]:
        return {
            "min_1q_fidelity": MIN_SINGLE_QUBIT_FIDELITY,
            "min_2q_fidelity": MIN_TWO_QUBIT_FIDELITY,
            "min_t1_us": MIN_T1_RELAXATION_US,
            "min_t2_us": MIN_T2_DEPHASING_US,
            "default_anharmonicity_mhz": DEFAULT_ANHARMONICITY_MHZ,
            "awg_sample_rate_gsps": AWG_SAMPLE_RATE_GSPS,
            "max_circuit_coherence_ratio": MAX_CIRCUIT_COHERENCE_RATIO,
        }

    @staticmethod
    def get_anti_patterns() -> List[str]:
        return [
            "Driving transmon gates with raw unshaped square pulses causing |2> state leakage",
            "Executing pulse schedules that exceed qubit T1 and T2* coherence horizons",
            "Accepting single-qubit gates with fidelity < 0.999 or two-qubit gates < 0.995",
            "Omitting DRAG quadrature derivative correction on fast microwave gates (<30ns)",
            "Uncalibrated dispersive readout without Chi shift modeling or integration windows",
            "Static ZZ frequency collision between adjacent capacitively coupled qubits",
        ]

    @staticmethod
    def get_calibration_checklist() -> List[str]:
        return [
            "Calibrate transmon frequencies and verify negative anharmonicity alpha ~ -300 MHz",
            "Perform Ramsey fringe experiment to extract T2* and echo to extract T2e",
            "Tune DRAG beta parameter to eliminate leakage into |2> non-computational state",
            "Measure Randomized Benchmarking (RB) curve to verify fidelity >= 0.999",
            "Calibrate dispersive readout cavity frequency and optimize IQ demodulation weights",
            "Verify AWG sample clock quantization alignment (2.4 Gsps grid)",
        ]

    @staticmethod
    def get_canonical_core() -> str:
        return r'''"""Canonical Quantum Hardware & Microwave Pulse Shaping Engine.
Standards: Transmon Hamiltonian, DRAG Waveforms, Coherence Verification (T1, T2*)
"""

import math
from typing import Dict, Any, List, Tuple

AWG_SAMPLE_RATE_GSPS = 2.4
MIN_SINGLE_QUBIT_FIDELITY = 0.999
MIN_T1_US = 50.0
MIN_T2_US = 30.0

class QubitCoherenceProfile:
    """Superconducting transmon qubit coherence and frequency profile."""

    def __init__(self, qubit_id: int, t1_us: float, t2_us: float, freq_ghz: float, anharmonicity_mhz: float = -300.0):
        self.qubit_id = qubit_id
        self.t1_us = t1_us
        self.t2_us = t2_us
        self.freq_ghz = freq_ghz
        self.anharmonicity_mhz = anharmonicity_mhz

    def is_sound(self) -> bool:
        return (
            self.t1_us >= MIN_T1_US and
            self.t2_us >= MIN_T2_US and
            self.t2_us <= 2.0 * self.t1_us and
            self.anharmonicity_mhz < 0.0
        )

class DragPulse:
    """Derivative Removal by Adiabatic Gate (DRAG) microwave waveform generator."""

    def __init__(self, duration_ns: float, amplitude: float, sigma_ns: float, beta_drag: float, phase_rad: float = 0.0):
        self.duration_ns = duration_ns
        self.amplitude = amplitude
        self.sigma_ns = sigma_ns
        self.beta_drag = beta_drag
        self.phase_rad = phase_rad

    def generate_waveform(self, sample_rate_gsps: float = AWG_SAMPLE_RATE_GSPS) -> Tuple[List[float], List[float]]:
        num_samples = int(round(self.duration_ns * sample_rate_gsps))
        dt = 1.0 / sample_rate_gsps
        t0 = self.duration_ns / 2.0
        i_samples, q_samples = [], []
        for idx in range(num_samples):
            t = (idx + 0.5) * dt - t0
            gauss = self.amplitude * math.exp(-(t ** 2) / (2.0 * (self.sigma_ns ** 2)))
            deriv = -(t / (self.sigma_ns ** 2)) * gauss
            drag_q = -self.beta_drag * deriv
            i_samples.append(gauss * math.cos(self.phase_rad) - drag_q * math.sin(self.phase_rad))
            q_samples.append(gauss * math.sin(self.phase_rad) + drag_q * math.cos(self.phase_rad))
        return i_samples, q_samples

class ReadoutResonator:
    """Dispersive readout resonator model."""

    def __init__(self, qubit_id: int, bare_freq_ghz: float, dispersive_shift_mhz: float = -1.5):
        self.qubit_id = qubit_id
        self.bare_freq_ghz = bare_freq_ghz
        self.dispersive_shift_mhz = dispersive_shift_mhz

    def separation_mhz(self) -> float:
        return 2.0 * abs(self.dispersive_shift_mhz)

def verify_gate_fidelity(fidelity: float, is_two_qubit: bool = False) -> bool:
    threshold = 0.995 if is_two_qubit else MIN_SINGLE_QUBIT_FIDELITY
    return fidelity >= threshold
'''
