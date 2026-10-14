"""
Dr. Evelyn Reed - Machine Learning & Data Science Subsystem.
"""

from .references import MLReferenceLibrary, ML_EVALUATION_STANDARDS, DRIFT_THRESHOLDS_PSI
from .inspector import MLPipelineInspector, MLMetrics, MLInspectionReport
from .rubric import MLRubric, MLRubricEvaluation
from .blind_critic import BlindMLCritic, MLDefectLedger, MLDefect
from .elevation_engine import MLElevationEngine
from .master import DrEvelynReedMaster

__all__ = [
    "MLReferenceLibrary",
    "ML_EVALUATION_STANDARDS",
    "DRIFT_THRESHOLDS_PSI",
    "MLPipelineInspector",
    "MLMetrics",
    "MLInspectionReport",
    "MLRubric",
    "MLRubricEvaluation",
    "BlindMLCritic",
    "MLDefectLedger",
    "MLDefect",
    "MLElevationEngine",
    "DrEvelynReedMaster"
]
