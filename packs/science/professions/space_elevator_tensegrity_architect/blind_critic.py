"""Adversarial Blind Critic for Dr. Valerius Sterling - Space Elevator & Active Tensegrity Megastructure Architect.

Performs independent, unsparing verification against megastructure tensegrity, taper ratios, and wave damping bounds.
"""

from typing import Dict, Any
from .inspector import SpaceElevatorInspector
from .rubric import SpaceElevatorRubric


class SpaceElevatorBlindCritic:
    """Adversarial critic producing objective quality scores and actionable remediation directives."""

    def __init__(self) -> None:
        self.inspector = SpaceElevatorInspector()
        self.rubric = SpaceElevatorRubric()

    def audit(self, source_code: str) -> Dict[str, Any]:
        """Conduct ruthless adversarial audit of space elevator and tensegrity megastructure code."""
        flaws = self.inspector.inspect_source(source_code)
        evaluation = self.rubric.evaluate(flaws)

        verdict = "APPROVED" if evaluation.passed else "REJECTED"

        return {
            "verdict": verdict,
            "score": evaluation.score,
            "passed": evaluation.passed,
            "flaw_count": len(flaws),
            "flaws": flaws,
            "deductions": evaluation.deductions,
            "summary": evaluation.summary
        }
