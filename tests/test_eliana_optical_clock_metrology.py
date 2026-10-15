"""Test suite for Dr. Eliana Sterling - Optical Lattice Clock & Quantum Metrology Architect.

Covers gravitational redshift, Allan deviation, AC Stark shifts, QPN limits, AST inspection, rubric, critic, elevation, and master reflection.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.optical_lattice_clock_metrology_architect import (
    MAX_FRACTIONAL_INACCURACY,
    MAX_ALLAN_DEV_COEFF,
    calculate_gravitational_redshift_fraction,
    calculate_allan_deviation,
    calculate_ac_stark_shift_fraction,
    calculate_quantum_projection_noise_limit,
    validate_optical_clock_parameters,
    OpticalClockInspector,
    OpticalClockRubric,
    OpticalClockBlindCritic,
    OpticalClockElevationEngine,
    OpticalClockMaster,
)


def test_gravitational_redshift_and_allan_deviation_scaling():
    # 1.0 meter elevation difference in standard Earth gravity:
    # Delta_nu / nu_0 = (g * Delta_h) / c^2 = (9.80665 * 1.0) / (299792458^2)
    # ~= 1.0909e-16
    shift_1m = calculate_gravitational_redshift_fraction(1.0)
    assert 1.08e-16 <= shift_1m <= 1.10e-16

    # 1.0 centimeter elevation difference: ~1.09e-18
    shift_1cm = calculate_gravitational_redshift_fraction(0.01)
    assert 1.08e-18 <= shift_1cm <= 1.10e-18

    # Allan deviation scaling: instability coeff = 1.0e-16
    # At tau = 100 seconds: sigma_y(100) = 1.0e-16 / 10 = 1.0e-17
    dev_100s = calculate_allan_deviation(1.0e-16, 100.0)
    assert abs(dev_100s - 1.0e-17) < 1.0e-20

    # Zero tau edge case
    assert calculate_allan_deviation(1.0e-16, 0.0) == float("inf")


def test_magic_wavelength_ac_stark_and_qpn_limits():
    # Residual Stark shift for detuning 0.02 nm at 20 uK trap depth
    # Delta_nu / nu_0 ~ 2.5e-19 * 0.02 * 20 = 1.0e-19
    stark_shift = calculate_ac_stark_shift_fraction(813.448, 813.428, trap_depth_microkelvin=20.0)
    assert abs(stark_shift - 1.0e-19) < 1.0e-21

    # Quantum projection noise limit for Q = 1e15, N = 10,000 atoms, T_cycle = 1.0 s, tau = 10,000 s
    # sigma_QPN = (1 / (pi * 1e15 * 100)) * sqrt(1 / 10000) = (1 / (3.14159e17)) * 0.01 ~= 3.18e-20
    qpn = calculate_quantum_projection_noise_limit(1.0e15, 10000, 1.0, 10000.0)
    assert 3.0e-20 <= qpn <= 3.4e-20

    # Degenerate zero inputs
    assert calculate_quantum_projection_noise_limit(0.0, 10000, 1.0, 10000.0) == float("inf")


def test_validate_optical_clock_parameters_nominal_and_breaches():
    res_nominal = validate_optical_clock_parameters(
        fractional_inaccuracy=8.5e-19,
        allan_deviation_1s=7.2e-17,
        magic_wavelength_detuning_nm=0.012,
        laser_linewidth_mhz=6.5,
        cavity_finesse=650000.0,
        cavity_temperature_k=124.0,
        bbr_temp_uncertainty_mk=6.0,
        atom_temperature_uk=1.2,
        collisional_shift_fraction=4.5e-20,
        residual_zeeman_ut=0.45
    )
    assert res_nominal.is_valid is True
    assert len(res_nominal.flaws) == 0

    # Breach case: high uncertainty (5.0e-17), poor stability (4.0e-15), detuning (0.15 nm), broad laser (45 mHz),
    # low finesse (200,000), wrong temp (295 K), high BBR error (80 mK), hot atoms (15 uK), high collisions (1e-17), high B-field (8.0 uT)
    res_breach = validate_optical_clock_parameters(
        fractional_inaccuracy=5.0e-17,
        allan_deviation_1s=4.0e-15,
        magic_wavelength_detuning_nm=0.15,
        laser_linewidth_mhz=45.0,
        cavity_finesse=200000.0,
        cavity_temperature_k=295.0,
        bbr_temp_uncertainty_mk=80.0,
        atom_temperature_uk=15.0,
        collisional_shift_fraction=1.0e-17,
        residual_zeeman_ut=8.0
    )
    assert res_breach.is_valid is False
    assert len(res_breach.flaws) == 10


def test_optical_clock_inspector_patterns_and_ast():
    inspector = OpticalClockInspector()

    flawed_code = (
        "# TODO: finish optical lattice trapping alignment\n"
        "fractional_inaccuracy = 3.5e-17\n"
        "allan_deviation_1s = 2.8e-15\n"
        "magic_wavelength_detuning_nm = 0.12\n"
        "laser_linewidth_mhz = 25.0\n"
        "cavity_finesse = 320000.0\n"
        "cavity_temperature_k = 130.0\n"
        "bbr_temp_uncertainty_mk = 22.0\n"
        "atom_temperature_uk = 4.5\n"
        "collisional_shift_fraction = 6.0e-18\n"
        "residual_zeeman_ut = 3.2\n"
        "def stabilize_laser() -> bool:\n"
        "    pass\n"
        "try:\n"
        "    count = 100\n"
        "except Exception:\n"
        "    pass\n"
    )

    flaws = inspector.inspect_source(flawed_code)
    flaw_ids = [f["id"] for f in flaws]

    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "FRACTIONAL_INACCURACY_EXCESS" in flaw_ids
    assert "ALLAN_DEVIATION_EXCESS" in flaw_ids
    assert "MAGIC_WAVELENGTH_DETUNING_EXCESS" in flaw_ids
    assert "LASER_LINEWIDTH_EXCESS" in flaw_ids
    assert "CAVITY_FINESSE_DEFICIT" in flaw_ids
    assert "CAVITY_TEMPERATURE_DEVIATION" in flaw_ids
    assert "BBR_UNCERTAINTY_EXCESS" in flaw_ids
    assert "ATOM_TEMPERATURE_EXCESS" in flaw_ids
    assert "COLLISIONAL_SHIFT_EXCESS" in flaw_ids
    assert "ZEEMAN_FIELD_EXCESS" in flaw_ids
    assert "EMPTY_FUNCTION_BODY" in flaw_ids
    assert "EMPTY_EXCEPT_BLOCK" in flaw_ids

    text_flaws = inspector.inspect_code(flawed_code)
    assert len(text_flaws) == len(flaws)


def test_optical_clock_rubric_scoring_and_passing():
    rubric = OpticalClockRubric()

    # Zero flaws -> 100
    eval_pass = rubric.evaluate([])
    assert eval_pass.score == 100
    assert eval_pass.passed is True

    # One CRITICAL flaw (-25 pts) -> score 75, rejected
    flaw_crit = [{"id": "FRACTIONAL_INACCURACY_EXCESS", "severity": "CRITICAL", "description": "Drift breach"}]
    eval_crit = rubric.evaluate(flaw_crit)
    assert eval_crit.score == 75
    assert eval_crit.passed is False

    # One LOW flaw (-3 pts) -> score 97, passes (>= 95)
    flaw_low = [{"id": "CALIBRATION_NOTICE", "severity": "LOW", "description": "Diagnostic notice"}]
    eval_low = rubric.evaluate(flaw_low)
    assert eval_low.score == 97
    assert eval_low.passed is True


def test_blind_critic_adversarial_rejection():
    critic = OpticalClockBlindCritic()

    clean_code = (
        "fractional_inaccuracy = 8.5e-19\n"
        "allan_deviation_1s = 7.2e-17\n"
        "magic_wavelength_detuning_nm = 0.012\n"
        "laser_linewidth_mhz = 6.5\n"
        "cavity_finesse = 650000.0\n"
        "cavity_temperature_k = 124.0\n"
        "bbr_temp_uncertainty_mk = 6.0\n"
        "atom_temperature_uk = 1.2\n"
        "collisional_shift_fraction = 4.5e-20\n"
        "residual_zeeman_ut = 0.45\n"
        "def clock_status() -> bool:\n"
        "    return True\n"
    )

    clean_res = critic.audit(clean_code)
    assert clean_res["verdict"] == "APPROVED"
    assert clean_res["score"] == 100
    assert clean_res["passed"] is True

    flawed_code = (
        "fractional_inaccuracy = 5.0e-17\n"
        "magic_wavelength_detuning_nm = 0.20\n"
    )
    flawed_res = critic.audit(flawed_code)
    assert flawed_res["verdict"] == "REJECTED"
    assert flawed_res["passed"] is False
    assert flawed_res["score"] < 95


def test_elevation_engine_and_master_closed_loop():
    engine = OpticalClockElevationEngine()

    flawed_code = (
        "# TODO: stabilize clock laser to silicon cavity\n"
        "fractional_inaccuracy = 4.2e-17\n"
        "allan_deviation_1s = 3.5e-15\n"
        "magic_wavelength_detuning_nm = 0.14\n"
        "laser_linewidth_mhz = 28.0\n"
        "cavity_finesse = 280000.0\n"
        "cavity_temperature_k = 129.5\n"
        "bbr_temp_uncertainty_mk = 25.0\n"
        "atom_temperature_uk = 5.2\n"
        "collisional_shift_fraction = 8.0e-18\n"
        "residual_zeeman_ut = 3.8\n"
        "def frequency_telemetry() -> dict:\n"
        "    pass\n"
        "try:\n"
        "    val = 1\n"
        "except ValueError:\n"
        "    pass\n"
    )

    elevated, actions = engine.elevate(flawed_code)
    assert len(actions) > 0

    critic = OpticalClockBlindCritic()
    audit_after = critic.audit(elevated)
    assert audit_after["passed"] is True
    assert audit_after["score"] >= 95

    # Test master closed-loop execution
    master = OpticalClockMaster()
    res = master.evaluate_and_elevate(flawed_code, target_file="optical_clock.py")
    assert res["status"] == "certified"
    assert res["final_score"] >= 95
    assert res["iterations"] >= 1
    assert len(res["repaired_flaws"]) > 0
