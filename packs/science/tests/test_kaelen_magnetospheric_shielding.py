"""Test suite for Commander Kaelen Vance - Magnetospheric Radiation Shielding Architect.

Covers relativistic kinematics, Stormer cut-off rigidity, Larmor gyroradius, AST inspection, rubric, critic, elevation, and master reflection.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.magnetospheric_radiation_shielding_architect import (
    MIN_STORMER_RIGIDITY_GV,
    MIN_COIL_PEAK_FIELD_T,
    MAX_HABITAT_LEAKAGE_FIELD_T,
    calculate_stormer_cutoff_rigidity,
    calculate_larmor_gyroradius,
    calculate_habitat_fringe_field,
    validate_magnetospheric_shield_parameters,
    MagnetosphericShieldInspector,
    MagnetosphericShieldRubric,
    MagnetosphericShieldBlindCritic,
    MagnetosphericShieldElevationEngine,
    MagnetosphericShieldMaster,
)


def test_stormer_cutoff_rigidity_and_larmor_gyroradius():
    # Magnetic moment M = 4.5e10 A*m^2 (45 GA*m^2) at radius r = 14.0 m
    # R_c = (mu_0 * c * M) / (4 * pi * r^2 * 1e9)
    # mu_0 * c / (4 * pi) = 29.9792458
    # R_c = 29.9792458 * 4.5e10 / (14^2 * 1e9) = 1.349e12 / (196 * 1e9) = 6.883 GV
    rigidity_gv = calculate_stormer_cutoff_rigidity(4.5e10, 14.0)
    assert 6.5 <= rigidity_gv <= 7.2
    assert rigidity_gv >= MIN_STORMER_RIGIDITY_GV

    # Relativistic Larmor radius for 500 MeV proton in 5.0 Tesla magnetic field
    # E_total = 500 + 938.272 = 1438.272 MeV
    # p = sqrt(1438.272^2 - 938.272^2) = 1090.07 MeV/c
    # r_L = p / (q * B) ~= 0.727 m
    r_larmor = calculate_larmor_gyroradius(500.0, 5.0)
    assert 0.70 <= r_larmor <= 0.76

    # Zero/negative inputs
    assert calculate_stormer_cutoff_rigidity(0.0, 14.0) == 0.0
    assert calculate_larmor_gyroradius(-50.0, 5.0) == float("inf")


def test_magnetic_dipole_field_attenuation():
    # Dipole field at distance r = 25.0 m for M = 4.5e10 A*m^2 with 1.0e-3 bucking cancellation
    # B_net = 1e-7 * 4.5e10 / (25^3) * 1e-3 = 4500 / 15625 * 1e-3 = 0.288 * 1e-3 T = 0.288 mT
    b_field = calculate_habitat_fringe_field(4.5e10, 25.0, bucking_attenuation_ratio=1.0e-3)
    assert 2.5e-4 <= b_field <= 3.2e-4
    assert b_field <= MAX_HABITAT_LEAKAGE_FIELD_T


def test_validate_magnetospheric_shield_parameters_nominal_and_breaches():
    res_nominal = validate_magnetospheric_shield_parameters(
        magnetic_moment_ga_m2=45.0,
        stormer_rigidity_gv=6.8,
        coil_peak_field_t=5.5,
        habitat_leakage_field_mt=0.35,
        hts_current_density_a_mm2=650.0,
        coil_operating_temp_k=20.0,
        quench_dump_time_ms=65.0,
        crew_annual_dose_msv=45.0,
        spe_dose_rate_mgy_h=12.0,
        electrostatic_potential_mv=2.5,
        neutralizer_current_ma=75.0
    )
    assert res_nominal.is_valid is True
    assert len(res_nominal.flaws) == 0

    # Breach case: weak moment (5 GA*m^2), low rigidity (2 GV), weak field (1.5 T), high leakage (2.5 mT), high dose (350 mSv)
    res_breach = validate_magnetospheric_shield_parameters(
        magnetic_moment_ga_m2=5.0,
        stormer_rigidity_gv=2.0,
        coil_peak_field_t=1.5,
        habitat_leakage_field_mt=2.5,
        hts_current_density_a_mm2=250.0,
        coil_operating_temp_k=45.0,
        quench_dump_time_ms=250.0,
        crew_annual_dose_msv=350.0,
        spe_dose_rate_mgy_h=65.0,
        electrostatic_potential_mv=0.5,
        neutralizer_current_ma=15.0
    )
    assert res_breach.is_valid is False
    assert len(res_breach.flaws) == 11


def test_magnetospheric_inspector_patterns_and_ast():
    inspector = MagnetosphericShieldInspector()

    flawed_code = (
        "# TODO: finish shield coil integration\n"
        "magnetic_moment_ga_m2 = 4.5\n"
        "stormer_rigidity_gv = 2.5\n"
        "coil_peak_field_t = 2.0\n"
        "habitat_leakage_field_mt = 1.8\n"
        "hts_current_density_a_mm2 = 300.0\n"
        "coil_operating_temp_k = 38.0\n"
        "quench_dump_time_ms = 180.0\n"
        "crew_annual_dose_msv = 240.0\n"
        "spe_dose_rate_mgy_h = 45.0\n"
        "electrostatic_potential_mv = 0.8\n"
        "neutralizer_current_ma = 20.0\n"
        "def quench_circuit() -> bool:\n"
        "    pass\n"
        "try:\n"
        "    current = 500\n"
        "except Exception:\n"
        "    pass\n"
    )

    flaws = inspector.inspect_source(flawed_code)
    flaw_ids = [f["id"] for f in flaws]

    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "MAGNETIC_MOMENT_DEFICIT" in flaw_ids
    assert "STORMER_RIGIDITY_DEFICIT" in flaw_ids
    assert "COIL_FIELD_DEFICIT" in flaw_ids
    assert "HABITAT_LEAKAGE_EXCESS" in flaw_ids
    assert "HTS_CURRENT_DENSITY_DEFICIT" in flaw_ids
    assert "COIL_TEMP_EXCESS" in flaw_ids
    assert "QUENCH_DUMP_DELAY" in flaw_ids
    assert "CREW_ANNUAL_DOSE_EXCESS" in flaw_ids
    assert "SPE_DOSE_RATE_EXCESS" in flaw_ids
    assert "ELECTROSTATIC_POTENTIAL_DEFICIT" in flaw_ids
    assert "NEUTRALIZER_CURRENT_DEFICIT" in flaw_ids
    assert "EMPTY_FUNCTION_BODY" in flaw_ids
    assert "EMPTY_EXCEPT_BLOCK" in flaw_ids

    text_flaws = inspector.inspect_code(flawed_code)
    assert len(text_flaws) == len(flaws)


def test_magnetospheric_rubric_scoring_and_passing():
    rubric = MagnetosphericShieldRubric()

    # Zero flaws
    eval_pass = rubric.evaluate([])
    assert eval_pass.score == 100
    assert eval_pass.passed is True

    # One CRITICAL flaw (-25 pts) -> score 75, rejected
    flaw_crit = [{"id": "STORMER_RIGIDITY_DEFICIT", "severity": "CRITICAL", "description": "Breach"}]
    eval_crit = rubric.evaluate(flaw_crit)
    assert eval_crit.score == 75
    assert eval_crit.passed is False

    # One LOW flaw (-3 pts) -> score 97, passes (>= 95)
    flaw_low = [{"id": "TELEMETRY_LOG", "severity": "LOW", "description": "Minor notice"}]
    eval_low = rubric.evaluate(flaw_low)
    assert eval_low.score == 97
    assert eval_low.passed is True


def test_blind_critic_adversarial_rejection():
    critic = MagnetosphericShieldBlindCritic()

    clean_code = (
        "magnetic_moment_ga_m2 = 45.0\n"
        "stormer_rigidity_gv = 6.8\n"
        "coil_peak_field_t = 5.5\n"
        "habitat_leakage_field_mt = 0.35\n"
        "hts_current_density_a_mm2 = 650.0\n"
        "coil_operating_temp_k = 20.0\n"
        "quench_dump_time_ms = 65.0\n"
        "crew_annual_dose_msv = 45.0\n"
        "spe_dose_rate_mgy_h = 12.0\n"
        "electrostatic_potential_mv = 2.5\n"
        "neutralizer_current_ma = 75.0\n"
        "def shield_status() -> bool:\n"
        "    return True\n"
    )

    clean_res = critic.audit(clean_code)
    assert clean_res["verdict"] == "APPROVED"
    assert clean_res["score"] == 100
    assert clean_res["passed"] is True

    flawed_code = (
        "magnetic_moment_ga_m2 = 4.0\n"
        "stormer_rigidity_gv = 2.0\n"
    )
    flawed_res = critic.audit(flawed_code)
    assert flawed_res["verdict"] == "REJECTED"
    assert flawed_res["passed"] is False
    assert flawed_res["score"] < 95


def test_elevation_engine_and_master_closed_loop():
    engine = MagnetosphericShieldElevationEngine()

    flawed_code = (
        "# TODO: optimize field geometry\n"
        "magnetic_moment_ga_m2 = 4.0\n"
        "stormer_rigidity_gv = 2.5\n"
        "coil_peak_field_t = 2.0\n"
        "habitat_leakage_field_mt = 1.2\n"
        "hts_current_density_a_mm2 = 320.0\n"
        "coil_operating_temp_k = 40.0\n"
        "quench_dump_time_ms = 160.0\n"
        "crew_annual_dose_msv = 220.0\n"
        "spe_dose_rate_mgy_h = 40.0\n"
        "electrostatic_potential_mv = 0.9\n"
        "neutralizer_current_ma = 25.0\n"
        "def telemetry() -> dict:\n"
        "    pass\n"
        "try:\n"
        "    val = 1\n"
        "except ValueError:\n"
        "    pass\n"
    )

    elevated, actions = engine.elevate(flawed_code)
    assert len(actions) > 0

    critic = MagnetosphericShieldBlindCritic()
    audit_after = critic.audit(elevated)
    assert audit_after["passed"] is True
    assert audit_after["score"] >= 95

    # Test master closed-loop execution
    master = MagnetosphericShieldMaster()
    res = master.evaluate_and_elevate(flawed_code, target_file="hts_radiation_shield.py")
    assert res["status"] == "certified"
    assert res["final_score"] >= 95
    assert res["iterations"] >= 1
    assert len(res["repaired_flaws"]) > 0
