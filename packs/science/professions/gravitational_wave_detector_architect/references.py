#!/usr/bin/env python3
"""
Gravitational Wave Detector & Optomechanical Interferometry References
Domain Invariants: Dimensionless strain sensitivity, squeezed vacuum injection,
Fabry-Perot arm cavity power, quadruple pendulum seismic isolation, Newtonian noise subtraction,
and Pound-Drever-Hall laser stabilization.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any, List

SPEED_OF_LIGHT = 299792458.0  # m / s
PLANCK_CONSTANT = 6.62607015e-34  # J * s
HBAR = PLANCK_CONSTANT / (2.0 * math.pi)


@dataclass
class GravitationalWaveValidationResult:
    is_valid: bool
    strain_sensitivity_hz: float
    squeezing_factor_db: float
    cavity_power_kw: float
    seismic_transfer_at_10hz: float
    newtonian_subtraction_pct: float
    lock_jitter_m: float
    violations: List[str] = field(default_factory=list)


def strain_sensitivity(delta_l_m: float, arm_length_m: float = 4000.0) -> float:
    """
    Computes dimensionless space-time metric perturbation strain:
    h = 2 * Delta_L / L
    where arm_length_m defaults to 4000 m (4 km LIGO baseline).
    """
    if arm_length_m <= 0:
        raise ValueError("Arm length must be strictly positive.")
    if delta_l_m < 0:
        raise ValueError("Displacement differential cannot be negative magnitude.")
    return (2.0 * delta_l_m) / arm_length_m


def fabry_perot_power(input_power_w: float, finesse: float) -> float:
    """
    Computes circulating optical power in a resonant Fabry-Perot arm cavity:
    P_cav = P_in * (2 * Finesse / pi)
    """
    if input_power_w < 0:
        raise ValueError("Input laser power must be non-negative.")
    if finesse <= 0:
        raise ValueError("Cavity finesse must be strictly positive.")
    power_gain = (2.0 * finesse) / math.pi
    return input_power_w * power_gain


def squeezed_light_noise_reduction(squeezing_db: float) -> float:
    """
    Calculates quantum noise power reduction factor from non-classical squeezed vacuum injection:
    factor = 10^(-squeezing_db / 10)
    """
    if squeezing_db < 0:
        raise ValueError("Squeezing factor in dB must be non-negative.")
    return 10.0 ** (-squeezing_db / 10.0)


def pdh_frequency_error(phase_rad: float, modulation_freq_hz: float = 9.0e6) -> float:
    """
    Calculates Pound-Drever-Hall error signal discriminator slope for laser phase/frequency lock:
    error = phase_rad * modulation_freq_hz
    """
    if modulation_freq_hz <= 0:
        raise ValueError("Modulation frequency must be strictly positive.")
    return phase_rad * modulation_freq_hz


def quad_pendulum_transfer_function(freq_hz: float, f0_hz: float = 1.0) -> float:
    """
    Calculates high-frequency seismic transfer function through a 4-stage monolithic pendulum:
    |T(f)| approx (f0 / f)^8 for f > f0.
    At f <= f0, returns 1.0 (unity transmission without resonance enhancement).
    """
    if freq_hz <= 0 or f0_hz <= 0:
        raise ValueError("Frequencies must be strictly positive.")
    if freq_hz <= f0_hz:
        return 1.0
    return (f0_hz / freq_hz) ** 8


def newtonian_noise_residual(raw_nn: float, subtraction_efficiency_pct: float) -> float:
    """
    Computes residual gravity gradient noise after array subtraction:
    residual = raw_nn * (1.0 - subtraction_efficiency_pct / 100.0)
    """
    if raw_nn < 0:
        raise ValueError("Raw Newtonian noise must be non-negative.")
    if not (0.0 <= subtraction_efficiency_pct <= 100.0):
        raise ValueError("Subtraction efficiency must be between 0 and 100%.")
    return raw_nn * (1.0 - (subtraction_efficiency_pct / 100.0))


def validate_gravitational_wave_detector(
    strain_sensitivity_hz: float,
    squeezing_factor_db: float,
    cavity_power_kw: float,
    seismic_transfer_at_10hz: float,
    newtonian_subtraction_pct: float,
    lock_jitter_m: float
) -> GravitationalWaveValidationResult:
    """
    Validates a gravitational wave interferometer against astrophysical sensitivity
    and optomechanical quantum invariants.
    """
    violations = []

    # 1. Strain Sensitivity (<= 1.0e-23 Hz^-1/2)
    if strain_sensitivity_hz > 1.0e-23:
        violations.append(
            f"Strain sensitivity {strain_sensitivity_hz:.2e} Hz^-1/2 exceeds 1.0e-23 Hz^-1/2 limit; astrophysical reach blind."
        )

    # 2. Squeezed Light Injection Factor (>= 6.0 dB)
    if squeezing_factor_db < 6.0:
        violations.append(
            f"Squeezing factor {squeezing_factor_db:.1f} dB < 6.0 dB minimum; failure to evade Standard Quantum Limit."
        )

    # 3. Arm Cavity Stored Power (>= 500.0 kW)
    if cavity_power_kw < 500.0:
        violations.append(
            f"Arm cavity power {cavity_power_kw:.1f} kW < 500.0 kW threshold; excessive photon shot noise."
        )

    # 4. Seismic Stack Isolation (|T| <= 1.0e-10 at 10 Hz)
    if seismic_transfer_at_10hz > 1.0e-10:
        violations.append(
            f"Seismic isolation transfer {seismic_transfer_at_10hz:.2e} > 1.0e-10 limit; seismic wall low-frequency saturation."
        )

    # 5. Newtonian Noise Subtraction (>= 80.0%)
    if newtonian_subtraction_pct < 80.0:
        violations.append(
            f"Newtonian noise subtraction {newtonian_subtraction_pct:.1f}% < 80.0% requirement; terrestrial gravity gradient unmitigated."
        )

    # 6. Differential Arm Lock Jitter (<= 1.0e-15 m)
    if lock_jitter_m > 1.0e-15:
        violations.append(
            f"Differential lock jitter {lock_jitter_m:.2e} m > 1.0e-15 m limit; loss of dark port destructive interference."
        )

    is_valid = (len(violations) == 0)
    return GravitationalWaveValidationResult(
        is_valid=is_valid,
        strain_sensitivity_hz=strain_sensitivity_hz,
        squeezing_factor_db=squeezing_factor_db,
        cavity_power_kw=cavity_power_kw,
        seismic_transfer_at_10hz=seismic_transfer_at_10hz,
        newtonian_subtraction_pct=newtonian_subtraction_pct,
        lock_jitter_m=lock_jitter_m,
        violations=violations
    )
