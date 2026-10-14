#!/usr/bin/env python3
"""
Optical Metamaterials & Transformation Optics Objective Quality Rubric
Evaluates negative-index metamaterial, superlens, and cloaking systems against strict electrodynamic criteria:
1. Optical Figure of Merit (FOM >= 15.0) (25 pts)
2. Scattering Cross-Section Reduction (sigma <= 0.05) (25 pts)
3. Superlens Sub-Diffraction Resolution (Delta_x <= 0.10 lambda) (20 pts)
4. Transformation Metric Non-Singularity (det(Lambda) >= 0.10) (15 pts)
5. Ohmic Loss Tangent (tan_delta <= 0.05) (10 pts)
6. SRR Magnetic Coupling Efficiency (eta >= 85%) (5 pts)
Total: 100 points. Passing threshold: >= 95 points.
"""

from typing import Dict, Any, List


class OpticalMetamaterialRubric:
    """
    Evaluates optical metamaterials against electrodynamic loss limits and transformation optics invariants.
    """

    PASSING_SCORE = 95

    @classmethod
    def evaluate(cls, flaws: List[Dict[str, Any]]) -> Dict[str, Any]:
        score = 100
        deductions = []

        flaw_weights = {
            "lazy_metamaterial_stub": 30,
            "empty_exception_handler": 25,
            "figure_of_merit_deficit": 25,
            "scattering_cross_section_violation": 25,
            "superlens_resolution_deficit": 20,
            "metric_determinant_singularity": 20,
            "loss_tangent_overrun": 15,
            "srr_magnetic_coupling_deficit": 10
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
