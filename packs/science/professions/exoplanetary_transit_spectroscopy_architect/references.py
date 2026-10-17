"""
Domain references and quantitative mathematical equations for
Dr. Linus 'The Exoplanet' Sterling - Principal Exoplanetary Atmosphere & Transit Spectroscopy Architect.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any, List

# Physical Constants
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K
ATOMIC_MASS_UNIT = 1.66053906660e-27  # kg
GRAVITATIONAL_CONSTANT = 6.67430e-11  # m^3 / (kg s^2)
PLANCK_CONSTANT = 6.62607015e-34  # J s
SPEED_OF_LIGHT = 299792458.0  # m/s

# Standard Reference Values
R_EARTH = 6.371e6  # m
R_JUPITER = 7.1492e7  # m
R_SUN = 6.957e8  # m
M_EARTH = 5.972e24  # kg
M_JUPITER = 1.898e27  # kg
M_SUN = 1.989e30  # kg

# Quantitative Standards
MIN_TRANSIT_DEPTH = 1.0e-5  # 10 ppm minimum detectable occultation
MIN_SCALE_HEIGHT_KM = 10.0  # km (rocky secondary atmosphere)
MAX_SCALE_HEIGHT_KM = 3000.0  # km (puffiest ultra-hot gas giant)
MIN_FEATURE_AMPLITUDE_PPM = 1.0  # ppm (1.0e-6)
MIN_DETECTION_SNR = 5.0  # 5-sigma detection significance
MAX_SPOT_FILLING_FACTOR = 0.30  # Maximum unocculted spot coverage fraction
MIN_REDUCED_CHI_SQUARED = 0.80  # Goodness-of-fit lower bound
MAX_REDUCED_CHI_SQUARED = 1.50  # Goodness-of-fit upper bound


def calculate_transit_depth(r_p_m: float, r_star_m: float) -> float:
    """Calculate geometric transit occultation depth delta = (R_p / R_*)^2."""
    if r_star_m <= 0.0 or r_p_m <= 0.0:
        return 0.0
    return (r_p_m / r_star_m) ** 2


def calculate_surface_gravity(m_p_kg: float, r_p_m: float) -> float:
    """Calculate exoplanet surface gravity g = G * M_p / R_p^2 (m/s^2)."""
    if r_p_m <= 0.0 or m_p_kg <= 0.0:
        return 0.0
    return (GRAVITATIONAL_CONSTANT * m_p_kg) / (r_p_m ** 2)


def calculate_scale_height(t_eq_k: float, mu_amu: float, g_m_s2: float) -> float:
    """
    Calculate atmospheric scale height H = (k_B * T_eq) / (mu * m_u * g) in meters.
    mu_amu: mean molecular weight in atomic mass units (e.g. 2.3 for H2/He, 28 for N2, 44 for CO2).
    """
    if mu_amu <= 0.0 or g_m_s2 <= 0.0 or t_eq_k <= 0.0:
        return 0.0
    mu_kg = mu_amu * ATOMIC_MASS_UNIT
    return (BOLTZMANN_CONSTANT * t_eq_k) / (mu_kg * g_m_s2)


def calculate_feature_amplitude(r_p_m: float, r_star_m: float, scale_height_m: float, n_h: float = 5.0) -> float:
    """
    Calculate transmission spectral feature amplitude Delta delta_lambda ~= 2 * (R_p / R_*) * (N_H * H / R_*).
    n_h: Number of atmospheric scale heights probed across transmission opacity window (typically 3.0 to 6.0).
    """
    if r_star_m <= 0.0 or r_p_m <= 0.0 or scale_height_m <= 0.0:
        return 0.0
    return 2.0 * (r_p_m / r_star_m) * (n_h * scale_height_m / r_star_m)


def calculate_spectroscopic_snr(signal_amplitude: float, noise_uncertainty: float) -> float:
    """Calculate detection significance SNR = signal / noise."""
    if noise_uncertainty <= 0.0 or signal_amplitude <= 0.0:
        return 0.0
    return signal_amplitude / noise_uncertainty


def planck_blackbody_radiance(wavelength_m: float, temperature_k: float) -> float:
    """Calculate blackbody spectral radiance B_lambda(T) = (2 h c^2 / lambda^5) / (exp(h c / lambda k_B T) - 1)."""
    if wavelength_m <= 0.0 or temperature_k <= 0.0:
        return 0.0
    try:
        exponent = (PLANCK_CONSTANT * SPEED_OF_LIGHT) / (wavelength_m * BOLTZMANN_CONSTANT * temperature_k)
        if exponent > 700.0:
            return 0.0
        numerator = 2.0 * PLANCK_CONSTANT * (SPEED_OF_LIGHT ** 2) / (wavelength_m ** 5)
        denominator = math.exp(exponent) - 1.0
        return numerator / denominator
    except (OverflowError, ZeroDivisionError):
        return 0.0


def calculate_stellar_spot_contamination(
    delta_true: float,
    f_spot: float,
    t_star_k: float,
    t_spot_k: float,
    wavelength_m: float = 1.4e-6
) -> float:
    """
    Calculate apparent transit depth under unocculted starspot contamination (Transit Light Source Effect).
    delta_obs = delta_true / (1 - f_spot * (1 - B_lambda(T_spot) / B_lambda(T_star)))
    """
    if delta_true <= 0.0 or f_spot < 0.0:
        return delta_true
    b_star = planck_blackbody_radiance(wavelength_m, t_star_k)
    b_spot = planck_blackbody_radiance(wavelength_m, t_spot_k)
    if b_star <= 0.0:
        return delta_true
    ratio = b_spot / b_star
    denominator = 1.0 - f_spot * (1.0 - ratio)
    if denominator <= 0.01:
        return delta_true
    return delta_true / denominator


def calculate_reduced_chi_squared(
    observed: List[float],
    model: List[float],
    uncertainties: List[float],
    num_parameters: int = 4
) -> float:
    """Calculate reduced chi-squared chi^2_nu = (1 / (N - M)) * sum(((y_i - f_i) / sigma_i)^2)."""
    n = len(observed)
    dof = n - num_parameters
    if dof <= 0 or len(model) != n or len(uncertainties) != n:
        return 1.0
    chi2_sum = 0.0
    for obs, mod, sigma in zip(observed, model, uncertainties):
        if sigma > 0.0:
            chi2_sum += ((obs - mod) / sigma) ** 2
    return chi2_sum / dof


@dataclass
class ExoplanetTransitSpecResult:
    """Result container for exoplanetary transit spectroscopy physical validation."""
    transit_depth: float
    surface_gravity: float
    scale_height_km: float
    feature_amplitude_ppm: float
    detection_snr: float
    spot_corrected_depth: float
    reduced_chi_squared: float
    is_valid: bool
    details: Dict[str, Any] = field(default_factory=dict)


def validate_exoplanet_transit_spectroscopy(
    r_p_m: float,
    r_star_m: float,
    m_p_kg: float,
    t_eq_k: float,
    mu_amu: float,
    noise_uncertainty: float,
    f_spot: float = 0.05,
    t_star_k: float = 5778.0,
    t_spot_k: float = 4500.0,
    n_scale_heights: float = 5.0,
    reduced_chi2: float = 1.05
) -> ExoplanetTransitSpecResult:
    """Validate full exoplanet transmission spectroscopy parameter set against astrophysical laws."""
    depth = calculate_transit_depth(r_p_m, r_star_m)
    gravity = calculate_surface_gravity(m_p_kg, r_p_m)
    scale_height_m = calculate_scale_height(t_eq_k, mu_amu, gravity)
    scale_height_km = scale_height_m / 1000.0
    feature_amp = calculate_feature_amplitude(r_p_m, r_star_m, scale_height_m, n_scale_heights)
    feature_ppm = feature_amp * 1.0e6
    snr = calculate_spectroscopic_snr(feature_amp, noise_uncertainty)
    spot_depth = calculate_stellar_spot_contamination(depth, f_spot, t_star_k, t_spot_k)

    depth_valid = depth >= MIN_TRANSIT_DEPTH
    scale_valid = MIN_SCALE_HEIGHT_KM <= scale_height_km <= MAX_SCALE_HEIGHT_KM
    feature_valid = feature_ppm >= MIN_FEATURE_AMPLITUDE_PPM
    snr_valid = snr >= MIN_DETECTION_SNR
    spot_valid = 0.0 <= f_spot <= MAX_SPOT_FILLING_FACTOR
    chi2_valid = MIN_REDUCED_CHI_SQUARED <= reduced_chi2 <= MAX_REDUCED_CHI_SQUARED

    all_valid = (
        depth_valid and scale_valid and feature_valid and
        snr_valid and spot_valid and chi2_valid
    )

    details = {
        "transit_depth_ppm": depth * 1.0e6,
        "depth_valid": depth_valid,
        "surface_gravity_m_s2": gravity,
        "scale_height_km": scale_height_km,
        "scale_height_valid": scale_valid,
        "feature_amplitude_ppm": feature_ppm,
        "feature_valid": feature_valid,
        "detection_snr": snr,
        "snr_valid": snr_valid,
        "spot_filling_factor": f_spot,
        "spot_valid": spot_valid,
        "reduced_chi_squared": reduced_chi2,
        "chi2_valid": chi2_valid,
    }

    return ExoplanetTransitSpecResult(
        transit_depth=depth,
        surface_gravity=gravity,
        scale_height_km=scale_height_km,
        feature_amplitude_ppm=feature_ppm,
        detection_snr=snr,
        spot_corrected_depth=spot_depth,
        reduced_chi_squared=reduced_chi2,
        is_valid=all_valid,
        details=details
    )
