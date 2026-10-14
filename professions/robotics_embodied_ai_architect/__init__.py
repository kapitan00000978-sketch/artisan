"""
Dr. Vespera 'The Kinematic' Sterling - Principal Autonomous Robotics & Embodied AI Master Subsystem.
"""

from professions.robotics_embodied_ai_architect.references import (
    RoboticsReferenceLibrary,
    ROBOTICS_CONTROL_BENCHMARKS,
    ROBOTICS_ARCHITECTURE_STANDARDS,
    TOXIC_ROBOTICS_ANTI_PATTERNS,
    CANONICAL_ROBOTICS_CORE,
    CANONICAL_ROBOTICS_CONTROL_LOOP,
)
from professions.robotics_embodied_ai_architect.inspector import (
    RoboticsSystemInspector,
    RoboticsMetrics,
    RoboticsInspectionReport,
)
from professions.robotics_embodied_ai_architect.rubric import (
    RoboticsRubric,
    RoboticsEvaluation,
    RoboticsDimensionScore,
)
from professions.robotics_embodied_ai_architect.blind_critic import (
    BlindRoboticsCritic,
    RoboticsDefect,
    RoboticsDefectLedger,
)
from professions.robotics_embodied_ai_architect.elevation_engine import RoboticsElevationEngine
from professions.robotics_embodied_ai_architect.master import VesperaSterlingMaster

__all__ = [
    "RoboticsReferenceLibrary",
    "ROBOTICS_CONTROL_BENCHMARKS",
    "ROBOTICS_ARCHITECTURE_STANDARDS",
    "TOXIC_ROBOTICS_ANTI_PATTERNS",
    "CANONICAL_ROBOTICS_CORE",
    "CANONICAL_ROBOTICS_CONTROL_LOOP",
    "RoboticsSystemInspector",
    "RoboticsMetrics",
    "RoboticsInspectionReport",
    "RoboticsRubric",
    "RoboticsEvaluation",
    "RoboticsDimensionScore",
    "BlindRoboticsCritic",
    "RoboticsDefect",
    "RoboticsDefectLedger",
    "RoboticsElevationEngine",
    "VesperaSterlingMaster",
]
