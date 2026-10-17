#!/usr/bin/env python3
"""
Unit Test Suite for Commander Rowan 'The Fusion-Drive' Sterling
Direct Fusion Rocket & Magnetoplasmadynamic Propulsion Architect Master Subsystem
"""

import math
import pytest
from professions.fusion_rocket_propulsion_architect import (
    exhaust_velocity_from_isp,
    alfven_velocity,
    magnetic_nozzle_alfven_mach,
    nozzle_divergence_efficiency,
    thrust_power_efficiency,
    validate_fusion_rocket,
    FusionRocketInspector,
    FusionRocketRubric,
    FusionRocketBlindCritic,
    FusionRocketElevationEngine,
    CommanderRowanSterling
)


def test_exhaust_velocity_and_isp():
    # Specific impulse 10,000 s
    isp = 10000.0
    v_e = exhaust_velocity_from_isp(isp)
    # Expected: 10000 * 9.80665 = 98066.5 m/s (~98.1 km/s)
    assert math.isclose(v_e, 98066.5, rel_tol=1e-5)

    with pytest.raises(ValueError):
        exhaust_velocity_from_isp(-50.0)


def test_alfven_velocity_and_mach_detachment():
    # Magnetic field 0.1 T, plasma density rho = 1.0e-7 kg/m^3
    b_field = 0.1
    rho = 1.0e-7
    v_a = alfven_velocity(b_field, rho)
    # v_A = 0.1 / sqrt(1.256637e-6 * 1e-7) = 0.1 / sqrt(1.256637e-13) ~ 0.1 / 3.5449e-7 ~ 2.82e5 m/s
    assert 2.5e5 < v_a < 3.0e5

    # Exhaust velocity 6.0e5 m/s
    v_exhaust = 6.0e5
    m_a = magnetic_nozzle_alfven_mach(v_exhaust, b_field, rho)
    # M_A ~ 6.0e5 / 2.82e5 ~ 2.13 > 1.50
    assert m_a > 1.50


def test_nozzle_divergence_efficiency_and_thrust_power():
    # Divergence half-angle 12.0 degrees
    theta = 12.0
    eta_div = nozzle_divergence_efficiency(theta)
    # Expected: (1 + cos(12 deg)) / 2 = (1 + 0.9781476) / 2 = 0.98907
    assert math.isclose(eta_div, (1.0 + math.cos(math.radians(12.0))) / 2.0, rel_tol=1e-5)
    assert eta_div > 0.98

    # Thrust power efficiency: F = 1000 N, m_dot = 0.01 kg/s, P_fusion = 7.0e7 W (70 MW)
    f = 1000.0
    m_dot = 0.01
    p_fusion = 7.0e7
    eta_thrust = thrust_power_efficiency(f, m_dot, p_fusion)
    # P_jet = 1000^2 / (2 * 0.01) = 1e6 / 0.02 = 5e7 W (50 MW)
    # eta = (5e7 / 7e7) * 100% ~ 71.43%
    assert math.isclose(eta_thrust, (5.0e7 / 7.0e7) * 100.0, rel_tol=1e-5)
    assert eta_thrust > 65.0


def test_validate_fusion_rocket():
    # Valid setup
    valid_res = validate_fusion_rocket(
        specific_impulse_s=18500.0,
        alfven_mach=2.45,
        divergence_half_angle_deg=6.8,
        neutron_wall_flux_mw_m2=0.85,
        thrust_efficiency_pct=78.5,
        plasma_purity_pct=99.4
    )
    assert valid_res.is_valid is True
    assert len(valid_res.violations) == 0

    # Invalid setup
    invalid_res = validate_fusion_rocket(
        specific_impulse_s=4500.0,   # < 10000.0
        alfven_mach=0.85,            # < 1.50
        divergence_half_angle_deg=22.0, # > 12.0
        neutron_wall_flux_mw_m2=4.8,    # > 2.0
        thrust_efficiency_pct=42.0,     # < 65.0
        plasma_purity_pct=88.0          # < 98.0
    )
    assert invalid_res.is_valid is False
    assert len(invalid_res.violations) == 6


def test_fusion_rocket_inspector_and_rubric():
    inspector = FusionRocketInspector()

    clean_code = """
def run_fusion_rocket_burn():
    specific_impulse = 18500.0
    alfven_mach = 2.45
    divergence_half_angle = 6.8
    neutron_wall_flux = 0.85
    thrust_efficiency = 78.5
    plasma_purity = 99.4
    return "Interplanetary Cruise Thrust Locked"
"""
    clean_flaws = inspector.inspect_code(clean_code)
    clean_eval = FusionRocketRubric.evaluate(clean_flaws)
    assert len(clean_flaws) == 0
    assert clean_eval["passed"] is True
    assert clean_eval["score"] == 100

    flawed_code = """
def run_fusion_rocket_burn():
    specific_impulse = 3500.0
    alfven_mach = 0.65
    divergence_half_angle = 28.0
    neutron_wall_flux = 6.5
    thrust_efficiency = 38.0
    plasma_purity = 85.0
    try:
        read_hts_flux_sensor()
    except Exception:
        pass
    return "Coil Quench Imminent"
"""
    flawed_issues = inspector.inspect_code(flawed_code)
    flawed_eval = FusionRocketRubric.evaluate(flawed_issues)
    assert len(flawed_issues) >= 6
    assert flawed_eval["passed"] is False
    assert flawed_eval["score"] < 40


def test_blind_critic_adversarial_rejection():
    critic = FusionRocketBlindCritic()
    leaky_thruster = """
def thruster_loop():
    specific_impulse = 2800.0
    alfven_mach = 0.45
    neutron_wall_flux = 8.0
    return "Plasma Detachment Failed"
"""
    audit = critic.audit(leaky_thruster)
    assert audit["verdict"] == "REJECTED"
    assert audit["score"] < 95
    assert audit["flaw_count"] >= 3


def test_elevation_engine_and_master_closed_loop():
    flawed_script = """
def fusion_propulsion_cruise_executive():
    specific_impulse = 5200.0
    alfven_mach = 0.90
    divergence_half_angle = 18.5
    neutron_wall_flux = 4.2
    thrust_efficiency = 52.0
    plasma_purity = 91.0
    try:
        detect_magnetic_nozzle_divergence()
    except Exception:
        pass
    return "Exhaust Deceleration"
"""
    master = CommanderRowanSterling(min_passing_score=95)
    result = master.execute_closed_loop(flawed_script, target_file="fusion_engine_core.py")

    assert result["status"] == "CERTIFIED"
    assert result["final_score"] >= 95
    assert "Rowan" in result["master"]
    assert len(result["actions_applied"]) >= 6

    # Verify that elevated code passes inspector with 100%
    inspector = FusionRocketInspector()
    post_flaws = inspector.inspect_code(result["elevated_code"])
    assert len(post_flaws) == 0
