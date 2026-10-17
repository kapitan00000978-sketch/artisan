#!/usr/bin/env python3
"""
Direct Fusion Rocket & Magnetoplasmadynamic Propulsion Objective Quality Rubric
Evaluates direct fusion drives and magnetic nozzle thrusters against strict aerospace criteria:
1. Specific Impulse (I_sp >= 10,000 s) (25 pts)
2. Magnetic Nozzle Alfven Mach Detachment (M_A >= 1.50) (25 pts)
3. HTS Magnet Neutron Shielding (q_wall <= 2.0 MW/m^2) (20 pts)
4. Nozzle Beam Divergence (theta_div <= 12.0 deg) (15 pts)
5. Kinetic Thrust Efficiency (eta_thrust >= 65.0%) (10 pts)
6. Plasma Ionization Purity (chi_ion >= 98.0%) (5 pts)
Total: 100 points. Passing threshold: >= 95 points.
"""

from typing import Dict, Any, List


class FusionRocketRubric:
    """
    Evaluates fusion propulsion systems against plasma detachment and thermonuclear flight envelopes.
    """

    PASSING_SCORE = 95

    @classmethod
    def evaluate(cls, flaws: List[Dict[str, Any]]) -> Dict[str, Any]:
        score = 100
        deductions = []

        flaw_weights = {
            "lazy_fusion_rocket_stub": 30,
            "empty_exception_handler": 25,
            "specific_impulse_deficit": 25,
            "magnetic_nozzle_detachment_failure": 25,
            "neutron_wall_flux_overrun": 25,
            "nozzle_divergence_overrun": 20,
            "thrust_power_efficiency_deficit": 15,
            "plasma_ionization_purity_deficit": 10
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
