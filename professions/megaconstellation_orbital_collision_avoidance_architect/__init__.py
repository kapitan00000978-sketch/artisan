"""Mega-Constellation Autonomous Orbital Traffic & Collision Avoidance Master Subsystem.

Embodying the domain mastery of Commander Mira 'The Orbit' Vance.
"""

from professions.megaconstellation_orbital_collision_avoidance_architect.references import (
    OrbitalConjunctionParameters,
    OrbitalConjunctionValidationResult,
    validate_orbital_conjunction_parameters,
    calculate_collision_probability_2d,
    calculate_tangential_delta_v_for_radial_separation,
    calculate_orbital_decay_time_years,
    MAX_ACTIONABLE_PC,
    MIN_MISS_DISTANCE_M,
    MIN_RADIAL_SEPARATION_M,
    MAX_COVARIANCE_SIGMA_M,
    MIN_LEAD_TIME_ORBITS,
    MAX_LEAD_TIME_ORBITS,
    MAX_SECONDARY_PC,
    MAX_SLOT_OFFSET_M,
    MIN_MANEUVER_DV_M_S,
    MAX_MANEUVER_DV_M_S,
    MAX_DEORBIT_YEARS,
    MAX_CASUALTY_RISK,
    MIN_SCREENING_HORIZON_H,
)
from professions.megaconstellation_orbital_collision_avoidance_architect.inspector import (
    OrbitalTrafficCodeInspector,
)
from professions.megaconstellation_orbital_collision_avoidance_architect.rubric import (
    OrbitalTrafficRubricEvaluator,
    OrbitalTrafficEvaluationReport,
    CriterionResult,
    PASSING_SCORE_THRESHOLD,
)
from professions.megaconstellation_orbital_collision_avoidance_architect.blind_critic import (
    OrbitalTrafficBlindCritic,
    BlindCriticVerdict,
)
from professions.megaconstellation_orbital_collision_avoidance_architect.elevation_engine import (
    OrbitalTrafficElevationEngine,
)
from professions.megaconstellation_orbital_collision_avoidance_architect.master import (
    OrbitalTrafficMaster,
)

__all__ = [
    "OrbitalConjunctionParameters",
    "OrbitalConjunctionValidationResult",
    "validate_orbital_conjunction_parameters",
    "calculate_collision_probability_2d",
    "calculate_tangential_delta_v_for_radial_separation",
    "calculate_orbital_decay_time_years",
    "MAX_ACTIONABLE_PC",
    "MIN_MISS_DISTANCE_M",
    "MIN_RADIAL_SEPARATION_M",
    "MAX_COVARIANCE_SIGMA_M",
    "MIN_LEAD_TIME_ORBITS",
    "MAX_LEAD_TIME_ORBITS",
    "MAX_SECONDARY_PC",
    "MAX_SLOT_OFFSET_M",
    "MIN_MANEUVER_DV_M_S",
    "MAX_MANEUVER_DV_M_S",
    "MAX_DEORBIT_YEARS",
    "MAX_CASUALTY_RISK",
    "MIN_SCREENING_HORIZON_H",
    "OrbitalTrafficCodeInspector",
    "OrbitalTrafficRubricEvaluator",
    "OrbitalTrafficEvaluationReport",
    "CriterionResult",
    "PASSING_SCORE_THRESHOLD",
    "OrbitalTrafficBlindCritic",
    "BlindCriticVerdict",
    "OrbitalTrafficElevationEngine",
    "OrbitalTrafficMaster",
]
