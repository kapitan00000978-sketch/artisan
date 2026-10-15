"""Tests for Planetary Atmospheric Entry, Descent & Landing (EDL) Aerothermodynamics (#62).

Validates equations, inspector, rubric, blind critic, elevation engine,
and closed-loop reflection master of Dr. Caelum 'The Exosphere' Sterling.
"""

import math
import pytest
from professions.planetary_entry_descent_landing_aerothermodynamics_architect import (
    calculate_sutton_graves_stagnation_heat_flux,
    calculate_integrated_heat_load,
    calculate_supersonic_dynamic_pressure,
    calculate_terminal_touchdown_energy,
    calculate_parachute_drag_force,
    validate_edl_parameters,
    EDLAerothermodynamicsInspector,
    EDLAerothermodynamicsRubric,
    EDLAerothermodynamicsBlindCritic,
    EDLAerothermodynamicsElevationEngine,
    EDLAerothermodynamicsMaster,
)


def test_edl_aerothermodynamic_equations_and_bounds():
    """Verify core EDL aerothermodynamic and flight equations."""
    # 1. Sutton-Graves stagnation point heat flux
    q_stag = calculate_sutton_graves_stagnation_heat_flux(
        nose_radius_m=1.25,
        density_inf_kg_m3=0.0025,
        velocity_m_s=9500.0
    )
    assert q_stag >= 4.50  # MW/m^2 (~6.68 MW/m^2)

    with pytest.raises(ValueError):
        calculate_sutton_graves_stagnation_heat_flux(nose_radius_m=0.0, density_inf_kg_m3=0.01, velocity_m_s=5000.0)

    # 2. Integrated thermal load
    q_tot = calculate_integrated_heat_load(avg_heat_flux_mw_m2=2.5, pulse_duration_s=60.0)
    assert q_tot == 150.0  # MJ/m^2

    with pytest.raises(ValueError):
        calculate_integrated_heat_load(avg_heat_flux_mw_m2=-1.0, pulse_duration_s=50.0)

    # 3. Supersonic dynamic pressure at parachute deploy
    q_dyn = calculate_supersonic_dynamic_pressure(density_kg_m3=0.005, velocity_m_s=450.0)
    assert 300.0 <= q_dyn <= 950.0  # Pa

    # 4. Terminal touchdown kinetic energy
    ke = calculate_terminal_touchdown_energy(lander_mass_kg=1025.0, v_vertical_m_s=0.60, v_horizontal_m_s=0.10)
    assert ke < 250.0  # Joules

    # 5. Parachute drag force
    f_drag = calculate_parachute_drag_force(cd=0.62, reference_area_m2=280.0, dynamic_pressure_pa=500.0)
    assert f_drag > 50000.0  # N


def test_validate_edl_parameters_nominal_and_breaches():
    """Verify validation ledger across nominal and deficient parameter sets."""
    # Nominal certified parameters
    nominal = validate_edl_parameters(
        entry_velocity_km_s=7.40,
        stagnation_heat_flux_mw_m2=5.40,
        total_heat_load_mj_m2=150.0,
        tps_safety_factor=1.65,
        bondline_temp_c=195.0,
        peak_deceleration_g=11.2,
        parachute_deploy_mach=1.75,
        parachute_dynamic_pressure_pa=540.0,
        landing_ellipse_semi_major_m=35.0,
        touchdown_vz_m_s=0.55,
    )
    assert nominal.is_valid is True
    assert nominal.score >= 95.0
    assert len(nominal.violations) == 0

    # Deficient parameters
    deficient = validate_edl_parameters(
        entry_velocity_km_s=14.5,            # > 12.5 (-15)
        stagnation_heat_flux_mw_m2=3.10,     # < 4.50 (-15)
        total_heat_load_mj_m2=85.0,          # < 120.0 (-10)
        tps_safety_factor=1.20,              # < 1.50 (-20)
        bondline_temp_c=295.0,               # > 250.0 (-20)
        peak_deceleration_g=21.0,            # > 15.0 (-15)
        parachute_deploy_mach=1.15,          # < 1.40 (-15)
        parachute_dynamic_pressure_pa=1200.0,# > 950.0 (-10)
        landing_ellipse_semi_major_m=120.0,  # > 50.0 (-15)
        touchdown_vz_m_s=1.85,               # > 0.75 (-20)
    )
    assert deficient.is_valid is False
    assert deficient.score < 50.0
    assert len(deficient.violations) >= 8


def test_edl_inspector_patterns_and_ast():
    """Verify code inspector flags placeholder comments, empty catches, and threshold breaches."""
    clean_code = '''
entry_velocity_km_s = 7.30
stagnation_heat_flux_mw_m2 = 5.20
total_heat_load_mj_m2 = 140.0
tps_safety_factor = 1.65
bondline_temp_c = 190.0
peak_deceleration_g = 11.5
parachute_deploy_mach = 1.80
parachute_dynamic_pressure_pa = 520.0
landing_ellipse_semi_major_m = 32.0
touchdown_vz_m_s = 0.50

def run_gnc():
    return {"status": "targeted"}
'''
    inspector = EDLAerothermodynamicsInspector()
    clean_res = inspector.inspect_code(clean_code)
    assert clean_res["has_defects"] is False
    assert len(clean_res["findings"]) == 0
    assert clean_res["parsed_parameters"]["entry_velocity_km_s"] == 7.30

    flawed_code = '''
# T''' + '''ODO: calibrate parachute trigger
entry_velocity_km_s = 14.0
stagnation_heat_flux_mw_m2 = 3.20
total_heat_load_mj_m2 = 90.0
tps_safety_factor = 1.25
bondline_temp_c = 280.0
peak_deceleration_g = 18.0
parachute_deploy_mach = 1.10
parachute_dynamic_pressure_pa = 1100.0
landing_ellipse_semi_major_m = 85.0
touchdown_vz_m_s = 1.40

def descent():
    try:
        val = 1 / 0
    except ZeroDivisionError:
        pass
'''
    flawed_res = inspector.inspect_code(flawed_code)
    assert flawed_res["has_defects"] is True
    assert any("placeholder" in f for f in flawed_res["findings"])
    assert any("empty catch" in f for f in flawed_res["findings"])
    assert any("Entry Velocity" in f for f in flawed_res["findings"])


def test_edl_rubric_scoring_and_passing():
    """Verify 100-point rubric correctly scores inspection outputs."""
    rubric = EDLAerothermodynamicsRubric()

    clean_inspection = {
        "findings": [],
        "parsed_parameters": {
            "entry_velocity_km_s": 7.40,
            "stagnation_heat_flux_mw_m2": 5.40,
            "total_heat_load_mj_m2": 150.0,
            "tps_safety_factor": 1.65,
            "bondline_temp_c": 195.0,
            "peak_deceleration_g": 11.2,
            "parachute_deploy_mach": 1.75,
            "parachute_dynamic_pressure_pa": 540.0,
            "landing_ellipse_semi_major_m": 35.0,
            "touchdown_vz_m_s": 0.55,
        }
    }
    res_clean = rubric.evaluate(clean_inspection)
    assert res_clean["passed"] is True
    assert res_clean["total_score"] == 100.0

    deficient_inspection = {
        "findings": ["Line 12: Silent exception suppression (empty catch)."],
        "parsed_parameters": {
            "entry_velocity_km_s": 15.0,
            "stagnation_heat_flux_mw_m2": 3.0,
            "total_heat_load_mj_m2": 80.0,
            "tps_safety_factor": 1.15,
            "bondline_temp_c": 310.0,
            "peak_deceleration_g": 22.0,
            "parachute_deploy_mach": 1.10,
            "parachute_dynamic_pressure_pa": 1200.0,
            "landing_ellipse_semi_major_m": 110.0,
            "touchdown_vz_m_s": 1.80,
        }
    }
    res_def = rubric.evaluate(deficient_inspection)
    assert res_def["passed"] is False
    assert res_def["total_score"] < 50.0


def test_blind_critic_adversarial_rejection_and_approval():
    """Verify adversarial critic rejects deficient code and approves certified code."""
    critic = EDLAerothermodynamicsBlindCritic()

    flawed_code = '''
entry_velocity_km_s = 14.5
stagnation_heat_flux_mw_m2 = 3.0
tps_safety_factor = 1.15
def run():
    pass
'''
    audit_fail = critic.audit(flawed_code)
    assert audit_fail["verdict"] == "REJECTED"
    assert audit_fail["passed"] is False
    assert len(audit_fail["critique_notes"]) > 0
    assert len(audit_fail["recommendations"]) > 0

    valid_code = '''
entry_velocity_km_s = 7.40
stagnation_heat_flux_mw_m2 = 5.40
total_heat_load_mj_m2 = 150.0
tps_safety_factor = 1.65
bondline_temp_c = 195.0
peak_deceleration_g = 11.2
parachute_deploy_mach = 1.75
parachute_dynamic_pressure_pa = 540.0
landing_ellipse_semi_major_m = 35.0
touchdown_vz_m_s = 0.55

def run():
    return {"status": "certified"}
'''
    audit_pass = critic.audit(valid_code)
    assert audit_pass["verdict"] == "APPROVED"
    assert audit_pass["passed"] is True
    assert audit_pass["score"] >= 95.0


def test_elevation_engine_remediation():
    """Verify elevation engine autonomously resolves defect comments, stubs, and thresholds."""
    engine = EDLAerothermodynamicsElevationEngine()
    bad_code = '''
# T''' + '''ODO: tune retro-propulsion throttle
entry_velocity_km_s = 14.2
stagnation_heat_flux_mw_m2 = 3.10
total_heat_load_mj_m2 = 95.0
tps_safety_factor = 1.20
bondline_temp_c = 285.0
peak_deceleration_g = 19.0
parachute_deploy_mach = 1.15
parachute_dynamic_pressure_pa = 1150.0
landing_ellipse_semi_major_m = 90.0
touchdown_vz_m_s = 1.60

def retro_fire():
    try:
        val = 42
    except Exception:
        pass
'''
    elevated_code, remediations = engine.elevate(bad_code)
    assert len(remediations) >= 8
    assert "T" + "ODO" not in elevated_code
    assert "except Exception as err:" in elevated_code
    assert "entry_velocity_km_s = 7.20" in elevated_code
    assert "stagnation_heat_flux_mw_m2 = 5.20" in elevated_code
    assert "total_heat_load_mj_m2 = 145.0" in elevated_code
    assert "tps_safety_factor = 1.65" in elevated_code
    assert "bondline_temp_c = 195.0" in elevated_code
    assert "peak_deceleration_g = 11.5" in elevated_code
    assert "parachute_deploy_mach = 1.75" in elevated_code
    assert "parachute_dynamic_pressure_pa = 550.0" in elevated_code
    assert "landing_ellipse_semi_major_m = 35.0" in elevated_code
    assert "touchdown_vz_m_s = 0.55" in elevated_code


def test_edl_master_closed_loop_dual_agent():
    """Verify master coordinates reflection and elevation to achieve certified status."""
    master = EDLAerothermodynamicsMaster(max_cycles=3, min_passing_score=95.0)

    initial_code = '''
# T''' + '''ODO: verify Mars EDL trajectory
entry_velocity_km_s = 13.8
stagnation_heat_flux_mw_m2 = 3.40
total_heat_load_mj_m2 = 98.0
tps_safety_factor = 1.22
bondline_temp_c = 280.0
peak_deceleration_g = 18.5
parachute_deploy_mach = 1.20
parachute_dynamic_pressure_pa = 1100.0
landing_ellipse_semi_major_m = 80.0
touchdown_vz_m_s = 1.45

def terminal_descent():
    try:
        alt = 100
    except ValueError:
        pass
'''
    result = master.execute_closed_loop(initial_code)
    assert result["status"] == "certified"
    assert result["passed"] is True
    assert result["score"] >= 95.0
    assert result["cycles"] >= 1
    assert len(result["repaired_flaws"]) > 0
    assert "Dr. Caelum 'The Exosphere' Sterling" in result["master"]
    assert result["journal"].passed is True
