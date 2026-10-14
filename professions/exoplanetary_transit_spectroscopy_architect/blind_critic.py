"""
Adversarial Blind Critic for Dr. Linus Sterling - Exoplanetary Atmosphere & Transit Spectroscopy Architect.
Performs independent, unsparing verification against astronomical and physical standards.
"""

from typing import Dict, Any
from .inspector import ExoplanetTransitSpecInspector
from .rubric import ExoplanetTransitSpecRubric


class ExoplanetTransitSpecBlindCritic:
    """Adversarial critic producing objective quality scores and actionable remediation directives."""

    def __init__(self):
        self.inspector = ExoplanetTransitSpecInspector()
        self.rubric = ExoplanetTransitSpecRubric()

    def audit(self, source_code: str) -> Dict[str, Any]:
        """Conduct ruthless adversarial audit of transit spectroscopy code."""
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
