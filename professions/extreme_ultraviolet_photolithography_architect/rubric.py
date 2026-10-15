"""Objective 100-Point Scoring Rubric for High-NA EUV Photolithography.

Formulated by Dr. Nadia 'The Sub-Micron' Vance,
Principal High-NA EUV Photolithography & Sub-2nm Semiconductor Patterning Architect.
"""

from typing import Any, Dict, List
from .references import calculate_rayleigh_resolution, EUV_WAVELENGTH_NM


PASSING_SCORE: float = 95.0


class EUVLithographyRubric:
    """Evaluates EUV lithography and computational OPC pipelines across 7 objective categories."""

    @staticmethod
    def evaluate(inspection_results: Dict[str, Any]) -> Dict[str, Any]:
        """Score an implementation based on inspection results and extracted parameters."""
        findings: List[str] = inspection_results.get("findings", [])
        params: Dict[str, float] = inspection_results.get("parsed_parameters", {})

        scores: Dict[str, float] = {
            "high_na_optics_resolution": 20.0,
            "stochastic_roughness_lwr_ler": 15.0,
            "exposure_dose_photon_flux": 15.0,
            "overlay_and_cdu_accuracy": 20.0,
            "pellicle_transmission_thermal": 10.0,
            "lpp_source_laser_power": 10.0,
            "code_integrity_cleanliness": 10.0,
        }

        feedback: List[str] = []

        # 1. High-NA Optics & Rayleigh Half-Pitch (20 pts)
        na = params.get("na")
        k1 = params.get("k1_factor")
        if na is not None and k1 is not None:
            if na < 0.55:
                scores["high_na_optics_resolution"] -= 12.0
                feedback.append(f"Deduction -12: NA {na:.2f} < 0.55 (fails High-NA standard).")
            if k1 < 0.30:
                scores["high_na_optics_resolution"] -= 8.0
                feedback.append(f"Deduction -8: k1 {k1:.2f} < 0.30.")
            hp = calculate_rayleigh_resolution(EUV_WAVELENGTH_NM, na, k1)
            if hp > 8.0:
                scores["high_na_optics_resolution"] -= 5.0
                feedback.append(f"Deduction -5: Rayleigh half-pitch {hp:.2f} nm > 8.0 nm.")
        else:
            scores["high_na_optics_resolution"] = 0.0
            feedback.append("Deduction -20: Missing na or k1_factor parameter.")

        # 2. Stochastic Line Width & Edge Roughness (15 pts)
        lwr = params.get("lwr_3sigma_nm")
        ler = params.get("ler_3sigma_nm")
        if lwr is not None and ler is not None:
            if lwr > 1.20:
                scores["stochastic_roughness_lwr_ler"] -= 10.0
                feedback.append(f"Deduction -10: LWR 3-sigma {lwr:.2f} nm > 1.20 nm.")
            if ler > 0.85:
                scores["stochastic_roughness_lwr_ler"] -= 5.0
                feedback.append(f"Deduction -5: LER 3-sigma {ler:.2f} nm > 0.85 nm.")
        else:
            scores["stochastic_roughness_lwr_ler"] = 0.0
            feedback.append("Deduction -15: Missing lwr_3sigma_nm or ler_3sigma_nm.")

        # 3. Exposure Dose & Photon Statistics (15 pts)
        dose = params.get("dose_to_size_mj_cm2")
        if dose is not None:
            if dose < 30.0:
                scores["exposure_dose_photon_flux"] = 0.0
                feedback.append(f"Deduction -15: Dose {dose:.1f} mJ/cm^2 < 30.0 mJ/cm^2 (stochastic defect cliff).")
            elif dose > 75.0:
                scores["exposure_dose_photon_flux"] -= 8.0
                feedback.append(f"Deduction -8: Dose {dose:.1f} mJ/cm^2 > 75.0 mJ/cm^2 (throughput penalty).")
        else:
            scores["exposure_dose_photon_flux"] = 0.0
            feedback.append("Deduction -15: Missing dose_to_size_mj_cm2 parameter.")

        # 4. Overlay & CDU Accuracy (20 pts)
        overlay = params.get("overlay_error_nm")
        cdu = params.get("cdu_3sigma_nm")
        if overlay is not None and cdu is not None:
            if overlay > 1.10:
                scores["overlay_and_cdu_accuracy"] -= 12.0
                feedback.append(f"Deduction -12: Overlay error {overlay:.2f} nm > 1.10 nm.")
            if cdu > 0.60:
                scores["overlay_and_cdu_accuracy"] -= 8.0
                feedback.append(f"Deduction -8: Wafer CDU {cdu:.2f} nm > 0.60 nm.")
        else:
            scores["overlay_and_cdu_accuracy"] = 0.0
            feedback.append("Deduction -20: Missing overlay_error_nm or cdu_3sigma_nm.")

        # 5. Pellicle EUV Transmission (10 pts)
        pellicle = params.get("pellicle_transmission")
        if pellicle is not None:
            if pellicle < 0.90:
                scores["pellicle_transmission_thermal"] = 0.0
                feedback.append(f"Deduction -10: Pellicle transmission {pellicle*100:.1f}% < 90.0%.")
        else:
            scores["pellicle_transmission_thermal"] = 0.0
            feedback.append("Deduction -10: Missing pellicle_transmission parameter.")

        # 6. LPP Tin Source & Laser Power (10 pts)
        freq = params.get("tin_droplet_freq_khz")
        laser = params.get("laser_power_kw")
        if freq is not None and laser is not None:
            if freq < 50.0:
                scores["lpp_source_laser_power"] -= 5.0
                feedback.append(f"Deduction -5: Tin droplet frequency {freq:.1f} kHz < 50.0 kHz.")
            if laser < 30.0:
                scores["lpp_source_laser_power"] -= 5.0
                feedback.append(f"Deduction -5: Laser drive power {laser:.1f} kW < 30.0 kW.")
        else:
            scores["lpp_source_laser_power"] = 0.0
            feedback.append("Deduction -10: Missing tin_droplet_freq_khz or laser_power_kw.")

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
