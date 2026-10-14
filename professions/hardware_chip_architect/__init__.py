"""
Ignis 'The Silicon' Thorne - Principal ASIC & FPGA Hardware Architect Master Subsystem.
"""

from professions.hardware_chip_architect.references import (
    HardwareReferenceLibrary,
    HARDWARE_TIMING_BENCHMARKS,
    HARDWARE_ARCHITECTURE_STANDARDS,
    TOXIC_HARDWARE_ANTI_PATTERNS,
    CANONICAL_HARDWARE_CORE,
)
from professions.hardware_chip_architect.inspector import (
    HardwareSystemInspector,
    HardwareMetrics,
    HardwareInspectionReport,
)
from professions.hardware_chip_architect.rubric import (
    HardwareRubric,
    HardwareEvaluation,
    HardwareDimensionScore,
)
from professions.hardware_chip_architect.blind_critic import (
    BlindHardwareCritic,
    HardwareDefect,
    HardwareDefectLedger,
)
from professions.hardware_chip_architect.elevation_engine import HardwareElevationEngine
from professions.hardware_chip_architect.master import IgnisThorneMaster

__all__ = [
    "HardwareReferenceLibrary",
    "HARDWARE_TIMING_BENCHMARKS",
    "HARDWARE_ARCHITECTURE_STANDARDS",
    "TOXIC_HARDWARE_ANTI_PATTERNS",
    "CANONICAL_HARDWARE_CORE",
    "HardwareSystemInspector",
    "HardwareMetrics",
    "HardwareInspectionReport",
    "HardwareRubric",
    "HardwareEvaluation",
    "HardwareDimensionScore",
    "BlindHardwareCritic",
    "HardwareDefect",
    "HardwareDefectLedger",
    "HardwareElevationEngine",
    "IgnisThorneMaster",
]
