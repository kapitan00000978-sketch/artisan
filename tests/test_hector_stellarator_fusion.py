"""Test suite for Dr. Hector Vance - Stellarator Magnet & Twisted Coil Fusion Architect.

Covers 3D space curve curvature, rotational transform, island divertor heat flux, neoclassical ripple, AST inspection, rubric, critic, elevation, and master reflection.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.stellarator_twisted_coil_fusion_architect import (
    MIN_ROTATIONAL_TRANSFORM,
    MAX_ROTATIONAL_TRANSFORM,
    MIN_COIL_BEND_RADIUS_M,
    MAX_DIVERTOR_HEAT_FLUX_MW_M2,
    calculate_rotational_transform,
    calculate_coil_bend_curvature,
    calculate_island_divertor_heat_flux,
    calculate_effective_ripple_transport_factor,
    validate_stellarator_fusion_parameters,
    StellaratorFusionInspector,
    StellaratorFusionRubric,
    StellaratorFusionBlindCritic,
    StellaratorFusionElevationEngine,
    StellaratorFusionMaster,
)


def test_rotational_transform_and_curvature_equations():
    # Rotational transform: 95 poloidal turns for 100 toroidal turns -> iota/2pi = 0.95
    iota = calculate_rotational_transform(95.0, 100.0)
    assert 0.949 <= iota <= 0.951
    assert MIN_ROTATIONAL_TRANSFORM <= iota <= MAX_ROTATIONAL_TRANSFORM

    # Zero toroidal turns edge case
    assert calculate_rotational_transform(50.0, 0.0) == 0.0

    # Circle of radius R = 0.80 m in xy plane: r(t) = (R*cos(t), R*sin(t), 0)
    # At t = 0: r'(0) = (0, R, 0), r''(0) = (-R, 0, 0)
    # r' x r'' = (0, 0, R^2)
    # kappa = R^2 / R^3 = 1 / R = 1 / 0.80 = 1.25 m^-1
    # rho_bend = 1 / 1.25 = 0.80 m
    R = 0.80
    kappa, rho = calculate_coil_bend_curvature(0.0, R, 0.0, -R, 0.0, 0.0)
    assert abs(kappa - 1.25) < 1.0e-4
    assert abs(rho - 0.80) < 1.0e-4
    assert rho >= MIN_COIL_BEND_RADIUS_M

    # Degenerate zero-velocity test
    k_zero, r_zero = calculate_coil_bend_curvature(0.0, 0.0, 0.0, 1.0, 0.0, 0.0)
    assert k_zero == 0.0
    assert r_zero == float("inf")


def test_island_divertor_heat_flux_and_ripple_transport():
    # Exhaust power P_exhaust = 100 MW, radiative fraction f_rad = 0.90, wetted area A_wetted = 2.0 m^2
    # Unradiated power = 10 MW
    # q_div = 10 MW / 2.0 m^2 = 5.0 MW/m^2 <= 10.0 MW/m^2
    q_div = calculate_island_divertor_heat_flux(100.0, 0.90, 2.0)
    assert 4.9 <= q_div <= 5.1
    assert q_div <= MAX_DIVERTOR_HEAT_FLUX_MW_M2

    # Zero wetted area edge case
    assert calculate_island_divertor_heat_flux(100.0, 0.90, 0.0) == float("inf")

    # Neoclassical ripple factor for epsilon_eff = 0.005, T = 15 keV, B = 5.0 T
    # D_neo ~ (0.005 * 15^3.5) / 25
    factor = calculate_effective_ripple_transport_factor(0.005, 15.0, 5.0)
    assert factor > 0.0
    assert calculate_effective_ripple_transport_factor(0.005, 15.0, 0.0) == 0.0


def test_validate_stellarator_fusion_parameters_nominal_and_breaches():
    res_nominal = validate_stellarator_fusion_parameters(
        rotational_transform=0.95,
        magnetic_shear=0.05,
        min_coil_bend_radius_m=0.65,
        coil_plasma_standoff_m=1.45,
        effective_helical_ripple=0.0065,
        divertor_heat_flux_mw_m2=7.5,
        divertor_rad_fraction=0.88,
        conductor_peak_field_t=13.8,
        casing_von_mises_mpa=520.0,
        hts_winding_strain_pct=0.22,
        quench_dump_time_ms=180.0,
        net_toroidal_current_ka=12.0
    )
    assert res_nominal.is_valid is True
    assert len(res_nominal.flaws) == 0

    # Breach case: resonant iota (1.00), high shear (0.35), sharp bend (0.25 m), tight standoff (0.75 m),
    # high ripple (0.04), extreme heat flux (25.0 MW/m^2), low radiation (0.50), high field (20.0 T),
    # high stress (850 MPa), excessive strain (0.60%), delayed quench (400 ms), high toroidal current (120 kA)
    res_breach = validate_stellarator_fusion_parameters(
        rotational_transform=1.00,
        magnetic_shear=0.35,
        min_coil_bend_radius_m=0.25,
        coil_plasma_standoff_m=0.75,
        effective_helical_ripple=0.04,
        divertor_heat_flux_mw_m2=25.0,
        divertor_rad_fraction=0.50,
        conductor_peak_field_t=20.0,
        casing_von_mises_mpa=850.0,
        hts_winding_strain_pct=0.60,
        quench_dump_time_ms=400.0,
        net_toroidal_current_ka=120.0
    )
    assert res_breach.is_valid is False
    assert len(res_breach.flaws) >= 11


def test_stellarator_inspector_patterns_and_ast():
    inspector = StellaratorFusionInspector()

    flawed_code = (
        "# TODO: finish 3D modular coil discretization\n"
        "rotational_transform = 1.00\n"
        "magnetic_shear = 0.28\n"
        "min_coil_bend_radius_m = 0.32\n"
        "coil_plasma_standoff_m = 0.85\n"
        "effective_helical_ripple = 0.025\n"
        "divertor_heat_flux_mw_m2 = 18.5\n"
        "divertor_rad_fraction = 0.65\n"
        "conductor_peak_field_t = 19.5\n"
        "casing_von_mises_mpa = 780.0\n"
        "hts_winding_strain_pct = 0.55\n"
        "quench_dump_time_ms = 350.0\n"
        "net_toroidal_current_ka = 95.0\n"
        "def compute_equilibrium() -> bool:\n"
        "    pass\n"
        "try:\n"
        "    current = 100\n"
        "except Exception:\n"
        "    pass\n"
    )

    flaws = inspector.inspect_source(flawed_code)
    flaw_ids = [f["id"] for f in flaws]

    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "RATIONAL_ISLAND_RESONANCE_RISK" in flaw_ids
    assert "MAGNETIC_SHEAR_EXCESS" in flaw_ids
    assert "COIL_BEND_RADIUS_DEFICIT" in flaw_ids
    assert "COIL_PLASMA_STANDOFF_DEFICIT" in flaw_ids
    assert "HELICAL_RIPPLE_EXCESS" in flaw_ids
    assert "DIVERTOR_HEAT_FLUX_EXCESS" in flaw_ids
    assert "DIVERTOR_RAD_FRACTION_DEFICIT" in flaw_ids
    assert "PEAK_MAGNETIC_FIELD_EXCESS" in flaw_ids
    assert "CASING_STRESS_EXCESS" in flaw_ids
    assert "HTS_STRAIN_EXCESS" in flaw_ids
    assert "QUENCH_DUMP_DELAY" in flaw_ids
    assert "TOROIDAL_CURRENT_EXCESS" in flaw_ids
    assert "EMPTY_FUNCTION_BODY" in flaw_ids
    assert "EMPTY_EXCEPT_BLOCK" in flaw_ids

    text_flaws = inspector.inspect_code(flawed_code)
    assert len(text_flaws) == len(flaws)


def test_stellarator_rubric_scoring_and_passing():
    rubric = StellaratorFusionRubric()

    # Zero flaws -> 100
    eval_pass = rubric.evaluate([])
    assert eval_pass.score == 100
    assert eval_pass.passed is True

    # One CRITICAL flaw (-25 pts) -> score 75, rejected
    flaw_crit = [{"id": "RATIONAL_ISLAND_RESONANCE_RISK", "severity": "CRITICAL", "description": "Resonance breach"}]
    eval_crit = rubric.evaluate(flaw_crit)
    assert eval_crit.score == 75
    assert eval_crit.passed is False

    # One LOW flaw (-3 pts) -> score 97, passes (>= 95)
    flaw_low = [{"id": "TELEMETRY_NOTICE", "severity": "LOW", "description": "Diagnostic notice"}]
    eval_low = rubric.evaluate(flaw_low)
    assert eval_low.score == 97
    assert eval_low.passed is True


def test_blind_critic_adversarial_rejection():
    critic = StellaratorFusionBlindCritic()

    clean_code = (
        "rotational_transform = 0.95\n"
        "magnetic_shear = 0.05\n"
        "min_coil_bend_radius_m = 0.65\n"
        "coil_plasma_standoff_m = 1.45\n"
        "effective_helical_ripple = 0.0065\n"
        "divertor_heat_flux_mw_m2 = 7.5\n"
        "divertor_rad_fraction = 0.88\n"
        "conductor_peak_field_t = 13.8\n"
        "casing_von_mises_mpa = 520.0\n"
        "hts_winding_strain_pct = 0.22\n"
        "quench_dump_time_ms = 180.0\n"
        "net_toroidal_current_ka = 12.0\n"
        "def coil_status() -> bool:\n"
        "    return True\n"
    )

    clean_res = critic.audit(clean_code)
    assert clean_res["verdict"] == "APPROVED"
    assert clean_res["score"] == 100
    assert clean_res["passed"] is True

    flawed_code = (
        "rotational_transform = 1.00\n"
        "min_coil_bend_radius_m = 0.20\n"
    )
    flawed_res = critic.audit(flawed_code)
    assert flawed_res["verdict"] == "REJECTED"
    assert flawed_res["passed"] is False
    assert flawed_res["score"] < 95


def test_elevation_engine_and_master_closed_loop():
    engine = StellaratorFusionElevationEngine()

    flawed_code = (
        "# TODO: calibrate modular coil winding pack\n"
        "rotational_transform = 1.00\n"
        "magnetic_shear = 0.30\n"
        "min_coil_bend_radius_m = 0.28\n"
        "coil_plasma_standoff_m = 0.90\n"
        "effective_helical_ripple = 0.035\n"
        "divertor_heat_flux_mw_m2 = 19.0\n"
        "divertor_rad_fraction = 0.60\n"
        "conductor_peak_field_t = 19.0\n"
        "casing_von_mises_mpa = 820.0\n"
        "hts_winding_strain_pct = 0.50\n"
        "quench_dump_time_ms = 360.0\n"
        "net_toroidal_current_ka = 85.0\n"
        "def equilibrium_profile() -> dict:\n"
        "    pass\n"
        "try:\n"
        "    val = 1\n"
        "except ValueError:\n"
        "    pass\n"
    )

    elevated, actions = engine.elevate(flawed_code)
    assert len(actions) > 0

    critic = StellaratorFusionBlindCritic()
    audit_after = critic.audit(elevated)
    assert audit_after["passed"] is True
    assert audit_after["score"] >= 95

    # Test master closed-loop execution
    master = StellaratorFusionMaster()
    res = master.evaluate_and_elevate(flawed_code, target_file="stellarator_coils.py")
    assert res["status"] == "certified"
    assert res["final_score"] >= 95
    assert res["iterations"] >= 1
    assert len(res["repaired_flaws"]) > 0
