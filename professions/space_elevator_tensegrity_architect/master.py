"""Master Dual-Agent Closed-Loop Reflection Engine for Dr. Valerius Sterling.

Coordinates adversarial inspection, autonomous elevation, and audit journaling.
"""

from typing import Dict, Any, List, Optional
from professions.space_elevator_tensegrity_architect.blind_critic import SpaceElevatorBlindCritic
from professions.space_elevator_tensegrity_architect.elevation_engine import SpaceElevatorElevationEngine


class SpaceElevatorMaster:
    """Master controller orchestrating closed-loop evaluation and self-healing elevation for space elevators."""

    def __init__(self, journal: Optional[Any] = None) -> None:
        self.critic = SpaceElevatorBlindCritic()
        self.elevation_engine = SpaceElevatorElevationEngine()
        self.journal = journal

    def evaluate_and_elevate(
        self,
        source_code: str,
        target_file: str = "space_elevator_tether.py",
        max_iterations: int = 3
    ) -> Dict[str, Any]:
        """Execute closed-loop reflection cycle until 95+ score is achieved or iterations exhausted."""
        current_code = source_code
        iteration = 0
        all_repaired_flaws: List[str] = []
        history: List[Dict[str, Any]] = []

        initial_audit = self.critic.audit(current_code)
        history.append({
            "stage": "initial",
            "score": initial_audit["score"],
            "verdict": initial_audit["verdict"],
            "flaw_count": initial_audit["flaw_count"]
        })

        if initial_audit["passed"]:
            return {
                "status": "certified",
                "final_score": initial_audit["score"],
                "elevated_code": current_code,
                "repaired_flaws": [],
                "iterations": 0,
                "history": history
            }

        score_before = initial_audit["score"]

        while iteration < max_iterations:
            iteration += 1
            current_code, actions = self.elevation_engine.elevate(current_code)
            all_repaired_flaws.extend(actions)

            post_audit = self.critic.audit(current_code)
            score_after = post_audit["score"]

            history.append({
                "stage": f"iteration_{iteration}",
                "score": score_after,
                "verdict": post_audit["verdict"],
                "actions": actions,
                "flaw_count": post_audit["flaw_count"]
            })

            # Record in journal if available (strictly 6 positional arguments)
            if self.journal and hasattr(self.journal, "record_decision"):
                try:
                    self.journal.record_decision(
                        iteration,
                        target_file,
                        [f.get("description", "") for f in post_audit["flaws"]],
                        actions,
                        score_before,
                        score_after
                    )
                except Exception as log_err:
                    import logging
                    logging.getLogger("space_elevator").warning(f"Journal record warning: {log_err}")

            if post_audit["passed"]:
                return {
                    "status": "certified",
                    "final_score": score_after,
                    "elevated_code": current_code,
                    "repaired_flaws": all_repaired_flaws,
                    "iterations": iteration,
                    "history": history
                }

            score_before = score_after

        final_audit = self.critic.audit(current_code)
        return {
            "status": "certified" if final_audit["passed"] else "remediation_incomplete",
            "final_score": final_audit["score"],
            "elevated_code": current_code,
            "repaired_flaws": all_repaired_flaws,
            "iterations": iteration,
            "history": history
        }
