"""Commander Kaelen 'The Shield' Vance - Principal Magnetospheric Radiation Shielding Architect.

Exports references, inspector, rubric, blind critic, elevation engine, and master controller.
"""

from .references import (
    SPEED_OF_LIGHT,
    VACUUM_PERMEABILITY,
    ELEMENTARY_CHARGE,
    PROTON_REST_MASS_KG,
    PROTON_REST_ENERGY_MEV,
    MIN_MAGNETIC_MOMENT_GA_M2,
    MIN_STORMER_RIGIDITY_GV,
    MIN_COIL_PEAK_FIELD_T,
    MAX_HABITAT_LEAKAGE_FIELD_T,
    MIN_HTS_CURRENT_DENSITY_A_M2,
    MAX_COIL_OPERATING_TEMP_K,
    MAX_QUENCH_DUMP_TIME_MS,
    MAX_CREW_ANNUAL_DOSE_MSV,
    MAX_SPE_DOSE_RATE_MGY_H,
    MIN_ELECTROSTATIC_POTENTIAL_MV,
    MIN_NEUTRALIZER_CURRENT_MA,
    calculate_stormer_cutoff_rigidity,
    calculate_larmor_gyroradius,
    calculate_habitat_fringe_field,
    MagnetosphericShieldValidationResult,
    validate_magnetospheric_shield_parameters,
)

from .inspector import MagnetosphericShieldInspector
from .rubric import MagnetosphericShieldRubric, RubricEvaluation
from .blind_critic import MagnetosphericShieldBlindCritic
from .elevation_engine import MagnetosphericShieldElevationEngine
from .master import MagnetosphericShieldMaster

__all__ = [
    "SPEED_OF_LIGHT",
    "VACUUM_PERMEABILITY",
    "ELEMENTARY_CHARGE",
    "PROTON_REST_MASS_KG",
    "PROTON_REST_ENERGY_MEV",
    "MIN_MAGNETIC_MOMENT_GA_M2",
    "MIN_STORMER_RIGIDITY_GV",
    "MIN_COIL_PEAK_FIELD_T",
    "MAX_HABITAT_LEAKAGE_FIELD_T",
    "MIN_HTS_CURRENT_DENSITY_A_M2",
    "MAX_COIL_OPERATING_TEMP_K",
    "MAX_QUENCH_DUMP_TIME_MS",
    "MAX_CREW_ANNUAL_DOSE_MSV",
    "MAX_SPE_DOSE_RATE_MGY_H",
    "MIN_ELECTROSTATIC_POTENTIAL_MV",
    "MIN_NEUTRALIZER_CURRENT_MA",
    "calculate_stormer_cutoff_rigidity",
    "calculate_larmor_gyroradius",
    "calculate_habitat_fringe_field",
    "MagnetosphericShieldValidationResult",
    "validate_magnetospheric_shield_parameters",
    "MagnetosphericShieldInspector",
    "MagnetosphericShieldRubric",
    "RubricEvaluation",
    "MagnetosphericShieldBlindCritic",
    "MagnetosphericShieldElevationEngine",
    "MagnetosphericShieldMaster",
]
