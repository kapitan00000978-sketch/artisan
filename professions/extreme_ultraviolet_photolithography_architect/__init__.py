"""High-NA EUV Photolithography & Sub-2nm Semiconductor Patterning Subsystem.

Formulated by Dr. Nadia 'The Sub-Micron' Vance,
Principal High-NA EUV Photolithography & Sub-2nm Semiconductor Patterning Architect.
"""

from .references import (
    EUV_WAVELENGTH_NM,
    MAX_EUV_BANDWIDTH_NM,
    MIN_HIGH_NA,
    MIN_K1_FACTOR,
    MAX_RAYLEIGH_HALF_PITCH_NM,
    MAX_LWR_3SIGMA_NM,
    MAX_LER_3SIGMA_NM,
    MIN_PHOTON_DENSITY_PER_NM2,
    MIN_DOSE_TO_SIZE_MJ_CM2,
    MAX_DOSE_TO_SIZE_MJ_CM2,
    MAX_OVERLAY_ERROR_NM,
    MAX_CDU_3SIGMA_NM,
    MIN_PELLICLE_TRANSMISSION,
    MIN_PELLICLE_THERMAL_WATTS,
    MIN_LPP_CONVERSION_EFFICIENCY,
    MIN_TIN_DROPLET_FREQ_KHZ,
    MIN_LASER_POWER_KW,
    EUVLithographyValidationResult,
    calculate_euv_photon_energy_ev,
    calculate_rayleigh_resolution,
    calculate_photon_density_per_nm2,
    calculate_stochastic_lwr_3sigma,
    calculate_lpp_conversion_efficiency,
    validate_euv_lithography_parameters,
)
from .inspector import EUVLithographyInspector
from .rubric import EUVLithographyRubric, PASSING_SCORE
from .blind_critic import EUVLithographyBlindCritic
from .elevation_engine import EUVLithographyElevationEngine
from .master import EUVLithographyMaster, ActiveDecisionJournal

__all__ = [
    "EUV_WAVELENGTH_NM",
    "MAX_EUV_BANDWIDTH_NM",
    "MIN_HIGH_NA",
    "MIN_K1_FACTOR",
    "MAX_RAYLEIGH_HALF_PITCH_NM",
    "MAX_LWR_3SIGMA_NM",
    "MAX_LER_3SIGMA_NM",
    "MIN_PHOTON_DENSITY_PER_NM2",
    "MIN_DOSE_TO_SIZE_MJ_CM2",
    "MAX_DOSE_TO_SIZE_MJ_CM2",
    "MAX_OVERLAY_ERROR_NM",
    "MAX_CDU_3SIGMA_NM",
    "MIN_PELLICLE_TRANSMISSION",
    "MIN_PELLICLE_THERMAL_WATTS",
    "MIN_LPP_CONVERSION_EFFICIENCY",
    "MIN_TIN_DROPLET_FREQ_KHZ",
    "MIN_LASER_POWER_KW",
    "EUVLithographyValidationResult",
    "calculate_euv_photon_energy_ev",
    "calculate_rayleigh_resolution",
    "calculate_photon_density_per_nm2",
    "calculate_stochastic_lwr_3sigma",
    "calculate_lpp_conversion_efficiency",
    "validate_euv_lithography_parameters",
    "EUVLithographyInspector",
    "EUVLithographyRubric",
    "PASSING_SCORE",
    "EUVLithographyBlindCritic",
    "EUVLithographyElevationEngine",
    "EUVLithographyMaster",
    "ActiveDecisionJournal",
]
