"""
Dr. Linus 'The Exoplanet' Sterling - Principal Exoplanetary Atmosphere & Transit Spectroscopy Architect.
Exports references, inspector, rubric, blind critic, elevation engine, and master controller.
"""

from .references import (
    BOLTZMANN_CONSTANT,
    ATOMIC_MASS_UNIT,
    GRAVITATIONAL_CONSTANT,
    PLANCK_CONSTANT,
    SPEED_OF_LIGHT,
    R_EARTH,
    R_JUPITER,
    R_SUN,
    M_EARTH,
    M_JUPITER,
    M_SUN,
    MIN_TRANSIT_DEPTH,
    MIN_SCALE_HEIGHT_KM,
    MAX_SCALE_HEIGHT_KM,
    MIN_FEATURE_AMPLITUDE_PPM,
    MIN_DETECTION_SNR,
    MAX_SPOT_FILLING_FACTOR,
    MIN_REDUCED_CHI_SQUARED,
    MAX_REDUCED_CHI_SQUARED,
    calculate_transit_depth,
    calculate_surface_gravity,
    calculate_scale_height,
    calculate_feature_amplitude,
    calculate_spectroscopic_snr,
    planck_blackbody_radiance,
    calculate_stellar_spot_contamination,
    calculate_reduced_chi_squared,
    ExoplanetTransitSpecResult,
    validate_exoplanet_transit_spectroscopy,
)

from .inspector import ExoplanetTransitSpecInspector
from .rubric import ExoplanetTransitSpecRubric, RubricEvaluation
from .blind_critic import ExoplanetTransitSpecBlindCritic
from .elevation_engine import ExoplanetTransitSpecElevationEngine
from .master import ExoplanetTransitSpecMaster

__all__ = [
    "BOLTZMANN_CONSTANT",
    "ATOMIC_MASS_UNIT",
    "GRAVITATIONAL_CONSTANT",
    "PLANCK_CONSTANT",
    "SPEED_OF_LIGHT",
    "R_EARTH",
    "R_JUPITER",
    "R_SUN",
    "M_EARTH",
    "M_JUPITER",
    "M_SUN",
    "MIN_TRANSIT_DEPTH",
    "MIN_SCALE_HEIGHT_KM",
    "MAX_SCALE_HEIGHT_KM",
    "MIN_FEATURE_AMPLITUDE_PPM",
    "MIN_DETECTION_SNR",
    "MAX_SPOT_FILLING_FACTOR",
    "MIN_REDUCED_CHI_SQUARED",
    "MAX_REDUCED_CHI_SQUARED",
    "calculate_transit_depth",
    "calculate_surface_gravity",
    "calculate_scale_height",
    "calculate_feature_amplitude",
    "calculate_spectroscopic_snr",
    "planck_blackbody_radiance",
    "calculate_stellar_spot_contamination",
    "calculate_reduced_chi_squared",
    "ExoplanetTransitSpecResult",
    "validate_exoplanet_transit_spectroscopy",
    "ExoplanetTransitSpecInspector",
    "ExoplanetTransitSpecRubric",
    "RubricEvaluation",
    "ExoplanetTransitSpecBlindCritic",
    "ExoplanetTransitSpecElevationEngine",
    "ExoplanetTransitSpecMaster",
]
