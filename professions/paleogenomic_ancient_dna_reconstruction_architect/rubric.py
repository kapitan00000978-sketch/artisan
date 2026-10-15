"""Objective 100-point rubric for Dr. Cassian Sterling - Paleogenomic Ancient DNA Reconstruction Architect.

Enforces a 95+ passing threshold for ancient DNA authentication and paleogenomic reconstruction systems.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class RubricEvaluation:
    score: int
    passed: bool
    deductions: List[Dict[str, Any]]
    summary: str


class PaleogenomicRubric:
    """100-point objective rubric evaluator for Ancient DNA Reconstruction systems."""

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
            summary = f"PASSED: Score {score}/100 meets Dr. Cassian Sterling's 95+ paleogenomic benchmark."
        else:
            summary = f"FAILED: Score {score}/100 falls below Dr. Cassian Sterling's 95+ threshold."

        return RubricEvaluation(
            score=score,
            passed=passed,
            deductions=deductions,
            summary=summary
        )
