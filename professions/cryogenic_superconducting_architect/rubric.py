#!/usr/bin/env python3
"""
Cryogenic Superconducting & Dilution Refrigerator Objective Quality Rubric
Evaluates millikelvin refrigeration systems against strict thermodynamic criteria:
1. Mixing Chamber Base Temperature (25 pts)
2. Superconducting Critical Current Margin (25 pts)
3. Parasitic Heat Leak Isolation (20 pts)
4. Pulse-Tube Vibration Damping (15 pts)
5. Vacuum Insulation Integrity (15 pts)
Total: 100 points. Passing threshold: >= 95 points.
"""

from typing import Dict, Any, List


class CryogenicRubric:
    """
    Evaluates cryogenic systems against thermodynamic and quantum hardware limits.
    """

    PASSING_SCORE = 95

    @classmethod
    def evaluate(cls, flaws: List[Dict[str, Any]]) -> Dict[str, Any]:
        score = 100
        deductions = []

        flaw_weights = {
            "lazy_cryogenic_stub": 30,
            "empty_exception_handler": 25,
            "vacuum_insulation_loss": 25,
            "base_temperature_elevation": 25,
            "superconducting_margin_deficit": 25,
            "parasitic_heat_leak_overrun": 20,
            "cryostat_vibration_violation": 15
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
