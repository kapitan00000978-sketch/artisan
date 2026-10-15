"""Closed-Loop Dual-Agent Event Horizon GRMHD Master Engine.

Embodying Dr. Vespera 'The Singularity' Vance,
Principal Event Horizon General Relativistic Magnetohydrodynamics (GRMHD) Architect.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from .inspector import GRMHDInspector
from .rubric import GRMHDRubric, PASSING_SCORE
from .blind_critic import GRMHDBlindCritic
from .elevation_engine import GRMHDElevationEngine


@dataclass
class ActiveDecisionJournal:
    """Audit trail of iterative GRMHD critique and elevation cycles."""
    initial_score: float = 0.0
    final_score: float = 0.0
    cycles_completed: int = 0
    passed: bool = False
    repaired_flaws: List[str] = field(default_factory=list)
    critic_notes: List[str] = field(default_factory=list)
    iteration_history: List[Dict[str, Any]] = field(default_factory=list)


class GRMHDMaster:
    """Master engine orchestrating dual-agent adversarial reflection and elevation."""

    def __init__(self, max_cycles: int = 3, min_passing_score: float = PASSING_SCORE) -> None:
        self.inspector = GRMHDInspector()
        self.rubric = GRMHDRubric()
        self.blind_critic = GRMHDBlindCritic()
        self.elevation_engine = GRMHDElevationEngine()
        self.max_cycles = max_cycles
        self.min_passing_score = min_passing_score

    def execute_closed_loop(self, source_code: str) -> Dict[str, Any]:
        """Execute closed-loop dual-agent elevation cycle until code passes with >= 95 score."""
        journal = ActiveDecisionJournal()
        current_code = source_code

        initial_audit = self.blind_critic.audit(current_code)
        journal.initial_score = initial_audit["score"]
        journal.critic_notes = initial_audit["critique_notes"]

        if initial_audit["passed"] and initial_audit["score"] >= self.min_passing_score:
            journal.final_score = initial_audit["score"]
            journal.passed = True
            return {
                "status": "certified",
                "master": "Dr. Vespera 'The Singularity' Vance",
                "code": current_code,
                "score": journal.final_score,
                "passed": True,
                "cycles": 0,
                "repaired_flaws": [],
                "critic_notes": journal.critic_notes,
                "journal": journal,
            }

        # Iterative remediation loop
        for cycle in range(1, self.max_cycles + 1):
            journal.cycles_completed = cycle
            elevated_code, remediations = self.elevation_engine.elevate(current_code)
            journal.repaired_flaws.extend(remediations)
            current_code = elevated_code

            audit = self.blind_critic.audit(current_code)
            journal.iteration_history.append({
                "cycle": cycle,
                "score": audit["score"],
                "passed": audit["passed"],
                "remediations": remediations,
            })

            if audit["passed"] and audit["score"] >= self.min_passing_score:
                journal.final_score = audit["score"]
                journal.passed = True
                journal.critic_notes = audit["critique_notes"]
                break
        else:
            final_audit = self.blind_critic.audit(current_code)
            journal.final_score = final_audit["score"]
            journal.passed = final_audit["passed"]
            journal.critic_notes = final_audit["critique_notes"]

        return {
            "status": "certified" if journal.passed else "needs_review",
            "master": "Dr. Vespera 'The Singularity' Vance",
            "code": current_code,
            "score": journal.final_score,
            "passed": journal.passed,
            "cycles": journal.cycles_completed,
            "repaired_flaws": journal.repaired_flaws,
            "critic_notes": journal.critic_notes,
            "journal": journal,
        }
