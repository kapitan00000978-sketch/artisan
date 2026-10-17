"""
Commander Cassiopeia 'The Orbital' Sterling - Principal Aerospace Avionics Architect Master Subsystem.
"""

from professions.aerospace_avionics_architect.references import (
    AvionicsReferenceLibrary,
    AVIONICS_FLIGHT_BENCHMARKS,
    AVIONICS_ARCHITECTURE_STANDARDS,
    TOXIC_AVIONICS_ANTI_PATTERNS,
    CANONICAL_AVIONICS_CORE,
)
from professions.aerospace_avionics_architect.inspector import (
    AvionicsSystemInspector,
    AvionicsMetrics,
    AvionicsInspectionReport,
)
from professions.aerospace_avionics_architect.rubric import (
    AvionicsRubric,
    AvionicsEvaluation,
    AvionicsDimensionScore,
)
from professions.aerospace_avionics_architect.blind_critic import (
    BlindAvionicsCritic,
    AvionicsDefect,
    AvionicsDefectLedger,
)
from professions.aerospace_avionics_architect.elevation_engine import AvionicsElevationEngine
from professions.aerospace_avionics_architect.master import CassiopeiaSterlingMaster

__all__ = [
    "AvionicsReferenceLibrary",
    "AVIONICS_FLIGHT_BENCHMARKS",
    "AVIONICS_ARCHITECTURE_STANDARDS",
    "TOXIC_AVIONICS_ANTI_PATTERNS",
    "CANONICAL_AVIONICS_CORE",
    "AvionicsSystemInspector",
    "AvionicsMetrics",
    "AvionicsInspectionReport",
    "AvionicsRubric",
    "AvionicsEvaluation",
    "AvionicsDimensionScore",
    "BlindAvionicsCritic",
    "AvionicsDefect",
    "AvionicsDefectLedger",
    "AvionicsElevationEngine",
    "CassiopeiaSterlingMaster",
]
