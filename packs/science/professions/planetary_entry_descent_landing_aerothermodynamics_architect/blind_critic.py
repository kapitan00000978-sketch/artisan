"""Adversarial Blind Critic for Planetary Atmospheric Entry, Descent & Landing (EDL).

Formulated by Dr. Caelum 'The Exosphere' Sterling,
Principal Planetary Atmospheric Entry, Descent & Landing (EDL) Aerothermodynamics Architect.
"""

from typing import Any, Dict, List
from .inspector import EDLAerothermodynamicsInspector
from .rubric import EDLAerothermodynamicsRubric, PASSING_SCORE


class EDLAerothermodynamicsBlindCritic:
    """Ruthless adversarial auditor examining planetary entry trajectories and aerothermal heating."""

    def __init__(self) -> None:
        self.inspector = EDLAerothermodynamicsInspector()
        self.rubric = EDLAerothermodynamicsRubric()

    def audit(self, source_code: str) -> Dict[str, Any]:
        """Adversarially evaluate source code without prior context, returning strict verdict."""
        inspection = self.inspector.inspect_code(source_code)
        evaluation = self.rubric.evaluate(inspection)

        score = evaluation["total_score"]
        passed = evaluation["passed"]

        critique_notes: List[str] = []
        recommendations: List[str] = []

        if not passed:
            critique_notes.append(
                "CRITICAL EDL REJECTION: Trajectory breaches hypersonic aerothermodynamic bounds or threatens capsule structural survival."
            )
            for item in evaluation["feedback"]:
                critique_notes.append(f"Adversarial Objection: {item}")
            for finding in inspection["findings"]:
                if finding not in evaluation["feedback"]:
                    critique_notes.append(f"Physical/Defect Flag: {finding}")

            recommendations.append(
                "Bound planetary entry interface velocity within [5.5, 12.5] km/s."
            )
            recommendations.append(
                "Model peak stagnation heat flux q_stag >= 4.50 MW/m^2 and total heat load Q_total >= 120.0 MJ/m^2."
            )
            recommendations.append(
                "Enforce TPS ablative thickness safety factor SF >= 1.50 and structural bondline temperature T_bond <= 250.0 C."
            )
            recommendations.append(
                "Constrain peak atmospheric deceleration g-load <= 15.0 g."
            )
            recommendations.append(
                "Trigger supersonic parachute deployment strictly within Mach [1.40, 2.20] and dynamic pressure [300, 950] Pa."
            )
            recommendations.append(
                "Enforce terminal touchdown vertical speed vz <= 0.75 m/s and landing ellipse semi-major axis <= 50.0 m."
            )
        else:
            critique_notes.append(
                "CERTIFIED COMPLIANT: Planetary entry trajectory, shock-layer aerothermodynamics, and touchdown velocities satisfy aerospace certification standards."
            )

        verdict = "APPROVED" if passed else "REJECTED"

        return {
            "verdict": verdict,
            "score": score,
            "passing_threshold": PASSING_SCORE,
            "passed": passed,
            "findings": inspection["findings"],
            "critique_notes": critique_notes,
            "recommendations": recommendations,
            "category_scores": evaluation["category_scores"],
        }
