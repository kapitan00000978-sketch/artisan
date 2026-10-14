"""
Unit tests for Seraphina 'The Aegis' Sterling (Principal Quantum-Resistant Cryptography & ZKP Architect Subsystem).
"""

import pytest
from professions.quantum_zkp_cryptographer.references import (
    QuantumZkpReferenceLibrary,
    CANONICAL_QUANTUM_ZKP_CORE,
)
from professions.quantum_zkp_cryptographer.inspector import QuantumZkpInspector
from professions.quantum_zkp_cryptographer.rubric import QuantumZkpRubric
from professions.quantum_zkp_cryptographer.blind_critic import BlindCryptoCritic
from professions.quantum_zkp_cryptographer.elevation_engine import QuantumZkpElevationEngine
from professions.quantum_zkp_cryptographer.master import SeraphinaSterlingMaster


def test_seraphina_references_loading():
    benchmarks = QuantumZkpReferenceLibrary.get_benchmarks()
    assert "FIPS 203" in benchmarks["nist_post_quantum_standard"]
    assert benchmarks["min_security_level"] == 3
    assert benchmarks["side_channel_constant_time"] is True
    assert benchmarks["nullifier_deduplication"] is True

    standards = QuantumZkpReferenceLibrary.get_standards()
    assert "post_quantum_encapsulation" in standards
    assert "zero_knowledge_nullifiers" in standards
    assert "constant_time_equality" in standards

    anti_patterns = QuantumZkpReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "shor_vulnerable_rsa_ecc" for ap in anti_patterns)


def test_seraphina_inspector_clean_code():
    inspector = QuantumZkpInspector()
    report = inspector.inspect(CANONICAL_QUANTUM_ZKP_CORE)

    assert report.is_crypto_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_post_quantum_primitives is True
    assert report.metrics.has_constant_time_comparison is True
    assert report.metrics.has_nullifier_tracking is True
    assert report.metrics.has_shor_vulnerable_primitives is False
    assert report.metrics.has_insecure_randomness is False


def test_seraphina_inspector_flawed_code():
    inspector = QuantumZkpInspector()
    flawed_code = (
        "def generate_key():\n"
        "    key = rsa.generate(2048)\n"
        "    seed = random.random()\n"
        "    return key, seed\n"
        "def verify_token(token, expected_token):\n"
        "    return token == expected_token\n"
    )
    report = inspector.inspect(flawed_code)

    assert report.is_crypto_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_shor_vulnerable_primitives is True
    assert report.metrics.has_timing_leak_comparison is True
    assert report.metrics.has_insecure_randomness is True


def test_seraphina_rubric_and_veto():
    inspector = QuantumZkpInspector()
    rubric = QuantumZkpRubric()

    bad_code = (
        "def authenticate_secret(secret_token):\n"
        "    return secret_token == expected_token\n"
    )
    report = inspector.inspect(bad_code)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) >= 1
    assert any("Side-Channel Timing Leak" in r for r in evaluation.veto_reasons)


def test_seraphina_critic_defect_ledger():
    critic = BlindCryptoCritic()
    flawed_code = (
        "def make_token():\n"
        "    return random.random()\n"
    )
    ledger = critic.review(flawed_code)

    assert ledger.verdict == "REJECTED_CRYPTOGRAPHIC_COLLAPSE"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 1
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_seraphina_elevation_engine():
    engine = QuantumZkpElevationEngine()
    flawed_code = (
        "class TokenManager:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    def verify_proof(self, proof):\n"
        "        return proof.hash == proof.commitment\n"
    )
    elevated_result = engine.elevate(flawed_code)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "compare_digest" in elevated_result["elevated_code"]
    assert "spent_nullifiers" in elevated_result["elevated_code"]
    assert "encapsulate_shared_secret" in elevated_result["elevated_code"]


def test_seraphina_master_autonomous_cycle():
    master = SeraphinaSterlingMaster(passing_threshold=85)
    raw_code = (
        "class SimpleCrypto:\n"
        "    def verify(self, proof):\n"
        "        return True\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_code)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE CRYPTOGRAPHIC & ZKP BRIEFING" in result["executive_briefing"]
    assert "QUANTUM RESILIENCE CERTIFIED" in result["executive_briefing"]
