"""Adversarial Blind Critic for Extreme Ocean Wave Hydrodynamics.

Formulated by Dr. Silas 'The Wave' Sterling,
Principal Extreme Non-Linear Ocean Wave & Rogue Wave Hydrodynamics Architect.
"""

from typing import Any, Dict, List
from .inspector import ExtremeWaveInspector
from .rubric import ExtremeWaveRubric, PASSING_SCORE


class ExtremeWaveBlindCritic:
    """Ruthless adversarial auditor examining wave kinematics and rogue wave simulations."""

    def __init__(self) -> None:
        self.inspector = ExtremeWaveInspector()
        self.rubric = ExtremeWaveRubric()

    def audit(self, source_code: str) -> Dict[str, Any]:
        """Adversarially evaluate code without prior context, returning strict verdict."""
        inspection = self.inspector.inspect_code(source_code)
        evaluation = self.rubric.evaluate(inspection)

        score = evaluation["total_score"]
        passed = evaluation["passed"]

        critique_notes: List[str] = []
        recommendations: List[str] = []

        if not passed:
            critique_notes.append(
                "CRITICAL HYDRODYNAMIC REJECTION: Code breaches non-linear wave invariants or contains amateur software flaws."
            )
            for item in evaluation["feedback"]:
                critique_notes.append(f"Adversarial Objection: {item}")
            for finding in inspection["findings"]:
                if finding not in evaluation["feedback"]:
                    critique_notes.append(f"Physical/Defect Flag: {finding}")

            recommendations.append(
                "Enforce Benjamin-Feir index BFI >= 1.0 and surface elevation kurtosis K >= 3.0 to model non-Gaussian rogue seas."
            )
            recommendations.append(
                "Bound non-linear wave steepness within ka in [0.10, 0.44] and enforce Stokes kinematic breaking dissipation."
            )
            recommendations.append(
                "Calculate hydrodynamic wave slamming impact pressure P_slam >= 500.0 kPa via Wagner-von Karman dynamics."
            )
            recommendations.append(
                "Maintain positive cellar deck air gap >= 2.0 m and eliminate all empty catches and placeholder stubs."
            )
        else:
            critique_notes.append(
                "CERTIFIED COMPLIANT: Hydrodynamic wave kinematics and extreme rogue wave bounds meet non-linear ocean physics benchmarks."
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
