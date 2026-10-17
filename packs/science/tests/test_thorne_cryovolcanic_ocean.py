"""Test suite for Commander Thorne Sterling - Cryovolcanic & Hydrothermal Ocean Explorer Architect.

Covers thermal ice melting dynamics, alien hydrostatic pressure, fiber tether link margins, AST inspection, rubric, critic, elevation, and master reflection.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.cryovolcanic_hydrothermal_ocean_explorer_architect import (
    MIN_THERMAL_DRILL_POWER_KW,
    MIN_PENETRATION_VELOCITY_M_H,
    MIN_OCEAN_PRESSURE_RATING_MPA,
    calculate_ice_melting_velocity,
    calculate_hydrostatic_pressure,
    calculate_tether_link_margin,
    validate_cryovolcanic_ocean_parameters,
    CryovolcanicOceanInspector,
    CryovolcanicOceanRubric,
    CryovolcanicOceanBlindCritic,
    CryovolcanicOceanElevationEngine,
    CryovolcanicOceanMaster,
)


def test_ice_melting_velocity_and_hydrostatic_pressure_models():
    # Probe cross-section A = 0.07 m^2 (diameter ~30 cm), thermal power = 30 kW
    # Energy to melt 1 kg of ice from 110 K (-163 C) to 273.15 K:
    # delta_T = 163.15 K -> c_p * delta_T = 2050 * 163.15 = 334457.5 J/kg
    # Total energy = 334457.5 + 334000 = 668457.5 J/kg
    # Energy per m^3 = 920 * 668457.5 = 6.1498e8 J/m^3
    # v_melt = 30000 / (0.07 * 6.1498e8) = 30000 / 43048670 ~= 6.968e-4 m/s = 2.508 m/h
    v_melt = calculate_ice_melting_velocity(30.0, 0.07, ambient_ice_temp_k=110.0)
    assert 2.30 <= v_melt <= 2.70
    assert v_melt >= MIN_PENETRATION_VELOCITY_M_H

    # Zero power / zero area
    assert calculate_ice_melting_velocity(0.0, 0.07) == 0.0
    assert calculate_ice_melting_velocity(30.0, 0.0) == 0.0

    # Hydrostatic pressure on Europa: 30 km ice shell + 100 km deep ocean, g = 1.315 m/s^2
    # P_ice = 920 * 1.315 * 30000 = 36.294 MPa
    # P_ocean = 1050 * 1.315 * 100000 = 138.075 MPa
    # Total P = 174.37 MPa
    p_hydro = calculate_hydrostatic_pressure(30.0, 100.0, surface_gravity=1.315)
    assert 170.0 <= p_hydro <= 180.0


def test_tether_link_margin_and_attenuation():
    # 40 km tether at 0.28 dB/km: fiber loss = 11.2 dB + 2.0 dB connectors = 13.2 dB
    # Power budget: Tx = 10 dBm, Rx sens = -35 dBm -> Budget = 45 dB
    # Margin = 45 - 13.2 = 31.8 dB
    margin = calculate_tether_link_margin(40.0, fiber_attenuation_db_km=0.28, laser_tx_power_dbm=10.0, rx_sensitivity_dbm=-35.0)
    assert 30.0 <= margin <= 33.0

    # Zero length edge case
    assert calculate_tether_link_margin(0.0) == 0.0


def test_validate_cryovolcanic_ocean_parameters_nominal_and_breaches():
    res_nominal = validate_cryovolcanic_ocean_parameters(
        thermal_drill_power_kw=32.0,
        penetration_velocity_m_h=1.85,
        ocean_pressure_rating_mpa=240.0,
        collapse_safety_factor=1.65,
        bioburden_spores_m2=0.015,
        dhmr_temperature_c=135.0,
        dhmr_duration_hours=48.0,
        lod_methane_nm=0.65,
        lod_hydrogen_nm=5.5,
        lod_amino_acids_nm=0.065,
        tether_tensile_strength_kn=3.2,
        fiber_attenuation_db_km=0.28,
        tether_length_km=40.0,
        sonar_range_km=6.5
    )
    assert res_nominal.is_valid is True
    assert len(res_nominal.flaws) == 0

    # Breach case: weak power (12 kW), slow velocity (0.6 m/h), low pressure rating (120 MPa), low SF (1.1),
    # bioburden breach (0.50 spores/m^2), low DHMR temp (100 C), short duration (15 h), insensitive sensors,
    # weak tether (1.2 kN), lossy fiber (0.6 dB/km), short tether (18 km), short sonar (2.0 km)
    res_breach = validate_cryovolcanic_ocean_parameters(
        thermal_drill_power_kw=12.0,
        penetration_velocity_m_h=0.6,
        ocean_pressure_rating_mpa=120.0,
        collapse_safety_factor=1.1,
        bioburden_spores_m2=0.50,
        dhmr_temperature_c=100.0,
        dhmr_duration_hours=15.0,
        lod_methane_nm=3.5,
        lod_hydrogen_nm=25.0,
        lod_amino_acids_nm=0.45,
        tether_tensile_strength_kn=1.2,
        fiber_attenuation_db_km=0.60,
        tether_length_km=18.0,
        sonar_range_km=2.0
    )
    assert res_breach.is_valid is False
    assert len(res_breach.flaws) == 14


def test_cryovolcanic_inspector_patterns_and_ast():
    inspector = CryovolcanicOceanInspector()

    flawed_code = (
        "# TODO: calibrate cryobot thermal drill nosecone\n"
        "thermal_drill_power_kw = 14.0\n"
        "penetration_velocity_m_h = 0.85\n"
        "ocean_pressure_rating_mpa = 150.0\n"
        "collapse_safety_factor = 1.25\n"
        "bioburden_spores_m2 = 0.12\n"
        "dhmr_temperature_c = 110.0\n"
        "dhmr_duration_hours = 24.0\n"
        "lod_methane_nm = 2.4\n"
        "lod_hydrogen_nm = 18.0\n"
        "lod_amino_acids_nm = 0.35\n"
        "tether_tensile_strength_kn = 1.8\n"
        "fiber_attenuation_db_km = 0.55\n"
        "tether_length_km = 22.0\n"
        "sonar_range_km = 3.2\n"
        "def melt_transit() -> bool:\n"
        "    pass\n"
        "try:\n"
        "    depth = 500\n"
        "except Exception:\n"
        "    pass\n"
    )

    flaws = inspector.inspect_source(flawed_code)
    flaw_ids = [f["id"] for f in flaws]

    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "THERMAL_DRILL_POWER_DEFICIT" in flaw_ids
    assert "PENETRATION_VELOCITY_DEFICIT" in flaw_ids
    assert "HYDROSTATIC_PRESSURE_DEFICIT" in flaw_ids
    assert "COLLAPSE_SAFETY_FACTOR_DEFICIT" in flaw_ids
    assert "BIOBURDEN_CONTAMINATION_BREACH" in flaw_ids
    assert "DHMR_TEMPERATURE_DEFICIT" in flaw_ids
    assert "DHMR_DURATION_DEFICIT" in flaw_ids
    assert "METHANE_LOD_EXCESS" in flaw_ids
    assert "HYDROGEN_LOD_EXCESS" in flaw_ids
    assert "AMINO_ACIDS_LOD_EXCESS" in flaw_ids
    assert "TETHER_TENSILE_DEFICIT" in flaw_ids
    assert "FIBER_ATTENUATION_EXCESS" in flaw_ids
    assert "TETHER_LENGTH_DEFICIT" in flaw_ids
    assert "SONAR_RANGE_DEFICIT" in flaw_ids
    assert "EMPTY_FUNCTION_BODY" in flaw_ids
    assert "EMPTY_EXCEPT_BLOCK" in flaw_ids

    text_flaws = inspector.inspect_code(flawed_code)
    assert len(text_flaws) == len(flaws)


def test_cryovolcanic_rubric_scoring_and_passing():
    rubric = CryovolcanicOceanRubric()

    # Zero flaws -> 100
    eval_pass = rubric.evaluate([])
    assert eval_pass.score == 100
    assert eval_pass.passed is True

    # One CRITICAL flaw (-25 pts) -> score 75, rejected
    flaw_crit = [{"id": "BIOBURDEN_CONTAMINATION_BREACH", "severity": "CRITICAL", "description": "COSPAR breach"}]
    eval_crit = rubric.evaluate(flaw_crit)
    assert eval_crit.score == 75
    assert eval_crit.passed is False

    # One LOW flaw (-3 pts) -> score 97, passes (>= 95)
    flaw_low = [{"id": "TELEMETRY_PING", "severity": "LOW", "description": "Diagnostic ping"}]
    eval_low = rubric.evaluate(flaw_low)
    assert eval_low.score == 97
    assert eval_low.passed is True


def test_blind_critic_adversarial_rejection():
    critic = CryovolcanicOceanBlindCritic()

    clean_code = (
        "thermal_drill_power_kw = 32.0\n"
        "penetration_velocity_m_h = 1.85\n"
        "ocean_pressure_rating_mpa = 240.0\n"
        "collapse_safety_factor = 1.65\n"
        "bioburden_spores_m2 = 0.015\n"
        "dhmr_temperature_c = 135.0\n"
        "dhmr_duration_hours = 48.0\n"
        "lod_methane_nm = 0.65\n"
        "lod_hydrogen_nm = 5.5\n"
        "lod_amino_acids_nm = 0.065\n"
        "tether_tensile_strength_kn = 3.2\n"
        "fiber_attenuation_db_km = 0.28\n"
        "tether_length_km = 40.0\n"
        "sonar_range_km = 6.5\n"
        "def cryobot_status() -> bool:\n"
        "    return True\n"
    )

    clean_res = critic.audit(clean_code)
    assert clean_res["verdict"] == "APPROVED"
    assert clean_res["score"] == 100
    assert clean_res["passed"] is True

    flawed_code = (
        "thermal_drill_power_kw = 10.0\n"
        "bioburden_spores_m2 = 0.80\n"
    )
    flawed_res = critic.audit(flawed_code)
    assert flawed_res["verdict"] == "REJECTED"
    assert flawed_res["passed"] is False
    assert flawed_res["score"] < 95


def test_elevation_engine_and_master_closed_loop():
    engine = CryovolcanicOceanElevationEngine()

    flawed_code = (
        "# TODO: assemble melt probe nosecone\n"
        "thermal_drill_power_kw = 15.0\n"
        "penetration_velocity_m_h = 0.90\n"
        "ocean_pressure_rating_mpa = 160.0\n"
        "collapse_safety_factor = 1.30\n"
        "bioburden_spores_m2 = 0.08\n"
        "dhmr_temperature_c = 115.0\n"
        "dhmr_duration_hours = 28.0\n"
        "lod_methane_nm = 2.2\n"
        "lod_hydrogen_nm = 16.0\n"
        "lod_amino_acids_nm = 0.25\n"
        "tether_tensile_strength_kn = 1.9\n"
        "fiber_attenuation_db_km = 0.48\n"
        "tether_length_km = 25.0\n"
        "sonar_range_km = 3.5\n"
        "def ocean_telemetry() -> dict:\n"
        "    pass\n"
        "try:\n"
        "    val = 1\n"
        "except ValueError:\n"
        "    pass\n"
    )

    elevated, actions = engine.elevate(flawed_code)
    assert len(actions) > 0

    critic = CryovolcanicOceanBlindCritic()
    audit_after = critic.audit(elevated)
    assert audit_after["passed"] is True
    assert audit_after["score"] >= 95

    # Test master closed-loop execution
    master = CryovolcanicOceanMaster()
    res = master.evaluate_and_elevate(flawed_code, target_file="cryobot_explorer.py")
    assert res["status"] == "certified"
    assert res["final_score"] >= 95
    assert res["iterations"] >= 1
    assert len(res["repaired_flaws"]) > 0
