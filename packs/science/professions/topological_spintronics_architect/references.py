"""
Domain references and quantitative mathematical equations for
Dr. Rosalind 'The Lattice' Vance - Principal Topological Insulator & Spintronic Device Architect.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any

# Physical Constants
REDUCED_PLANCK_CONSTANT = 1.054571817e-34  # J s (hbar)
PLANCK_CONSTANT = 6.62607015e-34  # J s (h)
ELEMENTARY_CHARGE = 1.602176634e-19  # C (e)
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K (k_B)
BOHR_MAGNETON = 9.2740100783e-24  # J/T (mu_B)
CONDUCTANCE_QUANTUM = (ELEMENTARY_CHARGE ** 2) / PLANCK_CONSTANT  # e^2 / h ~= 3.874e-5 S

# Quantitative Standards
MIN_SPIN_HALL_ANGLE = 0.50  # Giant spin Hall angle in topological insulators
MAX_SWITCHING_CURRENT_DENSITY_A_M2 = 1.0e11  # 1.0e11 A/m^2 (10^7 A/cm^2) critical SOT limit
MAX_BULK_LEAKAGE_RATIO = 0.05  # 5% maximum parasitic bulk conduction leakage
MIN_TMR_RATIO = 1.50  # 150% minimum room-temperature tunneling magnetoresistance
MIN_THERMAL_STABILITY_FACTOR = 60.0  # 10-year non-volatile retention barrier (Delta = Ku*V / kB*T)
MIN_SURFACE_MOBILITY_CM2_V_S = 2000.0  # Dirac surface state electron mobility
MIN_MEAN_FREE_PATH_NM = 20.0  # Nanometers minimum surface mean free path


VACUUM_PERMEABILITY = 1.25663706212e-6  # H/m (mu_0)


def calculate_sot_switching_current_density(
    gilbert_damping_alpha: float,
    saturation_magnetization_a_m: float,
    ferromagnet_thickness_m: float,
    effective_anisotropy_field_a_m: float,
    spin_hall_angle: float
) -> float:
    """
    Calculate critical SOT switching current density J_c0 = (2 * e * alpha * mu_0 * M_s * t_FM * H_k) / (hbar * theta_SH) in A/m^2.
    """
    if spin_hall_angle <= 0.0 or ferromagnet_thickness_m <= 0.0 or saturation_magnetization_a_m <= 0.0:
        return 0.0
    numerator = (
        2.0 * ELEMENTARY_CHARGE * gilbert_damping_alpha *
        VACUUM_PERMEABILITY * saturation_magnetization_a_m *
        ferromagnet_thickness_m * effective_anisotropy_field_a_m
    )
    denominator = REDUCED_PLANCK_CONSTANT * spin_hall_angle
    return numerator / denominator


def calculate_tmr_ratio(polarization_1: float, polarization_2: float) -> float:
    """Calculate tunneling magnetoresistance ratio TMR = (2 * P1 * P2) / (1 - P1 * P2) via Julliere model."""
    if not (0.0 < polarization_1 < 1.0) or not (0.0 < polarization_2 < 1.0):
        return 0.0
    product = polarization_1 * polarization_2
    if product >= 1.0:
        return 0.0
    return (2.0 * product) / (1.0 - product)


def calculate_thermal_stability(
    effective_anisotropy_j_m3: float,
    magnetic_volume_m3: float,
    temperature_k: float = 300.0
) -> float:
    """Calculate thermal stability factor Delta = (K_u * V) / (k_B * T)."""
    if temperature_k <= 0.0 or effective_anisotropy_j_m3 <= 0.0 or magnetic_volume_m3 <= 0.0:
        return 0.0
    return (effective_anisotropy_j_m3 * magnetic_volume_m3) / (BOLTZMANN_CONSTANT * temperature_k)


def calculate_bulk_leakage_ratio(g_bulk_siemens: float, g_edge_siemens: float) -> float:
    """Calculate bulk parasitic conduction fraction = G_bulk / G_edge."""
    if g_edge_siemens <= 0.0:
        return 1.0
    return g_bulk_siemens / g_edge_siemens


def calculate_mean_free_path_nm(
    fermi_velocity_m_s: float,
    mobility_cm2_v_s: float,
    effective_mass_fraction: float = 0.15
) -> float:
    """
    Calculate surface state transport mean free path l_mfp = (v_F * m* * mu) / e in nanometers.
    """
    if fermi_velocity_m_s <= 0.0 or mobility_cm2_v_s <= 0.0 or effective_mass_fraction <= 0.0:
        return 0.0
    mobility_si = mobility_cm2_v_s * 1.0e-4  # m^2 / (V s)
    m_star = effective_mass_fraction * 9.1093837015e-31  # kg
    l_m = (fermi_velocity_m_s * m_star * mobility_si) / ELEMENTARY_CHARGE
    return l_m * 1.0e9  # nm


@dataclass
class TopologicalSpintronicsValidationResult:
    """Validation report for topological insulator spintronic device physics."""
    spin_hall_angle: float
    switching_current_density_a_m2: float
    tmr_ratio: float
    thermal_stability_factor: float
    bulk_leakage_ratio: float
    mean_free_path_nm: float
    is_valid: bool
    details: Dict[str, Any] = field(default_factory=dict)


def validate_topological_spintronics(
    alpha: float,
    m_s_a_m: float,
    t_fm_m: float,
    h_k_a_m: float,
    theta_sh: float,
    pol_1: float,
    pol_2: float,
    k_u_j_m3: float,
    volume_m3: float,
    g_bulk_s: float,
    g_edge_s: float,
    fermi_vel_m_s: float,
    mobility_cm2_v_s: float,
    temperature_k: float = 300.0
) -> TopologicalSpintronicsValidationResult:
    """Validate topological insulator SOT-MRAM and spintronic cell parameters against quantum bounds."""
    j_c0 = calculate_sot_switching_current_density(alpha, m_s_a_m, t_fm_m, h_k_a_m, theta_sh)
    tmr = calculate_tmr_ratio(pol_1, pol_2)
    delta_th = calculate_thermal_stability(k_u_j_m3, volume_m3, temperature_k)
    leakage = calculate_bulk_leakage_ratio(g_bulk_s, g_edge_s)
    l_mfp = calculate_mean_free_path_nm(fermi_vel_m_s, mobility_cm2_v_s)

    theta_valid = theta_sh >= MIN_SPIN_HALL_ANGLE
    jc0_valid = 0.0 < j_c0 <= MAX_SWITCHING_CURRENT_DENSITY_A_M2
    tmr_valid = tmr >= MIN_TMR_RATIO
    delta_valid = delta_th >= MIN_THERMAL_STABILITY_FACTOR
    leakage_valid = leakage <= MAX_BULK_LEAKAGE_RATIO
    mfp_valid = l_mfp >= MIN_MEAN_FREE_PATH_NM

    all_valid = (
        theta_valid and jc0_valid and tmr_valid and
        delta_valid and leakage_valid and mfp_valid
    )

    details = {
        "spin_hall_angle": theta_sh,
        "theta_valid": theta_valid,
        "switching_current_density_a_cm2": j_c0 / 1.0e4,
        "jc0_valid": jc0_valid,
        "tmr_percent": tmr * 100.0,
        "tmr_valid": tmr_valid,
        "thermal_stability_factor": delta_th,
        "delta_valid": delta_valid,
        "bulk_leakage_ratio": leakage,
        "leakage_valid": leakage_valid,
        "mean_free_path_nm": l_mfp,
        "mfp_valid": mfp_valid
    }

    return TopologicalSpintronicsValidationResult(
        spin_hall_angle=theta_sh,
        switching_current_density_a_m2=j_c0,
        tmr_ratio=tmr,
        thermal_stability_factor=delta_th,
        bulk_leakage_ratio=leakage,
        mean_free_path_nm=l_mfp,
        is_valid=all_valid,
        details=details
    )
