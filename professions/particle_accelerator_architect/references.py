"""Empirical references and physical constants for Particle Accelerators & Relativistic Beam Dynamics.

Maintained by Dr. Julian 'The Accelerator' Vance.
Enforces relativistic Lorentz beam kinematics, Courant-Snyder Twiss parameters,
betatron tune resonance avoidance, and superconducting RF cavity sub-microsecond quench mitigation.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# Speed of light in vacuum (m/s)
SPEED_OF_LIGHT: float = 299792458.0

# Proton rest mass (GeV / c^2)
PROTON_REST_MASS_GEV: float = 0.938272088
ELECTRON_REST_MASS_GEV: float = 0.0005109989

# Elementary charge (Coulombs)
ELEMENTARY_CHARGE: float = 1.602176634e-19


@dataclass(frozen=True)
class RelativisticBeamState:
    """Relativistic particle beam parameters and magnetic rigidity."""
    rest_mass_gev: float
    total_energy_gev: float
    lorentz_gamma: float
    relativistic_beta: float
    magnetic_rigidity_t_m: float
    bunch_intensity_protons: float

    def is_ultra_relativistic(self) -> bool:
        """Verify Lorentz factor exceeds 100.0 (ultra-relativistic regime, v approx c)."""
        return self.lorentz_gamma >= 100.0 and self.relativistic_beta >= 0.9999


@dataclass(frozen=True)
class TwissLatticeState:
    """Courant-Snyder Twiss parameters and betatron tune coordinates."""
    beta_m: float
    alpha: float
    gamma_cs: float
    horizontal_tune_nux: float
    vertical_tune_nuy: float
    emittance_m_rad: float

    def is_symplectic_valid(self) -> bool:
        """Verify Courant-Snyder invariant: beta * gamma - alpha^2 == 1."""
        invariant_diff = abs(self.beta_m * self.gamma_cs - (self.alpha ** 2) - 1.0)
        return invariant_diff <= 1e-3

    def is_resonance_safe(self, min_margin: float = 0.05) -> Tuple[bool, List[str]]:
        """Verify horizontal and vertical tunes are isolated from integer, half, and third resonances."""
        reasons: List[str] = []
        for name, tune in [("horizontal", self.horizontal_tune_nux), ("vertical", self.vertical_tune_nuy)]:
            frac = tune - math.floor(tune)
            # Check integer, half-integer, third-integer, quarter-integer
            for denom in [1, 2, 3, 4]:
                for num in range(denom + 1):
                    target = num / denom
                    diff = abs(frac - target)
                    if diff < min_margin:
                        reasons.append(f"{name} tune {tune:.3f} is dangerously close to {num}/{denom} resonance (delta={diff:.4f} < {min_margin})")
        return (len(reasons) == 0, reasons)


@dataclass(frozen=True)
class SuperconductingCavityState:
    """Superconducting RF (SRF) Niobium cavity parameters and quench interlocks."""
    frequency_mhz: float
    accelerating_gradient_mv_m: float
    quality_factor_q0: float
    cavity_temperature_k: float
    quench_trip_time_us: float
    is_quenched: bool = False

    def is_cavity_safe(self) -> bool:
        """Verify superfluid helium cryogenic temperature and sub-10us fast RF trip."""
        return (
            self.cavity_temperature_k <= 2.0 and
            self.accelerating_gradient_mv_m >= 25.0 and
            self.quality_factor_q0 >= 1e10 and
            self.quench_trip_time_us <= 10.0 and
            not self.is_quenched
        )


@dataclass(frozen=True)
class MachineProtectionState:
    """Machine Protection System (MPS) beam loss monitoring and kicker dump state."""
    beam_loss_fraction: float
    kicker_abort_time_us: float
    vacuum_pressure_pa: float
    interlock_active: bool

    def is_protection_intact(self) -> bool:
        """Verify microsecond kicker abort response and ultra-high vacuum."""
        return (
            self.beam_loss_fraction <= 1e-6 and
            self.kicker_abort_time_us <= 3.0 and
            self.vacuum_pressure_pa <= 1.0e-8 and
            self.interlock_active
        )


@dataclass
class AcceleratorMissionReport:
    """Comprehensive accelerator physics and beam stability evaluation report."""
    machine_id: str
    relativistic_valid: bool
    lattice_stable: bool
    cavity_cryo_ok: bool
    protection_active: bool
    safety_score: float
    anomalies: List[str] = field(default_factory=list)
    summary: str = ""


def calculate_lorentz_gamma(total_energy_gev: float, rest_mass_gev: float = PROTON_REST_MASS_GEV) -> float:
    """Calculate relativistic Lorentz factor gamma = E / (m0 * c^2)."""
    if rest_mass_gev <= 0.0 or total_energy_gev < rest_mass_gev:
        raise ValueError("Total energy must exceed positive rest mass.")
    return total_energy_gev / rest_mass_gev


def calculate_magnetic_rigidity(total_energy_gev: float, rest_mass_gev: float = PROTON_REST_MASS_GEV) -> float:
    """Calculate magnetic beam rigidity (B * rho) in Tesla-meters for singly charged particle."""
    gamma = calculate_lorentz_gamma(total_energy_gev, rest_mass_gev)
    beta = math.sqrt(max(0.0, 1.0 - (1.0 / (gamma ** 2))))
    momentum_gev = gamma * rest_mass_gev * beta
    # B * rho = p / (q * c) => in practical units B * rho [T*m] = p [GeV/c] / 0.299792458
    return momentum_gev / 0.299792458


def calculate_twiss_gamma(beta_m: float, alpha: float) -> float:
    """Calculate Courant-Snyder gamma: gamma_cs = (1 + alpha^2) / beta."""
    if beta_m <= 0.0:
        raise ValueError("Beta function must be strictly positive.")
    return (1.0 + (alpha ** 2)) / beta_m


class AcceleratorReferenceLibrary:
    """Empirical bounds and canonical reference implementation for Particle Accelerator Physics."""

    MIN_LORENTZ_GAMMA: float = 100.0
    MIN_TUNE_RESONANCE_DISTANCE: float = 0.05
    MAX_CAVITY_TEMP_K: float = 2.00
    MAX_QUENCH_TRIP_TIME_US: float = 10.0
    MAX_KICKER_ABORT_TIME_US: float = 3.0
    MAX_UHV_PRESSURE_PA: float = 1.0e-8
    MIN_ACCELERATING_GRADIENT_MV_M: float = 25.0

    @classmethod
    def get_canonical_core(cls) -> str:
        """Returns reference production-grade implementation for accelerator beam executive."""
        return r'''"""Canonical Particle Accelerator Beam Physics & Machine Protection Core.
Authored to the strict physical benchmarks of Dr. Julian Vance.
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class AcceleratorBeamTelemetry:
    total_energy_gev: float
    rest_mass_gev: float
    beta_twiss_m: float
    alpha_twiss: float
    horizontal_tune: float
    vertical_tune: float
    cavity_temp_k: float
    accelerating_gradient_mv_m: float
    quench_trip_latency_us: float
    beam_loss_rate: float
    kicker_abort_latency_us: float
    vacuum_pressure_pa: float


class ParticleBeamExecutive:
    """Deterministic executive managing relativistic particle beams and machine protection."""

    def __init__(self) -> None:
        self.min_lorentz_gamma = 100.0
        self.min_tune_margin = 0.05
        self.max_cavity_temp_k = 2.0
        self.max_quench_latency_us = 10.0
        self.max_abort_latency_us = 3.0
        self.max_uhv_pa = 1.0e-8
        self.is_beam_dump_active = False
        self.dump_reason: Optional[str] = None

    def compute_relativistic_lorentz_state(
        self,
        total_energy_gev: float,
        rest_mass_gev: float
    ) -> Tuple[float, float, float]:
        """Calculate Lorentz factor gamma, beta, and magnetic rigidity in Tesla-meters."""
        gamma = total_energy_gev / max(rest_mass_gev, 1e-6)
        beta = math.sqrt(max(0.0, 1.0 - (1.0 / (gamma ** 2))))
        rigidity_t_m = (total_energy_gev * beta) / 0.299792458
        return (gamma, beta, rigidity_t_m)

    def evaluate_betatron_tune_resonances(
        self,
        tune_x: float,
        tune_y: float
    ) -> Tuple[bool, List[str]]:
        """Verify tunes are isolated from dangerous resonance stopbands."""
        violations: List[str] = []
        for name, tune in [("Horizontal", tune_x), ("Vertical", tune_y)]:
            frac = tune - math.floor(tune)
            for denom in [1, 2, 3, 4]:
                for num in range(denom + 1):
                    target = num / denom
                    diff = abs(frac - target)
                    if diff < self.min_tune_margin:
                        violations.append(f"{name} tune {tune:.3f} encroaches {num}/{denom} resonance (gap={diff:.4f} < {self.min_tune_margin})")
        return (len(violations) == 0, violations)

    def evaluate_telemetry_safety(self, telem: AcceleratorBeamTelemetry) -> Tuple[bool, List[str]]:
        """Ruthlessly audit accelerator telemetry against beam physics invariants."""
        anomalies: List[str] = []

        # 1. Relativistic Lorentz factor check
        gamma, beta, _ = self.compute_relativistic_lorentz_state(telem.total_energy_gev, telem.rest_mass_gev)
        if gamma < self.min_lorentz_gamma:
            anomalies.append(f"Sub-relativistic Lorentz factor gamma={gamma:.1f} < 100.0")

        # 2. Betatron tune resonance check
        tune_ok, tune_reasons = self.evaluate_betatron_tune_resonances(telem.horizontal_tune, telem.vertical_tune)
        if not tune_ok:
            anomalies.extend(tune_reasons)

        # 3. Superconducting RF cavity cryogenic & quench check
        if telem.cavity_temp_k > self.max_cavity_temp_k:
            anomalies.append(f"SRF cavity temperature {telem.cavity_temp_k:.2f}K exceeds 2.0K superfluid limit")
        if telem.quench_trip_latency_us > self.max_quench_latency_us:
            anomalies.append(f"Quench interlock trip latency {telem.quench_trip_latency_us:.1f}us exceeds 10.0us threshold")

        # 4. Machine protection & vacuum check
        if telem.kicker_abort_latency_us > self.max_abort_latency_us:
            anomalies.append(f"Kicker dump abort latency {telem.kicker_abort_latency_us:.1f}us exceeds 3.0us limit")
        if telem.vacuum_pressure_pa > self.max_uhv_pa:
            anomalies.append(f"Beam pipe vacuum {telem.vacuum_pressure_pa:.2e} Pa violates UHV threshold (1.0e-8 Pa)")

        # Fast abort trigger
        if telem.cavity_temp_k > 2.2 or telem.beam_loss_rate > 1e-5 or not tune_ok:
            self.is_beam_dump_active = True
            self.dump_reason = "CRITICAL ACCELERATOR FAULT: Fast kicker magnet extraction to beam absorber"

        return (len(anomalies) == 0, anomalies)

    def trigger_machine_protection_dump(self) -> Dict[str, str]:
        """Fire fast kicker magnets to dump relativistic beam into external absorber."""
        self.is_beam_dump_active = True
        return {
            "status": "BEAM_EXTRACTED_TO_DUMP",
            "kicker_field": "PULSED_MAXIMUM",
            "extraction_latency_us": "2.2",
            "rf_drive": "TRIPPED_TO_ZERO"
        }
'''
