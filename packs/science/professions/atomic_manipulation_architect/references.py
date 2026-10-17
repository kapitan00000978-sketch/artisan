#!/usr/bin/env python3
"""
Scanning Probe Microscopy & Atomic Manipulation References
Domain Invariants: Exponential quantum tunneling current, qPlus quartz tuning fork mechanics,
piezoelectric creep and hysteresis, cryogenic thermal drift, ultra-high vacuum physisorption,
and single-atom placement accuracy.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any, List

ELECTRON_MASS = 9.1093837e-31  # kg
ELEMENTARY_CHARGE = 1.602176634e-19  # C (J per eV)
HBAR = 1.054571817e-34  # J * s


@dataclass
class AtomicManipulationValidationResult:
    is_valid: bool
    thermal_drift_pm_h: float
    vibration_amp_pm: float
    base_pressure_mbar: float
    stage_temp_k: float
    qplus_q_factor: float
    placement_accuracy_pm: float
    violations: List[str] = field(default_factory=list)


def tunneling_decay_constant(work_function_ev: float) -> float:
    """
    Computes inverse decay length kappa (1/m) of electron wave function into vacuum barrier:
    kappa = sqrt(2 * m_e * Phi * e) / hbar
    """
    if work_function_ev <= 0:
        raise ValueError("Work function must be strictly positive.")
    phi_joules = work_function_ev * ELEMENTARY_CHARGE
    return math.sqrt(2.0 * ELECTRON_MASS * phi_joules) / HBAR


def tunneling_current(i0_a: float, z_gap_m: float, work_function_ev: float = 4.0) -> float:
    """
    Computes STM tunneling current across gap z:
    I(z) = I_0 * exp(-2 * kappa * z)
    """
    if i0_a <= 0 or z_gap_m < 0:
        raise ValueError("Current prefactor must be positive and gap non-negative.")
    kappa = tunneling_decay_constant(work_function_ev)
    return i0_a * math.exp(-2.0 * kappa * z_gap_m)


def qplus_frequency_shift(f0_hz: float, spring_const_n_per_m: float, force_gradient_n_per_m: float) -> float:
    """
    Calculates frequency shift Delta_f in frequency-modulation AFM:
    Delta_f = - (f0 / (2 * k)) * (dF_ts / dz)
    """
    if f0_hz <= 0 or spring_const_n_per_m <= 0:
        raise ValueError("Resonance frequency and spring constant must be strictly positive.")
    return - (f0_hz / (2.0 * spring_const_n_per_m)) * force_gradient_n_per_m


def piezo_creep_displacement(x0_m: float, time_sec: float, t0_sec: float = 1.0, beta: float = 0.01) -> float:
    """
    Calculates time-dependent logarithmic creep displacement of piezoelectric actuator:
    x(t) = x0 * (1 + beta * ln(t / t0)) for t > t0.
    """
    if x0_m < 0 or time_sec <= 0 or t0_sec <= 0:
        raise ValueError("Displacement and time arguments must be positive.")
    if time_sec <= t0_sec:
        return x0_m
    return x0_m * (1.0 + beta * math.log(time_sec / t0_sec))


def validate_atomic_microscope(
    thermal_drift_pm_h: float,
    vibration_amp_pm: float,
    base_pressure_mbar: float,
    stage_temp_k: float,
    qplus_q_factor: float,
    placement_accuracy_pm: float
) -> AtomicManipulationValidationResult:
    """
    Validates a scanning probe microscope and atomic manipulation instrument against
    sub-atomic spatial resolution and cryogenic vacuum invariants.
    """
    violations = []

    # 1. Thermal Drift Rate (<= 5.0 pm/hour)
    if thermal_drift_pm_h > 5.0:
        violations.append(
            f"Thermal drift {thermal_drift_pm_h:.1f} pm/h > 5.0 pm/h threshold; causes lattice distortion and tip crashes."
        )

    # 2. Tip-Sample Vibration Amplitude (<= 1.0 pm)
    if vibration_amp_pm > 1.0:
        violations.append(
            f"Tip-sample vibration amplitude {vibration_amp_pm:.2f} pm > 1.0 pm limit; destroys single-atom spatial resolution."
        )

    # 3. UHV Base Pressure (<= 1.0e-10 mbar)
    if base_pressure_mbar > 1.0e-10:
        violations.append(
            f"Base pressure {base_pressure_mbar:.2e} mbar > 1.0e-10 mbar limit; residual gas poisons pristine crystalline surface."
        )

    # 4. Cryogenic Stage Temperature (<= 4.5 K)
    if stage_temp_k > 4.5:
        violations.append(
            f"Stage temperature {stage_temp_k:.1f} K > 4.5 K threshold; thermal diffusion causes adatoms to escape manipulation sites."
        )

    # 5. qPlus Resonator Q-Factor (>= 25,000)
    if qplus_q_factor < 25000.0:
        violations.append(
            f"qPlus tuning fork Q-factor {qplus_q_factor:.0f} < 25,000 minimum; insufficient force gradient sensitivity."
        )

    # 6. Atomic Placement Accuracy (<= 20.0 pm)
    if placement_accuracy_pm > 20.0:
        violations.append(
            f"Atomic positioning accuracy {placement_accuracy_pm:.1f} pm > 20.0 pm threshold; fails quantum corral atomic tolerances."
        )

    is_valid = (len(violations) == 0)
    return AtomicManipulationValidationResult(
        is_valid=is_valid,
        thermal_drift_pm_h=thermal_drift_pm_h,
        vibration_amp_pm=vibration_amp_pm,
        base_pressure_mbar=base_pressure_mbar,
        stage_temp_k=stage_temp_k,
        qplus_q_factor=qplus_q_factor,
        placement_accuracy_pm=placement_accuracy_pm,
        violations=violations
    )
