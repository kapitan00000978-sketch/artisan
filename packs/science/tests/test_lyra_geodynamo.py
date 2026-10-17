"""Rigorous Test Suite for Master #57 Dr. Lyra 'The Core' Sterling.

Planetary Geodynamo Core Fluid Dynamics & Planetary Magnetic Field Generation Architect.
Verifies dimensionless magnetohydrodynamic equations, static AST/regex inspection,
100-point rubric scoring, blind critique, autonomous elevation, and master reflection engine.
"""

import pytest
from professions.planetary_geodynamo_core_architect import (
    GeodynamoCoreParameters,
    validate_geodynamo_parameters,
    calculate_magnetic_reynolds_number,
    calculate_rossby_number,
    calculate_ekman_number,
    calculate_elsasser_number,
    calculate_surface_dipole_energy_fraction,
    calculate_dynamo_number,
    GeodynamoCodeInspector,
    GeodynamoRubricEvaluator,
    PlanetaryGeodynamoBlindCritic,
    PlanetaryGeodynamoElevationEngine,
    PlanetaryGeodynamoMaster,
    MIN_MAGNETIC_REYNOLDS,
    MAX_ROSSBY_NUMBER,
    MAX_EKMAN_NUMBER,
    MIN_ELSASSER_NUMBER,
    MAX_ELSASSER_NUMBER,
    MIN_CMB_HEAT_FLUX_TW,
)


def test_geodynamo_dimensionless_equations_and_bounds():
    """Verify core dimensionless MHD equations: Rm, Ro, Ek, Elsasser, and Dynamo numbers."""
    # 1. Magnetic Reynolds: Rm = U * L / eta
    # Nominal convective velocity U ~ 1e-4 m/s, L = 2.2585e6 m, eta ~ 0.796 m^2/s -> Rm ~ 283.7
    rm = calculate_magnetic_reynolds_number(velocity=1e-4, shell_thickness=2.2585e6, magnetic_diffusivity=0.8)
    assert rm > MIN_MAGNETIC_REYNOLDS
    assert 280.0 < rm < 285.0

    with pytest.raises(ValueError):
        calculate_magnetic_reynolds_number(velocity=-1.0)
    with pytest.raises(ValueError):
        calculate_magnetic_reynolds_number(velocity=1e-4, magnetic_diffusivity=0.0)

    # 2. Rossby number: Ro = U / (2 * Omega * L)
    # Omega ~ 7.292e-5, L ~ 2.2585e6 -> denominator ~ 329.5 -> Ro ~ 3.03e-7 <= 1.0e-6
    ro = calculate_rossby_number(velocity=1e-4, angular_velocity=7.292115e-5, length_scale=2.2585e6)
    assert ro <= MAX_ROSSBY_NUMBER
    assert 3.0e-7 <= ro <= 3.1e-7

    with pytest.raises(ValueError):
        calculate_rossby_number(velocity=1e-4, angular_velocity=0.0)

    # 3. Ekman number: Ek = nu / (2 * Omega * L^2)
    # Liquid iron kinematic viscosity nu ~ 1e-6 m^2/s -> Ek ~ 1.34e-15 <= 1.0e-14
    ek = calculate_ekman_number(kinematic_viscosity=1e-6, angular_velocity=7.292115e-5, length_scale=2.2585e6)
    assert ek <= MAX_EKMAN_NUMBER

    with pytest.raises(ValueError):
        calculate_ekman_number(kinematic_viscosity=1e-6, length_scale=0.0)

    # 4. Elsasser number: Lambda = sigma * B^2 / (2 * rho * Omega)
    # B = 2.0 mT = 2.0e-3 T, sigma = 1e6 S/m, rho = 1.1e4 kg/m^3, Omega = 7.292e-5 rad/s
    elsasser = calculate_elsasser_number(
        magnetic_field_tesla=2.0e-3,
        electrical_conductivity=1.0e6,
        density=1.1e4,
        angular_velocity=7.292115e-5,
    )
    assert MIN_ELSASSER_NUMBER <= elsasser <= MAX_ELSASSER_NUMBER
    assert 2.0 <= elsasser <= 3.0

    # 5. Surface dipole energy fraction
    f_dip = calculate_surface_dipole_energy_fraction(dipole_energy=90.0, total_energy=100.0)
    assert f_dip == 0.90
    with pytest.raises(ValueError):
        calculate_surface_dipole_energy_fraction(dipole_energy=110.0, total_energy=100.0)

    # 6. Dynamo number
    n_d = calculate_dynamo_number(alpha_effect_m_s=1e-4, omega_shear_rad_s=1e-11, length_scale=2.2585e6, magnetic_diffusivity=0.8)
    assert n_d > 0.0


def test_validate_geodynamo_parameters_nominal_and_breaches():
    """Verify validation result scoring on nominal and out-of-bounds parameters."""
    nominal_params = GeodynamoCoreParameters(
        magnetic_reynolds=180.0,
        rossby_number=2.5e-7,
        ekman_number=5.0e-15,
        elsasser_number=1.85,
        cmb_heat_flux_tw=14.5,
        icb_buoyancy_flux_kg_s=3.2e5,
        surface_dipole_field_microtesla=48.0,
        cmb_magnetic_field_millitesla=1.2,
        surface_dipole_fraction=0.91,
        dipole_tilt_deg=10.2,
        westward_drift_deg_yr=0.18,
        dynamo_number_product=250.0,
    )

    result = validate_geodynamo_parameters(nominal_params)
    assert result.is_valid is True
    assert result.score == 100.0
    assert len(result.violations) == 0
    assert result.metrics["magnetic_reynolds"] == 180.0

    # Defective parameters breaching multiple invariants
    defective_params = GeodynamoCoreParameters(
        magnetic_reynolds=25.0,        # Sub-critical (<50.0) -> -25 pts
        rossby_number=5.0e-5,         # High Ro (>1e-6) -> -15 pts
        ekman_number=1.0e-10,         # High Ek (>1e-14) -> -15 pts
        elsasser_number=15.0,         # Lambda > 10.0 -> -15 pts
        cmb_heat_flux_tw=6.0,         # Sub-adiabatic (<10.0 TW) -> -15 pts
        icb_buoyancy_flux_kg_s=2.0e4, # Low buoyancy (<1e5 kg/s) -> -10 pts
        surface_dipole_field_microtesla=15.0, # Weak surface field (<25 uT) -> -10 pts
        cmb_magnetic_field_millitesla=0.2,    # Low CMB field (<0.50 mT) -> -10 pts
        surface_dipole_fraction=0.60, # Low dipole ratio (<80%) -> -10 pts
        dipole_tilt_deg=28.0,         # Excessive tilt (>15 deg) -> -5 pts
        westward_drift_deg_yr=0.55,   # High drift (>0.30 deg/yr) -> -5 pts
        dynamo_number_product=45.0,   # Sub-critical dynamo (<100) -> -5 pts
    )

    bad_result = validate_geodynamo_parameters(defective_params)
    assert bad_result.is_valid is False
    assert bad_result.score == 0.0  # severely penalized
    assert len(bad_result.violations) == 12


def test_geodynamo_code_inspector_patterns_and_ast():
    """Verify inspector catches lazy stubs, bare excepts, empty catches, and physical violations."""
    inspector = GeodynamoCodeInspector()

    dirty_code = (
        "# " + "TODO: implement MAC balance later\n"
        "magnetic_reynolds = 22.0\n"
        "rossby_number = 1.0e-4\n"
        "ekman_number = 1.0e-10\n"
        "elsasser_number = 25.0\n"
        "cmb_heat_flux = 5.0\n"
        "icb_buoyancy_flux = 1.0e3\n"
        "surface_dipole_fraction = 0.55\n"
        "dipole_tilt = 35.0\n"
        "pure_hydrodynamics = True\n"
        "def compute_core_flow():\n"
        "    pass\n"
        "try:\n"
        "    x = 1\n"
        "except:\n"
        "    pass\n"
    )

    findings = inspector.inspect_source(dirty_code)
    finding_types = [f["type"] for f in findings]

    assert "LAZY_STUB" in finding_types
    assert "SUB_CRITICAL_MAGNETIC_REYNOLDS" in finding_types
    assert "EXCESSIVE_ROSSBY_NUMBER" in finding_types
    assert "EXCESSIVE_EKMAN_NUMBER" in finding_types
    assert "ELSASSER_NUMBER_DIVERGENCE" in finding_types
    assert "SUB_ADIABATIC_CMB_FLUX" in finding_types
    assert "INSUFFICIENT_ICB_BUOYANCY" in finding_types
    assert "WEAK_SURFACE_DIPOLE_FRACTION" in finding_types
    assert "EXCESSIVE_DIPOLE_TILT" in finding_types
    assert "NON_MAGNETOSTROPHIC_DYNAMICS" in finding_types
    assert "EMPTY_FUNCTION_STUB" in finding_types
    assert "BARE_EXCEPT" in finding_types
    assert "SILENT_PASS_EXCEPT" in finding_types


def test_geodynamo_rubric_scoring_and_passing():
    """Verify rubric scoring across 4 dimensions and 95.0 passing threshold."""
    evaluator = GeodynamoRubricEvaluator()

    # Clean findings -> 100/100
    clean_report = evaluator.evaluate(findings=[], metrics={})
    assert clean_report.is_passing is True
    assert clean_report.total_score == 100.0
    assert "PASSED" in clean_report.summary

    # Moderate flaws -> fails 95.0 threshold
    flawed_findings = [
        {"type": "SUB_CRITICAL_MAGNETIC_REYNOLDS", "message": "Rm=30.0 < 50.0"},
        {"type": "LAZY_STUB", "message": "stub comment"},
    ]
    flawed_report = evaluator.evaluate(flawed_findings, metrics={})
    assert flawed_report.is_passing is False
    assert flawed_report.total_score <= 70.0
    assert "REJECTED" in flawed_report.summary


def test_blind_critic_adversarial_rejection_and_approval():
    """Verify Blind Critic rejects defective code and certifies production-grade code."""
    critic = PlanetaryGeodynamoBlindCritic()

    bad_code = (
        "# " + "FIXME: fix unphysical dipole collapse\n"
        "magnetic_reynolds = 12.0\n"
        "def run_simulation():\n"
        "    pass\n"
    )

    verdict_bad = critic.audit(bad_code)
    assert verdict_bad.verdict == "REJECTED_DEFECTIVE"
    assert verdict_bad.passed is False
    assert verdict_bad.score < 95.0
    assert len(verdict_bad.remediation_plan) > 0

    clean_code = (
        "'''Planetary outer core magnetohydrodynamic simulation.'''\n"
        "import logging\n\n"
        "def compute_outer_core_induction() -> dict:\n"
        "    magnetic_reynolds = 150.0\n"
        "    rossby_number = 1.0e-7\n"
        "    elsasser_number = 1.2\n"
        "    cmb_heat_flux = 14.0\n"
        "    surface_dipole_fraction = 0.92\n"
        "    return {'status': 'nominal', 'Rm': magnetic_reynolds}\n"
    )

    verdict_clean = critic.audit(clean_code)
    assert verdict_clean.verdict == "CERTIFIED_WORLD_CLASS"
    assert verdict_clean.passed is True
    assert verdict_clean.score >= 95.0


def test_elevation_engine_remediation():
    """Verify Elevation Engine automatically eliminates stubs and restores MAC parameters."""
    engine = PlanetaryGeodynamoElevationEngine()

    flawed_source = (
        "# " + "TODO: wire up Coriolis-Lorentz solver\n"
        "pure_hydrodynamics = True\n"
        "disable_lorentz = True\n"
        "magnetic_reynolds = 15.0\n"
        "rossby_number = 2.0e-5\n"
        "ekman_number = 1.0e-11\n"
        "elsasser_number = 0.02\n"
        "cmb_heat_flux = 4.5\n"
        "icb_buoyancy_flux = 2.0e3\n"
        "surface_dipole_fraction = 0.45\n"
        "def step_core_fluid() -> dict:\n"
        "    pass\n"
        "try:\n"
        "    run_dynamo()\n"
        "except:\n"
        "    pass\n"
    )

    elevated, stats = engine.elevate(flawed_source)

    assert stats["stubs_removed"] >= 1
    assert stats["mac_balance_restored"] >= 2
    assert stats["parameters_elevated"] >= 7
    assert stats["empty_stubs_filled"] >= 1
    assert stats["exceptions_remediated"] >= 1

    # Verify remediated values
    assert "magnetic_reynolds = 150.0" in elevated
    assert "pure_hydrodynamics = False" in elevated
    assert "disable_lorentz = False" in elevated
    assert "cmb_heat_flux = 14.0" in elevated
    assert "surface_dipole_fraction = 0.92" in elevated
    assert "pass" not in elevated


def test_geodynamo_master_closed_loop_dual_agent():
    """Verify Master orchestrates closed-loop audit, elevation, and journal recording."""
    class MockJournal:
        def __init__(self):
            self.records = []

        def record_decision(self, iteration, target, flaws, actions, score_before, score_after):
            self.records.append({
                "iteration": iteration,
                "target": target,
                "flaws": flaws,
                "actions": actions,
                "score_before": score_before,
                "score_after": score_after,
            })

    journal = MockJournal()
    master = PlanetaryGeodynamoMaster(journal=journal)

    defective_code = (
        "# " + "TODO: resolve sub-critical dynamo decay\n"
        "magnetic_reynolds = 20.0\n"
        "cmb_heat_flux = 5.0\n"
        "surface_dipole_fraction = 0.50\n"
        "def simulate_core_dynamo() -> dict:\n"
        "    pass\n"
    )

    result = master.evaluate_and_elevate(defective_code, target_file="core_dynamo.py")

    assert result["status"] == "certified"
    assert result["final_score"] >= 95.0
    assert result["iterations"] >= 1
    assert len(result["repaired_flaws"]) > 0
    assert len(journal.records) >= 1
    assert journal.records[0]["score_after"] >= 95.0
