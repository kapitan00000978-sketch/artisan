"""Adversarial Blind Critic for Dr. Hector Vance - Stellarator Magnet & Twisted Coil Fusion Architect.

Performs independent, unsparing verification against rotational transform stability, coil curvature, and divertor heat exhaust envelopes.
"""

from typing import Dict, Any
from .inspector import StellaratorFusionInspector
from .rubric import StellaratorFusionRubric


class StellaratorFusionBlindCritic:
    """Adversarial critic producing objective quality scores and actionable remediation directives."""

    def __init__(self) -> None:
        self.inspector = StellaratorFusionInspector()
        self.rubric = StellaratorFusionRubric()

    def audit(self, source_code: str) -> Dict[str, Any]:
        """Conduct ruthless adversarial audit of stellarator fusion code."""
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
