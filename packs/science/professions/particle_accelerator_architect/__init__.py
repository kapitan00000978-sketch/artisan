"""Dr. Julian 'The Accelerator' Vance — Particle Accelerator & Relativistic Beam Dynamics Architecture Subsystem.

Lorentz relativistic kinematics, Courant-Snyder Twiss parameters, betatron tune resonance avoidance,
superconducting RF cavity quench interlocks, and sub-3us kicker machine protection dumps.
"""

from .references import (
    AcceleratorReferenceLibrary,
    RelativisticBeamState,
    TwissLatticeState,
    SuperconductingCavityState,
    MachineProtectionState,
    AcceleratorMissionReport,
    calculate_lorentz_gamma,
    calculate_magnetic_rigidity,
    calculate_twiss_gamma,
    SPEED_OF_LIGHT,
    PROTON_REST_MASS_GEV,
    ELECTRON_REST_MASS_GEV,
    ELEMENTARY_CHARGE,
)
from .inspector import AcceleratorInspector, AcceleratorInspectionResult
from .rubric import AcceleratorRubric, AcceleratorRubricEvaluation
from .blind_critic import AcceleratorBlindCritic, AcceleratorDefectLedger
from .elevation_engine import AcceleratorElevationEngine
from .master import JulianVanceMaster, AcceleratorMaster

__all__ = [
    "JulianVanceMaster",
    "AcceleratorMaster",
    "AcceleratorReferenceLibrary",
    "RelativisticBeamState",
    "TwissLatticeState",
    "SuperconductingCavityState",
    "MachineProtectionState",
    "AcceleratorMissionReport",
    "calculate_lorentz_gamma",
    "calculate_magnetic_rigidity",
    "calculate_twiss_gamma",
    "SPEED_OF_LIGHT",
    "PROTON_REST_MASS_GEV",
    "ELECTRON_REST_MASS_GEV",
    "ELEMENTARY_CHARGE",
    "AcceleratorInspector",
    "AcceleratorInspectionResult",
    "AcceleratorRubric",
    "AcceleratorRubricEvaluation",
    "AcceleratorBlindCritic",
    "AcceleratorDefectLedger",
    "AcceleratorElevationEngine",
]
