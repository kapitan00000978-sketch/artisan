"""Dr. Silas 'The Plasma' Vance — Tokamak Magnetic Confinement & Fusion Plasma Stability Architecture.

The Council of Masters — Domain Master #29
"""

from .references import (
    FusionReferenceLibrary,
    PlasmaEquilibrium,
    SafetyFactorProfile,
    TroyonBetaMonitor,
    GreenwaldDensityMonitor,
    NeoclassicalTearingMode,
    DivertorThermalProtection,
    MIN_SAFETY_FACTOR_Q95,
    KRUSKAL_SHAFRANOV_MIN_Q,
    MAX_TROYON_BETA_N,
    MAX_GREENWALD_FRACTION,
    MAX_DIVERTOR_HEAT_FLUX_MW_M2,
    MAX_ISLAND_WIDTH_RATIO,
    MIN_RADIATIVE_FRACTION,
)
from .inspector import FusionPlasmaInspector
from .rubric import FusionPlasmaRubric
from .blind_critic import FusionPlasmaBlindCritic
from .elevation_engine import FusionPlasmaElevationEngine
from .master import SilasVanceMaster

__all__ = [
    "FusionReferenceLibrary",
    "PlasmaEquilibrium",
    "SafetyFactorProfile",
    "TroyonBetaMonitor",
    "GreenwaldDensityMonitor",
    "NeoclassicalTearingMode",
    "DivertorThermalProtection",
    "MIN_SAFETY_FACTOR_Q95",
    "KRUSKAL_SHAFRANOV_MIN_Q",
    "MAX_TROYON_BETA_N",
    "MAX_GREENWALD_FRACTION",
    "MAX_DIVERTOR_HEAT_FLUX_MW_M2",
    "MAX_ISLAND_WIDTH_RATIO",
    "MIN_RADIATIVE_FRACTION",
    "FusionPlasmaInspector",
    "FusionPlasmaRubric",
    "FusionPlasmaBlindCritic",
    "FusionPlasmaElevationEngine",
    "SilasVanceMaster",
]
