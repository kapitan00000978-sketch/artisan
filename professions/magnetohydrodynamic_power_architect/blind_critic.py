"""
Adversarial Blind Critic for Dr. Evander Sterling - Magnetohydrodynamic Energy Conversion Architect.
Performs independent, unsparing verification against MHD generator and direct plasma physics standards.
"""

from typing import Dict, Any
from .inspector import MhdPowerInspector
from .rubric import MhdPowerRubric


class MhdPowerBlindCritic:
    """Adversarial critic producing objective quality scores and actionable remediation directives."""

    def __init__(self):
        self.inspector = MhdPowerInspector()
        self.rubric = MhdPowerRubric()

    def audit(self, source_code: str) -> Dict[str, Any]:
        """Conduct ruthless adversarial audit of MHD power generation code."""
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
