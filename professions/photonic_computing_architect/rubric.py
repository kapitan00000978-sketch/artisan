#!/usr/bin/env python3
"""
Photonic Computing & Neuromorphic Optical Objective Quality Rubric
Evaluates optical matrix processor designs against rigorous physical criteria:
1. Unitary Decomposition Fidelity (25 pts)
2. MZI Extinction Ratio (20 pts)
3. Thermo-Optic Phase Drift Calibration (20 pts)
4. WDM Crosstalk Isolation (20 pts)
5. Photodetector OSNR & MAC Energy Efficiency (15 pts)
Total: 100 points. Passing threshold: >= 95 points.
"""

from typing import Dict, Any, List


class PhotonicRubric:
    """
    Evaluates photonic computing designs against hardware and physical limits.
    """

    PASSING_SCORE = 95

    @classmethod
    def evaluate(cls, flaws: List[Dict[str, Any]]) -> Dict[str, Any]:
        score = 100
        deductions = []

        flaw_weights = {
            "lazy_photonic_stub": 30,
            "empty_exception_handler": 25,
            "unitary_error_violation": 25,
            "wdm_crosstalk_violation": 25,
            "extinction_ratio_deficit": 20,
            "thermal_phase_drift_violation": 20,
            "osnr_precision_deficit": 15,
            "mac_energy_overrun": 10
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
