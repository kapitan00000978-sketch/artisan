"""Commander Orion 'The Deep' Sterling — Subsea Autonomous Robotics & Navigation Architecture Subsystem.

Full Ocean Depth (11,000m) hydrostatic crush envelopes, Mackenzie acoustic models,
dielectric positive pressure compensation, and passive ballast jettison fail-safes.
"""

from .references import (
    DeepSeaReferenceLibrary,
    HydrostaticHullSpec,
    AcousticNavState,
    BuoyancySystemState,
    PressureCompensationState,
    SubseaMissionReport,
    calculate_hydrostatic_pressure,
    calculate_sound_speed_mackenzie,
    evaluate_hull_safety_factor,
    evaluate_net_buoyancy,
    STANDARD_GRAVITY,
    AVERAGE_HADAL_DENSITY,
)
from .inspector import DeepSeaInspector, DeepSeaInspectionResult
from .rubric import DeepSeaRubric, DeepSeaRubricEvaluation
from .blind_critic import DeepSeaBlindCritic, DeepSeaDefectLedger
from .elevation_engine import DeepSeaElevationEngine
from .master import OrionSterlingMaster, DeepSeaMaster

__all__ = [
    "OrionSterlingMaster",
    "DeepSeaMaster",
    "DeepSeaReferenceLibrary",
    "HydrostaticHullSpec",
    "AcousticNavState",
    "BuoyancySystemState",
    "PressureCompensationState",
    "SubseaMissionReport",
    "calculate_hydrostatic_pressure",
    "calculate_sound_speed_mackenzie",
    "evaluate_hull_safety_factor",
    "evaluate_net_buoyancy",
    "STANDARD_GRAVITY",
    "AVERAGE_HADAL_DENSITY",
    "DeepSeaInspector",
    "DeepSeaInspectionResult",
    "DeepSeaRubric",
    "DeepSeaRubricEvaluation",
    "DeepSeaBlindCritic",
    "DeepSeaDefectLedger",
    "DeepSeaElevationEngine",
]
