"""Adversarial Blind Critic for High-NA EUV Photolithography.

Formulated by Dr. Nadia 'The Sub-Micron' Vance,
Principal High-NA EUV Photolithography & Sub-2nm Semiconductor Patterning Architect.
"""

from typing import Any, Dict, List
from .inspector import EUVLithographyInspector
from .rubric import EUVLithographyRubric, PASSING_SCORE


class EUVLithographyBlindCritic:
    """Ruthless adversarial auditor examining High-NA EUV computational lithography code."""

    def __init__(self) -> None:
        self.inspector = EUVLithographyInspector()
        self.rubric = EUVLithographyRubric()

    def audit(self, source_code: str) -> Dict[str, Any]:
        """Adversarially evaluate source code without prior context, returning strict verdict."""
        inspection = self.inspector.inspect_code(source_code)
        evaluation = self.rubric.evaluate(inspection)

        score = evaluation["total_score"]
        passed = evaluation["passed"]

        critique_notes: List[str] = []
        recommendations: List[str] = []

        if not passed:
            critique_notes.append(
                "CRITICAL LITHOGRAPHIC REJECTION: Code breaches High-NA physical invariants or contains stochastic defect risks."
            )
            for item in evaluation["feedback"]:
                critique_notes.append(f"Adversarial Objection: {item}")
            for finding in inspection["findings"]:
                if finding not in evaluation["feedback"]:
                    critique_notes.append(f"Physical/Defect Flag: {finding}")

            recommendations.append(
                "Adopt 0.55 NA anamorphic projection optics and enforce Rayleigh half-pitch HP <= 8.0 nm."
            )
            recommendations.append(
                "Bound 3-sigma line width roughness LWR <= 1.20 nm and LER <= 0.85 nm via optimized photon dose."
            )
            recommendations.append(
                "Constrain exposure dose within [30.0, 75.0] mJ/cm^2 to avoid stochastic microbridges."
            )
            recommendations.append(
                "Enforce dedicated chuck overlay error Delta_overlay <= 1.10 nm and wafer CDU <= 0.60 nm."
            )
            recommendations.append(
                "Ensure carbon nanotube pellicle transmission >= 90.0% and pulsed laser power >= 30.0 kW."
            )
        else:
            critique_notes.append(
                "CERTIFIED COMPLIANT: High-NA EUV parameters, stochastic shot noise margins, and overlay tolerances satisfy sub-2nm foundry standards."
            )

        verdict = "APPROVED" if passed else "REJECTED"

        return {
            "verdict": verdict,
            "score": score,
            "passing_threshold": PASSING_SCORE,
            "passed": passed,
            "findings": inspection["findings"],
            "critique_notes": critique_notes,
            "recommendations": recommendations,
            "category_scores": evaluation["category_scores"],
        }
