"""Extreme Non-Linear Ocean Wave & Rogue Wave Hydrodynamics Subsystem.

Formulated by Dr. Silas 'The Wave' Sterling,
Principal Extreme Non-Linear Ocean Wave & Rogue Wave Hydrodynamics Architect.
"""

from .references import (
    MIN_BENJAMIN_FEIR_INDEX,
    MAX_BENJAMIN_FEIR_INDEX,
    ROGUE_HEIGHT_RATIO_THRESHOLD,
    CREST_ABNORMALITY_THRESHOLD,
    MIN_WAVE_STEEPNESS,
    MAX_WAVE_STEEPNESS_BREAKING,
    MIN_SLAMMING_PRESSURE_KPA,
    MIN_SURFACE_KURTOSIS,
    MAX_DIRECTIONAL_SPREADING_DEG,
    MIN_PEREGRINE_AMPLIFICATION,
    MAX_PEREGRINE_AMPLIFICATION,
    MIN_HOSM_NONLINEAR_ORDER,
    MIN_DECK_AIRGAP_METERS,
    MAX_DYNAMIC_AMPLIFICATION_FACTOR,
    SEAWATER_DENSITY_KG_M3,
    GRAVITY_ACCELERATION,
    ExtremeWaveValidationResult,
    calculate_benjamin_feir_index,
    calculate_rogue_wave_criteria,
    calculate_wave_steepness,
    calculate_slamming_pressure,
    calculate_peregrine_breather_amplitude,
    calculate_wave_in_deck_airgap,
    validate_extreme_wave_parameters,
)
from .inspector import ExtremeWaveInspector
from .rubric import ExtremeWaveRubric, PASSING_SCORE
from .blind_critic import ExtremeWaveBlindCritic
from .elevation_engine import ExtremeWaveElevationEngine
from .master import ExtremeWaveMaster, ActiveDecisionJournal

__all__ = [
    "MIN_BENJAMIN_FEIR_INDEX",
    "MAX_BENJAMIN_FEIR_INDEX",
    "ROGUE_HEIGHT_RATIO_THRESHOLD",
    "CREST_ABNORMALITY_THRESHOLD",
    "MIN_WAVE_STEEPNESS",
    "MAX_WAVE_STEEPNESS_BREAKING",
    "MIN_SLAMMING_PRESSURE_KPA",
    "MIN_SURFACE_KURTOSIS",
    "MAX_DIRECTIONAL_SPREADING_DEG",
    "MIN_PEREGRINE_AMPLIFICATION",
    "MAX_PEREGRINE_AMPLIFICATION",
    "MIN_HOSM_NONLINEAR_ORDER",
    "MIN_DECK_AIRGAP_METERS",
    "MAX_DYNAMIC_AMPLIFICATION_FACTOR",
    "SEAWATER_DENSITY_KG_M3",
    "GRAVITY_ACCELERATION",
    "ExtremeWaveValidationResult",
    "calculate_benjamin_feir_index",
    "calculate_rogue_wave_criteria",
    "calculate_wave_steepness",
    "calculate_slamming_pressure",
    "calculate_peregrine_breather_amplitude",
    "calculate_wave_in_deck_airgap",
    "validate_extreme_wave_parameters",
    "ExtremeWaveInspector",
    "ExtremeWaveRubric",
    "PASSING_SCORE",
    "ExtremeWaveBlindCritic",
    "ExtremeWaveElevationEngine",
    "ExtremeWaveMaster",
    "ActiveDecisionJournal",
]
