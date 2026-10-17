"""Master Dual-Agent Closed-Loop Reflection Engine for Dr. Thaddeus Vance.

Orchestrates adversarial inspection, autonomous self-healing elevation,
and audit journaling for Pulsed Power & Terawatt Z-Pinch Plasma Confinement.
"""

import logging
from typing import Any, Dict, List, Optional

from professions.pulsed_power_terawatt_plasma_architect.blind_critic import PulsedPowerBlindCritic
from professions.pulsed_power_terawatt_plasma_architect.elevation_engine import PulsedPowerElevationEngine


logger = logging.getLogger("pulsed_power")


class PulsedPowerMaster:
    """Master controller orchestrating closed-loop evaluation and self-healing elevation for pulsed power code."""

    def __init__(self, journal: Optional[Any] = None) -> None:
        self.critic = PulsedPowerBlindCritic()
        self.elevation_engine = PulsedPowerElevationEngine()
        self.journal = journal

    def evaluate_and_elevate(
        self,
        source_code: str,
        target_file: str = "pulsed_power_drive.py",
        max_iterations: int = 3,
    ) -> Dict[str, Any]:
        """Execute closed-loop reflection cycle until 95+ score is achieved or iterations exhausted."""
        current_code = source_code
        iteration = 0
        all_repaired_flaws: List[str] = []
        history: List[Dict[str, Any]] = []

        initial_verdict = self.critic.audit(current_code)
        history.append({
            "stage": "initial",
            "score": initial_verdict.score,
            "verdict": initial_verdict.verdict,
            "flaw_count": len(initial_verdict.deductions),
        })

        if initial_verdict.passed:
            return {
                "status": "certified",
                "final_score": initial_verdict.score,
                "elevated_code": current_code,
                "repaired_flaws": [],
                "iterations": 0,
                "history": history,
            }

        score_before = initial_verdict.score

        while iteration < max_iterations:
            iteration += 1
            current_code, stats = self.elevation_engine.elevate(current_code)
            action_desc = [f"Remediated {k}: {v}" for k, v in stats.items() if v > 0]
            all_repaired_flaws.extend(action_desc)

            post_verdict = self.critic.audit(current_code)
            score_after = post_verdict.score

            history.append({
                "stage": f"iteration_{iteration}",
                "score": score_after,
                "verdict": post_verdict.verdict,
                "actions": action_desc,
                "flaw_count": len(post_verdict.deductions),
            })

            # Record in journal if available (strictly 6 positional arguments)
            if self.journal and hasattr(self.journal, "record_decision"):
                try:
                    self.journal.record_decision(
                        iteration,
                        target_file,
                        [d.get("dimension", "") for d in post_verdict.deductions],
                        action_desc,
                        score_before,
                        score_after,
                    )
                except Exception as log_err:
                    logger.warning(f"Journal record warning: {log_err}")

            if post_verdict.passed:
                return {
                    "status": "certified",
                    "final_score": score_after,
                    "elevated_code": current_code,
                    "repaired_flaws": all_repaired_flaws,
                    "iterations": iteration,
                    "history": history,
                }

            score_before = score_after

        final_verdict = self.critic.audit(current_code)
        return {
            "status": "certified" if final_verdict.passed else "remediation_incomplete",
            "final_score": final_verdict.score,
            "elevated_code": current_code,
            "repaired_flaws": all_repaired_flaws,
            "iterations": iteration,
            "history": history,
        }
