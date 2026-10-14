"""
Unit tests for Victor Montgomery (Startup Fractional CFO & Capital Defense Subsystem).
"""

import pytest
from professions.fractional_cfo_analyst.references import FinancialReferenceLibrary
from professions.fractional_cfo_analyst.inspector import FinancialInspector
from professions.fractional_cfo_analyst.rubric import FinancialRubric
from professions.fractional_cfo_analyst.blind_critic import BlindFinancialCritic
from professions.fractional_cfo_analyst.elevation_engine import FinancialElevationEngine
from professions.fractional_cfo_analyst.master import VictorMontgomeryMaster


def test_victor_references_loading():
    benchmarks = FinancialReferenceLibrary.get_saas_benchmarks()
    assert "gross_margin" in benchmarks
    assert "ltv_cac_ratio" in benchmarks
    assert "cac_payback_months" in benchmarks
    assert benchmarks["gross_margin"]["target"] >= 0.80

    tiers = FinancialReferenceLibrary.get_runway_tiers()
    assert "insolvency_crisis" in tiers
    assert "fortress" in tiers
    assert FinancialReferenceLibrary.evaluate_runway_tier(2.0) == "insolvency_crisis"
    assert FinancialReferenceLibrary.evaluate_runway_tier(24.0) == "fortress"


def test_victor_inspector_fortress_model():
    inspector = FinancialInspector()
    fortress_data = {
        "mrr": 100000,
        "cogs": 18000,
        "cogs_breakdown": ["aws_cloud_hosting", "tier_1_customer_support", "stripe_fees"],
        "sm_expense": 40000,
        "new_customers": 50,
        "arpu": 2000,
        "churn_rate": 0.05,
        "cash": 2500000,
        "opex": 120000,
        "has_sensitivity_scenarios": True
    }
    report = inspector.inspect(fortress_data)
    assert report.is_financially_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.gross_margin_pct >= 0.80
    assert report.metrics.ltv_cac_ratio >= 4.0
    assert report.metrics.runway_months >= 18.0


def test_victor_inspector_distressed_model():
    inspector = FinancialInspector()
    distressed_data = {
        "mrr": 30000,
        "cogs": 16000,
        "cogs_breakdown": ["unspecified_misc"],
        "sm_expense": 45000,
        "new_customers": 10,
        "arpu": 300,
        "churn_rate": 0.15,
        "cash": 120000,
        "opex": 90000
    }
    report = inspector.inspect(distressed_data)
    assert report.is_financially_viable is False
    assert len(report.critical_violations) > 0
    # Gross margin is ~46.7%, runway is ~1.5 months
    assert report.metrics.gross_margin_pct < 0.60
    assert report.metrics.runway_months < 3.0


def test_victor_rubric_and_veto():
    inspector = FinancialInspector()
    rubric = FinancialRubric()

    distressed_data = {
        "mrr": 20000,
        "cogs": 12000,
        "cash": 50000,
        "opex": 70000,
        "cac": 3000,
        "arpu": 100,
        "churn_rate": 0.20
    }
    report = inspector.inspect(distressed_data)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) > 0


def test_victor_critic_defect_ledger():
    critic = BlindFinancialCritic()
    distressed_data = {
        "mrr": 40000,
        "cogs": 25000,
        "cash": 80000,
        "opex": 90000,
        "cac": 4000,
        "ltv": 2000
    }
    ledger = critic.review(distressed_data)
    assert ledger.verdict == "REJECTED_UNVIABLE"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count > 0
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_victor_elevation_engine():
    engine = FinancialElevationEngine()
    flawed_data = {
        "mrr": 25000,
        "cogs": 15000,
        "cogs_breakdown": ["miscellaneous"],
        "cash": 100000,
        "opex": 60000,
        "sm_expense": 30000,
        "new_customers": 5,
        "arpu": 500,
        "churn_rate": 0.12
    }
    elevated_result = engine.elevate(flawed_data)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert elevated_result["metrics"].gross_margin_pct >= 0.80
    assert elevated_result["metrics"].runway_months >= 18.0
    assert "austerity_protocol" in elevated_result["elevated_model"]
    assert "scenarios" in elevated_result["elevated_model"]
    assert "bear_case" in elevated_result["elevated_model"]["scenarios"]


def test_victor_master_autonomous_cycle():
    master = VictorMontgomeryMaster(passing_threshold=85)
    unhealthy_input = {
        "mrr": 35000,
        "cogs": 18000,
        "cogs_breakdown": ["contractors"],
        "cash": 150000,
        "opex": 80000,
        "sm_expense": 40000,
        "new_customers": 10,
        "arpu": 800,
        "churn_rate": 0.10
    }
    result = master.run_autonomous_cycle(input_data=unhealthy_input)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE CFO BRIEFING" in result["executive_briefing"]
    assert "FORTRESS CERTIFIED" in result["executive_briefing"]
