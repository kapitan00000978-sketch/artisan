"""Commander Jaxen 'The Fusion-Torch' Sterling - Principal Continuous-Detonation Wave & Rotating Detonation Rocket Engine Architect.

Exports physical references, mathematical models, inspector, rubric, blind critic, elevation engine, and master controller.
"""

from .references import (
    UNIVERSAL_GAS_CONSTANT,
    STANDARD_GRAVITY,
    MIN_CJ_DETONATION_VELOCITY_M_S,
    MIN_CJ_PRESSURE_RATIO,
    MIN_ZND_SPIKE_PRESSURE_RATIO,
    MAX_DDT_RUNUP_DISTANCE_MM,
    MIN_DETONATION_FREQUENCY_KHZ,
    MIN_CO_ROTATING_WAVES,
    MIN_ANNULAR_GAP_MM,
    MAX_ANNULAR_GAP_MM,
    MIN_ANNULAR_DIAMETER_MM,
    MAX_ANNULAR_DIAMETER_MM,
    MIN_PRESSURE_GAIN_EFFICIENCY,
    MIN_AEROSPIKE_NOZZLE_EFFICIENCY,
    MIN_SPECIFIC_IMPULSE_S,
    MAX_CHAMBER_WALL_HEAT_FLUX_MW_M2,
    calculate_cj_detonation_velocity,
    calculate_detonation_frequency,
    calculate_pressure_gain_ratio,
    calculate_aerospike_thrust_efficiency,
    RotatingDetonationValidationResult,
    validate_rotating_detonation_parameters,
)

from .inspector import RotatingDetonationInspector
from .rubric import RotatingDetonationRubric, RubricEvaluation
from .blind_critic import RotatingDetonationBlindCritic
from .elevation_engine import RotatingDetonationElevationEngine
from .master import RotatingDetonationMaster

__all__ = [
    "UNIVERSAL_GAS_CONSTANT",
    "STANDARD_GRAVITY",
    "MIN_CJ_DETONATION_VELOCITY_M_S",
    "MIN_CJ_PRESSURE_RATIO",
    "MIN_ZND_SPIKE_PRESSURE_RATIO",
    "MAX_DDT_RUNUP_DISTANCE_MM",
    "MIN_DETONATION_FREQUENCY_KHZ",
    "MIN_CO_ROTATING_WAVES",
    "MIN_ANNULAR_GAP_MM",
    "MAX_ANNULAR_GAP_MM",
    "MIN_ANNULAR_DIAMETER_MM",
    "MAX_ANNULAR_DIAMETER_MM",
    "MIN_PRESSURE_GAIN_EFFICIENCY",
    "MIN_AEROSPIKE_NOZZLE_EFFICIENCY",
    "MIN_SPECIFIC_IMPULSE_S",
    "MAX_CHAMBER_WALL_HEAT_FLUX_MW_M2",
    "calculate_cj_detonation_velocity",
    "calculate_detonation_frequency",
    "calculate_pressure_gain_ratio",
    "calculate_aerospike_thrust_efficiency",
    "RotatingDetonationValidationResult",
    "validate_rotating_detonation_parameters",
    "RotatingDetonationInspector",
    "RotatingDetonationRubric",
    "RubricEvaluation",
    "RotatingDetonationBlindCritic",
    "RotatingDetonationElevationEngine",
    "RotatingDetonationMaster",
]
