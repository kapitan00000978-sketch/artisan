"""Adversarial Blind Critic for Event Horizon GRMHD Subsystem.

Formulated by Dr. Vespera 'The Singularity' Vance,
Principal Event Horizon General Relativistic Magnetohydrodynamics (GRMHD) Architect.
"""

from typing import Any, Dict, List
from .inspector import GRMHDInspector
from .rubric import GRMHDRubric, PASSING_SCORE


class GRMHDBlindCritic:
    """Ruthless adversarial auditor examining black hole accretion disks and relativistic jets."""

    def __init__(self) -> None:
        self.inspector = GRMHDInspector()
        self.rubric = GRMHDRubric()

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
                "CRITICAL GRMHD REJECTION: Accretion simulation violates relativistic general relativity, magnetic invariants, or solver causality."
            )
            for item in evaluation["feedback"]:
                critique_notes.append(f"Adversarial Objection: {item}")
            for finding in inspection["findings"]:
                if finding not in evaluation["feedback"]:
                    critique_notes.append(f"Physical/Defect Flag: {finding}")

            recommendations.append(
                "Enforce lapse function floor alpha >= 0.05 outside Boyer-Lindquist event horizon."
            )
            recommendations.append(
                "Bound Kerr black hole dimensionless spin |a_*| <= 0.998 to respect Thorne equilibrium."
            )
            recommendations.append(
                "Accumulate large-scale poloidal magnetic flux to achieve MAD state phi_BH >= 50.0."
            )
            recommendations.append(
                "Ensure Blandford-Znajek jet extraction efficiency eta_BZ >= 1.00 (100%)."
            )
            recommendations.append(
                "Constrain conserved-to-primitive Newton-Raphson inversion tolerance <= 1.0e-10."
            )
            recommendations.append(
                "Enforce divergence-free Constraint Transport with div(B) <= 1.0e-12."
            )
            recommendations.append(
                "Resolve relativistic synchrotron cooling timescale tau_synch <= 100.0 s in jet core."
            )
            recommendations.append(
                "Constrain fast magnetosonic phase speed strictly sub-luminal v_ms <= 1.00 c."
            )
            recommendations.append(
                "Apply density floor limiter to prevent funnel magnetization sigma_M exceeding 100.0."
            )
        else:
            critique_notes.append(
                "CERTIFIED COMPLIANT: Event horizon GRMHD simulation strictly satisfies Kerr metric foliation, MAD magnetic flux saturation, and relativistic causality."
            )

        return {
            "score": score,
            "passed": passed,
            "findings": inspection["findings"],
            "parsed_parameters": inspection["parsed_parameters"],
            "critique_notes": critique_notes,
            "recommendations": recommendations,
        }
