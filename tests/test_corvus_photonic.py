#!/usr/bin/env python3
"""
Unit Test Suite for Dr. Corvus 'The Photonic' Vance
Photonic Computing & Neuromorphic Optical Architect Master Subsystem
"""

import math
import pytest
from professions.photonic_computing_architect import (
    SPEED_OF_LIGHT,
    SI_GROUP_INDEX,
    SI_THERMO_OPTIC_COEFF,
    mzi_transfer_matrix,
    unitary_error_norm,
    thermo_optic_phase_shift,
    optical_mac_latency,
    photodiode_shot_noise_current,
    optical_snr_db,
    validate_photonic_mesh,
    PhotonicInspector,
    PhotonicRubric,
    PhotonicBlindCritic,
    PhotonicElevationEngine,
    DrCorvusVance
)


def test_mzi_transfer_matrix_unitarity():
    # 1. 50:50 beam splitter (theta = pi/2, phi = 0)
    u_5050 = mzi_transfer_matrix(math.pi / 2.0, 0.0)
    err = unitary_error_norm(u_5050)
    assert err < 1.0e-12, f"Unitary error {err} must be near zero machine precision."

    # 2. Arbitrary phase shifts (theta = 1.234 rad, phi = 0.567 rad)
    u_arb = mzi_transfer_matrix(1.234, 0.567)
    err_arb = unitary_error_norm(u_arb)
    assert err_arb < 1.0e-12


def test_thermo_optic_phase_shift_and_mac_latency():
    # Phase shift in 50 um silicon heater for delta_T = 5 K at 1550 nm
    length_m = 50.0e-6
    delta_t = 5.0
    shift = thermo_optic_phase_shift(SI_THERMO_OPTIC_COEFF, delta_t, length_m)
    # Expected: (2 * pi / 1.55e-6) * 1.86e-4 * 5 * 50e-6 ~ 0.188 rad
    assert 0.15 < shift < 0.25

    # Transit time through 100 um waveguide: tau = n_g * L / c in ps
    latency_ps = optical_mac_latency(100.0e-6, SI_GROUP_INDEX)
    # Expected: (4.2 * 100e-6) / 3e8 = 1.4e-12 s = 1.4 ps
    assert 1.3 < latency_ps < 1.5


def test_photodiode_shot_noise_and_osnr():
    # 1 mW optical power, responsivity 0.9 A/W, 10 GHz bandwidth
    resp = 0.9
    p_opt = 1.0e-3
    bw = 10.0e9
    i_shot = photodiode_shot_noise_current(resp, p_opt, bw)
    assert i_shot > 0
    # Expected order: sqrt(2 * 1.6e-19 * 0.9e-3 * 10e9) ~ 1.7e-6 A (1.7 uA)
    assert 1.0e-6 < i_shot < 2.5e-6

    # Signal 1 mW, noise 1 uW -> 30 dB OSNR
    snr = optical_snr_db(1.0e-3, 1.0e-6)
    assert math.isclose(snr, 30.0, rel_tol=1e-5)


def test_validate_photonic_mesh_bounds():
    # Clean validation
    valid = validate_photonic_mesh(
        unitary_error=3.5e-5,
        extinction_ratio_db=32.0,
        residual_phase_drift_rad=0.003,
        wdm_crosstalk_db=-30.0,
        mac_latency_ps=1.4,
        energy_per_mac_fj=4.2,
        osnr_db=38.0
    )
    assert valid.is_valid is True
    assert len(valid.violations) == 0

    # Violating validation
    invalid = validate_photonic_mesh(
        unitary_error=5.0e-3,
        extinction_ratio_db=18.0,
        residual_phase_drift_rad=0.08,
        wdm_crosstalk_db=-15.0,
        mac_latency_ps=1.4,
        energy_per_mac_fj=25.0,
        osnr_db=22.0
    )
    assert invalid.is_valid is False
    assert len(invalid.violations) == 6


def test_photonic_inspector_and_rubric():
    inspector = PhotonicInspector()

    clean_code = """
def run_optical_tensor_core():
    unitary_error = 3.5e-5
    extinction_ratio = 32.0
    phase_drift = 0.003
    wdm_crosstalk = -30.0
    energy_per_mac = 4.2
    osnr_db = 38.0
    return "Matrix-Vector Multiply OK"
"""
    clean_flaws = inspector.inspect_code(clean_code)
    clean_eval = PhotonicRubric.evaluate(clean_flaws)
    assert len(clean_flaws) == 0
    assert clean_eval["passed"] is True
    assert clean_eval["score"] == 100

    flawed_code = """
def run_optical_tensor_core():
    unitary_error = 8.5e-3
    extinction_ratio = 18.0
    phase_drift = 0.05
    wdm_crosstalk = -15.0
    energy_per_mac = 22.0
    osnr_db = 22.0
    try:
        tune_microheaters()
    except Exception:
        pass
    return "Degraded"
"""
    flawed_issues = inspector.inspect_code(flawed_code)
    flawed_eval = PhotonicRubric.evaluate(flawed_issues)
    assert len(flawed_issues) >= 6
    assert flawed_eval["passed"] is False
    assert flawed_eval["score"] < 40


def test_blind_critic_catches_phase_drift_and_crosstalk():
    critic = PhotonicBlindCritic()
    leaky_mesh = """
def optical_gemm():
    phase_drift = 0.08
    wdm_crosstalk = -12.0
    mzi_er = 15.0
    return "Cross-Talk Heavy"
"""
    audit = critic.audit(leaky_mesh)
    assert audit["verdict"] == "REJECTED"
    assert audit["score"] < 95
    assert audit["flaw_count"] >= 3


def test_elevation_engine_and_master_closed_loop():
    flawed_script = """
def neuromorphic_core():
    unitary_error = 5.0e-3
    extinction_ratio = 19.0
    phase_drift = 0.06
    wdm_crosstalk = -14.0
    energy_per_mac = 18.0
    osnr_db = 24.0
    try:
        calibrate_phase_shifters()
    except Exception:
        pass
    return "Computed"
"""
    master = DrCorvusVance(min_passing_score=95)
    result = master.execute_closed_loop(flawed_script, target_file="optical_mvm.py")

    assert result["status"] == "CERTIFIED"
    assert result["final_score"] >= 95
    assert "Corvus" in result["master"]
    assert len(result["actions_applied"]) >= 5

    # Verify that elevated code has zero remaining flaws
    inspector = PhotonicInspector()
    post_flaws = inspector.inspect_code(result["elevated_code"])
    assert len(post_flaws) == 0
