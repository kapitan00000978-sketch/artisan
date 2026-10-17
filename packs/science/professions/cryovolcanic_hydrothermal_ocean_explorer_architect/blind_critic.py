"""Adversarial Blind Critic for Commander Thorne Sterling - Cryovolcanic & Hydrothermal Ocean Explorer Architect.

Performs independent, unsparing verification against planetary protection bioburden, thermal ice melting, and hydrostatic crush envelopes.
"""

from typing import Dict, Any
from .inspector import CryovolcanicOceanInspector
from .rubric import CryovolcanicOceanRubric


class CryovolcanicOceanBlindCritic:
    """Adversarial critic producing objective quality scores and actionable remediation directives."""

    def __init__(self) -> None:
        self.inspector = CryovolcanicOceanInspector()
        self.rubric = CryovolcanicOceanRubric()

    def audit(self, source_code: str) -> Dict[str, Any]:
        """Conduct ruthless adversarial audit of sub-ice ocean exploration code."""
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
