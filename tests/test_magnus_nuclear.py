"""Unit tests for Dr. Magnus 'The Core' Sterling — Nuclear Reactor Physics & Criticality Safety Master.

Validates the complete 7-step autonomous craftsmanship standard for Domain Master #28.
"""

import pytest
from professions.nuclear_criticality_architect.references import (
    NuclearReferenceLibrary,
    DelayedPrecursorGroup,
    ReactivityState,
    PointReactorKineticsSolver,
    ThermalHydraulicsSafety,
    ControlRodBank,
    BETA_EFF_U235,
    MIN_DNBR_THRESHOLD,
    MAX_SCRAM_INSERTION_TIME_SEC,
)
from professions.nuclear_criticality_architect.inspector import NuclearCriticalityInspector
from professions.nuclear_criticality_architect.rubric import NuclearCriticalityRubric
from professions.nuclear_criticality_architect.blind_critic import NuclearCriticalityBlindCritic
from professions.nuclear_criticality_architect.elevation_engine import NuclearCriticalityElevationEngine
from professions.nuclear_criticality_architect.master import MagnusSterlingMaster


def test_reactivity_and_prompt_criticality_physics():
    """Validates reactivity calculations, dollar units, and prompt critical checks."""
    # Critical state: keff = 1.0 => reactivity = 0.0$
    critical_state = ReactivityState(keff=1.0, doppler_coeff_pcm_k=-2.5)
    assert critical_state.reactivity() == 0.0
    assert critical_state.reactivity_dollars() == 0.0
    assert critical_state.is_prompt_critical() is False
    safe, reasons = critical_state.is_passively_safe()
    assert safe is True
    assert len(reasons) == 0

    # Prompt critical state: rho >= beta_eff => >= 1.00$
    # If beta_eff = 0.0065, keff = 1 / (1 - 0.0065) ~= 1.00654
    prompt_state = ReactivityState(keff=1.0080, doppler_coeff_pcm_k=-2.0)
    assert prompt_state.reactivity_dollars() > 1.00
    assert prompt_state.is_prompt_critical() is True
    safe, reasons = prompt_state.is_passively_safe()
    assert safe is False
    assert any("Prompt critical" in r for r in reasons)


def test_prke_kinetics_solver_step():
    """Validates 6-group delayed neutron PRKE solver equilibrium and transient stepping."""
    solver = PointReactorKineticsSolver(beta_eff=BETA_EFF_U235)
    assert len(solver.precursor_groups) == 6

    # Steady state equilibrium
    n0 = 1.0e12  # neutrons / cm^3
    precursors0 = solver.equilibrium_precursors(n0)
    assert len(precursors0) == 6
    assert all(c > 0.0 for c in precursors0)

    # Step at zero reactivity (rho = 0) -> power should remain constant
    n1, precursors1 = solver.step(dt_sec=0.01, neutron_density=n0, precursors=precursors0, reactivity=0.0)
    assert pytest.approx(n1, rel=1e-3) == n0
    assert pytest.approx(precursors1[0], rel=1e-3) == precursors0[0]

    # Step with small positive reactivity insertion ($0.10)
    rho_small = 0.10 * BETA_EFF_U235
    n2, precursors2 = solver.step(dt_sec=0.05, neutron_density=n0, precursors=precursors0, reactivity=rho_small)
    assert n2 > n0


def test_thermal_dnbr_safety_margin():
    """Validates Departure from Nucleate Boiling Ratio (DNBR >= 1.30) calculations."""
    safe_thermal = ThermalHydraulicsSafety(
        local_heat_flux_kw_m2=1000.0,
        critical_heat_flux_kw_m2=1500.0,
    )
    assert pytest.approx(safe_thermal.dnbr(), rel=1e-3) == 1.50
    assert safe_thermal.is_thermal_margin_acceptable(min_threshold=1.30) is True

    unsafe_thermal = ThermalHydraulicsSafety(
        local_heat_flux_kw_m2=1200.0,
        critical_heat_flux_kw_m2=1400.0,  # DNBR = 1400 / 1200 = 1.166 < 1.30
    )
    assert unsafe_thermal.dnbr() < 1.30
    assert unsafe_thermal.is_thermal_margin_acceptable(min_threshold=1.30) is False


def test_scram_control_rod_insertion():
    """Validates emergency SCRAM insertion times and stuck rod margin."""
    fast_rod = ControlRodBank(bank_name="Bank_A", worth_pcm=2000.0, insertion_time_sec=2.1, is_stuck=False)
    assert fast_rod.can_scram_within_limit() is True

    slow_rod = ControlRodBank(bank_name="Bank_B", worth_pcm=2000.0, insertion_time_sec=3.2, is_stuck=False)
    assert slow_rod.can_scram_within_limit() is False

    stuck_rod = ControlRodBank(bank_name="Bank_C", worth_pcm=2500.0, insertion_time_sec=1.5, is_stuck=True)
    assert stuck_rod.can_scram_within_limit() is False


def test_inspector_and_rubric_evaluation():
    """Validates nuclear inspector AST analysis, comment stripping, and 100-point rubric."""
    canonical_code = NuclearReferenceLibrary.get_canonical_core()
    metrics = NuclearCriticalityInspector.inspect(canonical_code)

    assert metrics["ast_valid"] is True
    assert metrics["has_prke_kinetics"] is True
    assert metrics["has_reactivity_dollars"] is True
    assert metrics["has_doppler_feedback"] is True
    assert metrics["has_dnbr_safety"] is True
    assert metrics["has_scram_control"] is True
    assert metrics["has_positive_doppler_hazard"] is False

    score, breakdown, passed, veto_reason = NuclearCriticalityRubric.evaluate(metrics)
    assert score >= 85
    assert passed is True
    assert veto_reason == ""


def test_veto_on_positive_doppler_and_prompt_critical():
    """Validates immediate veto on positive Doppler coefficient or prompt critical runaway."""
    bad_code = "doppler_pcm_k = 2.5 # positive feedback hazard"
    bad_metrics = NuclearCriticalityInspector.inspect(bad_code)
    score, _, passed, veto_reason = NuclearCriticalityRubric.evaluate(bad_metrics)
    assert passed is False
    assert "ChernobylHazard" in veto_reason or "KineticsDeficit" in veto_reason


def test_blind_critic_elevation_and_master():
    """Validates blind critique defect ledger, elevation engine remediation, and master runner."""
    flawed_code = '''
def run_reactor(power):
    doppler_pcm_k = 1.5
    # TODO: implement SCRAM
    return power
'''
    critique = NuclearCriticalityBlindCritic.evaluate(flawed_code)
    assert critique["verdict"] == "REJECTED"
    assert critique["fatal_defects_count"] > 0

    elevation = NuclearCriticalityElevationEngine.elevate(flawed_code, target_score=85)
    assert elevation["passed"] is True
    assert elevation["final_score"] >= 85
    assert "PointReactorKineticsSolver" in elevation["elevated_code"]

    master = MagnusSterlingMaster()
    result = master.run_autonomous_cycle()

    assert result["status"] == "CERTIFIED"
    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert result["verdict"] == "APPROVED"
    assert "EXECUTIVE NUCLEAR SAFETY BRIEFING" in result["executive_briefing"]
