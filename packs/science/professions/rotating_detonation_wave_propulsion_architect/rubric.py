"""Objective 100-point rubric for Commander Jaxen Sterling - Rotating Detonation Wave Propulsion Architect.

Enforces a 95+ passing threshold for continuous rotating detonation rocket engine systems.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class RubricEvaluation:
    score: int
    passed: bool
    deductions: List[Dict[str, Any]]
    summary: str


class RotatingDetonationRubric:
    """100-point objective rubric evaluator for Rotating Detonation Rocket Engines."""

    PASSING_THRESHOLD: int = 95

    SEVERITY_WEIGHTS: Dict[str, int] = {
        "CRITICAL": 25,
        "HIGH": 12,
        "MEDIUM": 6,
        "LOW": 3,
    }

    def evaluate(self, flaws: List[Dict[str, Any]]) -> RubricEvaluation:
        """Evaluate identified flaws and compute final score."""
        score = 100
        deductions: List[Dict[str, Any]] = []

        for flaw in flaws:
            severity = flaw.get("severity", "MEDIUM")
            points = self.SEVERITY_WEIGHTS.get(severity, 6)
            score -= points
            deductions.append({
                "flaw_id": flaw.get("id", "UNKNOWN"),
                "severity": severity,
                "points_deducted": points,
                "description": flaw.get("description", "")
            })

        score = max(0, score)
        passed = score >= self.PASSING_THRESHOLD

        if passed:
            summary = f"PASSED: Score {score}/100 meets Commander Jaxen Sterling's 95+ RDRE benchmark."
        else:
            summary = f"FAILED: Score {score}/100 falls below Commander Jaxen Sterling's 95+ threshold."

        return RubricEvaluation(
            score=score,
            passed=passed,
            deductions=deductions,
            summary=summary
        )
