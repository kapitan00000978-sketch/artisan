"""Dr. Zephyrus 'The Void' Vance - Principal Interstellar Bussard Ramjet & Relativistic Magnetic Scoop Electrodynamics Architect.

Exports physical references, mathematical models, inspector, rubric, blind critic, elevation engine, and master controller.
"""

from .references import (
    SPEED_OF_LIGHT,
    PROTON_MASS_KG,
    ELEMENTARY_CHARGE,
    VACUUM_PERMITTIVITY,
    MIN_SCOOP_RADIUS_KM,
    MIN_RELATIVISTIC_VELOCITY_FRACTION,
    MIN_MAGNETIC_SCOOP_FIELD_T,
    MIN_PHOTO_IONIZATION_EFFICIENCY,
    MIN_CAPTURE_CROSS_SECTION_EFFICIENCY,
    MIN_THRUST_TO_DRAG_RATIO,
    MIN_EXHAUST_VELOCITY_M_S,
    MIN_NOZZLE_COLLIMATION_EFFICIENCY,
    MIN_SHIP_ACCELERATION_M_S2,
    MAX_SHIP_ACCELERATION_M_S2,
    MIN_CORE_FUSION_TEMP_K,
    MAX_BREMSSTRAHLUNG_LOSS_RATIO,
    calculate_lorentz_factor,
    calculate_proton_intake_rate,
    calculate_relativistic_ram_drag,
    calculate_fusion_thrust,
    BussardRamjetValidationResult,
    validate_bussard_ramjet_parameters,
)

from .inspector import BussardRamjetInspector
from .rubric import BussardRamjetRubric, RubricEvaluation
from .blind_critic import BussardRamjetBlindCritic
from .elevation_engine import BussardRamjetElevationEngine
from .master import BussardRamjetMaster

__all__ = [
    "SPEED_OF_LIGHT",
    "PROTON_MASS_KG",
    "ELEMENTARY_CHARGE",
    "VACUUM_PERMITTIVITY",
    "MIN_SCOOP_RADIUS_KM",
    "MIN_RELATIVISTIC_VELOCITY_FRACTION",
    "MIN_MAGNETIC_SCOOP_FIELD_T",
    "MIN_PHOTO_IONIZATION_EFFICIENCY",
    "MIN_CAPTURE_CROSS_SECTION_EFFICIENCY",
    "MIN_THRUST_TO_DRAG_RATIO",
    "MIN_EXHAUST_VELOCITY_M_S",
    "MIN_NOZZLE_COLLIMATION_EFFICIENCY",
    "MIN_SHIP_ACCELERATION_M_S2",
    "MAX_SHIP_ACCELERATION_M_S2",
    "MIN_CORE_FUSION_TEMP_K",
    "MAX_BREMSSTRAHLUNG_LOSS_RATIO",
    "calculate_lorentz_factor",
    "calculate_proton_intake_rate",
    "calculate_relativistic_ram_drag",
    "calculate_fusion_thrust",
    "BussardRamjetValidationResult",
    "validate_bussard_ramjet_parameters",
    "BussardRamjetInspector",
    "BussardRamjetRubric",
    "RubricEvaluation",
    "BussardRamjetBlindCritic",
    "BussardRamjetElevationEngine",
    "BussardRamjetMaster",
]
