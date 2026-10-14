#!/usr/bin/env python3
"""
Unit Test Suite for Dr. Aurelius 'The Orbital' Sterling
Interplanetary Astrodynamics & Trajectory Architect Master Subsystem
"""

import math
import pytest
from professions.interplanetary_astrodynamics_architect import (
    MU_SUN,
    MU_EARTH,
    AU_KM,
    vis_viva_velocity,
    hohmann_transfer_delta_v,
    tisserand_parameter,
    cr3bp_jacobi_constant,
    srp_acceleration,
    validate_interplanetary_mission,
    AstrodynamicsInspector,
    AstrodynamicsRubric,
    AstrodynamicsBlindCritic,
    AstrodynamicsElevationEngine,
    DrAureliusSterling
)


def test_vis_viva_and_hohmann_delta_v():
    # 1. Circular Low Earth Orbit (LEO) speed at r = 6378 + 300 = 6678 km
    r_leo = 6678.0
    v_leo = vis_viva_velocity(MU_EARTH, r_leo, r_leo)
    expected_v = math.sqrt(MU_EARTH / r_leo)
    assert math.isclose(v_leo, expected_v, rel_tol=1e-5)
    assert 7.5 < v_leo < 7.9  # km/s

    # 2. Hohmann transfer Earth (1 AU) to Mars (1.524 AU)
    r_earth = 1.0 * AU_KM
    r_mars = 1.524 * AU_KM
    dv1, dv2, dv_total = hohmann_transfer_delta_v(MU_SUN, r_earth, r_mars)
    assert dv1 > 0
    assert dv2 > 0
    assert 5.0 < dv_total < 6.5  # ~5.6 km/s total heliocentric transfer


def test_tisserand_parameter_conservation():
    # Comet or spacecraft before and after Jupiter gravity assist
    a_jup = 5.2044 * AU_KM
    
    # Pre-encounter orbit: a = 3.5 AU, e = 0.5, inc = 10 deg
    a_pre = 3.5 * AU_KM
    e_pre = 0.5
    i_pre = math.radians(10.0)
    tiss_pre = tisserand_parameter(a_pre, e_pre, i_pre, a_jup)

    # Post-encounter orbit: a = 3.2 AU, e = 0.55, inc = 9.5 deg
    a_post = 3.2 * AU_KM
    e_post = 0.55
    i_post = math.radians(9.5)
    tiss_post = tisserand_parameter(a_post, e_post, i_post, a_jup)

    delta_t = abs(tiss_post - tiss_pre)
    assert delta_t <= 0.05, f"Tisserand delta {delta_t} must be conserved <= 0.05"


def test_cr3bp_jacobi_constant_and_zero_velocity():
    # Sun-Earth CR3BP mass ratio ~ 3.0e-6
    mu_se = 3.003e-6
    # Point at Sun-Earth L2 (x ~ 1.01, y = 0, z = 0, zero velocity)
    x = 1.01007
    y = 0.0
    z = 0.0
    vx = 0.0
    vy = 0.0
    vz = 0.0

    c_j = cr3bp_jacobi_constant(x, y, z, vx, vy, vz, mu_se)
    assert c_j > 2.9  # Canonical Sun-Earth L2 Jacobi constant ~ 3.0008


def test_srp_non_gravitational_acceleration():
    # Spacecraft at 1 AU, 1000 kg, 20 m^2 solar array, reflectivity 0.2, sun angle 0
    flux_p0 = 4.56e-6  # N/m^2
    mass = 1000.0
    area = 20.0
    rho = 0.2
    accel = srp_acceleration(flux_p0, 1.0, area, mass, rho, 0.0)
    expected_accel = flux_p0 * (20.0 / 1000.0) * 1.2
    assert math.isclose(accel, expected_accel, rel_tol=1e-5)
    assert accel < 1.0e-6  # Bounded order of magnitude


def test_astrodynamics_inspector_and_rubric():
    inspector = AstrodynamicsInspector()

    clean_code = """
def execute_trajectory():
    delta_v_margin = 1.20
    tisserand_error = 0.012
    periapsis_altitude = 450.0
    jacobi_barrier_breach = False
    unmodeled_srp_drift = 2.5e-7
    return True
"""
    flaws = inspector.inspect_code(clean_code)
    eval_clean = AstrodynamicsRubric.evaluate(flaws)
    assert len(flaws) == 0
    assert eval_clean["passed"] is True
    assert eval_clean["score"] == 100

    flawed_code = """
def execute_trajectory():
    delta_v_margin = 1.05
    tisserand_error = 0.12
    periapsis_altitude = 120.0
    jacobi_barrier_breach = True
    unmodeled_srp_drift = 8.5e-5
    try:
        calculate_ephemeris()
    except Exception:
        pass
    return False
"""
    flawed_issues = inspector.inspect_code(flawed_code)
    eval_flawed = AstrodynamicsRubric.evaluate(flawed_issues)
    assert len(flawed_issues) >= 5
    assert eval_flawed["passed"] is False
    assert eval_flawed["score"] < 40


def test_blind_critic_adversarial_rejection():
    critic = AstrodynamicsBlindCritic()
    suicidal_trajectory = """
def mars_orbit_insertion():
    propellant_margin = 1.02
    tiss_delta = 0.085
    flyby_clearance = 150.0
    return "Burn Complete"
"""
    audit = critic.audit(suicidal_trajectory)
    assert audit["verdict"] == "REJECTED"
    assert audit["score"] < 95
    assert audit["flaw_count"] >= 3


def test_elevation_engine_and_master_closed_loop():
    flawed_script = """
def interplanetary_cruise():
    delta_v_margin = 1.05
    tisserand_error = 0.095
    periapsis_altitude = 180.0
    jacobi_barrier_breach = True
    unmodeled_srp_drift = 4.0e-5
    try:
        star_tracker_update()
    except Exception:
        pass
    return "Cruising"
"""
    master = DrAureliusSterling(min_passing_score=95)
    result = master.execute_closed_loop(flawed_script, target_file="cruise_nav.py")

    assert result["status"] == "CERTIFIED"
    assert result["final_score"] >= 95
    assert "Aurelius" in result["master"]
    assert len(result["actions_applied"]) >= 4

    # Verify that repaired code passes inspector with 100%
    inspector = AstrodynamicsInspector()
    post_flaws = inspector.inspect_code(result["elevated_code"])
    assert len(post_flaws) == 0
