"""Dr. Cassian 'The Relic' Sterling - Principal Paleogenomic Ancient DNA Reconstruction Architect.

Exports physical references, mathematical models, inspector, rubric, blind critic, elevation engine, and master controller.
"""

from .references import (
    MIN_TERMINAL_DEAMINATION_RATE,
    MIN_FRAGMENT_LENGTH_BP,
    MAX_FRAGMENT_LENGTH_BP,
    MAX_MODERN_CONTAMINATION_RATE,
    MIN_AUTHENTICITY_CONFIDENCE,
    MIN_UDG_REPAIR_EFFICIENCY,
    MIN_SEQUENCING_DEPTH_X,
    MIN_PHRED_QUALITY_SCORE,
    MAX_REFERENCE_MAPPING_BIAS,
    MIN_DAMAGE_LOG_LIKELIHOOD,
    calculate_briggs_deamination_probability,
    calculate_fragment_length_density,
    calculate_phred_error_probability,
    PaleogenomicValidationResult,
    validate_paleogenomic_parameters,
)

from .inspector import PaleogenomicInspector
from .rubric import PaleogenomicRubric, RubricEvaluation
from .blind_critic import PaleogenomicBlindCritic
from .elevation_engine import PaleogenomicElevationEngine
from .master import PaleogenomicMaster

__all__ = [
    "MIN_TERMINAL_DEAMINATION_RATE",
    "MIN_FRAGMENT_LENGTH_BP",
    "MAX_FRAGMENT_LENGTH_BP",
    "MAX_MODERN_CONTAMINATION_RATE",
    "MIN_AUTHENTICITY_CONFIDENCE",
    "MIN_UDG_REPAIR_EFFICIENCY",
    "MIN_SEQUENCING_DEPTH_X",
    "MIN_PHRED_QUALITY_SCORE",
    "MAX_REFERENCE_MAPPING_BIAS",
    "MIN_DAMAGE_LOG_LIKELIHOOD",
    "calculate_briggs_deamination_probability",
    "calculate_fragment_length_density",
    "calculate_phred_error_probability",
    "PaleogenomicValidationResult",
    "validate_paleogenomic_parameters",
    "PaleogenomicInspector",
    "PaleogenomicRubric",
    "RubricEvaluation",
    "PaleogenomicBlindCritic",
    "PaleogenomicElevationEngine",
    "PaleogenomicMaster",
]
