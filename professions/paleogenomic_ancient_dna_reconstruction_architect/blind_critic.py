"""Adversarial Blind Critic for Dr. Cassian Sterling - Paleogenomic Ancient DNA Reconstruction Architect.

Performs independent, unsparing verification against terminal deamination rates, modern contamination ceilings, and high-coverage sequencing depth.
"""

from typing import Dict, Any
from .inspector import PaleogenomicInspector
from .rubric import PaleogenomicRubric


class PaleogenomicBlindCritic:
    """Adversarial critic producing objective quality scores and actionable remediation directives."""

    def __init__(self) -> None:
        self.inspector = PaleogenomicInspector()
        self.rubric = PaleogenomicRubric()

    def audit(self, source_code: str) -> Dict[str, Any]:
        """Conduct ruthless adversarial audit of paleogenomic ancient DNA code."""
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
