"""Adversarial Blind Critic for Commander Jaxen Sterling - Rotating Detonation Wave Propulsion Architect.

Performs independent, unsparing verification against Chapman-Jouguet detonation velocities, DDT run-up limits, and aerospike efficiencies.
"""

from typing import Dict, Any
from .inspector import RotatingDetonationInspector
from .rubric import RotatingDetonationRubric


class RotatingDetonationBlindCritic:
    """Adversarial critic producing objective quality scores and actionable remediation directives."""

    def __init__(self) -> None:
        self.inspector = RotatingDetonationInspector()
        self.rubric = RotatingDetonationRubric()

    def audit(self, source_code: str) -> Dict[str, Any]:
        """Conduct ruthless adversarial audit of rotating detonation rocket engine code."""
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
