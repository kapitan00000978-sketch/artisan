"""Dr. Magnus 'The Core' Sterling — Nuclear Reactor Physics, Neutron Kinetics & Criticality Safety Architecture.

The Council of Masters — Domain Master #28
"""

from .references import (
    NuclearReferenceLibrary,
    DelayedPrecursorGroup,
    ReactivityState,
    PointReactorKineticsSolver,
    ThermalHydraulicsSafety,
    ControlRodBank,
    BETA_EFF_U235,
    PROMPT_NEUTRON_LIFETIME_SEC,
    MAX_TRANSIENT_REACTIVITY_DOLLARS,
    MAX_SHUTDOWN_KEFF,
    MIN_DNBR_THRESHOLD,
    MAX_SCRAM_INSERTION_TIME_SEC,
    MAX_DOPPLER_COEFF_PCM_K,
)
from .inspector import NuclearCriticalityInspector
from .rubric import NuclearCriticalityRubric
from .blind_critic import NuclearCriticalityBlindCritic
from .elevation_engine import NuclearCriticalityElevationEngine
from .master import MagnusSterlingMaster

__all__ = [
    "NuclearReferenceLibrary",
    "DelayedPrecursorGroup",
    "ReactivityState",
    "PointReactorKineticsSolver",
    "ThermalHydraulicsSafety",
    "ControlRodBank",
    "BETA_EFF_U235",
    "PROMPT_NEUTRON_LIFETIME_SEC",
    "MAX_TRANSIENT_REACTIVITY_DOLLARS",
    "MAX_SHUTDOWN_KEFF",
    "MIN_DNBR_THRESHOLD",
    "MAX_SCRAM_INSERTION_TIME_SEC",
    "MAX_DOPPLER_COEFF_PCM_K",
    "NuclearCriticalityInspector",
    "NuclearCriticalityRubric",
    "NuclearCriticalityBlindCritic",
    "NuclearCriticalityElevationEngine",
    "MagnusSterlingMaster",
]
