"""Relativistic Heavy-Ion Quark-Gluon Plasma (QGP) Hydrodynamics Subsystem.

Formulated by Dr. Kaelen 'The Quark' Sterling,
Principal Relativistic Heavy-Ion Quark-Gluon Plasma (QGP) Hydrodynamics Architect.
"""

from .references import (
    KSS_BOUND_ETA_OVER_S,
    MIN_ETA_OVER_S,
    MAX_ETA_OVER_S,
    MAX_ZETA_OVER_S,
    MIN_QCD_CRITICAL_TEMP_MEV,
    MAX_QCD_CRITICAL_TEMP_MEV,
    NOMINAL_QCD_CRITICAL_TEMP_MEV,
    MIN_THERMALIZATION_TAU_FM_C,
    MAX_THERMALIZATION_TAU_FM_C,
    MIN_JET_QUENCHING_QHAT_GEV2_FM,
    MIN_ISRAEL_STEWART_RELAXATION_RATIO,
    MIN_FREEZEOUT_TEMP_MEV,
    MAX_FREEZEOUT_TEMP_MEV,
    MIN_ELLIPTIC_FLOW_V2,
    MAX_ELLIPTIC_FLOW_V2,
    MIN_SOUND_SPEED_SQ_AT_TC,
    HBAR_C_MEV_FM,
    SPEED_OF_LIGHT,
    QGPValidationResult,
    calculate_israel_stewart_shear_relaxation_time,
    calculate_bjorken_energy_density,
    calculate_kss_viscosity_margin,
    calculate_speed_of_sound_squared,
    validate_qgp_parameters,
)
from .inspector import QGPHydrodynamicsInspector
from .rubric import QGPHydrodynamicsRubric, PASSING_SCORE
from .blind_critic import QGPHydrodynamicsBlindCritic
from .elevation_engine import QGPHydrodynamicsElevationEngine
from .master import QGPHydrodynamicsMaster, ActiveDecisionJournal

__all__ = [
    "KSS_BOUND_ETA_OVER_S",
    "MIN_ETA_OVER_S",
    "MAX_ETA_OVER_S",
    "MAX_ZETA_OVER_S",
    "MIN_QCD_CRITICAL_TEMP_MEV",
    "MAX_QCD_CRITICAL_TEMP_MEV",
    "NOMINAL_QCD_CRITICAL_TEMP_MEV",
    "MIN_THERMALIZATION_TAU_FM_C",
    "MAX_THERMALIZATION_TAU_FM_C",
    "MIN_JET_QUENCHING_QHAT_GEV2_FM",
    "MIN_ISRAEL_STEWART_RELAXATION_RATIO",
    "MIN_FREEZEOUT_TEMP_MEV",
    "MAX_FREEZEOUT_TEMP_MEV",
    "MIN_ELLIPTIC_FLOW_V2",
    "MAX_ELLIPTIC_FLOW_V2",
    "MIN_SOUND_SPEED_SQ_AT_TC",
    "HBAR_C_MEV_FM",
    "SPEED_OF_LIGHT",
    "QGPValidationResult",
    "calculate_israel_stewart_shear_relaxation_time",
    "calculate_bjorken_energy_density",
    "calculate_kss_viscosity_margin",
    "calculate_speed_of_sound_squared",
    "validate_qgp_parameters",
    "QGPHydrodynamicsInspector",
    "QGPHydrodynamicsRubric",
    "PASSING_SCORE",
    "QGPHydrodynamicsBlindCritic",
    "QGPHydrodynamicsElevationEngine",
    "QGPHydrodynamicsMaster",
    "ActiveDecisionJournal",
]
