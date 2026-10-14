"""
Dr. Rosalind 'The Lattice' Vance - Principal Topological Insulator & Spintronic Device Architect.
Exports references, inspector, rubric, blind critic, elevation engine, and master controller.
"""

from .references import (
    VACUUM_PERMEABILITY,
    REDUCED_PLANCK_CONSTANT,
    PLANCK_CONSTANT,
    ELEMENTARY_CHARGE,
    BOLTZMANN_CONSTANT,
    BOHR_MAGNETON,
    CONDUCTANCE_QUANTUM,
    MIN_SPIN_HALL_ANGLE,
    MAX_SWITCHING_CURRENT_DENSITY_A_M2,
    MAX_BULK_LEAKAGE_RATIO,
    MIN_TMR_RATIO,
    MIN_THERMAL_STABILITY_FACTOR,
    MIN_SURFACE_MOBILITY_CM2_V_S,
    MIN_MEAN_FREE_PATH_NM,
    calculate_sot_switching_current_density,
    calculate_tmr_ratio,
    calculate_thermal_stability,
    calculate_bulk_leakage_ratio,
    calculate_mean_free_path_nm,
    TopologicalSpintronicsValidationResult,
    validate_topological_spintronics,
)

from .inspector import TopologicalSpintronicsInspector
from .rubric import TopologicalSpintronicsRubric, RubricEvaluation
from .blind_critic import TopologicalSpintronicsBlindCritic
from .elevation_engine import TopologicalSpintronicsElevationEngine
from .master import TopologicalSpintronicsMaster

__all__ = [
    "REDUCED_PLANCK_CONSTANT",
    "PLANCK_CONSTANT",
    "ELEMENTARY_CHARGE",
    "BOLTZMANN_CONSTANT",
    "BOHR_MAGNETON",
    "CONDUCTANCE_QUANTUM",
    "MIN_SPIN_HALL_ANGLE",
    "MAX_SWITCHING_CURRENT_DENSITY_A_M2",
    "MAX_BULK_LEAKAGE_RATIO",
    "MIN_TMR_RATIO",
    "MIN_THERMAL_STABILITY_FACTOR",
    "MIN_SURFACE_MOBILITY_CM2_V_S",
    "MIN_MEAN_FREE_PATH_NM",
    "calculate_sot_switching_current_density",
    "calculate_tmr_ratio",
    "calculate_thermal_stability",
    "calculate_bulk_leakage_ratio",
    "calculate_mean_free_path_nm",
    "TopologicalSpintronicsValidationResult",
    "validate_topological_spintronics",
    "TopologicalSpintronicsInspector",
    "TopologicalSpintronicsRubric",
    "RubricEvaluation",
    "TopologicalSpintronicsBlindCritic",
    "TopologicalSpintronicsElevationEngine",
    "TopologicalSpintronicsMaster",
]
