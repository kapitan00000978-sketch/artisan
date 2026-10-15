"""Test suite for Dr. Zephyrus Vance - Interstellar Bussard Ramjet Architect.

Covers relativistic Lorentz dynamics, proton intake rates, relativistic ram-drag,
thermonuclear fusion thrust, static and AST inspection, rubric scoring, adversarial criticism,
elevation engine, and master dual-agent closed-loop reflection.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.interstellar_ramjet_bussard_propulsion_architect import (
    SPEED_OF_LIGHT,
    PROTON_MASS_KG,
    MIN_SCOOP_RADIUS_KM,
    MIN_RELATIVISTIC_VELOCITY_FRACTION,
    MIN_MAGNETIC_SCOOP_FIELD_T,
    MIN_PHOTO_IONIZATION_EFFICIENCY,
    MIN_CAPTURE_CROSS_SECTION_EFFICIENCY,
    MIN_THRUST_TO_DRAG_RATIO,
    MIN_EXHAUST_VELOCITY_M_S,
    MIN_NOZZLE_COLLIMATION_EFFICIENCY,
    MIN_SHIP_ACCELERATION_M_S2,
    MAX_SHIP_ACCELERATION_M_S2,
    MIN_CORE_FUSION_TEMP_K,
    MAX_BREMSSTRAHLUNG_LOSS_RATIO,
    calculate_lorentz_factor,
    calculate_proton_intake_rate,
    calculate_relativistic_ram_drag,
    calculate_fusion_thrust,
    validate_bussard_ramjet_parameters,
    BussardRamjetInspector,
    BussardRamjetRubric,
    BussardRamjetBlindCritic,
    BussardRamjetElevationEngine,
    BussardRamjetMaster,
)


def test_lorentz_factor_and_proton_intake_models():
    """Verify relativistic Lorentz factor and proton scoop intake rate calculations."""
    # Stationary case beta = 0.0 -> gamma = 1.0
    assert calculate_lorentz_factor(0.0) == 1.0

    # Relativistic beta = 0.60 -> gamma = 1 / sqrt(1 - 0.36) = 1 / 0.8 = 1.25
    gamma_60 = calculate_lorentz_factor(0.60)
    assert gamma_60 == pytest.approx(1.25, rel=1e-4)

    # Edge cases
    assert calculate_lorentz_factor(-0.1) == 1.0
    assert calculate_lorentz_factor(1.0) == 1.0

    # Proton intake: R = 1.2e6 m (1200 km), v = 0.20 c = 5.996e7 m/s, n = 1.0e6 /m^3, capture_eff = 0.89
    # Area = pi * (1.2e6)^2 ~= 4.524e12 m^2
    # mass density = 1.0e6 * 1.6726e-27 = 1.6726e-21 kg/m^3
    # mdot = 4.524e12 * 5.996e7 * 1.6726e-21 * 0.89 ~= 0.404 kg/s
    mdot = calculate_proton_intake_rate(1.2e6, 0.20 * SPEED_OF_LIGHT, ism_density_m3=1.0e6, capture_eff=0.89)
    assert 0.35 <= mdot <= 0.45

    # Zero radius edge case
    assert calculate_proton_intake_rate(0.0, 1.0e7) == 0.0


def test_ram_drag_and_fusion_thrust_ratios():
    """Verify relativistic ram-drag and thermonuclear fusion thrust physics."""
    # Ram-drag for R = 1.0e6 m (1000 km), v = 0.10 c = 2.998e7 m/s, n = 1.0e6
    r_drag = calculate_relativistic_ram_drag(1.0e6, 0.10 * SPEED_OF_LIGHT, ism_density_m3=1.0e6)
    assert r_drag > 0.0

    # Zero drag edge case
    assert calculate_relativistic_ram_drag(0.0, 1.0e7) == 0.0

    # Fusion thrust: mdot = 0.50 kg/s, v_e = 4.0e7 m/s, collimation = 0.90 -> Thrust = 0.5 * 4e7 * 0.9 = 1.8e7 N (18 MN)
    thrust = calculate_fusion_thrust(0.50, 4.0e7, collimation_eff=0.90)
    assert thrust == pytest.approx(1.8e7, rel=1e-3)

    # Zero flow edge case
    assert calculate_fusion_thrust(0.0, 4.0e7) == 0.0


def test_validate_bussard_ramjet_parameters_nominal_and_breaches():
    """Verify validation dataclass against nominal parameters and boundary breaches."""
    # Nominal case
    res_nominal = validate_bussard_ramjet_parameters(
        scoop_radius_km=1200.0,
        flight_velocity_beta=0.25,
        magnetic_scoop_field_t=18.5,
        photo_ionization_efficiency=0.992,
        capture_cross_section_efficiency=0.89,
        thrust_to_drag_ratio=1.45,
        exhaust_velocity_m_s=4.2e7,
        nozzle_collimation_efficiency=0.92,
        ship_acceleration_m_s2=4.5,
        core_fusion_temp_k=1.5e8,
        bremsstrahlung_loss_ratio=0.28
    )
    assert res_nominal.is_valid is True
    assert len(res_nominal.flaws) == 0

    # Breach case: small scoop (400 km), low beta (0.04), weak field (8 T), low ionization (0.90),
    # low capture (0.65), low thrust-to-drag (0.80), low exhaust velocity (1.5e7), poor nozzle (0.75),
    # low acceleration (0.05), cold core (4e7), high Bremsstrahlung loss (0.65)
    res_breach = validate_bussard_ramjet_parameters(
        scoop_radius_km=400.0,
        flight_velocity_beta=0.04,
        magnetic_scoop_field_t=8.0,
        photo_ionization_efficiency=0.90,
        capture_cross_section_efficiency=0.65,
        thrust_to_drag_ratio=0.80,
        exhaust_velocity_m_s=1.5e7,
        nozzle_collimation_efficiency=0.75,
        ship_acceleration_m_s2=0.05,
        core_fusion_temp_k=4.0e7,
        bremsstrahlung_loss_ratio=0.65
    )
    assert res_breach.is_valid is False
    assert len(res_breach.flaws) == 11


def test_bussard_ramjet_inspector_patterns_and_ast():
    """Verify static and AST inspection detects placeholders, deficits, and empty stubs."""
    inspector = BussardRamjetInspector()

    flawed_code = (
        "# TODO: calibrate Bussard magnetic scoop choke coil\n"
        "scoop_radius_km = 600.0\n"
        "flight_velocity_beta = 0.05\n"
        "magnetic_scoop_field_t = 10.0\n"
        "photo_ionization_efficiency = 0.92\n"
        "capture_cross_section_efficiency = 0.70\n"
        "thrust_to_drag_ratio = 0.85\n"
        "exhaust_velocity_m_s = 2.0e7\n"
        "nozzle_collimation_efficiency = 0.80\n"
        "ship_acceleration_m_s2 = 0.45\n"
        "core_fusion_temp_k = 6.0e7\n"
        "bremsstrahlung_loss_ratio = 0.55\n"
        "def engage_magnetic_scoop() -> bool:\n"
        "    pass\n"
        "try:\n"
        "    field = 10\n"
        "except Exception:\n"
        "    pass\n"
    )

    flaws = inspector.inspect_source(flawed_code)
    flaw_ids = [f["id"] for f in flaws]

    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "SCOOP_RADIUS_DEFICIT" in flaw_ids
    assert "VELOCITY_BETA_DEFICIT" in flaw_ids
    assert "SCOOP_FIELD_DEFICIT" in flaw_ids
    assert "PHOTO_IONIZATION_DEFICIT" in flaw_ids
    assert "CAPTURE_CROSS_SECTION_DEFICIT" in flaw_ids
    assert "THRUST_TO_DRAG_DEFICIT" in flaw_ids
    assert "EXHAUST_VELOCITY_DEFICIT" in flaw_ids
    assert "NOZZLE_COLLIMATION_DEFICIT" in flaw_ids
    assert "ACCELERATION_OUT_OF_BOUNDS" in flaw_ids
    assert "CORE_TEMP_DEFICIT" in flaw_ids
    assert "BREMSSTRAHLUNG_LOSS_EXCESS" in flaw_ids
    assert "EMPTY_FUNCTION_BODY" in flaw_ids
    assert "EMPTY_EXCEPT_BLOCK" in flaw_ids

    text_flaws = inspector.inspect_code(flawed_code)
    assert len(text_flaws) == len(flaws)


def test_bussard_ramjet_rubric_scoring_and_passing():
    """Verify objective rubric scoring logic and passing thresholds."""
    rubric = BussardRamjetRubric()

    # Zero flaws -> 100 passed
    eval_pass = rubric.evaluate([])
    assert eval_pass.score == 100
    assert eval_pass.passed is True

    # One CRITICAL flaw (-25 pts) -> 75 rejected
    flaw_crit = [{"id": "THRUST_TO_DRAG_DEFICIT", "severity": "CRITICAL", "description": "Drag parachute deceleration"}]
    eval_crit = rubric.evaluate(flaw_crit)
    assert eval_crit.score == 75
    assert eval_crit.passed is False

    # One LOW flaw (-3 pts) -> 97 passed
    flaw_low = [{"id": "TELEMETRY_SAMPLE", "severity": "LOW", "description": "Diagnostic sample"}]
    eval_low = rubric.evaluate(flaw_low)
    assert eval_low.score == 97
    assert eval_low.passed is True


def test_blind_critic_adversarial_rejection():
    """Verify blind critic accurately certifies clean ramjet code and rejects flawed submissions."""
    critic = BussardRamjetBlindCritic()

    clean_code = (
        "scoop_radius_km = 1200.0\n"
        "flight_velocity_beta = 0.25\n"
        "magnetic_scoop_field_t = 18.5\n"
        "photo_ionization_efficiency = 0.992\n"
        "capture_cross_section_efficiency = 0.89\n"
        "thrust_to_drag_ratio = 1.45\n"
        "exhaust_velocity_m_s = 4.2e7\n"
        "nozzle_collimation_efficiency = 0.92\n"
        "ship_acceleration_m_s2 = 4.5\n"
        "core_fusion_temp_k = 1.5e8\n"
        "bremsstrahlung_loss_ratio = 0.28\n"
        "def engage_magnetic_scoop() -> bool:\n"
        "    return True\n"
    )

    clean_res = critic.audit(clean_code)
    assert clean_res["verdict"] == "APPROVED"
    assert clean_res["score"] == 100
    assert clean_res["passed"] is True

    flawed_code = (
        "scoop_radius_km = 500.0\n"
        "thrust_to_drag_ratio = 0.85\n"
    )
    flawed_res = critic.audit(flawed_code)
    assert flawed_res["verdict"] == "REJECTED"
    assert flawed_res["passed"] is False
    assert flawed_res["score"] < 95


def test_elevation_engine_and_master_closed_loop():
    """Verify autonomous elevation restores code to >=95 standards and master coordinates reflection."""
    engine = BussardRamjetElevationEngine()

    flawed_code = (
        "# TODO: adjust relativistic magnetic intake funnel geometry\n"
        "scoop_radius_km = 700.0\n"
        "flight_velocity_beta = 0.06\n"
        "magnetic_scoop_field_t = 11.0\n"
        "photo_ionization_efficiency = 0.93\n"
        "capture_cross_section_efficiency = 0.72\n"
        "thrust_to_drag_ratio = 0.90\n"
        "exhaust_velocity_m_s = 2.2e7\n"
        "nozzle_collimation_efficiency = 0.82\n"
        "ship_acceleration_m_s2 = 0.50\n"
        "core_fusion_temp_k = 7.0e7\n"
        "bremsstrahlung_loss_ratio = 0.50\n"
        "def monitor_scoop_intake() -> dict:\n"
        "    pass\n"
        "try:\n"
        "    flux = 100\n"
        "except ValueError:\n"
        "    pass\n"
    )

    elevated, actions = engine.elevate(flawed_code)
    assert len(actions) > 0

    critic = BussardRamjetBlindCritic()
    audit_after = critic.audit(elevated)
    assert audit_after["passed"] is True
    assert audit_after["score"] >= 95

    # Test master closed-loop execution
    master = BussardRamjetMaster()
    res = master.evaluate_and_elevate(flawed_code, target_file="bussard_ramjet.py")
    assert res["status"] == "certified"
    assert res["final_score"] >= 95
    assert res["iterations"] >= 1
    assert len(res["repaired_flaws"]) > 0
