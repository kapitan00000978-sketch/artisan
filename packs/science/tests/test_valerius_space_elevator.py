"""Test suite for Dr. Valerius Sterling - Space Elevator & Active Tensegrity Megastructure Architect.

Covers orbital mechanics, taper ratio equations, Coriolis deflection, AST inspection, rubric, critic, elevation, and master reflection.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.space_elevator_tensegrity_architect import (
    GEOSTATIONARY_RADIUS_M,
    GEOSTATIONARY_ALTITUDE_M,
    MIN_TENSILE_STRENGTH_PA,
    MIN_SPECIFIC_STRENGTH_N_M_KG,
    MAX_TAPER_RATIO,
    calculate_specific_strength,
    calculate_tether_taper_ratio,
    calculate_coriolis_deflection,
    calculate_transverse_wave_speed,
    validate_space_elevator_parameters,
    SpaceElevatorInspector,
    SpaceElevatorRubric,
    SpaceElevatorBlindCritic,
    SpaceElevatorElevationEngine,
    SpaceElevatorMaster,
)


def test_geostationary_orbit_and_taper_ratio():
    # Verify GEO orbital radius: ~42,164 km and altitude ~35,786 km
    assert 4.21e7 <= GEOSTATIONARY_RADIUS_M <= 4.22e7
    assert 3.57e7 <= GEOSTATIONARY_ALTITUDE_M <= 3.59e7

    # Specific strength: sigma_t = 85.0 GPa, rho = 1250.0 kg/m^3
    spec_strength = calculate_specific_strength(85.0e9, 1250.0)
    # Expected: 85.0e9 / 1250.0 = 6.8e7 N*m/kg (68.0 MYuri)
    assert spec_strength == pytest.approx(6.8e7)
    assert spec_strength >= MIN_SPECIFIC_STRENGTH_N_M_KG

    # Taper ratio with sigma_t = 85 GPa, rho = 1250 kg/m^3
    taper = calculate_tether_taper_ratio(85.0e9, 1250.0)
    # Exponent = (1250 / 85e9) * 4.8423e7 = 0.7121 -> exp(0.7121) ~= 2.038
    assert 1.80 <= taper <= 2.30
    assert taper <= MAX_TAPER_RATIO

    # Zero/negative guards
    assert calculate_specific_strength(0.0, 1250.0) == 0.0
    assert calculate_tether_taper_ratio(-10.0, 1250.0) == float("inf")


def test_coriolis_deflection_and_transverse_wave_speed():
    # Climber: 15,000 kg, v = 50.0 m/s (180 km/h)
    f_c, theta_c = calculate_coriolis_deflection(15000.0, 50.0, effective_gravity_m_s2=9.81)
    # F_c = 2 * 15000 * 7.2921e-5 * 50 = 109.38 N
    assert 105.0 <= f_c <= 115.0
    # theta = 2 * 7.2921e-5 * 50 / 9.81 = 7.433e-4 rad (~0.0426 deg)
    assert 0.0005 <= theta_c <= 0.0010
    assert theta_c <= 0.05  # Within 0.05 rad safety envelope

    # Transverse acoustic wave speed: Tension = 1.0e7 N, linear density = 0.1 kg/m
    # c = sqrt(1.0e7 / 0.1) = sqrt(1.0e8) = 10,000 m/s
    c_wave = calculate_transverse_wave_speed(1.0e7, 0.1)
    assert c_wave == pytest.approx(10000.0)
    assert c_wave >= 7000.0


def test_validate_space_elevator_parameters_nominal_and_breaches():
    res_nominal = validate_space_elevator_parameters(
        tensile_strength_gpa=85.0,
        tether_density_kg_m3=1250.0,
        tether_length_km=105000.0,
        anchor_pretension_mn=14.5,
        climber_mass_kg=15000.0,
        climber_velocity_km_h=180.0,
        active_damping_ratio=0.08,
        quality_factor=12.5,
        wave_velocity_m_s=9200.0
    )
    assert res_nominal.is_valid is True
    assert len(res_nominal.flaws) == 0

    # Breach case: weak material (35 GPa), dense (2200 kg/m^3), short (60000 km), low pretension (4 MN)
    res_breach = validate_space_elevator_parameters(
        tensile_strength_gpa=35.0,
        tether_density_kg_m3=2200.0,
        tether_length_km=60000.0,
        anchor_pretension_mn=4.0,
        climber_mass_kg=35000.0,
        climber_velocity_km_h=350.0,
        active_damping_ratio=0.01,
        quality_factor=45.0,
        wave_velocity_m_s=4500.0
    )
    assert res_breach.is_valid is False
    assert len(res_breach.flaws) >= 8


def test_space_elevator_inspector_patterns_and_ast():
    inspector = SpaceElevatorInspector()

    flawed_code = (
        "# TODO: optimize tensegrity anchor\n"
        "tensile_strength_gpa = 42.0\n"
        "tether_density_kg_m3 = 1650.0\n"
        "tether_length_km = 80000.0\n"
        "anchor_pretension_mn = 5.0\n"
        "climber_mass_kg = 28000.0\n"
        "climber_velocity_km_h = 260.0\n"
        "active_damping_ratio = 0.02\n"
        "quality_factor = 35.0\n"
        "wave_velocity_m_s = 5500.0\n"
        "def tension_control() -> bool:\n"
        "    pass\n"
        "try:\n"
        "    tension = 100\n"
        "except Exception:\n"
        "    pass\n"
    )

    flaws = inspector.inspect_source(flawed_code)
    flaw_ids = [f["id"] for f in flaws]

    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "TENSILE_STRENGTH_DEFICIT" in flaw_ids
    assert "TETHER_DENSITY_EXCESS" in flaw_ids
    assert "TETHER_LENGTH_DEFICIT" in flaw_ids
    assert "ANCHOR_PRETENSION_DEFICIT" in flaw_ids
    assert "CLIMBER_MASS_OVERLOAD" in flaw_ids
    assert "CLIMBER_VELOCITY_EXCESS" in flaw_ids
    assert "DAMPING_RATIO_DEFICIT" in flaw_ids
    assert "QUALITY_FACTOR_RESONANCE" in flaw_ids
    assert "WAVE_VELOCITY_DEFICIT" in flaw_ids
    assert "EMPTY_FUNCTION_BODY" in flaw_ids
    assert "EMPTY_EXCEPT_BLOCK" in flaw_ids

    text_flaws = inspector.inspect_code(flawed_code)
    assert len(text_flaws) == len(flaws)


def test_space_elevator_rubric_scoring_and_passing():
    rubric = SpaceElevatorRubric()

    # Zero flaws
    eval_pass = rubric.evaluate([])
    assert eval_pass.score == 100
    assert eval_pass.passed is True

    # One CRITICAL flaw (-25 pts) -> score 75, rejected
    flaw_crit = [{"id": "TENSILE_STRENGTH_DEFICIT", "severity": "CRITICAL", "description": "Breach"}]
    eval_crit = rubric.evaluate(flaw_crit)
    assert eval_crit.score == 75
    assert eval_crit.passed is False

    # One LOW flaw (-3 pts) -> score 97, passes (>= 95)
    flaw_low = [{"id": "TELEMETRY_LAG", "severity": "LOW", "description": "Minor lag"}]
    eval_low = rubric.evaluate(flaw_low)
    assert eval_low.score == 97
    assert eval_low.passed is True


def test_blind_critic_adversarial_rejection():
    critic = SpaceElevatorBlindCritic()

    clean_code = (
        "tensile_strength_gpa = 85.0\n"
        "tether_density_kg_m3 = 1250.0\n"
        "tether_length_km = 105000.0\n"
        "anchor_pretension_mn = 14.5\n"
        "climber_mass_kg = 15000.0\n"
        "climber_velocity_km_h = 180.0\n"
        "active_damping_ratio = 0.08\n"
        "quality_factor = 12.5\n"
        "wave_velocity_m_s = 9200.0\n"
        "def anchor_status() -> bool:\n"
        "    return True\n"
    )

    clean_res = critic.audit(clean_code)
    assert clean_res["verdict"] == "APPROVED"
    assert clean_res["score"] == 100
    assert clean_res["passed"] is True

    flawed_code = (
        "tensile_strength_gpa = 40.0\n"
        "anchor_pretension_mn = 4.0\n"
    )
    flawed_res = critic.audit(flawed_code)
    assert flawed_res["verdict"] == "REJECTED"
    assert flawed_res["passed"] is False
    assert flawed_res["score"] < 95


def test_elevation_engine_and_master_closed_loop():
    engine = SpaceElevatorElevationEngine()

    flawed_code = (
        "# TODO: refine climber motor\n"
        "tensile_strength_gpa = 45.0\n"
        "tether_density_kg_m3 = 1550.0\n"
        "tether_length_km = 75000.0\n"
        "anchor_pretension_mn = 6.0\n"
        "climber_mass_kg = 25000.0\n"
        "climber_velocity_km_h = 240.0\n"
        "active_damping_ratio = 0.02\n"
        "quality_factor = 30.0\n"
        "wave_velocity_m_s = 5500.0\n"
        "def telemetry() -> dict:\n"
        "    pass\n"
        "try:\n"
        "    c = 10\n"
        "except ValueError:\n"
        "    pass\n"
    )

    elevated, actions = engine.elevate(flawed_code)
    assert len(actions) > 0

    critic = SpaceElevatorBlindCritic()
    audit_after = critic.audit(elevated)
    assert audit_after["passed"] is True
    assert audit_after["score"] >= 95

    # Test master closed-loop execution
    master = SpaceElevatorMaster()
    res = master.evaluate_and_elevate(flawed_code, target_file="tensegrity_megastructure.py")
    assert res["status"] == "certified"
    assert res["final_score"] >= 95
    assert res["iterations"] >= 1
    assert len(res["repaired_flaws"]) > 0
