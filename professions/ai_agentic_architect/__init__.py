"""
Naomi Chen - Principal AI Agentic Systems & LLM Architect Master Subsystem.
"""

from professions.ai_agentic_architect.references import (
    AgenticReferenceLibrary,
    AGENTIC_SYSTEM_BENCHMARKS,
    CONTEXT_BUDGET_PARTITIONS,
    TOXIC_AGENTIC_ANTI_PATTERNS,
    CANONICAL_AGENTIC_LOOP_CORE,
)
from professions.ai_agentic_architect.inspector import (
    AgenticSystemInspector,
    AgenticMetrics,
    AgenticInspectionReport,
)
from professions.ai_agentic_architect.rubric import (
    AgenticArchitectureRubric,
    AgenticRubricEvaluation,
)
from professions.ai_agentic_architect.blind_critic import (
    BlindAgenticCritic,
    AgenticDefect,
    AgenticDefectLedger,
)
from professions.ai_agentic_architect.elevation_engine import AgenticElevationEngine
from professions.ai_agentic_architect.master import NaomiChenMaster

__all__ = [
    "AgenticReferenceLibrary",
    "AGENTIC_SYSTEM_BENCHMARKS",
    "CONTEXT_BUDGET_PARTITIONS",
    "TOXIC_AGENTIC_ANTI_PATTERNS",
    "CANONICAL_AGENTIC_LOOP_CORE",
    "AgenticSystemInspector",
    "AgenticMetrics",
    "AgenticInspectionReport",
    "AgenticArchitectureRubric",
    "AgenticRubricEvaluation",
    "BlindAgenticCritic",
    "AgenticDefect",
    "AgenticDefectLedger",
    "AgenticElevationEngine",
    "NaomiChenMaster",
]
