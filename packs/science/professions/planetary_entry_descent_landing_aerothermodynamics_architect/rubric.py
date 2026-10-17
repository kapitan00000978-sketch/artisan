"""Objective 100-Point Scoring Rubric for Planetary EDL Aerothermodynamics.

Formulated by Dr. Caelum 'The Exosphere' Sterling,
Principal Planetary Atmospheric Entry, Descent & Landing (EDL) Aerothermodynamics Architect.
"""

from typing import Any, Dict, List


PASSING_SCORE: float = 95.0


class EDLAerothermodynamicsRubric:
    """Evaluates planetary EDL trajectory, aerothermal heating, and landing implementations."""

    @staticmethod
    def evaluate(inspection_results: Dict[str, Any]) -> Dict[str, Any]:
        """Score an implementation based on inspection results and extracted parameters."""
        findings: List[str] = inspection_results.get("findings", [])
        params: Dict[str, float] = inspection_results.get("parsed_parameters", {})

        scores: Dict[str, float] = {
            "entry_velocity_mach": 15.0,
            "stagnation_heat_flux_and_load": 15.0,
            "tps_safety_and_bondline": 20.0,
            "deceleration_g_load": 15.0,
            "supersonic_parachute_envelope": 15.0,
            "pinpoint_landing_and_touchdown": 10.0,
            "code_integrity_cleanliness": 10.0,
        }

        feedback: List[str] = []

        # 1. Entry Velocity & Mach Envelope (15 pts)
        v_entry = params.get("entry_velocity_km_s")
        if v_entry is not None:
            if v_entry < 5.5 or v_entry > 12.5:
                scores["entry_velocity_mach"] = 0.0
                feedback.append(f"Deduction -15: Entry velocity {v_entry:.2f} km/s outside certified range [5.5, 12.5] km/s.")
        else:
            scores["entry_velocity_mach"] = 0.0
            feedback.append("Deduction -15: Missing entry_velocity_km_s parameter.")

        # 2. Stagnation Heat Flux & Total Integrated Thermal Load (15 pts)
        q_stag = params.get("stagnation_heat_flux_mw_m2")
        q_tot = params.get("total_heat_load_mj_m2")
        if q_stag is not None and q_tot is not None:
            if q_stag < 4.50:
                scores["stagnation_heat_flux_and_load"] -= 10.0
                feedback.append(f"Deduction -10: Stagnation heat flux {q_stag:.2f} MW/m^2 < 4.50 MW/m^2.")
            if q_tot < 120.0:
                scores["stagnation_heat_flux_and_load"] -= 5.0
                feedback.append(f"Deduction -5: Total heat load {q_tot:.1f} MJ/m^2 < 120.0 MJ/m^2.")
        else:
            scores["stagnation_heat_flux_and_load"] = 0.0
            feedback.append("Deduction -15: Missing stagnation_heat_flux_mw_m2 or total_heat_load_mj_m2.")

        # 3. TPS Safety Factor & Bondline Temperature (20 pts)
        sf_tps = params.get("tps_safety_factor")
        t_bond = params.get("bondline_temp_c")
        if sf_tps is not None and t_bond is not None:
            if sf_tps < 1.50:
                scores["tps_safety_and_bondline"] -= 12.0
                feedback.append(f"Deduction -12: TPS safety factor {sf_tps:.2f} < 1.50.")
            if t_bond > 250.0:
                scores["tps_safety_and_bondline"] -= 8.0
                feedback.append(f"Deduction -8: Bondline temperature {t_bond:.1f} C > 250.0 C.")
        else:
            scores["tps_safety_and_bondline"] = 0.0
            feedback.append("Deduction -20: Missing tps_safety_factor or bondline_temp_c.")

        # 4. Deceleration & G-Load Limits (15 pts)
        g_load = params.get("peak_deceleration_g")
        if g_load is not None:
            if g_load > 15.0:
                scores["deceleration_g_load"] = 0.0
                feedback.append(f"Deduction -15: Peak deceleration {g_load:.1f} g > 15.0 g.")
        else:
            scores["deceleration_g_load"] = 0.0
            feedback.append("Deduction -15: Missing peak_deceleration_g parameter.")

        # 5. Supersonic Parachute Extraction Envelope (15 pts)
        m_dep = params.get("parachute_deploy_mach")
        q_dep = params.get("parachute_dynamic_pressure_pa")
        if m_dep is not None and q_dep is not None:
            if m_dep < 1.40 or m_dep > 2.20:
                scores["supersonic_parachute_envelope"] -= 8.0
                feedback.append(f"Deduction -8: Parachute deploy Mach {m_dep:.2f} outside [1.40, 2.20].")
            if q_dep < 300.0 or q_dep > 950.0:
                scores["supersonic_parachute_envelope"] -= 7.0
                feedback.append(f"Deduction -7: Parachute dynamic pressure {q_dep:.1f} Pa outside [300.0, 950.0] Pa.")
        else:
            scores["supersonic_parachute_envelope"] = 0.0
            feedback.append("Deduction -15: Missing parachute_deploy_mach or parachute_dynamic_pressure_pa.")

        # 6. Pinpoint Landing Ellipse & Touchdown Velocity (10 pts)
        ellipse = params.get("landing_ellipse_semi_major_m")
        vz = params.get("touchdown_vz_m_s")
        if ellipse is not None and vz is not None:
            if ellipse > 50.0:
                scores["pinpoint_landing_and_touchdown"] -= 5.0
                feedback.append(f"Deduction -5: Landing ellipse {ellipse:.1f} m > 50.0 m.")
            if vz > 0.75:
                scores["pinpoint_landing_and_touchdown"] -= 5.0
                feedback.append(f"Deduction -5: Touchdown vertical speed {vz:.2f} m/s > 0.75 m/s.")
        else:
            scores["pinpoint_landing_and_touchdown"] = 0.0
            feedback.append("Deduction -10: Missing landing_ellipse_semi_major_m or touchdown_vz_m_s.")

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
