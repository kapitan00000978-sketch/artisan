"""
Unit tests for Arthur Pendelton (Senior Commercial Counsel & Contract Auditor Subsystem).
"""

import pytest
from professions.legal_contract_auditor.references import ContractReferenceLibrary
from professions.legal_contract_auditor.inspector import ContractInspector
from professions.legal_contract_auditor.rubric import ContractRubric
from professions.legal_contract_auditor.blind_critic import BlindLegalCritic
from professions.legal_contract_auditor.elevation_engine import ContractElevationEngine
from professions.legal_contract_auditor.master import ArthurPendeltonMaster


def test_arthur_references_loading():
    clauses = ContractReferenceLibrary.get_standard_clauses()
    assert "limitation_of_liability" in clauses
    assert "intellectual_property_assignment" in clauses
    assert "mutual_indemnification" in clauses
    assert "termination_for_cause" in clauses
    assert "confidentiality" in clauses
    assert "governing_law_and_forum" in clauses

    toxics = ContractReferenceLibrary.get_toxic_signatures()
    assert len(toxics) >= 5
    assert any(t["id"] == "vague_future_ip_assignment" for t in toxics)


def test_arthur_inspector_ironclad_contract():
    inspector = ContractInspector()
    standard_clauses = ContractReferenceLibrary.get_standard_clauses()
    ironclad_text = (
        "MASTER SERVICES AGREEMENT\n\n" +
        standard_clauses["limitation_of_liability"] + "\n\n" +
        standard_clauses["intellectual_property_assignment"] + "\n\n" +
        standard_clauses["mutual_indemnification"] + "\n\n" +
        standard_clauses["termination_for_cause"] + "\n\n" +
        standard_clauses["confidentiality"] + "\n\n" +
        standard_clauses["governing_law_and_forum"]
    )
    report = inspector.inspect(ironclad_text)
    assert report.is_legally_sound is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_limitation_of_liability is True
    assert report.metrics.is_liability_mutual is True
    assert report.metrics.has_consequential_damages_waiver is True
    assert report.metrics.is_present_ip_assignment is True
    assert report.metrics.is_indemnification_mutual is True
    assert report.metrics.has_cure_period is True


def test_arthur_inspector_hazardous_contract():
    inspector = ContractInspector()
    hazardous_text = (
        "CONSULTING AGREEMENT\n"
        "1. IP Rights: Consultant agrees to assign deliverables upon completion.\n"
        "2. Liability: Customer shall be solely liable without limitation for all claims.\n"
        "3. Indemnity: Consultant shall defend and indemnify Company against all third party claims.\n"
        "4. Termination: Either party may terminate immediately without notice or cure.\n"
    )
    report = inspector.inspect(hazardous_text)
    assert report.is_legally_sound is False
    assert len(report.critical_violations) >= 3
    assert report.metrics.is_liability_uncapped is True
    assert report.metrics.is_present_ip_assignment is False
    assert report.metrics.is_indemnification_mutual is False


def test_arthur_rubric_and_veto():
    inspector = ContractInspector()
    rubric = ContractRubric()

    hazardous_text = (
        "VENDOR AGREEMENT\n"
        "Customer agrees to assign rights. Vendor liability is unlimited.\n"
    )
    report = inspector.inspect(hazardous_text)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) > 0


def test_arthur_critic_defect_ledger():
    critic = BlindLegalCritic()
    flawed_text = (
        "AGREEMENT: Contractor will assign inventions next year. Contractor liability is uncapped."
    )
    ledger = critic.review(flawed_text)
    assert ledger.verdict == "REJECTED_HIGH_RISK"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 2
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_arthur_elevation_engine():
    engine = ContractElevationEngine()
    flawed_contract = (
        "SOFTWARE DEVELOPMENT SERVICES AGREEMENT\n"
        "1. Scope: Contractor develops mobile app.\n"
        "2. IP: Contractor agrees to assign copyright to Customer.\n"
        "3. Liability: Contractor shall be solely liable without limitation.\n"
        "4. Indemnity: Contractor shall indemnify Company.\n"
    )
    elevated_result = engine.elevate(flawed_contract)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "hereby irrevocably assigns, transfers, and conveys" in elevated_result["elevated_contract"]
    assert "SECTION: LIMITATION OF LIABILITY" in elevated_result["elevated_contract"]
    assert "SECTION: INDEMNIFICATION" in elevated_result["elevated_contract"]


def test_arthur_master_autonomous_cycle():
    master = ArthurPendeltonMaster(passing_threshold=85)
    raw_agreement = (
        "PROPRIETARY SERVICES CONTRACT\n"
        "Party A will assign patent rights. Party B has uncapped damages.\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_agreement)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE LEGAL COUNSEL BRIEFING" in result["executive_briefing"]
    assert "IRONCLAD CERTIFIED" in result["executive_briefing"]
