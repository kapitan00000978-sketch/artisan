"""
Seraphina 'The Aegis' Sterling - 100-Point Post-Quantum & ZKP Cryptography Rubric.

Evaluates cryptographic protocols, key encapsulation routines, zero-knowledge circuits,
and side-channel timing attack defenses.
Passing threshold: 85/100 points.
Veto criteria: Shor-vulnerable RSA/ECC, timing leak comparisons, or insecure PRNG usage.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.quantum_zkp_cryptographer.inspector import CryptoInspectionReport, CryptoMetrics


@dataclass
class CryptoRubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class QuantumZkpRubric:
    """Rigorous 100-point weighted evaluation rubric for post-quantum safety and zero-knowledge integrity."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: CryptoInspectionReport) -> CryptoRubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Post-Quantum Resilience & Lattice KEM (30 pts)
        # ----------------------------------------------------
        p1_score = 0
        if m.has_shor_vulnerable_primitives:
            veto_reasons.append(
                "Shor-Vulnerable Cryptography: Using standalone RSA or discrete-log ECC exposes secrets to quantum decryption."
            )
            recommendations.append(
                "Migrate to FIPS 203 ML-KEM (Kyber-768) lattice key encapsulation or hybrid post-quantum schemes."
            )
        elif m.has_post_quantum_primitives:
            p1_score = 30
        else:
            p1_score = 15
            recommendations.append("Explicitly adopt post-quantum lattice primitives (ML-KEM / ML-DSA).")
        pillar_scores["post_quantum_resilience"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Constant-Time & Timing Side-Channel Defense (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if m.has_timing_leak_comparison:
            veto_reasons.append(
                "Side-Channel Timing Leak: Secret tokens or cryptographic hashes compared using variable-time operators (==)."
            )
            recommendations.append(
                "Enforce constant-time comparison via secrets.compare_digest() or CRYPTO_memcmp()."
            )
        elif m.has_constant_time_comparison:
            p2_score = 25
        else:
            p2_score = 15
            recommendations.append("Add constant-time equality guards on sensitive cryptographic outputs.")
        pillar_scores["side_channel_constant_time"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: ZKP & Nullifier Double-Spend Defense (25 pts)
        # ----------------------------------------------------
        p3_score = 0
        if m.has_nullifier_tracking:
            p3_score = 25
        else:
            p3_score = 10
            recommendations.append(
                "Implement persistent nullifier deduplication registry (spent_nullifiers.add) to prevent double-spending in ZKP."
            )
        pillar_scores["zkp_nullifier_defense"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: CSPRNG Entropy & Nonce Hygiene (20 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.has_insecure_randomness:
            veto_reasons.append(
                "Insecure Pseudo-Random Number Generator: Using non-cryptographic random generator allows key predictability."
            )
            recommendations.append(
                "Substitute random.random() with cryptographically secure hardware-seeded secrets.token_bytes()."
            )
        else:
            p4_score = 20
        pillar_scores["csprng_entropy_hygiene"] = p4_score

        total_score = sum(pillar_scores.values())
        veto_triggered = len(veto_reasons) > 0

        if veto_triggered:
            total_score = min(total_score, 50)
            is_certified = False
        else:
            is_certified = total_score >= self.PASSING_THRESHOLD

        return CryptoRubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
