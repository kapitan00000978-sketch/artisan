#!/usr/bin/env python3
"""
Scanning Probe Microscopy & Atomic Manipulation Objective Quality Rubric
Evaluates SPM and single-atom nanotechnology systems against strict atomic-scale criteria:
1. Thermal Drift Rate (25 pts)
2. Tip-Sample Vibration Damping (25 pts)
3. Single-Atom Placement Accuracy (20 pts)
4. UHV Vacuum Integrity (15 pts)
5. Cryogenic Stage Temperature (10 pts)
6. qPlus Tuning Fork Resonator Q-Factor (5 pts)
Total: 100 points. Passing threshold: >= 95 points.
"""

from typing import Dict, Any, List


class AtomicManipulationRubric:
    """
    Evaluates scanning probe microscopes against sub-atomic spatial resolution and cryogenic limits.
    """

    PASSING_SCORE = 95

    @classmethod
    def evaluate(cls, flaws: List[Dict[str, Any]]) -> Dict[str, Any]:
        score = 100
        deductions = []

        flaw_weights = {
            "lazy_atomic_manipulation_stub": 30,
            "empty_exception_handler": 25,
            "thermal_drift_violation": 25,
            "tip_vibration_excessive": 25,
            "atomic_placement_inaccuracy": 20,
            "uhv_pressure_degradation": 20,
            "cryogenic_stage_heating": 15,
            "qplus_quality_factor_deficit": 10
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
