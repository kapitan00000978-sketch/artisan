"""
Soren 'The Conductor' Lindqvist - Blind Distributed Consensus & Protocol Critic.

Evaluates distributed state machines strictly against split-brain hazards,
re-entrancy exposures, stale-term replays, and non-deterministic state drift.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.distributed_consensus_architect.inspector import ConsensusSystemInspector, ConsensusInspectionReport
from professions.distributed_consensus_architect.rubric import ConsensusProtocolRubric, ConsensusRubricEvaluation


@dataclass
class ConsensusDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    protocol_risk: str
    actionable_fix: str


@dataclass
class ConsensusDefectLedger:
    verdict: str  # CERTIFIED_DETERMINISTIC_CONSENSUS or REJECTED_CHAOTIC_PARTITION_DIVERGENCE
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[ConsensusDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindConsensusCritic:
    """Protocol adversary auditing distributed consensus routines for forks, race conditions, and ledger drain."""

    def __init__(self):
        self.inspector = ConsensusSystemInspector()
        self.rubric = ConsensusProtocolRubric()

    def review(self, code_input: Any) -> ConsensusDefectLedger:
        """
        Runs objective inspection and adversarial rubric scoring, producing a Consensus Defect Ledger.
        """
        report: ConsensusInspectionReport = self.inspector.inspect(code_input)
        evaluation: ConsensusRubricEvaluation = self.rubric.evaluate(report)

        defects: List[ConsensusDefect] = []

        # Map critical violations to FATAL / HIGH defects
        for i, violation in enumerate(report.critical_violations, 1):
            if "Split-Brain" in violation:
                defects.append(
                    ConsensusDefect(
                        defect_id=f"CONS-FATAL-00{i}",
                        severity="FATAL",
                        title="Split-Brain Minority Write Exposure",
                        description=violation,
                        protocol_risk="Dual divergent ledgers committed during partition, resulting in permanent consensus fork and double-spending.",
                        actionable_fix="Enforce strict majority quorum: len(acks) >= (cluster_size // 2) + 1 before state mutation."
                    )
                )
            elif "Re-Entrancy" in violation:
                defects.append(
                    ConsensusDefect(
                        defect_id=f"CONS-FATAL-00{i}",
                        severity="FATAL",
                        title="Re-Entrancy Exploit Risk",
                        description=violation,
                        protocol_risk="External call allows malicious contracts to re-enter state-altering routines before balance updates.",
                        actionable_fix="Implement atomic re-entrancy mutex (_is_reentrant_locked) and Checks-Effects-Interactions (CEI)."
                    )
                )
            elif "Non-Deterministic" in violation:
                defects.append(
                    ConsensusDefect(
                        defect_id=f"CONS-FATAL-00{i}",
                        severity="FATAL",
                        title="Non-Deterministic State Transition",
                        description=violation,
                        protocol_risk="Different validator nodes will compute divergent state hashes, permanently fracturing the network.",
                        actionable_fix="Purge wall-clock timestamps and random seeds. Transition functions must be pure and reproducible."
                    )
                )
            else:
                defects.append(
                    ConsensusDefect(
                        defect_id=f"CONS-HIGH-00{i}",
                        severity="HIGH",
                        title="Consensus Protocol Violation",
                        description=violation,
                        protocol_risk="Severe risk to network safety or liveness.",
                        actionable_fix="Remediate against standard Raft/Paxos/BFT protocol invariants."
                    )
                )

        # Map warnings
        for j, warning in enumerate(report.warnings, 1):
            severity = "HIGH" if "term" in warning.lower() else "MEDIUM"
            defects.append(
                ConsensusDefect(
                    defect_id=f"CONS-WARN-00{j}",
                    severity=severity,
                    title="Consensus Robustness Warning",
                    description=warning,
                    protocol_risk="Sub-optimal protocol resilience under high churn or network partitions.",
                    actionable_fix="Adopt Soren Lindqvist canonical consensus pattern with term fencing."
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = (
            "CERTIFIED_DETERMINISTIC_CONSENSUS"
            if evaluation.is_certified and fatal_count == 0
            else "REJECTED_CHAOTIC_PARTITION_DIVERGENCE"
        )

        summary = (
            f"Soren Lindqvist Protocol Review: Score {evaluation.total_score}/100. "
            f"Verdict: {verdict}. Fatal defects: {fatal_count}, High defects: {high_count}."
        )

        return ConsensusDefectLedger(
            verdict=verdict,
            score=evaluation.total_score,
            passing_threshold=evaluation.passing_threshold,
            is_certified=evaluation.is_certified and fatal_count == 0,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
