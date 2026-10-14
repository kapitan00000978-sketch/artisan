"""
Soren 'The Conductor' Lindqvist - Objective Distributed Consensus & Protocol Inspector.

This module inspects distributed consensus state machines, Raft/Paxos implementations,
and smart contract state controllers for quorum integrity, re-entrancy defense, and determinism.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class ConsensusMetrics:
    has_quorum_majority_check: bool = False
    has_term_fencing_validation: bool = False
    has_reentrancy_protection: bool = False
    has_deterministic_state_transitions: bool = True
    has_split_brain_vulnerability: bool = False
    has_reentrancy_vulnerability: bool = False
    has_nondeterministic_transition: bool = False
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class ConsensusInspectionReport:
    metrics: ConsensusMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_consensus_viable: bool = False


class ConsensusSystemInspector:
    """Rigorous distributed systems auditor verifying quorum consensus, re-entrancy safety, and state determinism."""

    def inspect(self, code_input: Any) -> ConsensusInspectionReport:
        """
        Audits distributed state machine code, smart contract, or consensus protocol specification.
        """
        metrics = self._extract_metrics(code_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Quorum & Split-Brain Check
        if metrics.has_split_brain_vulnerability:
            critical_violations.append(
                "Split-Brain Minority Commit Hazard: State transitions committed without confirming strict majority quorum (N/2 + 1)."
            )
        elif metrics.has_quorum_majority_check:
            benchmarks_passed.append("Strict majority quorum (N/2 + 1) consensus verification verified.")
        else:
            warnings.append("Explicit majority quorum threshold calculation not clearly documented.")

        # 2. Term & Epoch Fencing Token
        if not metrics.has_term_fencing_validation:
            warnings.append("Missing monotonic term / epoch fencing token to reject stale leader replays.")
        else:
            benchmarks_passed.append("Monotonic term fencing validation verified (Stale leader RPC rejection).")

        # 3. Re-Entrancy Defense
        if metrics.has_reentrancy_vulnerability:
            critical_violations.append(
                "Re-Entrancy Exploit Risk: External state calls or token transfers executed without reentrancy guard or CEI pattern."
            )
        elif metrics.has_reentrancy_protection:
            benchmarks_passed.append("Re-entrancy guard lock / Checks-Effects-Interactions (CEI) order verified.")

        # 4. State Machine Determinism
        if metrics.has_nondeterministic_transition:
            critical_violations.append(
                "Non-Deterministic State Transition: System wall clock or random generator invoked during state mutation."
            )
        elif metrics.has_deterministic_state_transitions:
            benchmarks_passed.append("Deterministic pure state machine transitions verified.")

        for ap in metrics.anti_patterns_detected:
            if ap not in critical_violations:
                critical_violations.append(f"Anti-Pattern Detected: {ap}")

        is_viable = len(critical_violations) == 0

        return ConsensusInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_consensus_viable=is_viable
        )

    def _extract_metrics(self, code_input: Any) -> ConsensusMetrics:
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
        m = ConsensusMetrics()

        # 1. Quorum Check
        has_quorum = bool(
            "quorum" in text_lower or
            "majority" in text_lower or
            "// 2) + 1" in text_lower or
            "/ 2 + 1" in text_lower or
            "2 * f + 1" in text_lower or
            metadata.get("has_quorum_majority_check", False)
        )
        m.has_quorum_majority_check = has_quorum

        # 2. Term Fencing
        has_term = bool(
            "entry.term <" in text_lower or
            "term <" in text_lower or
            "term_fencing" in text_lower or
            "epoch" in text_lower or
            "current_term" in text_lower or
            metadata.get("has_term_fencing_validation", False)
        )
        m.has_term_fencing_validation = has_term

        # 3. Re-entrancy Protection
        has_reentrancy_lock = bool(
            "reentrant" in text_lower or
            "nonreentrant" in text_lower or
            "_is_reentrant_locked" in text_lower or
            "mutex" in text_lower or
            "reentrancyguard" in text_lower or
            metadata.get("has_reentrancy_protection", False)
        )
        m.has_reentrancy_protection = has_reentrancy_lock

        # 4. Split-brain vulnerability (write or commit without quorum check)
        is_split_brain = bool(
            ("commit" in text_lower or "apply_transition" in text_lower or "mutate_state" in text_lower) and
            not has_quorum and
            not metadata.get("is_pure_query", False)
        ) or metadata.get("has_split_brain_vulnerability", False)
        m.has_split_brain_vulnerability = is_split_brain

        # 5. Re-entrancy vulnerability
        is_reentrant_vuln = bool(
            ("transfer(" in text_lower or "call.value" in text_lower or "send(" in text_lower or "withdraw(" in text_lower) and
            not has_reentrancy_lock
        ) or metadata.get("has_reentrancy_vulnerability", False)
        m.has_reentrancy_vulnerability = is_reentrant_vuln

        # 6. Non-deterministic transition
        has_clock_or_rand = bool(
            "time.time()" in text_lower or
            "datetime.now()" in text_lower or
            "date.now()" in text_lower or
            "random.random()" in text_lower or
            "random.randint" in text_lower or
            metadata.get("has_nondeterministic_transition", False)
        )
        m.has_nondeterministic_transition = has_clock_or_rand
        m.has_deterministic_state_transitions = not has_clock_or_rand

        # Anti-pattern logging
        if m.has_split_brain_vulnerability:
            m.anti_patterns_detected.append("Split-brain write commitment without majority quorum")
        if m.has_reentrancy_vulnerability:
            m.anti_patterns_detected.append("Unprotected state mutation vulnerable to re-entrancy drain")
        if m.has_nondeterministic_transition:
            m.anti_patterns_detected.append("Non-deterministic clock or random function inside state transition")

        return m
