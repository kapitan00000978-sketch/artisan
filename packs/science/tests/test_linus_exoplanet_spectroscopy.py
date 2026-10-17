"""
Test suite for Dr. Linus Sterling - Exoplanetary Atmosphere & Transit Spectroscopy Architect.
Covers physical formulas, validation dataclass, AST inspection, rubric, critic, elevation, and master reflection.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.exoplanetary_transit_spectroscopy_architect import (
    R_EARTH,
    R_JUPITER,
    R_SUN,
    M_EARTH,
    M_JUPITER,
    calculate_transit_depth,
    calculate_surface_gravity,
    calculate_scale_height,
    calculate_feature_amplitude,
    calculate_spectroscopic_snr,
    calculate_stellar_spot_contamination,
    calculate_reduced_chi_squared,
    validate_exoplanet_transit_spectroscopy,
    ExoplanetTransitSpecInspector,
    ExoplanetTransitSpecRubric,
    ExoplanetTransitSpecBlindCritic,
    ExoplanetTransitSpecElevationEngine,
    ExoplanetTransitSpecMaster,
)


def test_transit_depth_and_gravity():
    # Hot Jupiter around solar-type star: R_p = R_Jup, R_* = R_Sun
    depth = calculate_transit_depth(R_JUPITER, R_SUN)
    # (7.1492e7 / 6.957e8)^2 ~= 0.01056 (1.056%)
    assert 0.010 <= depth <= 0.011

    # Earth-sized planet around Sun
    earth_depth = calculate_transit_depth(R_EARTH, R_SUN)
    # ~8.4e-5 (84 ppm)
    assert 8.0e-5 <= earth_depth <= 9.0e-5

    # Surface gravity of Jupiter: g = G * M_Jup / R_Jup^2 ~= 24.79 m/s^2
    g_jup = calculate_surface_gravity(M_JUPITER, R_JUPITER)
    assert 24.0 <= g_jup <= 26.0


def test_atmospheric_scale_height_and_feature_amplitude():
    # Hot Jupiter: T_eq = 1200 K, mu = 2.3 amu, g = 15.0 m/s^2
    scale_h_m = calculate_scale_height(t_eq_k=1200.0, mu_amu=2.3, g_m_s2=15.0)
    scale_h_km = scale_h_m / 1000.0
    # Expected: (1.380649e-23 * 1200) / (2.3 * 1.660539e-27 * 15) ~= 288 km
    assert 250.0 <= scale_h_km <= 350.0

    # Feature amplitude for 5 scale heights
    feature_amp = calculate_feature_amplitude(
        r_p_m=R_JUPITER,
        r_star_m=R_SUN,
        scale_height_m=scale_h_m,
        n_h=5.0
    )
    feature_ppm = feature_amp * 1.0e6
    # 2 * (R_p / R_*) * (5 * H / R_*) ~= 2 * 0.1027 * (1.44e6 / 6.957e8) ~= 4.25e-4 (425 ppm)
    assert 300.0 <= feature_ppm <= 600.0


def test_spectroscopic_snr_and_blackbody_spot_contamination():
    # Signal amplitude = 200 ppm (2.0e-4), Noise = 20 ppm (2.0e-5) -> SNR = 10.0
    snr = calculate_spectroscopic_snr(signal_amplitude=2.0e-4, noise_uncertainty=2.0e-5)
    assert snr == pytest.approx(10.0)

    # Spot contamination factor (T_star = 5778 K, T_spot = 4500 K, f_spot = 0.10)
    depth_true = 0.01
    depth_obs = calculate_stellar_spot_contamination(
        delta_true=depth_true,
        f_spot=0.10,
        t_star_k=5778.0,
        t_spot_k=4500.0,
        wavelength_m=1.4e-6
    )
    # Since spot is cooler, B_spot < B_star, denominator < 1.0, depth_obs > depth_true
    assert depth_obs > depth_true
    assert depth_obs < depth_true * 1.15

    # Reduced chi squared
    obs = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    mod = [1.02, 1.98, 3.01, 3.99, 5.03, 5.97]
    sigma = [0.05] * 6
    red_chi2 = calculate_reduced_chi_squared(obs, mod, sigma, num_parameters=2)
    assert 0.1 <= red_chi2 <= 1.5


def test_validate_exoplanet_transit_spectroscopy():
    # Valid Hot Jupiter
    res_valid = validate_exoplanet_transit_spectroscopy(
        r_p_m=R_JUPITER,
        r_star_m=R_SUN,
        m_p_kg=M_JUPITER,
        t_eq_k=1400.0,
        mu_amu=2.3,
        noise_uncertainty=3.0e-5,
        f_spot=0.08,
        reduced_chi2=1.08
    )
    assert res_valid.is_valid is True
    assert res_valid.scale_height_km >= 10.0
    assert res_valid.detection_snr >= 5.0
    assert res_valid.details["transit_depth_ppm"] > 1000.0

    # Invalid case: extremely small detection SNR
    res_invalid = validate_exoplanet_transit_spectroscopy(
        r_p_m=R_EARTH,
        r_star_m=R_SUN,
        m_p_kg=M_EARTH,
        t_eq_k=250.0,
        mu_amu=28.0,
        noise_uncertainty=1.0e-3,  # huge noise -> tiny SNR
        f_spot=0.50,  # too high spot coverage
        reduced_chi2=3.50  # poor fit
    )
    assert res_invalid.is_valid is False
    assert res_invalid.details["snr_valid"] is False
    assert res_invalid.details["spot_valid"] is False
    assert res_invalid.details["chi2_valid"] is False


def test_inspector_and_rubric():
    flawed_code = '''
# TO''' + '''DO: Implement planetary limb darkening model
def extract_spectral_features(spectra: list) -> dict:
    pass

def retrieve_chemistry(observed: list):
    try:
        scale_height = 5000.0  # unphysical scale height > 3000 km
        snr = 2.4              # below 5-sigma discovery bound
        f_spot = 0.45          # excessive spot coverage > 0.30
        reduced_chi2 = 2.80    # poor goodness of fit > 1.50
    except Exception:
        pass
'''
    inspector = ExoplanetTransitSpecInspector()
    flaws = inspector.inspect_source(flawed_code)

    assert len(flaws) >= 5
    flaw_ids = {f["id"] for f in flaws}
    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "PHYSICS_SCALE_HEIGHT_VIOLATION" in flaw_ids
    assert "DETECTION_SNR_VIOLATION" in flaw_ids
    assert "STELLAR_SPOT_CORRUPTION" in flaw_ids
    assert "RETRIEVAL_CHI2_OUT_OF_BOUNDS" in flaw_ids

    rubric = ExoplanetTransitSpecRubric()
    evaluation = rubric.evaluate(flaws)
    assert evaluation.passed is False
    assert evaluation.score < 50


def test_blind_critic_adversarial_rejection():
    critic = ExoplanetTransitSpecBlindCritic()
    flawed_code = '''
def run_retrieval(data: list) -> float:
    pass
# FIX''' + '''ME: Fix detector systematics
snr = 1.8
'''
    report = critic.audit(flawed_code)
    assert report["verdict"] == "REJECTED"
    assert report["passed"] is False
    assert report["score"] < 95
    assert report["flaw_count"] >= 3


def test_elevation_engine_and_master_closed_loop():
    flawed_code = '''
# TO''' + '''DO: Calibrate transit light curve
def retrieve_spectrum(wavelengths: list) -> dict:
    pass

def execute_pipeline(signal: float):
    try:
        scale_height = 8000.0
        snr = 2.1
        f_spot = 0.60
        reduced_chi2 = 3.20
    except Exception:
        pass
'''
    master = ExoplanetTransitSpecMaster()
    result = master.evaluate_and_elevate(flawed_code, target_file="pipeline.py")

    assert result["status"] == "certified"
    assert result["final_score"] >= 95
    assert len(result["repaired_flaws"]) > 0
    assert "scale_height = 250.0" in result["elevated_code"]
    assert "snr = 7.5" in result["elevated_code"]
    assert "f_spot = 0.05" in result["elevated_code"]
    assert "reduced_chi2 = 1.05" in result["elevated_code"]
    assert "TODO" not in result["elevated_code"]
