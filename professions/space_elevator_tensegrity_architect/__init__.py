"""Dr. Valerius 'The Megastructure' Sterling - Principal Space Elevator & Active Tensegrity Megastructure Architect.

Exports references, inspector, rubric, blind critic, elevation engine, and master controller.
"""

from .references import (
    GRAVITATIONAL_CONSTANT,
    EARTH_MASS_KG,
    EARTH_EQUATORIAL_RADIUS_M,
    EARTH_ANGULAR_VELOCITY_RAD_S,
    GEOSTATIONARY_RADIUS_M,
    GEOSTATIONARY_ALTITUDE_M,
    MIN_TENSILE_STRENGTH_PA,
    MAX_TETHER_DENSITY_KG_M3,
    MIN_SPECIFIC_STRENGTH_N_M_KG,
    MAX_TAPER_RATIO,
    MIN_TETHER_LENGTH_M,
    MIN_ANCHOR_PRETENSION_N,
    MAX_CLIMBER_MASS_KG,
    MAX_CLIMBER_VELOCITY_M_S,
    MAX_CORIOLIS_DEFLECTION_RAD,
    MIN_ACTIVE_DAMPING_RATIO,
    MAX_RESONANT_QUALITY_FACTOR,
    MIN_WAVE_VELOCITY_M_S,
    calculate_specific_strength,
    calculate_tether_taper_ratio,
    calculate_coriolis_deflection,
    calculate_transverse_wave_speed,
    SpaceElevatorValidationResult,
    validate_space_elevator_parameters,
)

from .inspector import SpaceElevatorInspector
from .rubric import SpaceElevatorRubric, RubricEvaluation
from .blind_critic import SpaceElevatorBlindCritic
from .elevation_engine import SpaceElevatorElevationEngine
from .master import SpaceElevatorMaster

__all__ = [
    "GRAVITATIONAL_CONSTANT",
    "EARTH_MASS_KG",
    "EARTH_EQUATORIAL_RADIUS_M",
    "EARTH_ANGULAR_VELOCITY_RAD_S",
    "GEOSTATIONARY_RADIUS_M",
    "GEOSTATIONARY_ALTITUDE_M",
    "MIN_TENSILE_STRENGTH_PA",
    "MAX_TETHER_DENSITY_KG_M3",
    "MIN_SPECIFIC_STRENGTH_N_M_KG",
    "MAX_TAPER_RATIO",
    "MIN_TETHER_LENGTH_M",
    "MIN_ANCHOR_PRETENSION_N",
    "MAX_CLIMBER_MASS_KG",
    "MAX_CLIMBER_VELOCITY_M_S",
    "MAX_CORIOLIS_DEFLECTION_RAD",
    "MIN_ACTIVE_DAMPING_RATIO",
    "MAX_RESONANT_QUALITY_FACTOR",
    "MIN_WAVE_VELOCITY_M_S",
    "calculate_specific_strength",
    "calculate_tether_taper_ratio",
    "calculate_coriolis_deflection",
    "calculate_transverse_wave_speed",
    "SpaceElevatorValidationResult",
    "validate_space_elevator_parameters",
    "SpaceElevatorInspector",
    "SpaceElevatorRubric",
    "RubricEvaluation",
    "SpaceElevatorBlindCritic",
    "SpaceElevatorElevationEngine",
    "SpaceElevatorMaster",
]
