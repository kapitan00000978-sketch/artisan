"""Dr. Hector 'The Stellar' Vance - Principal Stellarator Magnet & Non-Planar Twisted Coil Fusion Architect.

Exports references, inspector, rubric, blind critic, elevation engine, and master controller.
"""

from .references import (
    VACUUM_PERMEABILITY,
    BOLTZMANN_CONSTANT,
    ELEMENTARY_CHARGE,
    MIN_ROTATIONAL_TRANSFORM,
    MAX_ROTATIONAL_TRANSFORM,
    MAX_MAGNETIC_SHEAR,
    MIN_COIL_BEND_RADIUS_M,
    MAX_COIL_CURVATURE_M_INV,
    MIN_COIL_PLASMA_STANDOFF_M,
    MAX_EFFECTIVE_HELICAL_RIPPLE,
    MAX_DIVERTOR_HEAT_FLUX_MW_M2,
    MIN_DIVERTOR_RAD_FRACTION,
    MAX_ON_CONDUCTOR_PEAK_FIELD_T,
    MAX_CASING_VON_MISES_MPA,
    MAX_HTS_WINDING_STRAIN_PCT,
    MAX_QUENCH_DUMP_TIME_MS,
    MAX_NET_TOROIDAL_CURRENT_KA,
    FORBIDDEN_CORE_RATIONALS,
    calculate_rotational_transform,
    calculate_coil_bend_curvature,
    calculate_island_divertor_heat_flux,
    calculate_effective_ripple_transport_factor,
    StellaratorFusionValidationResult,
    validate_stellarator_fusion_parameters,
)

from .inspector import StellaratorFusionInspector
from .rubric import StellaratorFusionRubric, RubricEvaluation
from .blind_critic import StellaratorFusionBlindCritic
from .elevation_engine import StellaratorFusionElevationEngine
from .master import StellaratorFusionMaster

__all__ = [
    "VACUUM_PERMEABILITY",
    "BOLTZMANN_CONSTANT",
    "ELEMENTARY_CHARGE",
    "MIN_ROTATIONAL_TRANSFORM",
    "MAX_ROTATIONAL_TRANSFORM",
    "MAX_MAGNETIC_SHEAR",
    "MIN_COIL_BEND_RADIUS_M",
    "MAX_COIL_CURVATURE_M_INV",
    "MIN_COIL_PLASMA_STANDOFF_M",
    "MAX_EFFECTIVE_HELICAL_RIPPLE",
    "MAX_DIVERTOR_HEAT_FLUX_MW_M2",
    "MIN_DIVERTOR_RAD_FRACTION",
    "MAX_ON_CONDUCTOR_PEAK_FIELD_T",
    "MAX_CASING_VON_MISES_MPA",
    "MAX_HTS_WINDING_STRAIN_PCT",
    "MAX_QUENCH_DUMP_TIME_MS",
    "MAX_NET_TOROIDAL_CURRENT_KA",
    "FORBIDDEN_CORE_RATIONALS",
    "calculate_rotational_transform",
    "calculate_coil_bend_curvature",
    "calculate_island_divertor_heat_flux",
    "calculate_effective_ripple_transport_factor",
    "StellaratorFusionValidationResult",
    "validate_stellarator_fusion_parameters",
    "StellaratorFusionInspector",
    "StellaratorFusionRubric",
    "RubricEvaluation",
    "StellaratorFusionBlindCritic",
    "StellaratorFusionElevationEngine",
    "StellaratorFusionMaster",
]
