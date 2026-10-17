"""Planetary Geodynamo Core Fluid Dynamics and Magnetic Generation Master Subsystem.

Embodying the domain mastery of Dr. Lyra 'The Core' Sterling.
"""

from professions.planetary_geodynamo_core_architect.references import (
    GeodynamoCoreParameters,
    GeodynamoValidationResult,
    validate_geodynamo_parameters,
    calculate_magnetic_reynolds_number,
    calculate_rossby_number,
    calculate_ekman_number,
    calculate_elsasser_number,
    calculate_surface_dipole_energy_fraction,
    calculate_dynamo_number,
    MIN_MAGNETIC_REYNOLDS,
    MAX_ROSSBY_NUMBER,
    MAX_EKMAN_NUMBER,
    MIN_ELSASSER_NUMBER,
    MAX_ELSASSER_NUMBER,
    MIN_CMB_HEAT_FLUX_TW,
    MIN_ICB_BUOYANCY_FLUX_KG_S,
    MIN_SURFACE_DIPOLE_UT,
    MAX_SURFACE_DIPOLE_UT,
    MIN_CMB_MAGNETIC_FIELD_MT,
    MIN_SURFACE_DIPOLE_FRACTION,
    MAX_DIPOLE_TILT_DEG,
    MAX_WESTWARD_DRIFT_DEG_YR,
    MIN_DYNAMO_NUMBER,
)
from professions.planetary_geodynamo_core_architect.inspector import GeodynamoCodeInspector
from professions.planetary_geodynamo_core_architect.rubric import (
    GeodynamoRubricEvaluator,
    GeodynamoEvaluationReport,
    CriterionResult,
    PASSING_SCORE_THRESHOLD,
)
from professions.planetary_geodynamo_core_architect.blind_critic import (
    PlanetaryGeodynamoBlindCritic,
    BlindCriticVerdict,
)
from professions.planetary_geodynamo_core_architect.elevation_engine import PlanetaryGeodynamoElevationEngine
from professions.planetary_geodynamo_core_architect.master import PlanetaryGeodynamoMaster

__all__ = [
    "GeodynamoCoreParameters",
    "GeodynamoValidationResult",
    "validate_geodynamo_parameters",
    "calculate_magnetic_reynolds_number",
    "calculate_rossby_number",
    "calculate_ekman_number",
    "calculate_elsasser_number",
    "calculate_surface_dipole_energy_fraction",
    "calculate_dynamo_number",
    "MIN_MAGNETIC_REYNOLDS",
    "MAX_ROSSBY_NUMBER",
    "MAX_EKMAN_NUMBER",
    "MIN_ELSASSER_NUMBER",
    "MAX_ELSASSER_NUMBER",
    "MIN_CMB_HEAT_FLUX_TW",
    "MIN_ICB_BUOYANCY_FLUX_KG_S",
    "MIN_SURFACE_DIPOLE_UT",
    "MAX_SURFACE_DIPOLE_UT",
    "MIN_CMB_MAGNETIC_FIELD_MT",
    "MIN_SURFACE_DIPOLE_FRACTION",
    "MAX_DIPOLE_TILT_DEG",
    "MAX_WESTWARD_DRIFT_DEG_YR",
    "MIN_DYNAMO_NUMBER",
    "GeodynamoCodeInspector",
    "GeodynamoRubricEvaluator",
    "GeodynamoEvaluationReport",
    "CriterionResult",
    "PASSING_SCORE_THRESHOLD",
    "PlanetaryGeodynamoBlindCritic",
    "BlindCriticVerdict",
    "PlanetaryGeodynamoElevationEngine",
    "PlanetaryGeodynamoMaster",
]
