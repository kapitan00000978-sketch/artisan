"""Unit tests for Dr. Seraphiel 'The SynBio' Sterling — Synthetic Biology & Genetic Circuit Master.

Validates the complete 7-step autonomous craftsmanship standard for Domain Master #33.
"""

import pytest
from professions.synthetic_biology_architect.references import (
    SynBioReferenceLibrary,
    HillKineticsState,
    MetabolicBurdenState,
    OrthogonalRegulonState,
    BiocontainmentState,
    calculate_hill_repression,
    calculate_dynamic_range,
    evaluate_metabolic_burden,
)
from professions.synthetic_biology_architect.inspector import SynBioInspector
from professions.synthetic_biology_architect.rubric import SynBioRubric
from professions.synthetic_biology_architect.blind_critic import SynBioBlindCritic
from professions.synthetic_biology_architect.elevation_engine import SynBioElevationEngine
from professions.synthetic_biology_architect.master import SeraphielSterlingMaster, SynBioMaster


def test_hill_kinetics_and_transfer_functions():
    """Validates Hill repression transfer function and non-linear cooperativity."""
    # Vmax = 1000, Kd = 10, n = 2.5, basal = 5.0
    # At I = 0: f(0) = 5 + 1000 = 1005
    rep_0 = calculate_hill_repression(0.0, vmax=1000.0, kd=10.0, n=2.5, basal=5.0)
    assert rep_0 == 1005.0

    # At I = 100 (I >> Kd): f(100) approx basal (5.0)
    rep_high = calculate_hill_repression(100.0, vmax=1000.0, kd=10.0, n=2.5, basal=5.0)
    assert rep_high < 10.0

    # Robust bistable switch state
    safe_kinetics = HillKineticsState(
        max_expression_au=1200.0,
        kd_umolar=8.5,
        hill_coefficient_n=2.6,
        basal_expression_au=12.0,
        dynamic_range_ratio=100.0
    )
    assert safe_kinetics.is_kinetics_robust() is True

    # Flawed low-cooperativity state (noisy state-flipping)
    noisy_kinetics = HillKineticsState(
        max_expression_au=500.0,
        kd_umolar=15.0,
        hill_coefficient_n=1.1,
        basal_expression_au=95.0,
        dynamic_range_ratio=5.26
    )
    assert noisy_kinetics.is_kinetics_robust() is False


def test_cellular_metabolic_burden_budget():
    """Validates composite metabolic burden index against host translation capacity."""
    # Ribosome allocation = 20%, ATP drain = 15% => Burden = 0.6*0.2 + 0.4*0.15 = 0.18 <= 0.30
    burden = evaluate_metabolic_burden(ribosome_fraction=0.20, atp_fraction=0.15)
    assert pytest.approx(burden, rel=1e-3) == 0.18

    # Sustainable burden state
    safe_burden = MetabolicBurdenState(
        ribosome_allocation_fraction=0.20,
        atp_drain_fraction=0.15,
        total_burden_fraction=burden,
        host_growth_rate_ratio=0.88
    )
    assert safe_burden.is_burden_sustainable() is True

    # Catastrophic burden provoking evolutionary mutational escape
    lethal_burden = MetabolicBurdenState(
        ribosome_allocation_fraction=0.55,
        atp_drain_fraction=0.40,
        total_burden_fraction=0.49,
        host_growth_rate_ratio=0.35
    )
    assert lethal_burden.is_burden_sustainable() is False


def test_orthogonal_regulon_and_crosstalk():
    """Validates host transcriptome crosstalk isolation and translation fidelity."""
    # Clean orthogonal regulon: 1.5% crosstalk, 99.1% fidelity
    safe_regulon = OrthogonalRegulonState(
        promoter_identity="P_T7_orthogonal",
        transcription_factor="T7_RNAP_mutant_V3",
        host_crosstalk_fraction=0.015,
        translation_fidelity_pct=99.1
    )
    assert safe_regulon.is_orthogonal_clean() is True

    # Leaky regulon cross-activating host sigma factors
    leaky_regulon = OrthogonalRegulonState(
        promoter_identity="P_lac_wildtype",
        transcription_factor="LacI",
        host_crosstalk_fraction=0.14,
        translation_fidelity_pct=88.5
    )
    assert leaky_regulon.is_orthogonal_clean() is False


def test_biocontainment_and_kill_switches():
    """Validates NIH recombinant DNA escape frequency bounds and dual-layer suicide switches."""
    # Secure containment: non-canonical amino acid auxotrophy + Cas3 kill switch (escape 4e-9 <= 1e-8)
    safe_containment = BiocontainmentState(
        synthetic_auxotrophy_nutrient="Biphenylalanine (Bpa)",
        suicide_switch_mechanism="CRISPR_Cas3_genome_shredder",
        measured_escape_frequency=4.0e-9,
        kill_switch_latency_min=18.5,
        is_dual_layer_contained=True
    )
    assert safe_containment.is_containment_secure() is True

    # Dangerous uncontained strain
    hazardous_containment = BiocontainmentState(
        synthetic_auxotrophy_nutrient="None",
        suicide_switch_mechanism="Single_Toxin_MazF",
        measured_escape_frequency=2.5e-5,
        kill_switch_latency_min=120.0,
        is_dual_layer_contained=False
    )
    assert hazardous_containment.is_containment_secure() is False


def test_synbio_inspector_and_rubric():
    """Validates static AST inspection and 100-point rubric on canonical synthetic biology core."""
    canonical_code = SynBioReferenceLibrary.get_canonical_core()
    metrics = SynBioInspector.inspect(canonical_code)

    assert metrics["ast_valid"] is True
    assert metrics["has_hill_kinetics"] is True
    assert metrics["has_metabolic_burden_calc"] is True
    assert metrics["has_crosstalk_check"] is True
    assert metrics["has_telemetry_eval"] is True
    assert metrics["has_suicide_kill_switch"] is True
    assert metrics["has_fatal_defects"] is False

    score, breakdown, passed, veto_reason = SynBioRubric.evaluate(metrics)
    assert score >= 85.0
    assert passed is True
    assert veto_reason == ""
    assert breakdown["biocontainment"] == 25.0
    assert breakdown["code_determinism"] == 15.0


def test_blind_critic_catches_flaws():
    """Validates adversarial blind critic identifying biocontainment hazard and stubs."""
    flawed_code = '''
def genetic_circuit_controller(input_signal):
    # Shallow Hill kinetics and catastrophic escape frequency
    min_hill_n = 1.1
    max_burden_limit = 0.65
    max_escape_freq = 1.0e-4
    # TODO: add dual-layer CRISPR kill switch
    raise NotImplementedError("biocontainment kill switch not wired")
'''
    critique = SynBioBlindCritic.evaluate(flawed_code)
    assert critique["verdict"] == "REJECT"
    assert critique["passed"] is False
    assert critique["fatal_defects_count"] > 0
    assert any("Biocontainment escape frequency" in d["description"] for d in critique["defect_ledger"])


def test_elevation_engine_and_master_closed_loop():
    """Validates closed-loop elevation of flawed synbio code and master certification."""
    flawed_code = '''
def genetic_logic_gate(input_conc):
    min_hill_n = 1.2
    max_burden_limit = 0.50
    # TODO: add auxotrophy and biocontainment
    return input_conc
'''
    elevation = SynBioElevationEngine.elevate(flawed_code, target_score=85)
    assert elevation["passed"] is True
    assert elevation["final_score"] >= 85.0
    assert "SynBioAutonomyExecutive" in elevation["elevated_code"] or "min_hill_n = 2.5" in elevation["elevated_code"]

    master = SeraphielSterlingMaster()
    result = master.run_autonomous_cycle()

    assert result["status"] == "CERTIFIED"
    assert result["is_certified"] is True
    assert result["final_score"] >= 85.0
    assert result["verdict"] == "APPROVED"
    assert "DR. SERAPHIEL STERLING — EXECUTIVE SYNTHETIC BIOLOGY BRIEFING" in result["executive_briefing"]
