"""
Seraphina 'The Aegis' Sterling - Blind Post-Quantum & ZKP Cryptography Critic.

Evaluates cryptographic protocols, key encapsulation routines, and zero-knowledge circuits
strictly against Shor vulnerabilities, timing side-channels, and nullifier omission.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.quantum_zkp_cryptographer.inspector import QuantumZkpInspector, CryptoInspectionReport
from professions.quantum_zkp_cryptographer.rubric import QuantumZkpRubric, CryptoRubricEvaluation


@dataclass
class CryptoDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    cryptographic_risk: str
    actionable_fix: str


@dataclass
class CryptoDefectLedger:
    verdict: str  # CERTIFIED_QUANTUM_RESILIENT_ZKP or REJECTED_CRYPTOGRAPHIC_COLLAPSE
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[CryptoDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindCryptoCritic:
    """Cryptographic adversary auditing implementations for quantum vulnerabilities, timing leaks, and replay attacks."""

    def __init__(self):
        self.inspector = QuantumZkpInspector()
        self.rubric = QuantumZkpRubric()

    def review(self, code_input: Any) -> CryptoDefectLedger:
        """
        Runs objective inspection and adversarial rubric scoring, producing a Cryptographic Defect Ledger.
        """
        report: CryptoInspectionReport = self.inspector.inspect(code_input)
        evaluation: CryptoRubricEvaluation = self.rubric.evaluate(report)

        defects: List[CryptoDefect] = []

        # Map critical violations to FATAL / HIGH defects
        for i, violation in enumerate(report.critical_violations, 1):
            if "Shor-Vulnerable" in violation:
                defects.append(
                    CryptoDefect(
                        defect_id=f"CRYPTO-FATAL-00{i}",
                        severity="FATAL",
                        title="Shor-Vulnerable Classical Cryptography",
                        description=violation,
                        cryptographic_risk="Classical discrete-log and factoring assumptions will collapse under quantum polynomial-time cryptanalysis.",
                        actionable_fix="Adopt FIPS 203 ML-KEM lattice encapsulation (Kyber-768/1024) or hybrid post-quantum schemes."
                    )
                )
            elif "Timing Leak" in violation:
                defects.append(
                    CryptoDefect(
                        defect_id=f"CRYPTO-FATAL-00{i}",
                        severity="FATAL",
                        title="Timing Side-Channel Vulnerability",
                        description=violation,
                        cryptographic_risk="Variable-time comparison leaks private key material via microsecond network timing discrepancies.",
                        actionable_fix="Use secrets.compare_digest() or CRYPTO_memcmp() for all cryptographic comparisons."
                    )
                )
            elif "Insecure Pseudo-Random" in violation:
                defects.append(
                    CryptoDefect(
                        defect_id=f"CRYPTO-FATAL-00{i}",
                        severity="FATAL",
                        title="Insecure PRNG Entropy Source",
                        description=violation,
                        cryptographic_risk="Predictable seed states allow adversaries to reconstruct private keys and forge signatures.",
                        actionable_fix="Replace random.random() with cryptographically secure secrets.token_bytes()."
                    )
                )
            else:
                defects.append(
                    CryptoDefect(
                        defect_id=f"CRYPTO-HIGH-00{i}",
                        severity="HIGH",
                        title="Cryptographic Architecture Violation",
                        description=violation,
                        cryptographic_risk="Severe risk to confidentiality, integrity, or forward secrecy.",
                        actionable_fix="Remediate against Seraphina Sterling post-quantum cryptographic standards."
                    )
                )

        # Map warnings
        for j, warning in enumerate(report.warnings, 1):
            severity = "HIGH" if "nullifier" in warning.lower() else "MEDIUM"
            defects.append(
                CryptoDefect(
                    defect_id=f"CRYPTO-WARN-00{j}",
                    severity=severity,
                    title="Cryptographic Robustness Warning",
                    description=warning,
                    cryptographic_risk="Sub-optimal forward secrecy or double-spend vulnerability.",
                    actionable_fix="Adopt Seraphina Sterling canonical ZKP nullifier tracking and ML-KEM encapsulation."
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = (
            "CERTIFIED_QUANTUM_RESILIENT_ZKP"
            if evaluation.is_certified and fatal_count == 0
            else "REJECTED_CRYPTOGRAPHIC_COLLAPSE"
        )

        summary = (
            f"Seraphina Sterling Cryptographic Review: Score {evaluation.total_score}/100. "
            f"Verdict: {verdict}. Fatal defects: {fatal_count}, High defects: {high_count}."
        )

        return CryptoDefectLedger(
            verdict=verdict,
            score=evaluation.total_score,
            passing_threshold=evaluation.passing_threshold,
            is_certified=evaluation.is_certified and fatal_count == 0,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
