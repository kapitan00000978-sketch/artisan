"""Adversarial Blind Critic for Dr. Morwenna Sterling - Closed-Loop ECLSS & Bioregenerative Space Architect.

Performs independent, unsparing verification against stoichiometric Sabatier/Bosch reactions and ECLSS safety margins.
"""

from typing import Dict, Any
from .inspector import ECLSSInspector
from .rubric import ECLSSRubric


class ECLSSBlindCritic:
    """Adversarial critic producing objective quality scores and actionable remediation directives."""

    def __init__(self) -> None:
        self.inspector = ECLSSInspector()
        self.rubric = ECLSSRubric()

    def audit(self, source_code: str) -> Dict[str, Any]:
        """Conduct ruthless adversarial audit of closed-loop ECLSS and life support code."""
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
