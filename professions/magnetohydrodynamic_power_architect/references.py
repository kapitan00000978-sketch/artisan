"""
Domain references and quantitative mathematical equations for
Dr. Evander 'The Plasma-Torch' Sterling - Principal Magnetohydrodynamic Energy Conversion & Direct Space-Power Architect.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any

# Physical Constants
VACUUM_PERMEABILITY = 1.25663706212e-6  # H/m (mu_0)
ELEMENTARY_CHARGE = 1.602176634e-19  # C (e)
ELECTRON_MASS = 9.1093837015e-31  # kg (m_e)
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K

# Quantitative Standards
MIN_POWER_DENSITY_W_M3 = 1.0e6  # 1.0 MW/m^3 minimum power density
MAX_HALL_PARAMETER = 4.0  # Maximum Hall parameter to prevent electrothermal breakdown
MIN_STUART_NUMBER = 0.20  # Minimum interaction parameter for viable enthalpy extraction
MAX_STUART_NUMBER = 2.00  # Maximum interaction parameter to prevent shock boundary separation
MIN_ENTHALPY_EXTRACTION = 0.15  # 15% minimum thermal enthalpy converted to electricity
MAX_HALL_ELECTRIC_FIELD_V_M = 4000.0  # 4.0 kV/m maximum axial Hall electric field
MAX_SHEATH_VOLTAGE_DROP_V = 150.0  # 150.0 V maximum cold boundary layer sheath drop
MIN_LOAD_FACTOR = 0.40  # Minimum optimal electrical load factor K = E / (u*B)
MAX_LOAD_FACTOR = 0.85  # Maximum optimal electrical load factor


def calculate_hall_parameter(b_field_t: float, electron_mobility_m2_v_s: float) -> float:
    """Calculate electron Hall parameter beta_H = mu_e * B = (e * B) / (m_e * nu_e)."""
    if b_field_t <= 0.0 or electron_mobility_m2_v_s <= 0.0:
        return 0.0
    return electron_mobility_m2_v_s * b_field_t


def calculate_effective_conductivity(sigma_0_s_m: float, beta_hall: float) -> float:
    """Calculate effective plasma electrical conductivity accounting for Hall reduction sigma_eff = sigma_0 / (1 + beta_H^2)."""
    if sigma_0_s_m <= 0.0:
        return 0.0
    if beta_hall < 0.0:
        beta_hall = abs(beta_hall)
    return sigma_0_s_m / (1.0 + (beta_hall ** 2))


def calculate_power_density(
    sigma_eff_s_m: float,
    velocity_m_s: float,
    b_field_t: float,
    load_factor_k: float
) -> float:
    """Calculate electrical power density P = sigma_eff * u^2 * B^2 * K * (1 - K) in W/m^3."""
    if sigma_eff_s_m <= 0.0 or velocity_m_s <= 0.0 or b_field_t <= 0.0:
        return 0.0
    if not (0.0 < load_factor_k < 1.0):
        return 0.0
    return sigma_eff_s_m * (velocity_m_s ** 2) * (b_field_t ** 2) * load_factor_k * (1.0 - load_factor_k)


def calculate_stuart_number(
    sigma_eff_s_m: float,
    b_field_t: float,
    duct_length_m: float,
    density_kg_m3: float,
    velocity_m_s: float
) -> float:
    """Calculate MHD interaction parameter (Stuart number) S = (sigma * B^2 * L) / (rho * u)."""
    if density_kg_m3 <= 0.0 or velocity_m_s <= 0.0:
        return 0.0
    numerator = sigma_eff_s_m * (b_field_t ** 2) * duct_length_m
    denominator = density_kg_m3 * velocity_m_s
    return numerator / denominator


def calculate_hall_electric_field(
    beta_hall: float,
    velocity_m_s: float,
    b_field_t: float,
    load_factor_k: float
) -> float:
    """Calculate axial Hall electric field E_x = beta_H * (1 - K) * u * B in V/m."""
    if beta_hall <= 0.0 or velocity_m_s <= 0.0 or b_field_t <= 0.0:
        return 0.0
    return beta_hall * (1.0 - load_factor_k) * velocity_m_s * b_field_t


def calculate_enthalpy_extraction(
    total_power_output_w: float,
    mass_flow_rate_kg_s: float,
    cp_j_kg_k: float,
    t_stagnation_k: float
) -> float:
    """Calculate thermal enthalpy extraction fraction eta_enthalpy = P_total / (m_dot * C_p * T_0)."""
    thermal_enthalpy_rate = mass_flow_rate_kg_s * cp_j_kg_k * t_stagnation_k
    if thermal_enthalpy_rate <= 0.0:
        return 0.0
    return total_power_output_w / thermal_enthalpy_rate


@dataclass
class MhdPowerValidationResult:
    """Validation report for magnetohydrodynamic power generator physics."""
    power_density_w_m3: float
    hall_parameter: float
    stuart_number: float
    hall_electric_field_v_m: float
    enthalpy_extraction_fraction: float
    sheath_voltage_drop_v: float
    is_valid: bool
    details: Dict[str, Any] = field(default_factory=dict)


def validate_mhd_power_generator(
    sigma_0_s_m: float,
    electron_mobility: float,
    velocity_m_s: float,
    b_field_t: float,
    load_factor_k: float,
    duct_length_m: float,
    density_kg_m3: float,
    duct_volume_m3: float,
    mass_flow_rate_kg_s: float,
    cp_j_kg_k: float,
    t_stagnation_k: float,
    sheath_voltage_drop_v: float = 85.0
) -> MhdPowerValidationResult:
    """Validate magnetohydrodynamic direct power generation parameters against quantitative bounds."""
    beta_h = calculate_hall_parameter(b_field_t, electron_mobility)
    sigma_eff = calculate_effective_conductivity(sigma_0_s_m, beta_h)
    p_density = calculate_power_density(sigma_eff, velocity_m_s, b_field_t, load_factor_k)
    stuart_no = calculate_stuart_number(sigma_eff, b_field_t, duct_length_m, density_kg_m3, velocity_m_s)
    e_hall = calculate_hall_electric_field(beta_h, velocity_m_s, b_field_t, load_factor_k)

    total_power = p_density * duct_volume_m3
    enthalpy_eff = calculate_enthalpy_extraction(total_power, mass_flow_rate_kg_s, cp_j_kg_k, t_stagnation_k)

    p_density_valid = p_density >= MIN_POWER_DENSITY_W_M3
    hall_valid = beta_h <= MAX_HALL_PARAMETER
    stuart_valid = MIN_STUART_NUMBER <= stuart_no <= MAX_STUART_NUMBER
    e_hall_valid = e_hall <= MAX_HALL_ELECTRIC_FIELD_V_M
    enthalpy_valid = enthalpy_eff >= MIN_ENTHALPY_EXTRACTION
    sheath_valid = sheath_voltage_drop_v <= MAX_SHEATH_VOLTAGE_DROP_V
    load_factor_valid = MIN_LOAD_FACTOR <= load_factor_k <= MAX_LOAD_FACTOR

    all_valid = (
        p_density_valid and hall_valid and stuart_valid and
        e_hall_valid and enthalpy_valid and sheath_valid and load_factor_valid
    )

    details = {
        "power_density_mw_m3": p_density / 1.0e6,
        "p_density_valid": p_density_valid,
        "hall_parameter": beta_h,
        "hall_valid": hall_valid,
        "stuart_number": stuart_no,
        "stuart_valid": stuart_valid,
        "hall_electric_field_v_m": e_hall,
        "e_hall_valid": e_hall_valid,
        "enthalpy_extraction_percent": enthalpy_eff * 100.0,
        "enthalpy_valid": enthalpy_valid,
        "sheath_voltage_drop_v": sheath_voltage_drop_v,
        "sheath_valid": sheath_valid,
        "load_factor_k": load_factor_k,
        "load_factor_valid": load_factor_valid,
        "total_electrical_megawatts": total_power / 1.0e6
    }

    return MhdPowerValidationResult(
        power_density_w_m3=p_density,
        hall_parameter=beta_h,
        stuart_number=stuart_no,
        hall_electric_field_v_m=e_hall,
        enthalpy_extraction_fraction=enthalpy_eff,
        sheath_voltage_drop_v=sheath_voltage_drop_v,
        is_valid=all_valid,
        details=details
    )
