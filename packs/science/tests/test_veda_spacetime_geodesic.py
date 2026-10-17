"""Test suite for Dr. Veda Vance - Relativistic Spacetime Geodesic Architect.

Covers Kerr black hole horizons, ergosphere radii, ISCO calculations, Blandford-Znajek jet power,
symplectic invariant drift inspection, rubric evaluation, adversarial criticism, elevation engine,
and master dual-agent closed-loop reflection.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.relativistic_spacetime_geodesic_architect import (
    SPEED_OF_LIGHT,
    GRAVITATIONAL_CONSTANT,
    SOLAR_MASS_KG,
    MAX_KERR_SPIN_PARAMETER,
    MAX_SYMPLECTIC_ENERGY_DRIFT,
    MAX_ANGULAR_MOMENTUM_DRIFT,
    MAX_CARTER_CONSTANT_DRIFT,
    MIN_BZ_JET_POWER_W,
    MIN_INTEGRATOR_ORDER,
    calculate_kerr_horizons,
    calculate_kerr_ergosphere_radius,
    calculate_isco_radius,
    calculate_blandford_znajek_power,
    validate_spacetime_geodesic_parameters,
    SpacetimeGeodesicInspector,
    SpacetimeGeodesicRubric,
    SpacetimeGeodesicBlindCritic,
    SpacetimeGeodesicElevationEngine,
    SpacetimeGeodesicMaster,
)


def test_kerr_horizons_and_ergosphere_mathematics():
    """Verify event horizons and ergosphere radii for Schwarzschild and Kerr spacetimes."""
    # Schwarzschild case: mass M = 1.0, spin a = 0.0
    r_plus, r_minus = calculate_kerr_horizons(1.0, 0.0)
    assert r_plus == pytest.approx(2.0, rel=1e-5)
    assert r_minus == pytest.approx(0.0, rel=1e-5)

    # Extreme Thorne limit: mass M = 1.0, spin a = 0.998
    r_plus_kerr, r_minus_kerr = calculate_kerr_horizons(1.0, 0.998)
    expected_disc = (1.0 - 0.998 ** 2) ** 0.5
    assert r_plus_kerr == pytest.approx(1.0 + expected_disc, rel=1e-5)
    assert r_minus_kerr == pytest.approx(1.0 - expected_disc, rel=1e-5)

    # Non-physical spin exceeding mass
    r_plus_bad, r_minus_bad = calculate_kerr_horizons(1.0, 1.05)
    assert r_plus_bad == 0.0 and r_minus_bad == 0.0

    # Ergosphere radius at equator (theta = pi/2) vs pole (theta = 0)
    import math
    r_ergo_equator = calculate_kerr_ergosphere_radius(1.0, 0.94, math.pi / 2.0)
    assert r_ergo_equator == pytest.approx(2.0, rel=1e-5)

    r_ergo_pole = calculate_kerr_ergosphere_radius(1.0, 0.94, 0.0)
    r_plus_94, _ = calculate_kerr_horizons(1.0, 0.94)
    assert r_ergo_pole == pytest.approx(r_plus_94, rel=1e-5)


def test_isco_radius_and_blandford_znajek_power():
    """Verify ISCO radius bounds and Blandford-Znajek jet extraction power."""
    # Schwarzschild ISCO: a_* = 0 -> r_ISCO = 6.0 M
    r_isco_schwarz = calculate_isco_radius(1.0, 0.0)
    assert r_isco_schwarz == pytest.approx(6.0, rel=1e-4)

    # Prograde high-spin ISCO: a_* = 0.998 -> r_ISCO approaches ~1.23 M
    r_isco_prograde = calculate_isco_radius(1.0, 0.998, prograde=True)
    assert 1.0 <= r_isco_prograde <= 1.30

    # Retrograde high-spin ISCO: a_* = 0.998 -> r_ISCO approaches ~9.0 M
    r_isco_retrograde = calculate_isco_radius(1.0, 0.998, prograde=False)
    assert 8.80 <= r_isco_retrograde <= 9.05

    # Blandford-Znajek power for supermassive black hole: M = 1e9 M_sun, a_* = 0.94, Phi = 1e22 Wb
    m_smbh = 1.0e9 * SOLAR_MASS_KG
    p_bz = calculate_blandford_znajek_power(m_smbh, 0.94, 1.0e22)
    assert p_bz >= MIN_BZ_JET_POWER_W


def test_validate_spacetime_geodesic_parameters_nominal_and_breaches():
    """Verify validation dataclass against nominal parameters and boundary breaches."""
    # Nominal case
    res_nominal = validate_spacetime_geodesic_parameters(
        dimensionless_spin=0.94,
        symplectic_energy_drift=4.2e-12,
        angular_momentum_drift=3.8e-12,
        carter_constant_drift=5.1e-12,
        bz_jet_power_w=4.5e38,
        integrator_order=4,
        isco_radius_m=2.05,
        outer_horizon_radius_m=1.34
    )
    assert res_nominal.is_valid is True
    assert len(res_nominal.flaws) == 0

    # Breach case: naked singularity (spin 1.05), non-symplectic drift (1e-6), low jet power (1e30), low order (2)
    res_breach = validate_spacetime_geodesic_parameters(
        dimensionless_spin=1.05,
        symplectic_energy_drift=1.5e-6,
        angular_momentum_drift=2.2e-7,
        carter_constant_drift=3.1e-7,
        bz_jet_power_w=1.0e30,
        integrator_order=2,
        isco_radius_m=0.5,
        outer_horizon_radius_m=2.5
    )
    assert res_breach.is_valid is False
    assert len(res_breach.flaws) == 8


def test_spacetime_geodesic_inspector_patterns_and_ast():
    """Verify static and AST inspection detects placeholders, drifts, and empty blocks."""
    inspector = SpacetimeGeodesicInspector()

    flawed_code = (
        "# TODO: calibrate Kerr metric spin tensor\n"
        "dimensionless_spin = 1.02\n"
        "symplectic_energy_drift = 5.0e-8\n"
        "angular_momentum_drift = 2.0e-8\n"
        "carter_constant_drift = 3.0e-8\n"
        "bz_jet_power_w = 5.0e36\n"
        "integrator_order = 2\n"
        "isco_radius_m = 0.8\n"
        "outer_horizon_radius_m = 2.4\n"
        "def compute_geodesic() -> None:\n"
        "    pass\n"
        "try:\n"
        "    step = 1\n"
        "except Exception:\n"
        "    pass\n"
    )

    flaws = inspector.inspect_source(flawed_code)
    flaw_ids = [f["id"] for f in flaws]

    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "COSMIC_CENSORSHIP_VIOLATION" in flaw_ids
    assert "SYMPLECTIC_ENERGY_DRIFT_EXCESS" in flaw_ids
    assert "ANGULAR_MOMENTUM_DRIFT_EXCESS" in flaw_ids
    assert "CARTER_CONSTANT_DRIFT_EXCESS" in flaw_ids
    assert "BZ_JET_POWER_DEFICIT" in flaw_ids
    assert "INTEGRATOR_ORDER_DEFICIT" in flaw_ids
    assert "ISCO_RADIUS_OUT_OF_BOUNDS" in flaw_ids
    assert "HORIZON_RADIUS_OUT_OF_BOUNDS" in flaw_ids
    assert "EMPTY_FUNCTION_BODY" in flaw_ids
    assert "EMPTY_EXCEPT_BLOCK" in flaw_ids

    text_flaws = inspector.inspect_code(flawed_code)
    assert len(text_flaws) == len(flaws)


def test_spacetime_geodesic_rubric_scoring_and_passing():
    """Verify objective rubric scoring logic and passing thresholds."""
    rubric = SpacetimeGeodesicRubric()

    # Zero flaws -> 100 passed
    eval_pass = rubric.evaluate([])
    assert eval_pass.score == 100
    assert eval_pass.passed is True

    # One CRITICAL flaw (-25 pts) -> 75 rejected
    flaw_crit = [{"id": "COSMIC_CENSORSHIP_VIOLATION", "severity": "CRITICAL", "description": "Naked singularity"}]
    eval_crit = rubric.evaluate(flaw_crit)
    assert eval_crit.score == 75
    assert eval_crit.passed is False

    # One LOW flaw (-3 pts) -> 97 passed
    flaw_low = [{"id": "TELEMETRY_SAMPLE", "severity": "LOW", "description": "Diagnostic sample"}]
    eval_low = rubric.evaluate(flaw_low)
    assert eval_low.score == 97
    assert eval_low.passed is True


def test_blind_critic_adversarial_rejection():
    """Verify blind critic accurately certifies clean code and rejects flawed submissions."""
    critic = SpacetimeGeodesicBlindCritic()

    clean_code = (
        "dimensionless_spin = 0.94\n"
        "symplectic_energy_drift = 1.0e-12\n"
        "angular_momentum_drift = 1.0e-12\n"
        "carter_constant_drift = 1.0e-12\n"
        "bz_jet_power_w = 2.0e39\n"
        "integrator_order = 4\n"
        "isco_radius_m = 2.05\n"
        "outer_horizon_radius_m = 1.34\n"
        "def compute_geodesic() -> bool:\n"
        "    return True\n"
    )

    clean_res = critic.audit(clean_code)
    assert clean_res["verdict"] == "APPROVED"
    assert clean_res["score"] == 100
    assert clean_res["passed"] is True

    flawed_code = (
        "dimensionless_spin = 1.05\n"
        "symplectic_energy_drift = 1.0e-6\n"
    )
    flawed_res = critic.audit(flawed_code)
    assert flawed_res["verdict"] == "REJECTED"
    assert flawed_res["passed"] is False
    assert flawed_res["score"] < 95


def test_elevation_engine_and_master_closed_loop():
    """Verify autonomous elevation restores code to >=95 standards and master coordinates reflection."""
    engine = SpacetimeGeodesicElevationEngine()

    flawed_code = (
        "# TODO: initialize Kerr ray tracing grid\n"
        "dimensionless_spin = 1.04\n"
        "symplectic_energy_drift = 5.0e-8\n"
        "angular_momentum_drift = 2.0e-8\n"
        "carter_constant_drift = 3.0e-8\n"
        "bz_jet_power_w = 1.0e35\n"
        "integrator_order = 2\n"
        "isco_radius_m = 0.5\n"
        "outer_horizon_radius_m = 2.8\n"
        "def trace_null_geodesic() -> dict:\n"
        "    pass\n"
        "try:\n"
        "    step_val = 1\n"
        "except ValueError:\n"
        "    pass\n"
    )

    elevated, actions = engine.elevate(flawed_code)
    assert len(actions) > 0

    critic = SpacetimeGeodesicBlindCritic()
    audit_after = critic.audit(elevated)
    assert audit_after["passed"] is True
    assert audit_after["score"] >= 95

    # Test master closed-loop execution
    master = SpacetimeGeodesicMaster()
    res = master.evaluate_and_elevate(flawed_code, target_file="spacetime_geodesic.py")
    assert res["status"] == "certified"
    assert res["final_score"] >= 95
    assert res["iterations"] >= 1
    assert len(res["repaired_flaws"]) > 0
