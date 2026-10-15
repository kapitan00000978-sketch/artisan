"""Physical references and mathematical models for Planetary Sub-Surface Cryovolcanic & Hydrothermal Ocean Exploration.

Architect: Commander Thorne 'The Sub-Surface' Sterling
Domain: cryovolcanic_hydrothermal_ocean_explorer_architect
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Physical constants for cryogenic ice and icy moon oceans (e.g. Europa / Enceladus)
ICE_FUSION_LATENT_HEAT_J_KG: float = 334000.0       # J/kg
ICE_DENSITY_KG_M3: float = 920.0                   # kg/m^3
ICE_SPECIFIC_HEAT_J_KG_K: float = 2050.0           # J/(kg*K)
EUROPA_SURFACE_GRAVITY: float = 1.315              # m/s^2 (Europa surface gravity)
EUROPA_SURFACE_TEMP_K: float = 110.0               # K (-163 °C)
ICE_MELTING_TEMP_K: float = 273.15                 # K (0 °C)
SALINE_OCEAN_DENSITY_KG_M3: float = 1050.0         # kg/m^3

# Quantitative engineering benchmarks for sub-ice robotic cryobots and ocean exploration
MIN_THERMAL_DRILL_POWER_KW: float = 25.0           # P_th >= 25.0 kW_th
MIN_PENETRATION_VELOCITY_M_H: float = 1.50         # v_melt >= 1.50 m/h
MIN_OCEAN_PRESSURE_RATING_MPA: float = 200.0       # P_crush >= 200.0 MPa
MIN_COLLAPSE_SAFETY_FACTOR: float = 1.50           # SF >= 1.50
MAX_ALLOWABLE_BIOBURDEN_SPORES_M2: float = 0.030   # Bioburden <= 0.030 spores/m^2 (COSPAR IVb)
MIN_DHMR_TEMPERATURE_C: float = 125.0              # T_dhmr >= 125.0 °C
MIN_DHMR_DURATION_HOURS: float = 40.0              # t_dhmr >= 40.0 hours
MAX_LOD_METHANE_NM: float = 1.0                    # LOD_CH4 <= 1.0 nM
MAX_LOD_HYDROGEN_NM: float = 10.0                  # LOD_H2 <= 10.0 nM
MAX_LOD_AMINO_ACIDS_NM: float = 0.10               # LOD_amino <= 0.10 nM
MIN_TETHER_TENSILE_STRENGTH_KN: float = 2.50       # F_tensile >= 2.50 kN
MAX_FIBER_ATTENUATION_DB_KM: float = 0.35          # alpha_opt <= 0.35 dB/km
MIN_TETHER_LENGTH_KM: float = 35.0                 # L_tether >= 35.0 km
MIN_SONAR_RANGE_KM: float = 5.0                    # R_sonar >= 5.0 km


def calculate_ice_melting_velocity(
    thermal_power_kw: float,
    probe_cross_section_m2: float,
    ambient_ice_temp_k: float = EUROPA_SURFACE_TEMP_K
) -> float:
    """Calculate the steady-state thermal ice melting velocity in meters per hour.

    v_melt = P_thermal / [ rho_ice * A_melt * (c_p * (T_m - T_0) + L_f) ]
    """
    if thermal_power_kw <= 0.0 or probe_cross_section_m2 <= 0.0:
        return 0.0

    delta_t = max(0.0, ICE_MELTING_TEMP_K - ambient_ice_temp_k)
    energy_per_kg = (ICE_SPECIFIC_HEAT_J_KG_K * delta_t) + ICE_FUSION_LATENT_HEAT_J_KG
    energy_per_m3 = ICE_DENSITY_KG_M3 * energy_per_kg

    power_watts = thermal_power_kw * 1000.0
    velocity_m_s = power_watts / (probe_cross_section_m2 * energy_per_m3)
    return velocity_m_s * 3600.0  # Convert to m/h


def calculate_hydrostatic_pressure(
    ice_thickness_km: float,
    ocean_depth_km: float,
    surface_gravity: float = EUROPA_SURFACE_GRAVITY
) -> float:
    """Calculate total hydrostatic pressure in MPa at the base of the alien ocean.

    P = (rho_ice * g * h_ice + rho_water * g * h_ocean) / 10^6  [MPa]
    """
    ice_h_m = max(0.0, ice_thickness_km) * 1000.0
    ocean_h_m = max(0.0, ocean_depth_km) * 1000.0

    p_ice = ICE_DENSITY_KG_M3 * surface_gravity * ice_h_m
    p_ocean = SALINE_OCEAN_DENSITY_KG_M3 * surface_gravity * ocean_h_m
    return (p_ice + p_ocean) / 1.0e6


def calculate_tether_link_margin(
    tether_length_km: float,
    fiber_attenuation_db_km: float = 0.35,
    laser_tx_power_dbm: float = 10.0,
    rx_sensitivity_dbm: float = -35.0
) -> float:
    """Calculate optical communication link margin in dB across the sub-ice tether.

    Link Margin = (P_tx - P_rx_sens) - (alpha * L_tether + Connector_losses)
    """
    if tether_length_km <= 0.0:
        return 0.0
    total_loss_db = (fiber_attenuation_db_km * tether_length_km) + 2.0  # 2.0 dB for dual hermetic feedthroughs
    power_budget_db = laser_tx_power_dbm - rx_sensitivity_dbm
    return power_budget_db - total_loss_db


@dataclass
class CryovolcanicOceanValidationResult:
    """Structured validation report for Cryovolcanic & Hydrothermal Ocean Exploration Subsystems."""
    is_valid: bool
    thermal_drill_power_kw: float
    penetration_velocity_m_h: float
    ocean_pressure_rating_mpa: float
    collapse_safety_factor: float
    bioburden_spores_m2: float
    dhmr_temperature_c: float
    dhmr_duration_hours: float
    lod_methane_nm: float
    lod_hydrogen_nm: float
    lod_amino_acids_nm: float
    tether_tensile_strength_kn: float
    fiber_attenuation_db_km: float
    tether_length_km: float
    sonar_range_km: float
    flaws: List[str]


def validate_cryovolcanic_ocean_parameters(
    thermal_drill_power_kw: float = 32.0,
    penetration_velocity_m_h: float = 1.85,
    ocean_pressure_rating_mpa: float = 240.0,
    collapse_safety_factor: float = 1.65,
    bioburden_spores_m2: float = 0.015,
    dhmr_temperature_c: float = 135.0,
    dhmr_duration_hours: float = 48.0,
    lod_methane_nm: float = 0.65,
    lod_hydrogen_nm: float = 5.5,
    lod_amino_acids_nm: float = 0.065,
    tether_tensile_strength_kn: float = 3.2,
    fiber_attenuation_db_km: float = 0.28,
    tether_length_km: float = 40.0,
    sonar_range_km: float = 6.5
) -> CryovolcanicOceanValidationResult:
    """Validate planetary cryobot parameters against Commander Thorne Sterling's strict astrobiology and engineering benchmarks."""
    flaws: List[str] = []

    if thermal_drill_power_kw < MIN_THERMAL_DRILL_POWER_KW:
        flaws.append(
            f"Thermal drill melting power {thermal_drill_power_kw:.1f} kW_th below minimum required {MIN_THERMAL_DRILL_POWER_KW:.1f} kW_th "
            f"(risking freeze-in stall in cryogenic ice)."
        )

    if penetration_velocity_m_h < MIN_PENETRATION_VELOCITY_M_H:
        flaws.append(
            f"Ice penetration velocity {penetration_velocity_m_h:.2f} m/h below operational threshold {MIN_PENETRATION_VELOCITY_M_H:.2f} m/h."
        )

    if ocean_pressure_rating_mpa < MIN_OCEAN_PRESSURE_RATING_MPA:
        flaws.append(
            f"Hull hydrostatic pressure rating {ocean_pressure_rating_mpa:.1f} MPa below alien abyss requirement {MIN_OCEAN_PRESSURE_RATING_MPA:.1f} MPa."
        )

    if collapse_safety_factor < MIN_COLLAPSE_SAFETY_FACTOR:
        flaws.append(
            f"Structural collapse safety factor {collapse_safety_factor:.2f} below margin {MIN_COLLAPSE_SAFETY_FACTOR:.2f}."
        )

    if bioburden_spores_m2 > MAX_ALLOWABLE_BIOBURDEN_SPORES_M2:
        flaws.append(
            f"Biological contamination level {bioburden_spores_m2:.3f} spores/m^2 exceeds COSPAR Category IVb planetary protection ceiling "
            f"{MAX_ALLOWABLE_BIOBURDEN_SPORES_M2:.3f} spores/m^2."
        )

    if dhmr_temperature_c < MIN_DHMR_TEMPERATURE_C:
        flaws.append(
            f"Dry heat microbial reduction temperature {dhmr_temperature_c:.1f} °C below sterilization benchmark {MIN_DHMR_TEMPERATURE_C:.1f} °C."
        )

    if dhmr_duration_hours < MIN_DHMR_DURATION_HOURS:
        flaws.append(
            f"Sterilization bakeout soak time {dhmr_duration_hours:.1f} hours below required duration {MIN_DHMR_DURATION_HOURS:.1f} hours."
        )

    if lod_methane_nm > MAX_LOD_METHANE_NM:
        flaws.append(
            f"Methane biosignature detection limit {lod_methane_nm:.2f} nM exceeds sensitivity threshold {MAX_LOD_METHANE_NM:.2f} nM."
        )

    if lod_hydrogen_nm > MAX_LOD_HYDROGEN_NM:
        flaws.append(
            f"Dissolved hydrogen detection limit {lod_hydrogen_nm:.2f} nM exceeds serpentinization sensitivity threshold {MAX_LOD_HYDROGEN_NM:.2f} nM."
        )

    if lod_amino_acids_nm > MAX_LOD_AMINO_ACIDS_NM:
        flaws.append(
            f"Amino acid detection limit {lod_amino_acids_nm:.3f} nM exceeds chiral biomarker threshold {MAX_LOD_AMINO_ACIDS_NM:.2f} nM."
        )

    if tether_tensile_strength_kn < MIN_TETHER_TENSILE_STRENGTH_KN:
        flaws.append(
            f"Micro-tether tensile strength {tether_tensile_strength_kn:.2f} kN below shear threshold {MIN_TETHER_TENSILE_STRENGTH_KN:.2f} kN."
        )

    if fiber_attenuation_db_km > MAX_FIBER_ATTENUATION_DB_KM:
        flaws.append(
            f"Optical fiber attenuation {fiber_attenuation_db_km:.2f} dB/km exceeds low-loss ceiling {MAX_FIBER_ATTENUATION_DB_KM:.2f} dB/km."
        )

    if tether_length_km < MIN_TETHER_LENGTH_KM:
        flaws.append(
            f"Umbilical tether continuous length {tether_length_km:.1f} km below ice shelf thickness margin {MIN_TETHER_LENGTH_KM:.1f} km."
        )

    if sonar_range_km < MIN_SONAR_RANGE_KM:
        flaws.append(
            f"Sonar bathymetry acoustic ranging range {sonar_range_km:.1f} km below navigation requirement {MIN_SONAR_RANGE_KM:.1f} km."
        )

    return CryovolcanicOceanValidationResult(
        is_valid=len(flaws) == 0,
        thermal_drill_power_kw=thermal_drill_power_kw,
        penetration_velocity_m_h=penetration_velocity_m_h,
        ocean_pressure_rating_mpa=ocean_pressure_rating_mpa,
        collapse_safety_factor=collapse_safety_factor,
        bioburden_spores_m2=bioburden_spores_m2,
        dhmr_temperature_c=dhmr_temperature_c,
        dhmr_duration_hours=dhmr_duration_hours,
        lod_methane_nm=lod_methane_nm,
        lod_hydrogen_nm=lod_hydrogen_nm,
        lod_amino_acids_nm=lod_amino_acids_nm,
        tether_tensile_strength_kn=tether_tensile_strength_kn,
        fiber_attenuation_db_km=fiber_attenuation_db_km,
        tether_length_km=tether_length_km,
        sonar_range_km=sonar_range_km,
        flaws=flaws
    )
