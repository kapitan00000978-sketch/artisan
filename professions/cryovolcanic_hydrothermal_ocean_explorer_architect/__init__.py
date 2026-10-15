"""Commander Thorne 'The Sub-Surface' Sterling - Principal Planetary Sub-Surface Cryovolcanic & Hydrothermal Ocean Explorer.

Exports references, inspector, rubric, blind critic, elevation engine, and master controller.
"""

from .references import (
    ICE_FUSION_LATENT_HEAT_J_KG,
    ICE_DENSITY_KG_M3,
    ICE_SPECIFIC_HEAT_J_KG_K,
    EUROPA_SURFACE_GRAVITY,
    EUROPA_SURFACE_TEMP_K,
    ICE_MELTING_TEMP_K,
    SALINE_OCEAN_DENSITY_KG_M3,
    MIN_THERMAL_DRILL_POWER_KW,
    MIN_PENETRATION_VELOCITY_M_H,
    MIN_OCEAN_PRESSURE_RATING_MPA,
    MIN_COLLAPSE_SAFETY_FACTOR,
    MAX_ALLOWABLE_BIOBURDEN_SPORES_M2,
    MIN_DHMR_TEMPERATURE_C,
    MIN_DHMR_DURATION_HOURS,
    MAX_LOD_METHANE_NM,
    MAX_LOD_HYDROGEN_NM,
    MAX_LOD_AMINO_ACIDS_NM,
    MIN_TETHER_TENSILE_STRENGTH_KN,
    MAX_FIBER_ATTENUATION_DB_KM,
    MIN_TETHER_LENGTH_KM,
    MIN_SONAR_RANGE_KM,
    calculate_ice_melting_velocity,
    calculate_hydrostatic_pressure,
    calculate_tether_link_margin,
    CryovolcanicOceanValidationResult,
    validate_cryovolcanic_ocean_parameters,
)

from .inspector import CryovolcanicOceanInspector
from .rubric import CryovolcanicOceanRubric, RubricEvaluation
from .blind_critic import CryovolcanicOceanBlindCritic
from .elevation_engine import CryovolcanicOceanElevationEngine
from .master import CryovolcanicOceanMaster

__all__ = [
    "ICE_FUSION_LATENT_HEAT_J_KG",
    "ICE_DENSITY_KG_M3",
    "ICE_SPECIFIC_HEAT_J_KG_K",
    "EUROPA_SURFACE_GRAVITY",
    "EUROPA_SURFACE_TEMP_K",
    "ICE_MELTING_TEMP_K",
    "SALINE_OCEAN_DENSITY_KG_M3",
    "MIN_THERMAL_DRILL_POWER_KW",
    "MIN_PENETRATION_VELOCITY_M_H",
    "MIN_OCEAN_PRESSURE_RATING_MPA",
    "MIN_COLLAPSE_SAFETY_FACTOR",
    "MAX_ALLOWABLE_BIOBURDEN_SPORES_M2",
    "MIN_DHMR_TEMPERATURE_C",
    "MIN_DHMR_DURATION_HOURS",
    "MAX_LOD_METHANE_NM",
    "MAX_LOD_HYDROGEN_NM",
    "MAX_LOD_AMINO_ACIDS_NM",
    "MIN_TETHER_TENSILE_STRENGTH_KN",
    "MAX_FIBER_ATTENUATION_DB_KM",
    "MIN_TETHER_LENGTH_KM",
    "MIN_SONAR_RANGE_KM",
    "calculate_ice_melting_velocity",
    "calculate_hydrostatic_pressure",
    "calculate_tether_link_margin",
    "CryovolcanicOceanValidationResult",
    "validate_cryovolcanic_ocean_parameters",
    "CryovolcanicOceanInspector",
    "CryovolcanicOceanRubric",
    "RubricEvaluation",
    "CryovolcanicOceanBlindCritic",
    "CryovolcanicOceanElevationEngine",
    "CryovolcanicOceanMaster",
]
