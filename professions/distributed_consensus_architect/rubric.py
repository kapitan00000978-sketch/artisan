"""
Soren 'The Conductor' Lindqvist - 100-Point Distributed Consensus & Protocol Rubric.

Evaluates distributed state machines, Raft/Paxos quorum adherence, re-entrancy defense,
and state transition determinism.
Passing threshold: 85/100 points.
Veto criteria: Split-brain minority writes, re-entrancy exposure, or non-deterministic state mutations.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.distributed_consensus_architect.inspector import ConsensusInspectionReport, ConsensusMetrics


@dataclass
class ConsensusRubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class ConsensusProtocolRubric:
    """Rigorous 100-point weighted evaluation rubric for distributed consensus and fault-tolerant protocols."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: ConsensusInspectionReport) -> ConsensusRubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Majority Quorum & Split-Brain Immunity (30 pts)
        # ----------------------------------------------------
        p1_score = 0
        if m.has_split_brain_vulnerability:
            veto_reasons.append(
                "Split-Brain Minority Write: State transitions committed without confirming majority quorum (N/2 + 1)."
            )
            recommendations.append(
                "Require strict quorum verification: Ensure len(acks) >= (cluster_size // 2) + 1 before committing log entries."
            )
        elif m.has_quorum_majority_check:
            p1_score = 30
        else:
            p1_score = 15
            recommendations.append("Explicitly annotate quorum confirmation logic.")
        pillar_scores["quorum_split_brain_immunity"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Term Fencing & Leader Monotonicity (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if m.has_term_fencing_validation:
            p2_score = 25
        else:
            p2_score = 10
            recommendations.append(
                "Implement monotonic term/epoch fencing: Immediately reject RPCs with term < current_term."
            )
        pillar_scores["term_fencing_monotonicity"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: Re-Entrancy Defense & CEI Discipline (25 pts)
        # ----------------------------------------------------
        p3_score = 0
        if m.has_reentrancy_vulnerability:
            veto_reasons.append(
                "Re-Entrancy Exploit Risk: External state mutations or funds transfers occur without mutex locks or CEI pattern."
            )
            recommendations.append(
                "Apply Checks-Effects-Interactions (CEI) order or lock-based reentrancy guard (_is_reentrant_locked / nonReentrant)."
            )
        elif m.has_reentrancy_protection:
            p3_score = 25
        else:
            p3_score = 15
            recommendations.append("Add explicit re-entrancy locks to all state-altering public endpoints.")
        pillar_scores["reentrancy_defense_cei"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: Determinism & Auditability (20 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.has_nondeterministic_transition:
            veto_reasons.append(
                "Non-Deterministic State Transition: Wall clock or random number generator detected inside transition logic."
            )
            recommendations.append(
                "Purge wall clock (time.time()) and random seeds from transition logic. Use deterministic block height or logical sequence numbers."
            )
        elif m.has_deterministic_state_transitions:
            p4_score = 20
        pillar_scores["determinism_auditability"] = p4_score

        total_score = sum(pillar_scores.values())
        veto_triggered = len(veto_reasons) > 0

        if veto_triggered:
            total_score = min(total_score, 50)
            is_certified = False
        else:
            is_certified = total_score >= self.PASSING_THRESHOLD

        return ConsensusRubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
