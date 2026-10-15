"""Objective 100-point rubric for Dr. Eliana Sterling - Optical Lattice Clock & Quantum Metrology Architect.

Enforces a 95/100 minimum passing threshold.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class RubricEvaluation:
    """Evaluation result from the Optical Lattice Clock rubric."""
    score: int
    passed: bool
    deductions: List[Dict[str, Any]] = field(default_factory=list)
    summary: str = ""


class OpticalClockRubric:
    """100-point strict grading rubric for Optical Lattice Atomic Clocks and Quantum Metrology."""

    PASSING_SCORE = 95

    SEVERITY_WEIGHTS = {
        "CRITICAL": 25,
        "HIGH": 15,
        "MEDIUM": 8,
        "LOW": 3
    }

    def evaluate(self, flaws: List[Dict[str, Any]]) -> RubricEvaluation:
        """Calculate rubric score based on detected flaws."""
        total_deduction = 0
        deductions = []

        for flaw in flaws:
            severity = flaw.get("severity", "MEDIUM")
            points = self.SEVERITY_WEIGHTS.get(severity, 10)
            total_deduction += points
            deductions.append({
                "flaw_id": flaw.get("id"),
                "severity": severity,
                "points_deducted": points,
                "description": flaw.get("description", "")
            })

        score = max(0, 100 - total_deduction)
        passed = score >= self.PASSING_SCORE

        if passed:
            summary = f"PASSED: Score {score}/100 meets the {self.PASSING_SCORE}-point threshold of Dr. Eliana Sterling."
        else:
            summary = f"REJECTED: Score {score}/100 is below the {self.PASSING_SCORE}-point threshold. Remediations required."

        return RubricEvaluation(
            score=score,
            passed=passed,
            deductions=deductions,
            summary=summary
        )
