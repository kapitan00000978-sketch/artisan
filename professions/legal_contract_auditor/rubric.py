"""
Arthur Pendelton - 100-Point Commercial Contract & Legal Risk Rubric.

Evaluates commercial contracts against institutional legal standards.
Passing threshold: 85/100 points.
Veto criteria: Uncapped unilateral liability, missing/defective IP assignment, or unilateral indemnification.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.legal_contract_auditor.inspector import LegalInspectionReport, ContractMetrics


@dataclass
class LegalRubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class ContractRubric:
    """Rigorous 100-point weighted evaluation rubric for commercial agreements."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: LegalInspectionReport) -> LegalRubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Liability & Sovereign Risk Capping (25 pts)
        # ----------------------------------------------------
        p1_score = 0
        if m.has_limitation_of_liability and not m.is_liability_uncapped:
            p1_score += 10
            if m.is_liability_mutual:
                p1_score += 5
            else:
                veto_reasons.append("Liability cap is one-sided; counterparty has zero exposure limit.")
                recommendations.append("Make limitation of liability strictly mutual for both parties.")
        else:
            veto_reasons.append("Catastrophic risk: Contract lacks an enforceable limitation of liability cap.")
            recommendations.append("Insert standard 12-month mutual aggregate liability cap.")

        if m.has_consequential_damages_waiver:
            p1_score += 10
        else:
            recommendations.append("Insert explicit mutual waiver of indirect, consequential, and punitive damages.")

        pillar_scores["liability_and_risk_capping"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Intellectual Property Sovereignty (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if m.is_present_ip_assignment:
            p2_score += 15
        elif m.has_ip_assignment:
            p2_score += 5
            veto_reasons.append("Defective IP Assignment: Uses future tense ('agrees to assign'). Fails to convey present title.")
            recommendations.append("Replace future promise with present conveyance: 'hereby irrevocably assigns, transfers, and conveys'.")
        else:
            veto_reasons.append("Total absence of Intellectual Property Assignment provision.")
            recommendations.append("Draft comprehensive Work Product IP assignment clause.")

        if m.has_work_made_for_hire:
            p2_score += 5
        else:
            recommendations.append("Add 'work made for hire' designation for copyrightable deliverables.")

        if m.has_ip_assignment:
            p2_score += 5

        pillar_scores["intellectual_property_sovereignty"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: Indemnification Symmetry & Defense (20 pts)
        # ----------------------------------------------------
        p3_score = 0
        if m.has_indemnification:
            if m.is_indemnification_mutual:
                p3_score += 20
            else:
                p3_score += 8
                veto_reasons.append("Unilateral indemnification forces one party to absorb third-party liability without reciprocity.")
                recommendations.append("Convert unilateral indemnity into balanced mutual defense for third-party IP infringement.")
        else:
            p3_score += 10  # Neutral if no indemnification, but recommended
            recommendations.append("Add reciprocal third-party IP infringement indemnification.")

        pillar_scores["indemnification_symmetry"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: Termination & Remedy Mechanics (15 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.has_termination_clause:
            p4_score += 5
        else:
            recommendations.append("Insert formal termination provisions (for cause and for convenience).")

        if m.has_cure_period and m.cure_period_days >= 30:
            p4_score += 10
        elif m.has_cure_period:
            p4_score += 6
            recommendations.append(f"Extend cure period from {m.cure_period_days} days to institutional standard 30 days.")
        else:
            recommendations.append("Require 30-day written notice and right to cure prior to termination for material breach.")

        pillar_scores["termination_and_remedy"] = p4_score

        # ----------------------------------------------------
        # Pillar 5: Confidentiality & Dispute Resolution (15 pts)
        # ----------------------------------------------------
        p5_score = 0
        if m.has_confidentiality:
            p5_score += 5
            if m.has_nda_exclusions:
                p5_score += 5
            else:
                recommendations.append("Incorporate standard carve-outs to confidentiality (public domain, required by law).")
        else:
            recommendations.append("Add comprehensive bilateral confidentiality covenants.")

        if m.has_dispute_resolution and m.has_neutral_governing_law:
            p5_score += 5
        elif m.has_dispute_resolution or m.has_neutral_governing_law:
            p5_score += 3
        else:
            recommendations.append("Specify neutral governing law (Delaware/NY) and binding AAA/JAMS arbitration.")

        pillar_scores["confidentiality_and_dispute_resolution"] = p5_score

        total_score = sum(pillar_scores.values())

        # Veto enforcement
        veto_triggered = len(veto_reasons) > 0
        if veto_triggered and total_score >= self.PASSING_THRESHOLD:
            total_score = 72

        is_certified = (total_score >= self.PASSING_THRESHOLD) and not veto_triggered

        return LegalRubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
