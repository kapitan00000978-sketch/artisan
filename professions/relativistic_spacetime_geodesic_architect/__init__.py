"""Dr. Veda 'The Spacetime' Vance - Principal Relativistic Spacetime Geodesic & Black Hole Magnetosphere Architect.

Exports physical references, mathematical models, inspector, rubric, blind critic, elevation engine, and master controller.
"""

from .references import (
    SPEED_OF_LIGHT,
    GRAVITATIONAL_CONSTANT,
    SOLAR_MASS_KG,
    VACUUM_PERMEABILITY,
    MAX_KERR_SPIN_PARAMETER,
    MAX_SYMPLECTIC_ENERGY_DRIFT,
    MAX_ANGULAR_MOMENTUM_DRIFT,
    MAX_CARTER_CONSTANT_DRIFT,
    MIN_BZ_JET_POWER_W,
    MIN_INTEGRATOR_ORDER,
    SCHWARZSCHILD_CRITICAL_IMPACT,
    calculate_kerr_horizons,
    calculate_kerr_ergosphere_radius,
    calculate_isco_radius,
    calculate_blandford_znajek_power,
    SpacetimeGeodesicValidationResult,
    validate_spacetime_geodesic_parameters,
)

from .inspector import SpacetimeGeodesicInspector
from .rubric import SpacetimeGeodesicRubric, RubricEvaluation
from .blind_critic import SpacetimeGeodesicBlindCritic
from .elevation_engine import SpacetimeGeodesicElevationEngine
from .master import SpacetimeGeodesicMaster

__all__ = [
    "SPEED_OF_LIGHT",
    "GRAVITATIONAL_CONSTANT",
    "SOLAR_MASS_KG",
    "VACUUM_PERMEABILITY",
    "MAX_KERR_SPIN_PARAMETER",
    "MAX_SYMPLECTIC_ENERGY_DRIFT",
    "MAX_ANGULAR_MOMENTUM_DRIFT",
    "MAX_CARTER_CONSTANT_DRIFT",
    "MIN_BZ_JET_POWER_W",
    "MIN_INTEGRATOR_ORDER",
    "SCHWARZSCHILD_CRITICAL_IMPACT",
    "calculate_kerr_horizons",
    "calculate_kerr_ergosphere_radius",
    "calculate_isco_radius",
    "calculate_blandford_znajek_power",
    "SpacetimeGeodesicValidationResult",
    "validate_spacetime_geodesic_parameters",
    "SpacetimeGeodesicInspector",
    "SpacetimeGeodesicRubric",
    "RubricEvaluation",
    "SpacetimeGeodesicBlindCritic",
    "SpacetimeGeodesicElevationEngine",
    "SpacetimeGeodesicMaster",
]
