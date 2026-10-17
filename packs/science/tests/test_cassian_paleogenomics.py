"""Test suite for Dr. Cassian Sterling - Paleogenomic Ancient DNA Reconstruction Architect.

Covers Briggs deamination kinetics, fragment length decay models, Phred quality conversions,
static and AST inspection, rubric scoring, adversarial criticism, elevation engine,
and master dual-agent closed-loop reflection.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.paleogenomic_ancient_dna_reconstruction_architect import (
    MIN_TERMINAL_DEAMINATION_RATE,
    MIN_FRAGMENT_LENGTH_BP,
    MAX_FRAGMENT_LENGTH_BP,
    MAX_MODERN_CONTAMINATION_RATE,
    MIN_AUTHENTICITY_CONFIDENCE,
    MIN_UDG_REPAIR_EFFICIENCY,
    MIN_SEQUENCING_DEPTH_X,
    MIN_PHRED_QUALITY_SCORE,
    MAX_REFERENCE_MAPPING_BIAS,
    MIN_DAMAGE_LOG_LIKELIHOOD,
    calculate_briggs_deamination_probability,
    calculate_fragment_length_density,
    calculate_phred_error_probability,
    validate_paleogenomic_parameters,
    PaleogenomicInspector,
    PaleogenomicRubric,
    PaleogenomicBlindCritic,
    PaleogenomicElevationEngine,
    PaleogenomicMaster,
)


def test_briggs_deamination_and_fragmentation_models():
    """Verify Briggs deamination decay kinetics and fragment length exponential distributions."""
    # Terminal position (i = 1): P = 0.28 * (1 - 0.30)^0 + 0.03 = 0.31 (31% C->T damage)
    prob_pos1 = calculate_briggs_deamination_probability(1, lambda_param=0.30, delta_s=0.28, delta_d=0.03)
    assert prob_pos1 == pytest.approx(0.31, rel=1e-3)
    assert prob_pos1 >= MIN_TERMINAL_DEAMINATION_RATE

    # Internal position (i = 10): P approaches delta_d = 0.03
    prob_pos10 = calculate_briggs_deamination_probability(10, lambda_param=0.30, delta_s=0.28, delta_d=0.03)
    assert 0.03 <= prob_pos10 <= 0.045

    # Invalid position edge case
    assert calculate_briggs_deamination_probability(0) == 0.0

    # Fragment length density: mean = 48.0 bp, L = 48.0 bp -> (1/48) * exp(-1) ~= 0.00766
    density = calculate_fragment_length_density(48.0, mean_length_bp=48.0)
    assert 0.0070 <= density <= 0.0085

    # Zero length edge case
    assert calculate_fragment_length_density(0.0) == 0.0


def test_phred_error_probability():
    """Verify Phred consensus quality score to base substitution error probability conversion."""
    p_err_q30 = calculate_phred_error_probability(30.0)
    assert p_err_q30 == pytest.approx(1.0e-3, rel=1e-4)

    p_err_q40 = calculate_phred_error_probability(40.0)
    assert p_err_q40 == pytest.approx(1.0e-4, rel=1e-4)

    # Edge cases
    assert calculate_phred_error_probability(0.0) == 1.0


def test_validate_paleogenomic_parameters_nominal_and_breaches():
    """Verify validation dataclass against nominal parameters and boundary breaches."""
    # Nominal case
    res_nominal = validate_paleogenomic_parameters(
        terminal_deamination_rate=0.22,
        mean_fragment_length_bp=48.5,
        modern_contamination_rate=0.005,
        authenticity_confidence=0.9995,
        udg_repair_efficiency=0.97,
        sequencing_depth_x=34.0,
        phred_quality_score=35.0,
        reference_mapping_bias=0.012,
        damage_log_likelihood=14.2
    )
    assert res_nominal.is_valid is True
    assert len(res_nominal.flaws) == 0

    # Breach case: low deamination (0.02), long fragments (120 bp), high contamination (0.05),
    # low confidence (0.95), low UDG (0.80), shallow depth (5x), low Phred (Q15),
    # high mapping bias (0.08), low damage likelihood (2.0)
    res_breach = validate_paleogenomic_parameters(
        terminal_deamination_rate=0.02,
        mean_fragment_length_bp=120.0,
        modern_contamination_rate=0.05,
        authenticity_confidence=0.95,
        udg_repair_efficiency=0.80,
        sequencing_depth_x=5.0,
        phred_quality_score=15.0,
        reference_mapping_bias=0.08,
        damage_log_likelihood=2.0
    )
    assert res_breach.is_valid is False
    assert len(res_breach.flaws) == 9


def test_paleogenomic_inspector_patterns_and_ast():
    """Verify static and AST inspection detects placeholders, deficits, and empty stubs."""
    inspector = PaleogenomicInspector()

    flawed_code = (
        "# TODO: calibrate ancient DNA deamination damage matrix\n"
        "terminal_deamination_rate = 0.04\n"
        "mean_fragment_length_bp = 110.0\n"
        "modern_contamination_rate = 0.045\n"
        "authenticity_confidence = 0.96\n"
        "udg_repair_efficiency = 0.82\n"
        "sequencing_depth_x = 8.0\n"
        "phred_quality_score = 18.0\n"
        "reference_mapping_bias = 0.055\n"
        "damage_log_likelihood = 3.5\n"
        "def map_paleogenomic_reads() -> bool:\n"
        "    pass\n"
        "try:\n"
        "    coverage = 10\n"
        "except Exception:\n"
        "    pass\n"
    )

    flaws = inspector.inspect_source(flawed_code)
    flaw_ids = [f["id"] for f in flaws]

    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "DEAMINATION_RATE_DEFICIT" in flaw_ids
    assert "FRAGMENT_LENGTH_OUT_OF_BOUNDS" in flaw_ids
    assert "CONTAMINATION_RATE_EXCESS" in flaw_ids
    assert "AUTHENTICITY_CONFIDENCE_DEFICIT" in flaw_ids
    assert "UDG_REPAIR_DEFICIT" in flaw_ids
    assert "SEQUENCING_DEPTH_DEFICIT" in flaw_ids
    assert "PHRED_QUALITY_DEFICIT" in flaw_ids
    assert "MAPPING_BIAS_EXCESS" in flaw_ids
    assert "DAMAGE_LIKELIHOOD_DEFICIT" in flaw_ids
    assert "EMPTY_FUNCTION_BODY" in flaw_ids
    assert "EMPTY_EXCEPT_BLOCK" in flaw_ids

    text_flaws = inspector.inspect_code(flawed_code)
    assert len(text_flaws) == len(flaws)


def test_paleogenomic_rubric_scoring_and_passing():
    """Verify objective rubric scoring logic and passing thresholds."""
    rubric = PaleogenomicRubric()

    # Zero flaws -> 100 passed
    eval_pass = rubric.evaluate([])
    assert eval_pass.score == 100
    assert eval_pass.passed is True

    # One CRITICAL flaw (-25 pts) -> 75 rejected
    flaw_crit = [{"id": "CONTAMINATION_RATE_EXCESS", "severity": "CRITICAL", "description": "High modern contamination"}]
    eval_crit = rubric.evaluate(flaw_crit)
    assert eval_crit.score == 75
    assert eval_crit.passed is False

    # One LOW flaw (-3 pts) -> 97 passed
    flaw_low = [{"id": "TELEMETRY_SAMPLE", "severity": "LOW", "description": "Diagnostic sample"}]
    eval_low = rubric.evaluate(flaw_low)
    assert eval_low.score == 97
    assert eval_low.passed is True


def test_blind_critic_adversarial_rejection():
    """Verify blind critic accurately certifies clean paleogenomic code and rejects flawed submissions."""
    critic = PaleogenomicBlindCritic()

    clean_code = (
        "terminal_deamination_rate = 0.22\n"
        "mean_fragment_length_bp = 48.5\n"
        "modern_contamination_rate = 0.005\n"
        "authenticity_confidence = 0.9995\n"
        "udg_repair_efficiency = 0.97\n"
        "sequencing_depth_x = 34.0\n"
        "phred_quality_score = 35.0\n"
        "reference_mapping_bias = 0.012\n"
        "damage_log_likelihood = 14.2\n"
        "def map_paleogenomic_reads() -> bool:\n"
        "    return True\n"
    )

    clean_res = critic.audit(clean_code)
    assert clean_res["verdict"] == "APPROVED"
    assert clean_res["score"] == 100
    assert clean_res["passed"] is True

    flawed_code = (
        "terminal_deamination_rate = 0.01\n"
        "modern_contamination_rate = 0.08\n"
    )
    flawed_res = critic.audit(flawed_code)
    assert flawed_res["verdict"] == "REJECTED"
    assert flawed_res["passed"] is False
    assert flawed_res["score"] < 95


def test_elevation_engine_and_master_closed_loop():
    """Verify autonomous elevation restores code to >=95 standards and master coordinates reflection."""
    engine = PaleogenomicElevationEngine()

    flawed_code = (
        "# TODO: optimize ancient DNA read alignment indexing\n"
        "terminal_deamination_rate = 0.05\n"
        "mean_fragment_length_bp = 105.0\n"
        "modern_contamination_rate = 0.035\n"
        "authenticity_confidence = 0.97\n"
        "udg_repair_efficiency = 0.85\n"
        "sequencing_depth_x = 12.0\n"
        "phred_quality_score = 22.0\n"
        "reference_mapping_bias = 0.045\n"
        "damage_log_likelihood = 4.0\n"
        "def authenticate_ancient_sample() -> dict:\n"
        "    pass\n"
        "try:\n"
        "    depth = 5\n"
        "except ValueError:\n"
        "    pass\n"
    )

    elevated, actions = engine.elevate(flawed_code)
    assert len(actions) > 0

    critic = PaleogenomicBlindCritic()
    audit_after = critic.audit(elevated)
    assert audit_after["passed"] is True
    assert audit_after["score"] >= 95

    # Test master closed-loop execution
    master = PaleogenomicMaster()
    res = master.evaluate_and_elevate(flawed_code, target_file="ancient_dna_reconstruction.py")
    assert res["status"] == "certified"
    assert res["final_score"] >= 95
    assert res["iterations"] >= 1
    assert len(res["repaired_flaws"]) > 0
