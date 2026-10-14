"""
Morpheus 'The Kernel' Vance - Principal Embedded Firmware Architect Master Subsystem.
"""

from professions.embedded_firmware_architect.references import (
    FirmwareReferenceLibrary,
    FIRMWARE_SYSTEM_BENCHMARKS,
    FIRMWARE_ARCHITECTURE_STANDARDS,
    TOXIC_FIRMWARE_ANTI_PATTERNS,
    CANONICAL_FIRMWARE_CORE,
)
from professions.embedded_firmware_architect.inspector import (
    FirmwareSystemInspector,
    FirmwareMetrics,
    FirmwareInspectionReport,
)
from professions.embedded_firmware_architect.rubric import (
    FirmwareRubric,
    FirmwareEvaluation,
    FirmwareDimensionScore,
)
from professions.embedded_firmware_architect.blind_critic import (
    BlindFirmwareCritic,
    FirmwareDefect,
    FirmwareDefectLedger,
)
from professions.embedded_firmware_architect.elevation_engine import FirmwareElevationEngine
from professions.embedded_firmware_architect.master import MorpheusVanceMaster

__all__ = [
    "FirmwareReferenceLibrary",
    "FIRMWARE_SYSTEM_BENCHMARKS",
    "FIRMWARE_ARCHITECTURE_STANDARDS",
    "TOXIC_FIRMWARE_ANTI_PATTERNS",
    "CANONICAL_FIRMWARE_CORE",
    "FirmwareSystemInspector",
    "FirmwareMetrics",
    "FirmwareInspectionReport",
    "FirmwareRubric",
    "FirmwareEvaluation",
    "FirmwareDimensionScore",
    "BlindFirmwareCritic",
    "FirmwareDefect",
    "FirmwareDefectLedger",
    "FirmwareElevationEngine",
    "MorpheusVanceMaster",
]
