"""
Unit tests for Soren 'The Conductor' Lindqvist (Principal Distributed Consensus & Protocol Architect Subsystem).
"""

import pytest
from professions.distributed_consensus_architect.references import (
    ConsensusReferenceLibrary,
    CANONICAL_CONSENSUS_CORE,
)
from professions.distributed_consensus_architect.inspector import ConsensusSystemInspector
from professions.distributed_consensus_architect.rubric import ConsensusProtocolRubric
from professions.distributed_consensus_architect.blind_critic import BlindConsensusCritic
from professions.distributed_consensus_architect.elevation_engine import ConsensusElevationEngine
from professions.distributed_consensus_architect.master import SorenLindqvistMaster


def test_soren_references_loading():
    benchmarks = ConsensusReferenceLibrary.get_protocol_benchmarks()
    assert benchmarks["min_quorum_percentage"] == 51.0
    assert benchmarks["byzantine_fault_threshold"] == 0.333
    assert benchmarks["reentrancy_guard_enforced"] is True

    standards = ConsensusReferenceLibrary.get_algorithm_standards()
    assert "raft_consensus" in standards
    assert "byzantine_fault_tolerance" in standards
    assert "smart_contract_state_safety" in standards

    anti_patterns = ConsensusReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "split_brain_minority_write" for ap in anti_patterns)


def test_soren_inspector_clean_code():
    inspector = ConsensusSystemInspector()
    report = inspector.inspect(CANONICAL_CONSENSUS_CORE)

    assert report.is_consensus_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_quorum_majority_check is True
    assert report.metrics.has_term_fencing_validation is True
    assert report.metrics.has_reentrancy_protection is True
    assert report.metrics.has_deterministic_state_transitions is True
    assert report.metrics.has_split_brain_vulnerability is False


def test_soren_inspector_flawed_code():
    inspector = ConsensusSystemInspector()
    flawed_code = (
        "def apply_transition(entry):\n"
        "    # commit directly without checking any quorum or term\n"
        "    ledger.append(entry)\n"
        "    now = time.time()\n"
        "    entry.timestamp = now\n"
    )
    report = inspector.inspect(flawed_code)

    assert report.is_consensus_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_split_brain_vulnerability is True
    assert report.metrics.has_nondeterministic_transition is True
    assert report.metrics.has_quorum_majority_check is False


def test_soren_rubric_and_veto():
    inspector = ConsensusSystemInspector()
    rubric = ConsensusProtocolRubric()

    bad_code = (
        "def mutate_state(user, amount):\n"
        "    # vulnerable minority commit\n"
        "    balances[user] += amount\n"
    )
    report = inspector.inspect(bad_code)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) >= 1
    assert any("Split-Brain Minority Write" in r for r in evaluation.veto_reasons)


def test_soren_critic_defect_ledger():
    critic = BlindConsensusCritic()
    flawed_code = (
        "def withdraw(recipient, amount):\n"
        "    recipient.call.value(amount)()\n"
        "    balances[recipient] -= amount\n"
    )
    ledger = critic.review(flawed_code)

    assert ledger.verdict == "REJECTED_CHAOTIC_PARTITION_DIVERGENCE"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 1
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_soren_elevation_engine():
    engine = ConsensusElevationEngine()
    flawed_code = (
        "class NodeState:\n"
        "    def __init__(self, cluster_size):\n"
        "        self.cluster_size = cluster_size\n"
        "    def apply_transition(self, entry):\n"
        "        timestamp = time.time()\n"
        "        self.ledger.append(entry)\n"
    )
    elevated_result = engine.elevate(flawed_code)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "quorum_size" in elevated_result["elevated_code"]
    assert "entry.term" in elevated_result["elevated_code"] or "term" in elevated_result["elevated_code"]
    assert "_is_reentrant_locked" in elevated_result["elevated_code"]


def test_soren_master_autonomous_cycle():
    master = SorenLindqvistMaster(passing_threshold=85)
    raw_code = (
        "class RawState:\n"
        "    def apply_transition(self, entry):\n"
        "        self.data = entry\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_code)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE DISTRIBUTED CONSENSUS BRIEFING" in result["executive_briefing"]
    assert "DETERMINISTIC CONSENSUS CERTIFIED" in result["executive_briefing"]
