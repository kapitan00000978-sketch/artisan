#!/usr/bin/env python3
"""
Adversarial Blind Critic for Astrodynamics & Interplanetary Trajectories
Audits flight code without bias to uncover hidden trajectory errors, propellant depletion,
unmodeled perturbations, or suicidal flyby periapses.
"""

from typing import Dict, Any, List
from .inspector import AstrodynamicsInspector
from .rubric import AstrodynamicsRubric


class AstrodynamicsBlindCritic:
    """
    Adversarial reviewer simulating an independent NASA / ESA Flight Dynamics
    Review Board.
    """

    def __init__(self):
        self.inspector = AstrodynamicsInspector()

    def audit(self, code: str) -> Dict[str, Any]:
        """
        Performs blind adversarial analysis of interplanetary trajectory software.
        """
        flaws = self.inspector.inspect_code(code)
        evaluation = AstrodynamicsRubric.evaluate(flaws)

        critique_notes = []
        for flaw in flaws:
            fid = flaw.get("id")
            sev = flaw.get("severity", "MEDIUM")
            msg = flaw.get("message", "")
            critique_notes.append(f"[{sev}] ({fid}): {msg}")

        return {
            "verdict": "CERTIFIED" if evaluation["passed"] else "REJECTED",
            "score": evaluation["score"],
            "flaw_count": len(flaws),
            "critique_notes": critique_notes,
            "deductions": evaluation["deductions"]
        }
