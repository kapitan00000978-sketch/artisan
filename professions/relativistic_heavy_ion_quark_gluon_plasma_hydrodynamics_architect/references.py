"""Relativistic Heavy-Ion Quark-Gluon Plasma (QGP) Reference Equations.

Formulated by Dr. Kaelen 'The Quark' Sterling,
Principal Relativistic Heavy-Ion Quark-Gluon Plasma (QGP) Hydrodynamics Architect.
"""

from dataclasses import dataclass, field
import math
from typing import Dict, List, Optional, Tuple


# Quantitative Physical Constants & QGP Invariants
KSS_BOUND_ETA_OVER_S: float = 1.0 / (4.0 * math.pi)  # ~0.079577
MIN_ETA_OVER_S: float = 0.08
MAX_ETA_OVER_S: float = 0.20
MAX_ZETA_OVER_S: float = 0.10
MIN_QCD_CRITICAL_TEMP_MEV: float = 150.0
MAX_QCD_CRITICAL_TEMP_MEV: float = 160.0
NOMINAL_QCD_CRITICAL_TEMP_MEV: float = 155.0
MIN_THERMALIZATION_TAU_FM_C: float = 0.20
MAX_THERMALIZATION_TAU_FM_C: float = 0.60
MIN_JET_QUENCHING_QHAT_GEV2_FM: float = 1.20
MIN_ISRAEL_STEWART_RELAXATION_RATIO: float = 5.0
MIN_FREEZEOUT_TEMP_MEV: float = 130.0
MAX_FREEZEOUT_TEMP_MEV: float = 150.0
MIN_ELLIPTIC_FLOW_V2: float = 0.05
MAX_ELLIPTIC_FLOW_V2: float = 0.15
MIN_SOUND_SPEED_SQ_AT_TC: float = 0.14
HBAR_C_MEV_FM: float = 197.32698  # hbar * c in MeV * fm
SPEED_OF_LIGHT: float = 299792458.0


@dataclass
class QGPValidationResult:
    """Diagnostic ledger and certification report for relativistic QGP hydrodynamic simulations."""
    is_valid: bool
    score: float
    violations: List[str] = field(default_factory=list)
    parameters: Dict[str, float] = field(default_factory=dict)
    remediation_notes: List[str] = field(default_factory=list)


def calculate_israel_stewart_shear_relaxation_time(
    eta_over_s: float,
    temperature_mev: float,
    relaxation_ratio: float = 5.0
) -> float:
    """Calculate the Israel-Stewart shear relaxation time tau_pi in fm/c.
    
    tau_pi = relaxation_ratio * (hbar * c * (eta / s)) / T
    """
    if eta_over_s < KSS_BOUND_ETA_OVER_S:
        raise ValueError(f"Shear viscosity ratio {eta_over_s:.4f} violates KSS lower bound {KSS_BOUND_ETA_OVER_S:.4f}.")
    if temperature_mev <= 0.0:
        raise ValueError("Temperature must be strictly positive in MeV.")
    if relaxation_ratio < MIN_ISRAEL_STEWART_RELAXATION_RATIO:
        raise ValueError(f"Relaxation ratio {relaxation_ratio} violates causality minimum {MIN_ISRAEL_STEWART_RELAXATION_RATIO}.")
    
    tau_fm_c = (relaxation_ratio * HBAR_C_MEV_FM * eta_over_s) / temperature_mev
    return tau_fm_c


def calculate_bjorken_energy_density(
    initial_tau_fm_c: float,
    d_et_dy_gev: float,
    transverse_area_fm2: float
) -> float:
    """Calculate Bjorken initial energy density in GeV/fm^3 at proper time tau_0.
    
    epsilon_0 = (dE_T / dy) / (pi * R^2 * tau_0) = (dE_T / dy) / (A_T * tau_0)
    """
    if initial_tau_fm_c <= 0.0:
        raise ValueError("Proper time tau_0 must be strictly positive.")
    if d_et_dy_gev <= 0.0:
        raise ValueError("Transverse energy per unit rapidity must be positive.")
    if transverse_area_fm2 <= 0.0:
        raise ValueError("Transverse nuclear overlap area must be strictly positive.")
    
    return d_et_dy_gev / (transverse_area_fm2 * initial_tau_fm_c)


def calculate_kss_viscosity_margin(eta_over_s: float) -> float:
    """Calculate percentage excess above the Kovtun-Son-Starinets holographic lower bound.
    
    margin = (eta/s - 1/(4*pi)) / (1/(4*pi)) * 100%
    """
    if eta_over_s < 0.0:
        raise ValueError("Shear viscosity to entropy density ratio cannot be negative.")
    return ((eta_over_s - KSS_BOUND_ETA_OVER_S) / KSS_BOUND_ETA_OVER_S) * 100.0


def calculate_speed_of_sound_squared(temperature_mev: float) -> float:
    """Calculate parameterized speed of sound squared c_s^2 across QCD crossover.
    
    At high T >> T_c, c_s^2 -> 1/3 (conformal Stefan-Boltzmann limit).
    At T ~ T_c (155 MeV), c_s^2 reaches its minimum (~0.14-0.16).
    """
    if temperature_mev <= 0.0:
        raise ValueError("Temperature must be strictly positive.")
    
    t_ratio = temperature_mev / NOMINAL_QCD_CRITICAL_TEMP_MEV
    # Smooth parameterization mimicking continuum lattice QCD EoS
    c_s_sq = (1.0 / 3.0) - (0.19 / (1.0 + (t_ratio - 1.0) ** 2))
    return max(0.14, min(1.0 / 3.0, c_s_sq))


def validate_qgp_parameters(
    eta_over_s: float = 0.12,
    zeta_over_s: float = 0.04,
    qcd_critical_temp_mev: float = 155.0,
    thermalization_tau_fm_c: float = 0.40,
    jet_quenching_qhat_gev2_fm: float = 1.65,
    israel_stewart_relaxation_ratio: float = 5.5,
    freezeout_temp_mev: float = 140.0,
    elliptic_flow_v2: float = 0.095,
    sound_speed_sq_tc: float = 0.155,
    custom_weights: Optional[Dict[str, float]] = None
) -> QGPValidationResult:
    """Audit and certify relativistic QGP hydrodynamic parameters against nuclear standards."""
    params: Dict[str, float] = {
        "eta_over_s": eta_over_s,
        "zeta_over_s": zeta_over_s,
        "qcd_critical_temp_mev": qcd_critical_temp_mev,
        "thermalization_tau_fm_c": thermalization_tau_fm_c,
        "jet_quenching_qhat_gev2_fm": jet_quenching_qhat_gev2_fm,
        "israel_stewart_relaxation_ratio": israel_stewart_relaxation_ratio,
        "freezeout_temp_mev": freezeout_temp_mev,
        "elliptic_flow_v2": elliptic_flow_v2,
        "sound_speed_sq_tc": sound_speed_sq_tc,
    }

    violations: List[str] = []
    remediation_notes: List[str] = []
    deductions: float = 0.0

    # 1. Shear Viscosity to Entropy Density Ratio (KSS Bound & QGP Perfect Fluid)
    if eta_over_s < MIN_ETA_OVER_S or eta_over_s > MAX_ETA_OVER_S:
        violations.append(
            f"Shear Viscosity eta/s {eta_over_s:.4f} outside certified QGP window [{MIN_ETA_OVER_S:.4f}, {MAX_ETA_OVER_S:.4f}]: "
            "Breaches KSS quantum lower bound or over-damps collective anisotropic flow."
        )
        remediation_notes.append("Calibrate QGP shear viscosity ratio eta/s within [0.08, 0.20].")
        deductions += 25.0

    # 2. Bulk Viscosity Peak near T_c
    if zeta_over_s > MAX_ZETA_OVER_S:
        violations.append(
            f"Bulk Viscosity zeta/s {zeta_over_s:.3f} > {MAX_ZETA_OVER_S:.3f}: "
            "Excessive bulk viscosity causes unphysical cavitation and negative effective pressures."
        )
        remediation_notes.append("Constrain peak bulk viscosity ratio zeta/s <= 0.10 near deconfinement crossover.")
        deductions += 15.0

    # 3. QCD Critical Crossover Temperature T_c
    if qcd_critical_temp_mev < MIN_QCD_CRITICAL_TEMP_MEV or qcd_critical_temp_mev > MAX_QCD_CRITICAL_TEMP_MEV:
        violations.append(
            f"QCD Critical Temp {qcd_critical_temp_mev:.1f} MeV outside lattice continuum range [{MIN_QCD_CRITICAL_TEMP_MEV:.1f}, {MAX_QCD_CRITICAL_TEMP_MEV:.1f}] MeV."
        )
        remediation_notes.append("Align pseudo-critical deconfinement temperature T_c to 155.0 +/- 5.0 MeV.")
        deductions += 20.0

    # 4. Thermalization Proper Time tau_0
    if thermalization_tau_fm_c < MIN_THERMALIZATION_TAU_FM_C or thermalization_tau_fm_c > MAX_THERMALIZATION_TAU_FM_C:
        violations.append(
            f"Thermalization Time tau_0 {thermalization_tau_fm_c:.2f} fm/c outside pre-equilibrium window [{MIN_THERMALIZATION_TAU_FM_C:.2f}, {MAX_THERMALIZATION_TAU_FM_C:.2f}] fm/c."
        )
        remediation_notes.append("Initialize relativistic hydrodynamics at proper time tau_0 in [0.20, 0.60] fm/c.")
        deductions += 15.0

    # 5. Jet Quenching Parameter q_hat
    if jet_quenching_qhat_gev2_fm < MIN_JET_QUENCHING_QHAT_GEV2_FM:
        violations.append(
            f"Jet Quenching q_hat {jet_quenching_qhat_gev2_fm:.2f} GeV^2/fm < {MIN_JET_QUENCHING_QHAT_GEV2_FM:.2f} GeV^2/fm: "
            "Underestimating radiative partonic energy loss and high-pT hadron suppression R_AA."
        )
        remediation_notes.append("Set jet quenching transport coefficient q_hat >= 1.20 GeV^2/fm.")
        deductions += 15.0

    # 6. Israel-Stewart Relaxation Time Ratio
    if israel_stewart_relaxation_ratio < MIN_ISRAEL_STEWART_RELAXATION_RATIO:
        violations.append(
            f"Israel-Stewart Relaxation Ratio {israel_stewart_relaxation_ratio:.2f} < {MIN_ISRAEL_STEWART_RELAXATION_RATIO:.2f}: "
            "Insufficient relaxation timescale violates relativistic causality; triggers acausal wave propagation."
        )
        remediation_notes.append("Enforce Israel-Stewart shear relaxation time ratio tau_pi / (eta/(s*T)) >= 5.0.")
        deductions += 25.0

    # 7. Particulate Freeze-out Temperature T_fo
    if freezeout_temp_mev < MIN_FREEZEOUT_TEMP_MEV or freezeout_temp_mev > MAX_FREEZEOUT_TEMP_MEV:
        violations.append(
            f"Freeze-out Temperature {freezeout_temp_mev:.1f} MeV outside chemical freeze-out band [{MIN_FREEZEOUT_TEMP_MEV:.1f}, {MAX_FREEZEOUT_TEMP_MEV:.1f}] MeV."
        )
        remediation_notes.append("Trigger Cooper-Frye hadronization sampling at T_fo in [130.0, 150.0] MeV.")
        deductions += 15.0

    # 8. Anisotropic Elliptic Flow v_2
    if elliptic_flow_v2 < MIN_ELLIPTIC_FLOW_V2 or elliptic_flow_v2 > MAX_ELLIPTIC_FLOW_V2:
        violations.append(
            f"Elliptic Flow v_2 {elliptic_flow_v2:.3f} outside experimental mid-central envelope [{MIN_ELLIPTIC_FLOW_V2:.3f}, {MAX_ELLIPTIC_FLOW_V2:.3f}]."
        )
        remediation_notes.append("Calibrate hydrodynamic pressure gradient to achieve v_2 in [0.05, 0.15].")
        deductions += 15.0

    # 9. Speed of Sound Softest Point at T_c
    if sound_speed_sq_tc < MIN_SOUND_SPEED_SQ_AT_TC:
        violations.append(
            f"Speed of Sound c_s^2(T_c) {sound_speed_sq_tc:.3f} < {MIN_SOUND_SPEED_SQ_AT_TC:.3f}: "
            "Softest point too deep, triggering mechanical thermodynamic instability."
        )
        remediation_notes.append("Constrain lattice QCD speed of sound minimum c_s^2(T_c) >= 0.14.")
        deductions += 15.0

    score = max(0.0, 100.0 - deductions)
    is_valid = (score >= 95.0) and (len(violations) == 0)

    return QGPValidationResult(
        is_valid=is_valid,
        score=score,
        violations=violations,
        parameters=params,
        remediation_notes=remediation_notes
    )
