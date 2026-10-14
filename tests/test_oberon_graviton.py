#!/usr/bin/env python3
"""
Unit Test Suite for Dr. Oberon 'The Graviton' Sterling
Gravitational Wave Detector & Optomechanical Interferometry Architect Master Subsystem
"""

import math
import pytest
from professions.gravitational_wave_detector_architect import (
    strain_sensitivity,
    fabry_perot_power,
    squeezed_light_noise_reduction,
    pdh_frequency_error,
    quad_pendulum_transfer_function,
    newtonian_noise_residual,
    validate_gravitational_wave_detector,
    GravitationalWaveInspector,
    GravitationalWaveRubric,
    GravitationalWaveBlindCritic,
    GravitationalWaveElevationEngine,
    DrOberonSterling
)


def test_strain_sensitivity_calculation():
    # Differential displacement 2.0e-20 m across 4000 m arm cavity
    delta_l = 2.0e-20
    arm_length = 4000.0
    h = strain_sensitivity(delta_l, arm_length)
    # Expected: 2 * 2.0e-20 / 4000 = 1.0e-23
    assert math.isclose(h, 1.0e-23, rel_tol=1e-6)

    with pytest.raises(ValueError):
        strain_sensitivity(delta_l, -100.0)
    with pytest.raises(ValueError):
        strain_sensitivity(-1.0, 4000.0)


def test_fabry_perot_power_build_up():
    # Input power 100 W, cavity finesse 450
    p_in = 100.0
    finesse = 450.0
    p_cav = fabry_perot_power(p_in, finesse)
    # Expected: 100 * (2 * 450 / pi) = 90000 / pi approx 28647.89 W
    expected = (100.0 * 2.0 * 450.0) / math.pi
    assert math.isclose(p_cav, expected, rel_tol=1e-5)


def test_squeezed_light_noise_reduction():
    # 6.0 dB squeezing
    eta_6db = squeezed_light_noise_reduction(6.0)
    # 10^(-0.6) approx 0.2511886
    assert math.isclose(eta_6db, 10.0 ** (-0.6), rel_tol=1e-5)

    # 10.0 dB squeezing gives 0.1 factor
    eta_10db = squeezed_light_noise_reduction(10.0)
    assert math.isclose(eta_10db, 0.1, rel_tol=1e-5)

    with pytest.raises(ValueError):
        squeezed_light_noise_reduction(-2.0)


def test_quad_pendulum_and_newtonian_noise():
    # 4-stage monolithic pendulum at 10 Hz with resonance f0 = 1 Hz
    t_10hz = quad_pendulum_transfer_function(10.0, 1.0)
    # Expected: (1/10)^8 = 1.0e-8
    assert math.isclose(t_10hz, 1.0e-8, rel_tol=1e-5)

    # Below resonance: unity transmission
    t_sub = quad_pendulum_transfer_function(0.5, 1.0)
    assert t_sub == 1.0

    # Newtonian noise subtraction
    raw_nn = 1.0e-21
    sub_eff = 85.0
    res_nn = newtonian_noise_residual(raw_nn, sub_eff)
    # Expected: 1.0e-21 * (1 - 0.85) = 1.5e-22
    assert math.isclose(res_nn, 1.5e-22, rel_tol=1e-5)


def test_interferometer_validation_result():
    # Valid configuration
    valid_res = validate_gravitational_wave_detector(
        strain_sensitivity_hz=8.0e-24,
        squeezing_factor_db=7.5,
        cavity_power_kw=650.0,
        seismic_transfer_at_10hz=5.0e-11,
        newtonian_subtraction_pct=85.0,
        lock_jitter_m=5.0e-16
    )
    assert valid_res.is_valid is True
    assert len(valid_res.violations) == 0

    # Invalid configuration
    invalid_res = validate_gravitational_wave_detector(
        strain_sensitivity_hz=5.0e-23,  # > 1.0e-23
        squeezing_factor_db=3.5,       # < 6.0
        cavity_power_kw=200.0,         # < 500.0
        seismic_transfer_at_10hz=2.0e-9,  # > 1.0e-10
        newtonian_subtraction_pct=50.0,   # < 80.0
        lock_jitter_m=8.0e-15          # > 1.0e-15
    )
    assert invalid_res.is_valid is False
    assert len(invalid_res.violations) == 6


def test_gravitational_wave_inspector_and_rubric():
    inspector = GravitationalWaveInspector()

    clean_code = """
def run_interferometer():
    strain_sensitivity = 4.5e-24
    squeezing_factor = 8.5
    cavity_power = 750.0
    seismic_transfer = 2.5e-11
    newtonian_subtraction = 88.5
    lock_jitter = 3.2e-16
    return "Locked at Dark Port"
"""
    clean_flaws = inspector.inspect_code(clean_code)
    clean_eval = GravitationalWaveRubric.evaluate(clean_flaws)
    assert len(clean_flaws) == 0
    assert clean_eval["passed"] is True
    assert clean_eval["score"] == 100

    flawed_code = """
def run_interferometer():
    strain_sensitivity = 8.0e-22
    squeezing_factor = 2.0
    cavity_power = 150.0
    seismic_transfer = 5.0e-8
    newtonian_subtraction = 45.0
    lock_jitter = 9.0e-14
    try:
        detect_photodiode_rf()
    except Exception:
        pass
    return "Interferometer Lock Lost"
"""
    flawed_issues = inspector.inspect_code(flawed_code)
    flawed_eval = GravitationalWaveRubric.evaluate(flawed_issues)
    assert len(flawed_issues) >= 6
    assert flawed_eval["passed"] is False
    assert flawed_eval["score"] < 40


def test_elevation_engine_and_master_closed_loop():
    flawed_script = """
def gravitational_wave_observatory_executive():
    strain_sensitivity = 6.0e-22
    squeezing_factor = 3.0
    cavity_power = 250.0
    seismic_transfer = 8.0e-9
    newtonian_subtraction = 55.0
    lock_jitter = 7.0e-15
    try:
        read_differential_arm_photocurrent()
    except Exception:
        pass
    return "Interferometer Drift"
"""
    master = DrOberonSterling(min_passing_score=95)
    result = master.execute_closed_loop(flawed_script, target_file="interferometer_core.py")

    assert result["status"] == "CERTIFIED"
    assert result["final_score"] >= 95
    assert "Oberon" in result["master"]
    assert len(result["actions_applied"]) >= 6

    # Verify that elevated code passes inspector with 100%
    inspector = GravitationalWaveInspector()
    post_flaws = inspector.inspect_code(result["elevated_code"])
    assert len(post_flaws) == 0
