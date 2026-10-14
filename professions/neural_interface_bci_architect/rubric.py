#!/usr/bin/env python3
"""
Neural Interface & Biomechatronic BCI Objective Quality Rubric
Evaluates intracortical neural implants and BCI systems against strict neurobiological criteria:
1. Shannon Charge Injection Safety (k <= 1.75) (25 pts)
2. Cortical Tissue Thermal Preservation (Delta_T <= 1.0 C) (25 pts)
3. Active Biphasic Charge Balance (Delta_Q <= 1.0 pC) (20 pts)
4. Closed-Loop Decoding Latency (tau <= 10.0 ms) (15 pts)
5. Electrode-Tissue Interface Impedance (|Z| <= 500 kohm) (10 pts)
6. Front-End Common-Mode Rejection Ratio (CMRR >= 90 dB) (5 pts)
Total: 100 points. Passing threshold: >= 95 points.
"""

from typing import Dict, Any, List


class NeuralInterfaceRubric:
    """
    Evaluates neural interfaces against neurobiological safety limits and BCI timing invariants.
    """

    PASSING_SCORE = 95

    @classmethod
    def evaluate(cls, flaws: List[Dict[str, Any]]) -> Dict[str, Any]:
        score = 100
        deductions = []

        flaw_weights = {
            "lazy_neural_interface_stub": 30,
            "empty_exception_handler": 25,
            "shannon_safety_index_violation": 25,
            "tissue_heating_overrun": 25,
            "residual_charge_imbalance_violation": 20,
            "decoding_latency_excessive": 20,
            "electrode_impedance_overrun": 15,
            "front_end_cmrr_deficit": 10
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
