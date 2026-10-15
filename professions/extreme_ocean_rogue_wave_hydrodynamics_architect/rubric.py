"""Objective 100-Point Scoring Rubric for Extreme Ocean Wave Hydrodynamics.

Formulated by Dr. Silas 'The Wave' Sterling,
Principal Extreme Non-Linear Ocean Wave & Rogue Wave Hydrodynamics Architect.
"""

from typing import Any, Dict, List


PASSING_SCORE: float = 95.0


class ExtremeWaveRubric:
    """Evaluates extreme wave hydrodynamics implementations across 7 objective categories."""

    @staticmethod
    def evaluate(inspection_results: Dict[str, Any]) -> Dict[str, Any]:
        """Score an implementation based on inspection results and extracted parameters."""
        findings: List[str] = inspection_results.get("findings", [])
        params: Dict[str, float] = inspection_results.get("parsed_parameters", {})

        scores: Dict[str, float] = {
            "benjamin_feir_instability": 15.0,
            "rogue_abnormality_criteria": 15.0,
            "steepness_breaking_limits": 20.0,
            "slamming_impact_pressure": 15.0,
            "kurtosis_directional_spread": 10.0,
            "hosm_order_and_airgap": 15.0,
            "code_integrity_cleanliness": 10.0,
        }

        feedback: List[str] = []

        # 1. Benjamin-Feir Modulational Instability (15 pts)
        bfi = params.get("benjamin_feir_index")
        if bfi is not None:
            if bfi < 1.0:
                scores["benjamin_feir_instability"] = 0.0
                feedback.append(f"Deduction -15: BFI {bfi:.2f} < 1.0 (sub-critical modulational instability).")
        else:
            scores["benjamin_feir_instability"] = 0.0
            feedback.append("Deduction -15: Missing benjamin_feir_index parameter.")

        # 2. Rogue Wave Abnormality Criteria (15 pts)
        h_ratio = params.get("rogue_height_ratio")
        crest_ab = params.get("crest_abnormality")
        if h_ratio is not None and crest_ab is not None:
            if h_ratio < 2.0:
                scores["rogue_abnormality_criteria"] -= 10.0
                feedback.append(f"Deduction -10: Rogue height ratio {h_ratio:.2f} < 2.0.")
            if crest_ab < 1.25:
                scores["rogue_abnormality_criteria"] -= 5.0
                feedback.append(f"Deduction -5: Crest abnormality {crest_ab:.2f} < 1.25.")
        else:
            scores["rogue_abnormality_criteria"] = 0.0
            feedback.append("Deduction -15: Missing rogue_height_ratio or crest_abnormality.")

        # 3. Wave Steepness & Kinematic Wave Breaking (20 pts)
        steepness = params.get("steepness")
        if steepness is not None:
            if steepness > 0.44:
                scores["steepness_breaking_limits"] = 0.0
                feedback.append(f"Deduction -20: Steepness {steepness:.3f} > 0.44 (exceeds Stokes breaking limit).")
            elif steepness < 0.10:
                scores["steepness_breaking_limits"] -= 10.0
                feedback.append(f"Deduction -10: Steepness {steepness:.3f} < 0.10 (sea state too mild).")
        else:
            scores["steepness_breaking_limits"] = 0.0
            feedback.append("Deduction -20: Missing steepness parameter.")

        # 4. Slamming Impact Pressure (15 pts)
        p_slam = params.get("slamming_pressure_kpa")
        if p_slam is not None:
            if p_slam < 500.0:
                scores["slamming_impact_pressure"] = 0.0
                feedback.append(f"Deduction -15: Slamming pressure {p_slam:.1f} kPa < 500.0 kPa.")
        else:
            scores["slamming_impact_pressure"] = 0.0
            feedback.append("Deduction -15: Missing slamming_pressure_kpa parameter.")

        # 5. Non-Gaussian Kurtosis & Directional Spreading (10 pts)
        kurt = params.get("kurtosis")
        spread = params.get("directional_spreading_deg")
        if kurt is not None and spread is not None:
            if kurt < 3.0:
                scores["kurtosis_directional_spread"] -= 5.0
                feedback.append(f"Deduction -5: Surface kurtosis {kurt:.2f} < 3.0.")
            if spread > 30.0:
                scores["kurtosis_directional_spread"] -= 5.0
                feedback.append(f"Deduction -5: Directional spreading {spread:.1f} deg > 30.0 deg.")
        else:
            scores["kurtosis_directional_spread"] = 0.0
            feedback.append("Deduction -10: Missing kurtosis or directional_spreading_deg.")

        # 6. High-Order Spectral Non-Linearity Order & Air Gap (15 pts)
        hosm = params.get("hosm_order")
        airgap = params.get("deck_airgap_m")
        if hosm is not None and airgap is not None:
            if int(hosm) < 3:
                scores["hosm_order_and_airgap"] -= 8.0
                feedback.append(f"Deduction -8: HOSM order {int(hosm)} < 3.")
            if airgap < 2.0:
                scores["hosm_order_and_airgap"] -= 7.0
                feedback.append(f"Deduction -7: Deck air gap {airgap:.2f} m < 2.0 m.")
        else:
            scores["hosm_order_and_airgap"] = 0.0
            feedback.append("Deduction -15: Missing hosm_order or deck_airgap_m.")

        # 7. Code Integrity & Cleanliness (10 pts)
        code_flaws = [f for f in findings if "Line" in f or "empty catch" in f or "placeholder" in f]
        if code_flaws:
            scores["code_integrity_cleanliness"] = max(0.0, 10.0 - 5.0 * len(code_flaws))
            for flaw in code_flaws:
                feedback.append(f"Deduction: Code defect: {flaw}")

        total_score = sum(scores.values())
        passed = (total_score >= PASSING_SCORE) and (len(code_flaws) == 0)

        return {
            "total_score": round(total_score, 2),
            "passed": passed,
            "category_scores": scores,
            "feedback": feedback,
            "passing_threshold": PASSING_SCORE,
        }
