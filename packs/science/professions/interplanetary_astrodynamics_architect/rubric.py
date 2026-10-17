#!/usr/bin/env python3
"""
Astrodynamics & Interplanetary Trajectory Objective Quality Rubric
Evaluates trajectory design against strict celestial mechanics criteria:
1. Delta-V Propellant Margin (25 pts)
2. Tisserand Parameter Conservation (20 pts)
3. Flyby Periapsis Clearance (20 pts)
4. CR3BP Jacobi Constant Stationkeeping (20 pts)
5. Solar Radiation Pressure Modeling (15 pts)
Total: 100 points. Passing threshold: >= 95 points.
"""

from typing import Dict, Any, List


class AstrodynamicsRubric:
    """
    Evaluates astrodynamics flight software and trajectory plans against
    celestial mechanics benchmarks.
    """

    PASSING_SCORE = 95

    @classmethod
    def evaluate(cls, flaws: List[Dict[str, Any]]) -> Dict[str, Any]:
        score = 100
        deductions = []

        flaw_weights = {
            "lazy_astrodynamic_stub": 30,
            "empty_exception_handler": 25,
            "delta_v_margin_deficit": 25,
            "flyby_periapsis_violation": 25,
            "tisserand_invariance_violation": 20,
            "cr3bp_jacobi_violation": 20,
            "srp_drift_uncompensated": 15
        }

        for flaw in flaws:
            fid = flaw.get("id")
            weight = flaw_weights.get(fid, 10)
            score -= weight
            deductions.append({
                "flaw_id": fid,
                "deduction": weight,
                "message": flaw.get("message")
            })

        score = max(0, score)
        return {
            "score": score,
            "passed": score >= cls.PASSING_SCORE,
            "flaw_count": len(flaws),
            "deductions": deductions
        }
