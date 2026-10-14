#!/usr/bin/env python3
"""
Adversarial Blind Critic for Direct Fusion Rocket & Magnetoplasmadynamic Propulsion Architectures
Audits fusion rocket flight controllers, magnetic nozzle detachment routines, and HTS shielding
without bias to uncover hidden specific impulse deficits, trapped magnetic field lines, divergence losses, or magnet quenching.
"""

from typing import Dict, Any, List
from .inspector import FusionRocketInspector
from .rubric import FusionRocketRubric


class FusionRocketBlindCritic:
    """
    Adversarial reviewer simulating an independent Interplanetary Fusion Propulsion Certification Board.
    """

    def __init__(self):
        self.inspector = FusionRocketInspector()

    def audit(self, code: str) -> Dict[str, Any]:
        """
        Performs blind adversarial analysis of fusion rocket flight software.
        """
        flaws = self.inspector.inspect_code(code)
        evaluation = FusionRocketRubric.evaluate(flaws)

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
