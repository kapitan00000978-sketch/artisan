"""
Interplanetary Astrodynamics & Trajectory Architect Profession Subsystem
Lead Master: Dr. Aurelius 'The Orbital' Sterling
"""

from .references import (
    MU_SUN,
    MU_EARTH,
    MU_MARS,
    MU_JUPITER,
    AU_KM,
    SOLAR_FLUX_P0,
    TrajectoryValidationResult,
    vis_viva_velocity,
    hohmann_transfer_delta_v,
    tisserand_parameter,
    cr3bp_jacobi_constant,
    srp_acceleration,
    validate_interplanetary_mission
)
from .inspector import AstrodynamicsInspector
from .rubric import AstrodynamicsRubric
from .blind_critic import AstrodynamicsBlindCritic
from .elevation_engine import AstrodynamicsElevationEngine
from .master import DrAureliusSterling

__all__ = [
    "MU_SUN",
    "MU_EARTH",
    "MU_MARS",
    "MU_JUPITER",
    "AU_KM",
    "SOLAR_FLUX_P0",
    "TrajectoryValidationResult",
    "vis_viva_velocity",
    "hohmann_transfer_delta_v",
    "tisserand_parameter",
    "cr3bp_jacobi_constant",
    "srp_acceleration",
    "validate_interplanetary_mission",
    "AstrodynamicsInspector",
    "AstrodynamicsRubric",
    "AstrodynamicsBlindCritic",
    "AstrodynamicsElevationEngine",
    "DrAureliusSterling"
]
