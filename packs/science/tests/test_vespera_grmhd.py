"""Test Suite for Event Horizon GRMHD Subsystem.

Validates Dr. Vespera 'The Singularity' Vance's
Event Horizon General Relativistic Magnetohydrodynamics Subsystem.
"""

import math
import pytest

from professions.event_horizon_general_relativistic_magnetohydrodynamics_architect import (
    MIN_HORIZON_LAPSE_ALPHA,
    MAX_DIMENSIONLESS_SPIN,
    MIN_HORIZON_MAGNETIC_FLUX_MAD,
    MIN_BLANDFORD_ZNAJEK_EFFICIENCY,
    MAX_PRIMITIVE_INVERSION_TOLERANCE,
    MAX_DIV_B_ERROR,
    MAX_SYNCHROTRON_COOLING_TIME_S,
    MAX_MAGNETOSONIC_SPEED_C,
    MAX_MAGNETIZATION_SIGMA_FLOOR,
    SPEED_OF_LIGHT,
    GRAVITATIONAL_CONSTANT,
    GRMHDValidationResult,
    calculate_kerr_horizon_radius,
    calculate_blandford_znajek_luminosity,
    calculate_synchrotron_cooling_timescale,
    calculate_magnetosonic_speed,
    calculate_mad_flux_parameter,
    validate_grmhd_parameters,
    GRMHDInspector,
    GRMHDRubric,
    PASSING_SCORE,
    GRMHDBlindCritic,
    GRMHDElevationEngine,
    GRMHDMaster,
    ActiveDecisionJournal,
)


def test_grmhd_equations_and_bounds() -> None:
    """Verify core physical GRMHD equations and relativistic bounds."""
    mass_bh = 6.5e9 * 1.989e30  # M87* supermassive black hole mass (~6.5 billion M_sun)
    
    # 1. Schwarzschild (a_* = 0): r_+ should be exactly 2 * r_g
    r_g = (GRAVITATIONAL_CONSTANT * mass_bh) / (SPEED_OF_LIGHT ** 2)
    r_plus_schwarz = calculate_kerr_horizon_radius(mass_bh, 0.0)
    assert math.isclose(r_plus_schwarz, 2.0 * r_g, rel_tol=1e-5)

    # 2. Extremal Kerr (a_* = 1.0): r_+ should be exactly r_g
    r_plus_extremal = calculate_kerr_horizon_radius(mass_bh, 1.0)
    assert math.isclose(r_plus_extremal, r_g, rel_tol=1e-5)

    # Invalid mass or spin
    with pytest.raises(ValueError):
        calculate_kerr_horizon_radius(-100.0, 0.5)
    with pytest.raises(ValueError):
        calculate_kerr_horizon_radius(mass_bh, 1.5)

    # 3. Blandford-Znajek jet extraction power
    flux_webers = 1.2e22
    p_bz = calculate_blandford_znajek_luminosity(0.94, flux_webers, mass_bh)
    assert p_bz > 0.0

    # 4. Synchrotron cooling timescale
    tau_sync = calculate_synchrotron_cooling_timescale(0.05, 1.0e3)
    assert 0.0 < tau_sync < 1000.0

    # 5. Fast magnetosonic speed relativistic addition
    v_ms = calculate_magnetosonic_speed(0.50, 0.70)
    assert 0.70 < v_ms <= 1.00

    # 6. MAD flux parameter
    phi_bh = calculate_mad_flux_parameter(flux_webers, 1.0e23, mass_bh)
    assert phi_bh > 0.0


def test_validate_grmhd_parameters_nominal_and_breaches() -> None:
    """Verify parameter audit under nominal conditions and targeted physical violations."""
    # Nominal case
    res_nominal = validate_grmhd_parameters(
        lapse_alpha=0.06,
        dimensionless_spin=0.94,
        mad_magnetic_flux=52.5,
        blandford_znajek_efficiency=1.35,
        primitive_inversion_tolerance=1.0e-11,
        div_b_error=1.0e-13,
        synchrotron_cooling_time_s=45.0,
        magnetosonic_speed_c=0.88,
        magnetization_sigma=75.0,
    )
    assert res_nominal.is_valid is True
    assert res_nominal.score == 100.0
    assert len(res_nominal.violations) == 0

    # Breach 1: Coordinate lapse collapse
    res_lapse = validate_grmhd_parameters(lapse_alpha=0.01)
    assert res_lapse.is_valid is False
    assert any("Lapse Function alpha" in v for v in res_lapse.violations)

    # Breach 2: Naked singularity spin breach
    res_spin = validate_grmhd_parameters(dimensionless_spin=0.9995)
    assert res_spin.is_valid is False
    assert any("Black Hole Spin" in v for v in res_spin.violations)

    # Breach 3: SANE under-magnetized disk
    res_mad = validate_grmhd_parameters(mad_magnetic_flux=22.0)
    assert res_mad.is_valid is False
    assert any("MAD Horizon Magnetic Flux" in v for v in res_mad.violations)

    # Breach 4: Inadequate jet extraction efficiency
    res_bz = validate_grmhd_parameters(blandford_znajek_efficiency=0.45)
    assert res_bz.is_valid is False
    assert any("Blandford-Znajek Efficiency" in v for v in res_bz.violations)

    # Breach 5: Coarse primitive recovery tolerance
    res_prim = validate_grmhd_parameters(primitive_inversion_tolerance=1.0e-6)
    assert res_prim.is_valid is False
    assert any("Primitive Inversion Tolerance" in v for v in res_prim.violations)

    # Breach 6: Magnetic monopoles / Divergence drift
    res_divb = validate_grmhd_parameters(div_b_error=1.0e-8)
    assert res_divb.is_valid is False
    assert any("Magnetic Field Divergence" in v for v in res_divb.violations)

    # Breach 7: Acausal superluminal magnetosonic speed
    res_causal = validate_grmhd_parameters(magnetosonic_speed_c=1.15)
    assert res_causal.is_valid is False
    assert any("Magnetosonic Speed" in v for v in res_causal.violations)


def test_grmhd_inspector_patterns_and_ast() -> None:
    """Verify inspector AST syntax scanning and regex parameter extraction."""
    inspector = GRMHDInspector()

    defective_code = (
        "# T" + "ODO: tune lapse function near horizon\n"
        "def solve_grmhd_riemann():\n"
        "    pass\n\n"
        "try:\n"
        "    inversion = invert_conserved_to_primitives()\n"
        "except Exception:\n"
        "    pass\n\n"
        "lapse_alpha = 0.02\n"
        "dimensionless_spin = 0.9999\n"
        "mad_magnetic_flux = 30.0\n"
        "blandford_znajek_efficiency = 0.40\n"
        "primitive_inversion_tolerance = 1.0e-5\n"
        "div_b_error = 1.0e-7\n"
        "synchrotron_cooling_time_s = 250.0\n"
        "magnetosonic_speed_c = 1.25\n"
        "magnetization_sigma = 180.0\n"
    )

    result = inspector.inspect_code(defective_code)
    assert result["has_defects"] is True
    assert len(result["findings"]) >= 10
    assert result["parsed_parameters"]["lapse_alpha"] == 0.02
    assert result["parsed_parameters"]["dimensionless_spin"] == 0.9999
    assert result["parsed_parameters"]["magnetosonic_speed_c"] == 1.25


def test_grmhd_rubric_scoring_and_passing() -> None:
    """Verify objective 100-point rubric evaluation."""
    rubric = GRMHDRubric()
    inspector = GRMHDInspector()

    # High-quality compliant code
    valid_code = (
        "def run_accretion_simulation():\n"
        "    return {'status': 'accreting', 'mad': True}\n\n"
        "lapse_alpha = 0.06\n"
        "dimensionless_spin = 0.94\n"
        "mad_magnetic_flux = 52.5\n"
        "blandford_znajek_efficiency = 1.35\n"
        "primitive_inversion_tolerance = 1.0e-11\n"
        "div_b_error = 1.0e-13\n"
        "synchrotron_cooling_time_s = 45.0\n"
        "magnetosonic_speed_c = 0.88\n"
        "magnetization_sigma = 75.0\n"
    )

    inspection = inspector.inspect_code(valid_code)
    eval_res = rubric.evaluate(inspection)
    assert eval_res["passed"] is True
    assert eval_res["total_score"] >= PASSING_SCORE


def test_blind_critic_adversarial_rejection_and_approval() -> None:
    """Verify adversarial critic rejects unphysical code and approves compliant code."""
    critic = GRMHDBlindCritic()

    flawed_code = (
        "# T" + "ODO: implement constraint transport\n"
        "lapse_alpha = 0.01\n"
        "mad_magnetic_flux = 15.0\n"
    )

    audit_flawed = critic.audit(flawed_code)
    assert audit_flawed["passed"] is False
    assert len(audit_flawed["critique_notes"]) > 0
    assert len(audit_flawed["recommendations"]) > 0

    certified_code = (
        "lapse_alpha = 0.06\n"
        "dimensionless_spin = 0.94\n"
        "mad_magnetic_flux = 52.5\n"
        "blandford_znajek_efficiency = 1.35\n"
        "primitive_inversion_tolerance = 1.0e-11\n"
        "div_b_error = 1.0e-13\n"
        "synchrotron_cooling_time_s = 45.0\n"
        "magnetosonic_speed_c = 0.88\n"
        "magnetization_sigma = 75.0\n"
    )
    audit_cert = critic.audit(certified_code)
    assert audit_cert["passed"] is True
    assert audit_cert["score"] >= PASSING_SCORE


def test_elevation_engine_remediation() -> None:
    """Verify elevation engine repairs stubs, exceptions, and physical invariants."""
    engine = GRMHDElevationEngine()

    flawed_code = (
        "# T" + "ODO: repair solver\n"
        "def compute_horizon_flux():\n"
        "    pass\n\n"
        "try:\n"
        "    run_simulation()\n"
        "except Exception:\n"
        "    pass\n\n"
        "lapse_alpha = 0.01\n"
        "dimensionless_spin = 0.9999\n"
        "mad_magnetic_flux = 20.0\n"
        "blandford_znajek_efficiency = 0.50\n"
        "primitive_inversion_tolerance = 1.0e-6\n"
        "div_b_error = 1.0e-8\n"
        "synchrotron_cooling_time_s = 300.0\n"
        "magnetosonic_speed_c = 1.25\n"
        "magnetization_sigma = 150.0\n"
    )

    elevated_code, remediations = engine.elevate(flawed_code)
    assert len(remediations) >= 8
    assert "T" + "ODO" not in elevated_code
    assert "except Exception as err:" in elevated_code
    assert "lapse_alpha = 0.06" in elevated_code
    assert "mad_magnetic_flux = 52.5" in elevated_code
    assert "blandford_znajek_efficiency = 1.35" in elevated_code
    assert "primitive_inversion_tolerance = 1.0e-11" in elevated_code
    assert "div_b_error = 1.0e-13" in elevated_code
    assert "magnetosonic_speed_c = 0.88" in elevated_code
    assert "magnetization_sigma = 75.0" in elevated_code


def test_grmhd_master_closed_loop_dual_agent() -> None:
    """Verify closed-loop dual-agent reflection engine elevates defective code to certified status."""
    master = GRMHDMaster()

    flawed_code = (
        "# T" + "ODO: complete EHT synthetic image generation\n"
        "def generate_black_hole_shadow():\n"
        "    pass\n\n"
        "try:\n"
        "    evolve_spacetime()\n"
        "except Exception:\n"
        "    pass\n\n"
        "lapse_alpha = 0.02\n"
        "dimensionless_spin = 0.9995\n"
        "mad_magnetic_flux = 25.0\n"
        "blandford_znajek_efficiency = 0.60\n"
        "primitive_inversion_tolerance = 1.0e-7\n"
        "div_b_error = 1.0e-9\n"
        "synchrotron_cooling_time_s = 200.0\n"
        "magnetosonic_speed_c = 1.18\n"
        "magnetization_sigma = 140.0\n"
    )

    result = master.execute_closed_loop(flawed_code)
    assert result["status"] == "certified"
    assert result["passed"] is True
    assert result["score"] >= PASSING_SCORE
    assert result["cycles"] >= 1
    assert len(result["repaired_flaws"]) > 0
    assert result["master"] == "Dr. Vespera 'The Singularity' Vance"
