"""
Domain references and quantitative mathematical equations for
Dr. Taras 'The Superfluid' Sterling - Principal Superfluid Quantum Hydrodynamics & Helium-4 Vortex Architect.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any

# Physical Constants
PLANCK_CONSTANT = 6.62607015e-34  # J s (h)
REDUCED_PLANCK_CONSTANT = 1.054571817e-34  # J s (hbar)
HELIUM4_MASS = 6.6464764e-27  # kg (m_He4)
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K (k_B)

# Superfluid Helium-4 Reference Constants
LAMBDA_TEMPERATURE_K = 2.1768  # K (T_lambda at saturated vapor pressure)
LIQUID_HELIUM_DENSITY = 145.1  # kg/m^3 (rho at 1.8 K)
CIRCULATION_QUANTUM = PLANCK_CONSTANT / HELIUM4_MASS  # kappa = h / m_He4 ~= 9.9693e-8 m^2/s
VORTEX_CORE_RADIUS_M = 1.0e-10  # a_0 = 1.0 Angstrom (0.1 nm)
LANDAU_ROTON_VELOCITY_M_S = 58.0  # v_L ~= 58.0 m/s roton excitation threshold

# Quantitative Standards
MAX_SUPERFLUID_TEMPERATURE_K = 2.10  # K maximum allowable for He-II phase
MIN_SUPERFLUID_FRACTION = 0.50  # 50% minimum superfluid density fraction (rho_s / rho)
MAX_SUPERFLUID_VELOCITY_M_S = 50.0  # m/s operating ceiling below Landau roton threshold
MAX_VORTEX_LINE_DENSITY_M2 = 1.0e12  # m^-2 maximum vortex tangle density before thermal choking
MAX_SUPERLEAK_PORE_NM = 10.0  # nm maximum superleak pore diameter for viscous clamping
MIN_SECOND_SOUND_VELOCITY_M_S = 12.0  # m/s minimum second sound propagation speed


def calculate_superfluid_fraction(temperature_k: float) -> float:
    """Calculate superfluid density fraction rho_s / rho = (1 - (T / T_lambda)^5.6) empirically."""
    if temperature_k >= LAMBDA_TEMPERATURE_K:
        return 0.0
    if temperature_k <= 0.0:
        return 1.0
    # Standard Gorter-Mellink / Khalatnikov empirical power law
    ratio = temperature_k / LAMBDA_TEMPERATURE_K
    fraction = 1.0 - (ratio ** 5.6)
    return max(0.0, min(1.0, fraction))


def calculate_feynman_critical_velocity(channel_diameter_m: float) -> float:
    """Calculate Feynman critical vortex nucleation velocity v_c = (hbar / (m_He4 * d)) * ln(d / a_0)."""
    if channel_diameter_m <= VORTEX_CORE_RADIUS_M:
        return LANDAU_ROTON_VELOCITY_M_S
    prefactor = REDUCED_PLANCK_CONSTANT / (HELIUM4_MASS * channel_diameter_m)
    log_factor = math.log(channel_diameter_m / VORTEX_CORE_RADIUS_M)
    v_c = prefactor * log_factor
    return min(LANDAU_ROTON_VELOCITY_M_S, v_c)


def calculate_fountain_pressure(
    density_kg_m3: float,
    entropy_j_kg_k: float,
    delta_t_k: float
) -> float:
    """Calculate London thermomechanical fountain pressure Delta P = rho * S * Delta T in Pascals."""
    if density_kg_m3 <= 0.0 or entropy_j_kg_k <= 0.0 or delta_t_k <= 0.0:
        return 0.0
    return density_kg_m3 * entropy_j_kg_k * delta_t_k


def calculate_second_sound_velocity(
    rho_s_fraction: float,
    entropy_j_kg_k: float,
    temperature_k: float,
    specific_heat_j_kg_k: float
) -> float:
    """
    Calculate second sound thermal wave propagation velocity:
    c_2 = sqrt((rho_s / rho_n) * (S^2 * T / C_v)) in m/s.
    """
    if rho_s_fraction <= 0.0 or rho_s_fraction >= 1.0:
        return 0.0
    rho_n_fraction = 1.0 - rho_s_fraction
    if rho_n_fraction <= 0.0 or specific_heat_j_kg_k <= 0.0 or temperature_k <= 0.0:
        return 0.0
    term1 = rho_s_fraction / rho_n_fraction
    term2 = (entropy_j_kg_k ** 2) * temperature_k / specific_heat_j_kg_k
    val = term1 * term2
    if val <= 0.0:
        return 0.0
    return math.sqrt(val)


def calculate_vortex_mutual_friction(
    rho_s_fraction: float,
    vortex_line_density_m2: float,
    relative_velocity_m_s: float,
    mutual_friction_coeff_b: float = 1.5
) -> float:
    """
    Calculate Vinen-Hall mutual friction force density F_sn = B * (rho_s * rho_n / (2 * rho)) * kappa * L * (v_s - v_n).
    Returns normalized force per unit volume / rho in m/s^2.
    """
    if rho_s_fraction <= 0.0 or rho_s_fraction >= 1.0 or vortex_line_density_m2 <= 0.0:
        return 0.0
    rho_n_fraction = 1.0 - rho_s_fraction
    return mutual_friction_coeff_b * (rho_s_fraction * rho_n_fraction / 2.0) * CIRCULATION_QUANTUM * vortex_line_density_m2 * relative_velocity_m_s


@dataclass
class SuperfluidHydroValidationResult:
    """Validation report for superfluid helium-4 quantum hydrodynamics."""
    temperature_k: float
    superfluid_fraction: float
    superfluid_velocity_m_s: float
    second_sound_velocity_m_s: float
    vortex_line_density_m2: float
    superleak_pore_nm: float
    is_valid: bool
    details: Dict[str, Any] = field(default_factory=dict)


def validate_superfluid_hydrodynamics(
    temperature_k: float,
    velocity_m_s: float,
    entropy_j_kg_k: float,
    specific_heat_j_kg_k: float,
    vortex_line_density_m2: float,
    superleak_pore_nm: float,
    channel_diameter_m: float = 1.0e-3
) -> SuperfluidHydroValidationResult:
    """Validate superfluid quantum hydrodynamic state and vortex tangle bounds."""
    rho_s_frac = calculate_superfluid_fraction(temperature_k)
    c2 = calculate_second_sound_velocity(rho_s_frac, entropy_j_kg_k, temperature_k, specific_heat_j_kg_k)
    v_c_feynman = calculate_feynman_critical_velocity(channel_diameter_m)

    temp_valid = 0.0 < temperature_k <= MAX_SUPERFLUID_TEMPERATURE_K
    fraction_valid = rho_s_frac >= MIN_SUPERFLUID_FRACTION
    velocity_valid = 0.0 <= velocity_m_s <= MAX_SUPERFLUID_VELOCITY_M_S
    c2_valid = c2 >= MIN_SECOND_SOUND_VELOCITY_M_S
    vortex_valid = 0.0 <= vortex_line_density_m2 <= MAX_VORTEX_LINE_DENSITY_M2
    pore_valid = 0.0 < superleak_pore_nm <= MAX_SUPERLEAK_PORE_NM

    all_valid = (
        temp_valid and fraction_valid and velocity_valid and
        c2_valid and vortex_valid and pore_valid
    )

    details = {
        "temperature_k": temperature_k,
        "temp_valid": temp_valid,
        "superfluid_fraction": rho_s_frac,
        "fraction_valid": fraction_valid,
        "superfluid_velocity_m_s": velocity_m_s,
        "velocity_valid": velocity_valid,
        "second_sound_velocity_m_s": c2,
        "c2_valid": c2_valid,
        "vortex_line_density_m2": vortex_line_density_m2,
        "vortex_valid": vortex_valid,
        "superleak_pore_nm": superleak_pore_nm,
        "pore_valid": pore_valid,
        "feynman_critical_velocity_m_s": v_c_feynman
    }

    return SuperfluidHydroValidationResult(
        temperature_k=temperature_k,
        superfluid_fraction=rho_s_frac,
        superfluid_velocity_m_s=velocity_m_s,
        second_sound_velocity_m_s=c2,
        vortex_line_density_m2=vortex_line_density_m2,
        superleak_pore_nm=superleak_pore_nm,
        is_valid=all_valid,
        details=details
    )
