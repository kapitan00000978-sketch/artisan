"""Dr. Zephyr 'The Hypersonic' Sterling — Hypersonic Aerothermodynamics & Scramjet Propulsion Architecture Subsystem.

Mach 5–25 flight envelopes, Sutton-Graves stagnation heating, non-equilibrium real-gas dissociation,
scramjet isolator shock train margins, and sub-5ms active unstart mitigation.
"""

from .references import (
    HypersonicReferenceLibrary,
    HypersonicFreestreamState,
    ShockLayerThermodynamics,
    ScramjetIsolatorState,
    ThermalProtectionState,
    HypersonicMissionReport,
    calculate_stagnation_temperature,
    calculate_sutton_graves_heat_flux,
    calculate_isolator_shock_train_length,
    evaluate_isolator_stability_margin,
    evaluate_tps_safety_factor,
    UNIVERSAL_GAS_CONSTANT,
    AIR_GAS_CONSTANT,
    SUTTON_GRAVES_CONSTANT,
)
from .inspector import HypersonicInspector, HypersonicInspectionResult
from .rubric import HypersonicRubric, HypersonicRubricEvaluation
from .blind_critic import HypersonicBlindCritic, HypersonicDefectLedger
from .elevation_engine import HypersonicElevationEngine
from .master import ZephyrSterlingMaster, HypersonicMaster

__all__ = [
    "ZephyrSterlingMaster",
    "HypersonicMaster",
    "HypersonicReferenceLibrary",
    "HypersonicFreestreamState",
    "ShockLayerThermodynamics",
    "ScramjetIsolatorState",
    "ThermalProtectionState",
    "HypersonicMissionReport",
    "calculate_stagnation_temperature",
    "calculate_sutton_graves_heat_flux",
    "calculate_isolator_shock_train_length",
    "evaluate_isolator_stability_margin",
    "evaluate_tps_safety_factor",
    "UNIVERSAL_GAS_CONSTANT",
    "AIR_GAS_CONSTANT",
    "SUTTON_GRAVES_CONSTANT",
    "HypersonicInspector",
    "HypersonicInspectionResult",
    "HypersonicRubric",
    "HypersonicRubricEvaluation",
    "HypersonicBlindCritic",
    "HypersonicDefectLedger",
    "HypersonicElevationEngine",
]
