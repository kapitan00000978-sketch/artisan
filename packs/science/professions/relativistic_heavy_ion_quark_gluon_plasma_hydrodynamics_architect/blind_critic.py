"""Adversarial Blind Critic for Relativistic QGP Hydrodynamics Subsystem.

Formulated by Dr. Kaelen 'The Quark' Sterling,
Principal Relativistic Heavy-Ion Quark-Gluon Plasma (QGP) Hydrodynamics Architect.
"""

from typing import Any, Dict, List
from .inspector import QGPHydrodynamicsInspector
from .rubric import QGPHydrodynamicsRubric, PASSING_SCORE


class QGPHydrodynamicsBlindCritic:
    """Ruthless adversarial auditor examining QGP viscous relativistic fluid implementations."""

    def __init__(self) -> None:
        self.inspector = QGPHydrodynamicsInspector()
        self.rubric = QGPHydrodynamicsRubric()

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
                "CRITICAL QGP REJECTION: Heavy-ion hydrodynamic simulation violates KSS quantum bounds, Israel-Stewart causality, or lattice QCD thermodynamics."
            )
            for item in evaluation["feedback"]:
                critique_notes.append(f"Adversarial Objection: {item}")
            for finding in inspection["findings"]:
                if finding not in evaluation["feedback"]:
                    critique_notes.append(f"Physical/Defect Flag: {finding}")

            recommendations.append(
                "Calibrate shear viscosity to entropy density ratio eta/s within [0.08, 0.20]."
            )
            recommendations.append(
                "Constrain bulk viscosity peak zeta/s <= 0.10 near deconfinement crossover."
            )
            recommendations.append(
                "Align pseudo-critical deconfinement temperature T_c to 155.0 +/- 5.0 MeV."
            )
            recommendations.append(
                "Initialize relativistic hydrodynamics at proper time tau_0 in [0.20, 0.60] fm/c."
            )
            recommendations.append(
                "Set jet quenching transport coefficient q_hat >= 1.20 GeV^2/fm."
            )
            recommendations.append(
                "Enforce Israel-Stewart shear relaxation time ratio tau_pi / (eta/(s*T)) >= 5.0."
            )
            recommendations.append(
                "Trigger Cooper-Frye hadronization sampling at T_fo in [130.0, 150.0] MeV."
            )
            recommendations.append(
                "Calibrate pressure gradients to yield elliptic flow v_2 in [0.05, 0.15]."
            )
            recommendations.append(
                "Constrain speed of sound softest point c_s^2(T_c) >= 0.14."
            )
        else:
            critique_notes.append(
                "CERTIFIED COMPLIANT: Relativistic QGP hydrodynamics simulation strictly satisfies Israel-Stewart causality, KSS viscosity limits, and lattice QCD equation of state."
            )

        return {
            "score": score,
            "passed": passed,
            "findings": inspection["findings"],
            "parsed_parameters": inspection["parsed_parameters"],
            "critique_notes": critique_notes,
            "recommendations": recommendations,
        }
