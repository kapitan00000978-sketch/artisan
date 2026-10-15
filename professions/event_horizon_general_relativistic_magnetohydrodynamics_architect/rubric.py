"""Objective 100-Point Scoring Rubric for Event Horizon GRMHD Subsystem.

Formulated by Dr. Vespera 'The Singularity' Vance,
Principal Event Horizon General Relativistic Magnetohydrodynamics (GRMHD) Architect.
"""

from typing import Any, Dict, List


PASSING_SCORE: float = 95.0


class GRMHDRubric:
    """Evaluates event horizon GRMHD simulation and relativistic accretion disk implementations."""

    @staticmethod
    def evaluate(inspection_results: Dict[str, Any]) -> Dict[str, Any]:
        """Score an implementation based on inspection results and extracted parameters."""
        findings: List[str] = inspection_results.get("findings", [])
        params: Dict[str, float] = inspection_results.get("parsed_parameters", {})

        scores: Dict[str, float] = {
            "adm_lapse_and_spin": 20.0,
            "mad_flux_and_bz_power": 20.0,
            "primitive_recovery_inversion": 15.0,
            "magnetic_divergence_free": 15.0,
            "relativistic_causality_and_cooling": 10.0,
            "funnel_magnetization_floor": 10.0,
            "code_integrity_cleanliness": 10.0,
        }

        feedback: List[str] = []

        # 1. 3+1 ADM Lapse Floor & Kerr Spin Limit (20 pts)
        alpha = params.get("lapse_alpha")
        spin = params.get("dimensionless_spin")
        if alpha is not None and spin is not None:
            if alpha < 0.05:
                scores["adm_lapse_and_spin"] -= 10.0
                feedback.append(f"Deduction -10: Lapse function alpha {alpha:.4f} < 0.05.")
            if abs(spin) > 0.998:
                scores["adm_lapse_and_spin"] -= 10.0
                feedback.append(f"Deduction -10: Spin |a_*| {abs(spin):.4f} > 0.998 exceeds Thorne limit.")
        else:
            scores["adm_lapse_and_spin"] = 0.0
            feedback.append("Deduction -20: Missing lapse_alpha or dimensionless_spin parameter.")

        # 2. MAD Horizon Magnetic Flux & Blandford-Znajek Power (20 pts)
        phi_bh = params.get("mad_magnetic_flux")
        eta_bz = params.get("blandford_znajek_efficiency")
        if phi_bh is not None and eta_bz is not None:
            if phi_bh < 50.0:
                scores["mad_flux_and_bz_power"] -= 10.0
                feedback.append(f"Deduction -10: MAD flux phi_BH {phi_bh:.1f} < 50.0 (SANE under-magnetized state).")
            if eta_bz < 1.00:
                scores["mad_flux_and_bz_power"] -= 10.0
                feedback.append(f"Deduction -10: Blandford-Znajek efficiency {eta_bz:.2f} < 1.00.")
        else:
            scores["mad_flux_and_bz_power"] = 0.0
            feedback.append("Deduction -20: Missing mad_magnetic_flux or blandford_znajek_efficiency.")

        # 3. Primitive Recovery Inversion Residual (15 pts)
        prim_tol = params.get("primitive_inversion_tolerance")
        if prim_tol is not None:
            if prim_tol > 1.0e-10:
                scores["primitive_recovery_inversion"] = 0.0
                feedback.append(f"Deduction -15: Primitive inversion tolerance {prim_tol:.2e} > 1.0e-10.")
        else:
            scores["primitive_recovery_inversion"] = 0.0
            feedback.append("Deduction -15: Missing primitive_inversion_tolerance parameter.")

        # 4. Divergence-Free Constraint Transport (15 pts)
        div_b = params.get("div_b_error")
        if div_b is not None:
            if div_b > 1.0e-12:
                scores["magnetic_divergence_free"] = 0.0
                feedback.append(f"Deduction -15: Magnetic field divergence {div_b:.2e} > 1.0e-12.")
        else:
            scores["magnetic_divergence_free"] = 0.0
            feedback.append("Deduction -15: Missing div_b_error parameter.")

        # 5. Relativistic Causality & Synchrotron Cooling (10 pts)
        v_ms = params.get("magnetosonic_speed_c")
        tau_sync = params.get("synchrotron_cooling_time_s")
        if v_ms is not None and tau_sync is not None:
            if v_ms > 1.00:
                scores["relativistic_causality_and_cooling"] -= 5.0
                feedback.append(f"Deduction -5: Fast magnetosonic speed {v_ms:.3f} c > 1.00 c breaches causality.")
            if tau_sync > 100.0:
                scores["relativistic_causality_and_cooling"] -= 5.0
                feedback.append(f"Deduction -5: Synchrotron cooling time {tau_sync:.1f} s > 100.0 s.")
        else:
            scores["relativistic_causality_and_cooling"] = 0.0
            feedback.append("Deduction -10: Missing magnetosonic_speed_c or synchrotron_cooling_time_s.")

        # 6. Funnel Magnetization Ceiling (10 pts)
        sigma = params.get("magnetization_sigma")
        if sigma is not None:
            if sigma > 100.0:
                scores["funnel_magnetization_floor"] = 0.0
                feedback.append(f"Deduction -10: Magnetization sigma {sigma:.1f} > 100.0 causes floor crash.")
        else:
            scores["funnel_magnetization_floor"] = 0.0
            feedback.append("Deduction -10: Missing magnetization_sigma parameter.")

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
