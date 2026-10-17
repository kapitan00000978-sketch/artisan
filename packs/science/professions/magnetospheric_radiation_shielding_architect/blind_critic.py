"""Adversarial Blind Critic for Commander Kaelen Vance - Magnetospheric Radiation Shielding Architect.

Performs independent, unsparing verification against Stormer rigidity, HTS coil stability, and ALARA dose envelopes.
"""

from typing import Dict, Any
from .inspector import MagnetosphericShieldInspector
from .rubric import MagnetosphericShieldRubric


class MagnetosphericShieldBlindCritic:
    """Adversarial critic producing objective quality scores and actionable remediation directives."""

    def __init__(self) -> None:
        self.inspector = MagnetosphericShieldInspector()
        self.rubric = MagnetosphericShieldRubric()

    def audit(self, source_code: str) -> Dict[str, Any]:
        """Conduct ruthless adversarial audit of magnetospheric radiation shield code."""
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
