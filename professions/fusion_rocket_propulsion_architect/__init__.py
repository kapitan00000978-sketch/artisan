#!/usr/bin/env python3
"""
Commander Rowan 'The Fusion-Drive' Sterling: Principal Direct Fusion Rocket & Magnetoplasmadynamic Propulsion Architect
Subsystem Package Initialization
"""

from .references import (
    exhaust_velocity_from_isp,
    alfven_velocity,
    magnetic_nozzle_alfven_mach,
    nozzle_divergence_efficiency,
    thrust_power_efficiency,
    FusionRocketValidationResult,
    validate_fusion_rocket,
)
from .inspector import FusionRocketInspector
from .rubric import FusionRocketRubric
from .blind_critic import FusionRocketBlindCritic
from .elevation_engine import FusionRocketElevationEngine
from .master import CommanderRowanSterling

__all__ = [
    "exhaust_velocity_from_isp",
    "alfven_velocity",
    "magnetic_nozzle_alfven_mach",
    "nozzle_divergence_efficiency",
    "thrust_power_efficiency",
    "FusionRocketValidationResult",
    "validate_fusion_rocket",
    "FusionRocketInspector",
    "FusionRocketRubric",
    "FusionRocketBlindCritic",
    "FusionRocketElevationEngine",
    "CommanderRowanSterling",
]
