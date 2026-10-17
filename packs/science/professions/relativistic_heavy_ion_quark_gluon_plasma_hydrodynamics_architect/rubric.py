"""Objective 100-Point Scoring Rubric for Relativistic QGP Hydrodynamics.

Formulated by Dr. Kaelen 'The Quark' Sterling,
Principal Relativistic Heavy-Ion Quark-Gluon Plasma (QGP) Hydrodynamics Architect.
"""

from typing import Any, Dict, List


PASSING_SCORE: float = 95.0


class QGPHydrodynamicsRubric:
    """Evaluates relativistic heavy-ion QGP simulation and hydrodynamic implementations."""

    @staticmethod
    def evaluate(inspection_results: Dict[str, Any]) -> Dict[str, Any]:
        """Score an implementation based on inspection results and extracted parameters."""
        findings: List[str] = inspection_results.get("findings", [])
        params: Dict[str, float] = inspection_results.get("parsed_parameters", {})

        scores: Dict[str, float] = {
            "viscosity_kss_and_bulk": 20.0,
            "israel_stewart_causality": 20.0,
            "lattice_qcd_eos_and_tc": 15.0,
            "thermalization_and_freezeout": 15.0,
            "jet_quenching_transport": 10.0,
            "elliptic_flow_anisotropy": 10.0,
            "code_integrity_cleanliness": 10.0,
        }

        feedback: List[str] = []

        # 1. Viscosity & KSS Bound Compliance (20 pts)
        eta_s = params.get("eta_over_s")
        zeta_s = params.get("zeta_over_s")
        if eta_s is not None and zeta_s is not None:
            if eta_s < 0.08 or eta_s > 0.20:
                scores["viscosity_kss_and_bulk"] -= 12.0
                feedback.append(f"Deduction -12: Shear viscosity eta/s {eta_s:.4f} outside [0.08, 0.20].")
            if zeta_s > 0.10:
                scores["viscosity_kss_and_bulk"] -= 8.0
                feedback.append(f"Deduction -8: Bulk viscosity zeta/s {zeta_s:.3f} > 0.10.")
        else:
            scores["viscosity_kss_and_bulk"] = 0.0
            feedback.append("Deduction -20: Missing eta_over_s or zeta_over_s parameter.")

        # 2. Israel-Stewart Hyperbolic Causality (20 pts)
        is_ratio = params.get("israel_stewart_relaxation_ratio")
        if is_ratio is not None:
            if is_ratio < 5.0:
                scores["israel_stewart_causality"] = 0.0
                feedback.append(f"Deduction -20: Israel-Stewart relaxation ratio {is_ratio:.2f} < 5.0 breaches causality.")
        else:
            scores["israel_stewart_causality"] = 0.0
            feedback.append("Deduction -20: Missing israel_stewart_relaxation_ratio parameter.")

        # 3. Lattice QCD EoS & Critical Temperature T_c (15 pts)
        tc = params.get("qcd_critical_temp_mev")
        cs2 = params.get("sound_speed_sq_tc")
        if tc is not None and cs2 is not None:
            if tc < 150.0 or tc > 160.0:
                scores["lattice_qcd_eos_and_tc"] -= 10.0
                feedback.append(f"Deduction -10: QCD critical temp {tc:.1f} MeV outside [150, 160] MeV.")
            if cs2 < 0.14:
                scores["lattice_qcd_eos_and_tc"] -= 5.0
                feedback.append(f"Deduction -5: Speed of sound c_s^2(T_c) {cs2:.3f} < 0.14.")
        else:
            scores["lattice_qcd_eos_and_tc"] = 0.0
            feedback.append("Deduction -15: Missing qcd_critical_temp_mev or sound_speed_sq_tc.")

        # 4. Thermalization Proper Time & Freeze-Out (15 pts)
        tau0 = params.get("thermalization_tau_fm_c")
        t_fo = params.get("freezeout_temp_mev")
        if tau0 is not None and t_fo is not None:
            if tau0 < 0.20 or tau0 > 0.60:
                scores["thermalization_and_freezeout"] -= 8.0
                feedback.append(f"Deduction -8: Thermalization tau_0 {tau0:.2f} fm/c outside [0.20, 0.60] fm/c.")
            if t_fo < 130.0 or t_fo > 150.0:
                scores["thermalization_and_freezeout"] -= 7.0
                feedback.append(f"Deduction -7: Freeze-out temp {t_fo:.1f} MeV outside [130, 150] MeV.")
        else:
            scores["thermalization_and_freezeout"] = 0.0
            feedback.append("Deduction -15: Missing thermalization_tau_fm_c or freezeout_temp_mev.")

        # 5. Jet Quenching Transport Coefficient (10 pts)
        qhat = params.get("jet_quenching_qhat_gev2_fm")
        if qhat is not None:
            if qhat < 1.20:
                scores["jet_quenching_transport"] = 0.0
                feedback.append(f"Deduction -10: Jet quenching q_hat {qhat:.2f} GeV^2/fm < 1.20 GeV^2/fm.")
        else:
            scores["jet_quenching_transport"] = 0.0
            feedback.append("Deduction -10: Missing jet_quenching_qhat_gev2_fm parameter.")

        # 6. Anisotropic Elliptic Flow v_2 (10 pts)
        v2 = params.get("elliptic_flow_v2")
        if v2 is not None:
            if v2 < 0.05 or v2 > 0.15:
                scores["elliptic_flow_anisotropy"] = 0.0
                feedback.append(f"Deduction -10: Elliptic flow v_2 {v2:.3f} outside [0.05, 0.15].")
        else:
            scores["elliptic_flow_anisotropy"] = 0.0
            feedback.append("Deduction -10: Missing elliptic_flow_v2 parameter.")

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
