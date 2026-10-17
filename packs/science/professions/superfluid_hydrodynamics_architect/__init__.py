"""
Dr. Taras 'The Superfluid' Sterling - Principal Superfluid Quantum Hydrodynamics & Helium-4 Vortex Architect.
Exports references, inspector, rubric, blind critic, elevation engine, and master controller.
"""

from .references import (
    PLANCK_CONSTANT,
    REDUCED_PLANCK_CONSTANT,
    HELIUM4_MASS,
    BOLTZMANN_CONSTANT,
    LAMBDA_TEMPERATURE_K,
    LIQUID_HELIUM_DENSITY,
    CIRCULATION_QUANTUM,
    VORTEX_CORE_RADIUS_M,
    LANDAU_ROTON_VELOCITY_M_S,
    MAX_SUPERFLUID_TEMPERATURE_K,
    MIN_SUPERFLUID_FRACTION,
    MAX_SUPERFLUID_VELOCITY_M_S,
    MAX_VORTEX_LINE_DENSITY_M2,
    MAX_SUPERLEAK_PORE_NM,
    MIN_SECOND_SOUND_VELOCITY_M_S,
    calculate_superfluid_fraction,
    calculate_feynman_critical_velocity,
    calculate_fountain_pressure,
    calculate_second_sound_velocity,
    calculate_vortex_mutual_friction,
    SuperfluidHydroValidationResult,
    validate_superfluid_hydrodynamics,
)

from .inspector import SuperfluidHydroInspector
from .rubric import SuperfluidHydroRubric, RubricEvaluation
from .blind_critic import SuperfluidHydroBlindCritic
from .elevation_engine import SuperfluidHydroElevationEngine
from .master import SuperfluidHydroMaster

__all__ = [
    "PLANCK_CONSTANT",
    "REDUCED_PLANCK_CONSTANT",
    "HELIUM4_MASS",
    "BOLTZMANN_CONSTANT",
    "LAMBDA_TEMPERATURE_K",
    "LIQUID_HELIUM_DENSITY",
    "CIRCULATION_QUANTUM",
    "VORTEX_CORE_RADIUS_M",
    "LANDAU_ROTON_VELOCITY_M_S",
    "MAX_SUPERFLUID_TEMPERATURE_K",
    "MIN_SUPERFLUID_FRACTION",
    "MAX_SUPERFLUID_VELOCITY_M_S",
    "MAX_VORTEX_LINE_DENSITY_M2",
    "MAX_SUPERLEAK_PORE_NM",
    "MIN_SECOND_SOUND_VELOCITY_M_S",
    "calculate_superfluid_fraction",
    "calculate_feynman_critical_velocity",
    "calculate_fountain_pressure",
    "calculate_second_sound_velocity",
    "calculate_vortex_mutual_friction",
    "SuperfluidHydroValidationResult",
    "validate_superfluid_hydrodynamics",
    "SuperfluidHydroInspector",
    "SuperfluidHydroRubric",
    "RubricEvaluation",
    "SuperfluidHydroBlindCritic",
    "SuperfluidHydroElevationEngine",
    "SuperfluidHydroMaster",
]
