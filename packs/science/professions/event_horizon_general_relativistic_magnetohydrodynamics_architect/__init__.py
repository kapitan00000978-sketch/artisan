"""Event Horizon General Relativistic Magnetohydrodynamics (GRMHD) Subsystem.

Formulated by Dr. Vespera 'The Singularity' Vance,
Principal Event Horizon General Relativistic Magnetohydrodynamics (GRMHD) Architect.
"""

from .references import (
    MIN_HORIZON_LAPSE_ALPHA,
    MAX_DIMENSIONLESS_SPIN,
    MIN_HORIZON_MAGNETIC_FLUX_MAD,
    MIN_BLANDFORD_ZNAJEK_EFFICIENCY,
    MAX_PRIMITIVE_INVERSION_TOLERANCE,
    MAX_DIV_B_ERROR,
    MAX_SYNCHROTRON_COOLING_TIME_S,
    MAX_MAGNETOSONIC_SPEED_C,
    MAX_MAGNETIZATION_SIGMA_FLOOR,
    SPEED_OF_LIGHT,
    GRAVITATIONAL_CONSTANT,
    GRMHDValidationResult,
    calculate_kerr_horizon_radius,
    calculate_blandford_znajek_luminosity,
    calculate_synchrotron_cooling_timescale,
    calculate_magnetosonic_speed,
    calculate_mad_flux_parameter,
    validate_grmhd_parameters,
)
from .inspector import GRMHDInspector
from .rubric import GRMHDRubric, PASSING_SCORE
from .blind_critic import GRMHDBlindCritic
from .elevation_engine import GRMHDElevationEngine
from .master import GRMHDMaster, ActiveDecisionJournal

__all__ = [
    "MIN_HORIZON_LAPSE_ALPHA",
    "MAX_DIMENSIONLESS_SPIN",
    "MIN_HORIZON_MAGNETIC_FLUX_MAD",
    "MIN_BLANDFORD_ZNAJEK_EFFICIENCY",
    "MAX_PRIMITIVE_INVERSION_TOLERANCE",
    "MAX_DIV_B_ERROR",
    "MAX_SYNCHROTRON_COOLING_TIME_S",
    "MAX_MAGNETOSONIC_SPEED_C",
    "MAX_MAGNETIZATION_SIGMA_FLOOR",
    "SPEED_OF_LIGHT",
    "GRAVITATIONAL_CONSTANT",
    "GRMHDValidationResult",
    "calculate_kerr_horizon_radius",
    "calculate_blandford_znajek_luminosity",
    "calculate_synchrotron_cooling_timescale",
    "calculate_magnetosonic_speed",
    "calculate_mad_flux_parameter",
    "validate_grmhd_parameters",
    "GRMHDInspector",
    "GRMHDRubric",
    "PASSING_SCORE",
    "GRMHDBlindCritic",
    "GRMHDElevationEngine",
    "GRMHDMaster",
    "ActiveDecisionJournal",
]
