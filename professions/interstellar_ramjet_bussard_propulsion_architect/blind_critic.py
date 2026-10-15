"""Adversarial Blind Critic for Dr. Zephyrus Vance - Interstellar Bussard Ramjet Architect.

Performs independent, unsparing verification against magnetic scoop intake thresholds, relativistic thrust-to-drag margins, and Bremsstrahlung limits.
"""

from typing import Dict, Any
from .inspector import BussardRamjetInspector
from .rubric import BussardRamjetRubric


class BussardRamjetBlindCritic:
    """Adversarial critic producing objective quality scores and actionable remediation directives."""

    def __init__(self) -> None:
        self.inspector = BussardRamjetInspector()
        self.rubric = BussardRamjetRubric()

    def audit(self, source_code: str) -> Dict[str, Any]:
        """Conduct ruthless adversarial audit of interstellar ramjet propulsion code."""
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
