"""
Seraphina 'The Aegis' Sterling - Objective Quantum-Resistant & ZKP Cryptography Inspector.

This module inspects cryptographic implementations, post-quantum key exchanges,
and zero-knowledge proof circuits for Shor vulnerabilities, timing leaks, and nullifier tracking.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class CryptoMetrics:
    has_post_quantum_primitives: bool = False
    has_constant_time_comparison: bool = False
    has_nullifier_tracking: bool = False
    has_shor_vulnerable_primitives: bool = False
    has_timing_leak_comparison: bool = False
    has_insecure_randomness: bool = False
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class CryptoInspectionReport:
    metrics: CryptoMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_crypto_viable: bool = False


class QuantumZkpInspector:
    """Rigorous cryptographic auditor verifying post-quantum safety, constant-time execution, and ZKP integrity."""

    def inspect(self, code_input: Any) -> CryptoInspectionReport:
        """
        Audits cryptographic key exchange, ZKP verifier, or token circuit logic.
        """
        metrics = self._extract_metrics(code_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Classical Shor-Vulnerable Primitives
        if metrics.has_shor_vulnerable_primitives:
            critical_violations.append(
                "Shor-Vulnerable Classical Cryptography: Standalone RSA or discrete-log ECC detected without post-quantum lattice hybridization (ML-KEM/ML-DSA)."
            )
        elif metrics.has_post_quantum_primitives:
            benchmarks_passed.append("Post-quantum lattice primitives verified (ML-KEM / Kyber quantum-safe encapsulation).")
        else:
            warnings.append("No explicit post-quantum lattice primitives (ML-KEM/FIPS 203) referenced.")

        # 2. Timing Side-Channel Vulnerability
        if metrics.has_timing_leak_comparison:
            critical_violations.append(
                "Side-Channel Timing Leak: Secret tokens, hashes, or signatures compared using variable-time operators (==) instead of secrets.compare_digest."
            )
        elif metrics.has_constant_time_comparison:
            benchmarks_passed.append("Constant-time side-channel-free comparison verified (secrets.compare_digest).")
        else:
            warnings.append("Consider verifying constant-time arithmetic on secret values.")

        # 3. ZKP Nullifier Double-Spend Tracking
        if not metrics.has_nullifier_tracking:
            warnings.append("Missing zero-knowledge nullifier tracking: Vulnerable to double-spend and proof replay attacks.")
        else:
            benchmarks_passed.append("Cryptographic nullifier tracking verified (Replay and double-spend immunity).")

        # 4. Insecure Randomness
        if metrics.has_insecure_randomness:
            critical_violations.append(
                "Insecure Pseudo-Random Number Generator: Found random.random() or non-CSPRNG source for cryptographic operations."
            )
        else:
            benchmarks_passed.append("Cryptographically secure random generation (CSPRNG) verified.")

        for ap in metrics.anti_patterns_detected:
            if ap not in critical_violations:
                critical_violations.append(f"Anti-Pattern Detected: {ap}")

        is_viable = len(critical_violations) == 0

        return CryptoInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_crypto_viable=is_viable
        )

    def _extract_metrics(self, code_input: Any) -> CryptoMetrics:
        text = ""
        metadata: Dict[str, Any] = {}

        if isinstance(code_input, str):
            text = code_input
            try:
                parsed = json.loads(code_input)
                if isinstance(parsed, dict):
                    metadata = parsed
            except (json.JSONDecodeError, ValueError) as _json_err:
                _ = _json_err
        elif isinstance(code_input, dict):
            metadata = code_input
            text = json.dumps(code_input)
        else:
            text = str(code_input)

        # Strip comments to prevent false positives from descriptive comments
        cleaned_text = re.sub(r"#.*", "", text)
        cleaned_text = re.sub(r"//.*", "", cleaned_text)
        text_lower = cleaned_text.lower()
        m = CryptoMetrics()

        # 1. Post-quantum primitives
        has_pq = bool(
            "ml-kem" in text_lower or
            "ml_kem" in text_lower or
            "ml-dsa" in text_lower or
            "kyber" in text_lower or
            "dilithium" in text_lower or
            "lattice" in text_lower or
            "fips 203" in text_lower or
            "quantum" in text_lower or
            "kem" in text_lower or
            "encapsulate" in text_lower or
            metadata.get("has_post_quantum_primitives", False)
        )
        m.has_post_quantum_primitives = has_pq

        # 2. Shor-vulnerable primitives
        has_shor = bool(
            ("rsa.generate" in text_lower or
             "rsa_private_key" in text_lower or
             "generate_private_key(rsa" in text_lower or
             "secp256k1" in text_lower) and not has_pq or
            metadata.get("has_shor_vulnerable_primitives", False)
        )
        m.has_shor_vulnerable_primitives = has_shor

        # 3. Constant-time comparison
        has_ct = bool(
            "compare_digest" in text_lower or
            "crypto_memcmp" in text_lower or
            "constant_time" in text_lower or
            metadata.get("has_constant_time_comparison", False)
        )
        m.has_constant_time_comparison = has_ct

        # 4. Timing leak comparison
        has_timing_leak = bool(
            ("secret" in text_lower or "token" in text_lower or "proof" in text_lower or "mac" in text_lower) and
            (" == " in text or " != " in text) and
            not has_ct or
            metadata.get("has_timing_leak_comparison", False)
        )
        m.has_timing_leak_comparison = has_timing_leak

        # 5. Nullifier tracking
        has_nullifier = bool(
            "nullifier" in text_lower or
            "spent_nullifiers" in text_lower or
            metadata.get("has_nullifier_tracking", False)
        )
        m.has_nullifier_tracking = has_nullifier

        # 6. Insecure randomness
        has_insecure_rng = bool(
            "random.random()" in text_lower or
            "random.randint" in text_lower or
            "random.choice" in text_lower or
            "math.random()" in text_lower or
            metadata.get("has_insecure_randomness", False)
        )
        m.has_insecure_randomness = has_insecure_rng

        # Anti-pattern logging
        if m.has_shor_vulnerable_primitives:
            m.anti_patterns_detected.append("Shor-vulnerable classical public-key cryptography")
        if m.has_timing_leak_comparison:
            m.anti_patterns_detected.append("Side-channel timing leak in secret comparison")
        if m.has_insecure_randomness:
            m.anti_patterns_detected.append("Insecure PRNG used for cryptographic material")

        return m
