"""Unit tests for Dr. Julian 'The Accelerator' Vance — Particle Accelerator & Relativistic Beam Dynamics Master.

Validates the complete 7-step autonomous craftsmanship standard for Domain Master #32.
"""

import pytest
from professions.particle_accelerator_architect.references import (
    AcceleratorReferenceLibrary,
    RelativisticBeamState,
    TwissLatticeState,
    SuperconductingCavityState,
    MachineProtectionState,
    calculate_lorentz_gamma,
    calculate_magnetic_rigidity,
    calculate_twiss_gamma,
    PROTON_REST_MASS_GEV,
)
from professions.particle_accelerator_architect.inspector import AcceleratorInspector
from professions.particle_accelerator_architect.rubric import AcceleratorRubric
from professions.particle_accelerator_architect.blind_critic import AcceleratorBlindCritic
from professions.particle_accelerator_architect.elevation_engine import AcceleratorElevationEngine
from professions.particle_accelerator_architect.master import JulianVanceMaster, AcceleratorMaster


def test_relativistic_beam_state_and_rigidity():
    """Validates 7 TeV proton relativistic Lorentz factor and magnetic rigidity."""
    energy_gev = 7000.0  # 7 TeV
    gamma = calculate_lorentz_gamma(energy_gev, PROTON_REST_MASS_GEV)
    assert gamma > 7400.0

    rigidity = calculate_magnetic_rigidity(energy_gev, PROTON_REST_MASS_GEV)
    assert rigidity > 23000.0  # B*rho > 23,000 T*m

    beam = RelativisticBeamState(
        rest_mass_gev=PROTON_REST_MASS_GEV,
        total_energy_gev=energy_gev,
        lorentz_gamma=gamma,
        relativistic_beta=0.99999999,
        magnetic_rigidity_t_m=rigidity,
        bunch_intensity_protons=1.15e11
    )
    assert beam.is_ultra_relativistic() is True

    # Classical non-relativistic state
    classical_beam = RelativisticBeamState(
        rest_mass_gev=PROTON_REST_MASS_GEV,
        total_energy_gev=0.95,
        lorentz_gamma=1.01,
        relativistic_beta=0.15,
        magnetic_rigidity_t_m=0.5,
        bunch_intensity_protons=1e9
    )
    assert classical_beam.is_ultra_relativistic() is False


def test_twiss_parameters_and_symplecticity():
    """Validates Courant-Snyder Twiss parameters and symplectic invariant relation."""
    # beta = 50.0m, alpha = -1.5 => gamma_cs = (1 + 2.25) / 50 = 0.065
    gamma_cs = calculate_twiss_gamma(beta_m=50.0, alpha=-1.5)
    assert pytest.approx(gamma_cs, rel=1e-3) == 0.065

    # Safe symplectic lattice state
    lattice = TwissLatticeState(
        beta_m=50.0,
        alpha=-1.5,
        gamma_cs=gamma_cs,
        horizontal_tune_nux=64.12,
        vertical_tune_nuy=59.18,
        emittance_m_rad=3.5e-10
    )
    assert lattice.is_symplectic_valid() is True

    # Non-symplectic invalid state
    invalid_lattice = TwissLatticeState(
        beta_m=50.0,
        alpha=-1.5,
        gamma_cs=0.100,  # Violates beta * gamma - alpha^2 == 1
        horizontal_tune_nux=64.12,
        vertical_tune_nuy=59.18,
        emittance_m_rad=3.5e-10
    )
    assert invalid_lattice.is_symplectic_valid() is False


def test_betatron_tune_resonance_avoidance():
    """Validates betatron tune resonance avoidance against integer and fractional stopbands."""
    # Safe working point: frac_x = 0.12, frac_y = 0.18 (gap to 0.0 is 0.12 >= 0.05, gap to 0.25 is 0.07 >= 0.05)
    safe_lattice = TwissLatticeState(
        beta_m=20.0,
        alpha=0.0,
        gamma_cs=0.05,
        horizontal_tune_nux=64.12,
        vertical_tune_nuy=59.18,
        emittance_m_rad=2.5e-10
    )
    safe, reasons = safe_lattice.is_resonance_safe(min_margin=0.05)
    assert safe is True
    assert len(reasons) == 0

    # Unsafe working point: frac_x = 0.51 (dangerously close to 1/2 resonance at 0.50)
    unsafe_lattice = TwissLatticeState(
        beta_m=20.0,
        alpha=0.0,
        gamma_cs=0.05,
        horizontal_tune_nux=64.51,
        vertical_tune_nuy=59.33,  # Dangerously close to 1/3 resonance at 0.333
        emittance_m_rad=2.5e-10
    )
    safe, reasons = unsafe_lattice.is_resonance_safe(min_margin=0.05)
    assert safe is False
    assert any("resonance" in r for r in reasons)


def test_superconducting_cavity_quench_protection():
    """Validates superconducting RF cavity cryogenic limits and fast quench trip latency."""
    # Safe SRF cavity: 1.8K (superfluid He), 32 MV/m, Q0 = 2e10, 6us trip
    safe_cavity = SuperconductingCavityState(
        frequency_mhz=1300.0,
        accelerating_gradient_mv_m=32.0,
        quality_factor_q0=2.0e10,
        cavity_temperature_k=1.80,
        quench_trip_time_us=6.0,
        is_quenched=False
    )
    assert safe_cavity.is_cavity_safe() is True

    # Compromised cavity: 2.5K (above superfluid lambda point) and sluggish trip
    unsafe_cavity = SuperconductingCavityState(
        frequency_mhz=1300.0,
        accelerating_gradient_mv_m=20.0,
        quality_factor_q0=5.0e9,
        cavity_temperature_k=2.50,
        quench_trip_time_us=25.0,
        is_quenched=True
    )
    assert unsafe_cavity.is_cavity_safe() is False


def test_accelerator_inspector_and_rubric():
    """Validates static AST inspection and 100-point rubric on canonical accelerator core."""
    canonical_code = AcceleratorReferenceLibrary.get_canonical_core()
    metrics = AcceleratorInspector.inspect(canonical_code)

    assert metrics["ast_valid"] is True
    assert metrics["has_relativistic_kinematics"] is True
    assert metrics["has_tune_resonance_guard"] is True
    assert metrics["has_cavity_quench_check"] is True
    assert metrics["has_telemetry_eval"] is True
    assert metrics["has_kicker_dump_abort"] is True
    assert metrics["has_fatal_defects"] is False

    score, breakdown, passed, veto_reason = AcceleratorRubric.evaluate(metrics)
    assert score >= 85.0
    assert passed is True
    assert veto_reason == ""
    assert breakdown["betatron_tune"] == 25.0
    assert breakdown["code_determinism"] == 15.0


def test_blind_critic_catches_flaws():
    """Validates adversarial blind critic identifying tune resonance hazard and stubs."""
    flawed_code = '''
def particle_beam_controller(tune):
    # Weak tune margin and high cavity temp
    min_tune_margin = 0.01
    max_cavity_temp_k = 4.2
    max_quench_latency_us = 80.0
    # TODO: implement fast kicker dump magnet
    raise NotImplementedError("kicker dump not wired")
'''
    critique = AcceleratorBlindCritic.evaluate(flawed_code)
    assert critique["verdict"] == "REJECT"
    assert critique["passed"] is False
    assert critique["fatal_defects_count"] > 0
    assert any("Substandard betatron tune" in d["description"] for d in critique["defect_ledger"])


def test_elevation_engine_and_master_closed_loop():
    """Validates closed-loop elevation of flawed accelerator code and master certification."""
    flawed_code = '''
def beam_optics(tune):
    min_tune_margin = 0.02
    max_cavity_temp_k = 3.5
    # TODO: add quench protection
    return tune
'''
    elevation = AcceleratorElevationEngine.elevate(flawed_code, target_score=85)
    assert elevation["passed"] is True
    assert elevation["final_score"] >= 85.0
    assert "ParticleBeamExecutive" in elevation["elevated_code"] or "min_tune_margin = 0.05" in elevation["elevated_code"]

    master = JulianVanceMaster()
    result = master.run_autonomous_cycle()

    assert result["status"] == "CERTIFIED"
    assert result["is_certified"] is True
    assert result["final_score"] >= 85.0
    assert result["verdict"] == "APPROVED"
    assert "DR. JULIAN VANCE — EXECUTIVE PARTICLE ACCELERATOR BRIEFING" in result["executive_briefing"]
