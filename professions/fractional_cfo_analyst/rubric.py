"""
Victor Montgomery - 100-Point Startup Financial & Unit-Economics Rubric.

Evaluates financial models and venture metrics against strict fiduciary standards.
Passing threshold: 85/100 points.
Veto criteria: Runway < 6 months, Gross Margin < 60%, or LTV/CAC < 2.0x.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.fractional_cfo_analyst.inspector import FinancialInspectionReport, FinancialMetrics


@dataclass
class RubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class FinancialRubric:
    """Rigorous 100-point weighted evaluation rubric for venture finance."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: FinancialInspectionReport) -> RubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Unit Economics & Margin Viability (25 pts)
        # ----------------------------------------------------
        p1_score = 0
        # Gross Margin (10 pts)
        if m.gross_margin_pct >= 0.80:
            p1_score += 10
        elif m.gross_margin_pct >= 0.70:
            p1_score += 7
        elif m.gross_margin_pct >= 0.60:
            p1_score += 4
        else:
            p1_score += 0
            veto_reasons.append(f"Gross margin {m.gross_margin_pct * 100:.1f}% is structurally unviable (< 60%).")
            recommendations.append("Renegotiate infrastructure COGS or increase enterprise pricing tier.")

        # LTV / CAC Ratio (10 pts)
        if m.ltv_cac_ratio >= 4.5:
            p1_score += 10
        elif m.ltv_cac_ratio >= 3.0:
            p1_score += 7
        elif m.ltv_cac_ratio >= 2.0:
            p1_score += 3
        else:
            p1_score += 0
            if m.cac > 0:
                veto_reasons.append(f"LTV/CAC ratio of {m.ltv_cac_ratio:.2f}x burns capital on every acquisition.")
                recommendations.append("Reduce customer acquisition spend or eliminate non-performing marketing channels.")

        # COGS Completeness (5 pts)
        if not m.missing_cogs_items:
            p1_score += 5
        else:
            p1_score += max(0, 5 - (len(m.missing_cogs_items) * 2))
            recommendations.append(f"Include {', '.join(m.missing_cogs_items)} into Cost of Goods Sold.")

        pillar_scores["unit_economics_and_margin"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Payback & Capital Efficiency (20 pts)
        # ----------------------------------------------------
        p2_score = 0
        # CAC Payback (10 pts)
        if m.cac_payback_months > 0 and m.cac_payback_months <= 9.0:
            p2_score += 10
        elif m.cac_payback_months <= 12.0 and m.cac_payback_months > 0:
            p2_score += 8
        elif m.cac_payback_months <= 18.0 and m.cac_payback_months > 0:
            p2_score += 4
        elif m.cac_payback_months == 0:
            p2_score += 5  # No paid CAC data available
        else:
            p2_score += 0
            recommendations.append(f"Accelerate CAC payback ({m.cac_payback_months:.1f} mo) through upfront annual billing discounts.")

        # Burn Multiple (10 pts)
        if m.burn_multiple > 0:
            if m.burn_multiple <= 1.2:
                p2_score += 10
            elif m.burn_multiple <= 1.8:
                p2_score += 7
            elif m.burn_multiple <= 2.5:
                p2_score += 4
            else:
                p2_score += 0
                recommendations.append(f"Burn multiple of {m.burn_multiple:.2f}x is inefficient. Cap headcount growth.")
        else:
            p2_score += 7  # Neutral default if no net new ARR recorded

        pillar_scores["payback_and_capital_efficiency"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: Runway Defense & Solvency (25 pts)
        # ----------------------------------------------------
        p3_score = 0
        # Cash Runway (15 pts)
        if m.runway_months >= 18.0:
            p3_score += 15
        elif m.runway_months >= 12.0:
            p3_score += 10
        elif m.runway_months >= 6.0:
            p3_score += 5
        else:
            p3_score += 0
            veto_reasons.append(f"Critical insolvency threat: only {m.runway_months:.1f} months of runway remaining (< 6.0 mo).")
            recommendations.append("Execute immediate capital preservation freeze (freeze hiring, cut non-essential vendor SaaS).")

        # Contingency and Buffer (10 pts)
        if m.runway_months >= 12.0:
            p3_score += 10
        elif m.runway_months >= 6.0:
            p3_score += 5
        else:
            p3_score += 0

        pillar_scores["runway_defense_and_solvency"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: Financial Rigor & Cohort Integrity (15 pts)
        # ----------------------------------------------------
        p4_score = 0
        # CAC Segmentation (8 pts)
        if not m.has_blended_cac_warning:
            p4_score += 8
        else:
            p4_score += 2
            recommendations.append("Isolate Paid CAC from Organic viral traffic to reveal true acquisition economics.")

        # Churn Realism (7 pts)
        if 0.02 <= m.churn_rate_annual <= 0.30:
            p4_score += 7
        elif m.churn_rate_annual < 0.02:
            p4_score += 3
            recommendations.append("Annual churn rate < 2% is unrealistic for early-stage SaaS; model 5-8% baseline.")
        else:
            p4_score += 2
            recommendations.append(f"Annual churn ({m.churn_rate_annual * 100:.1f}%) is excessively high; focus on onboarding retention.")

        pillar_scores["financial_rigor_and_cohorts"] = p4_score

        # ----------------------------------------------------
        # Pillar 5: Dynamic Scenarios & Stress Testing (15 pts)
        # ----------------------------------------------------
        p5_score = 0
        if m.has_sensitivity_scenarios:
            p5_score += 12
        else:
            p5_score += 4
            recommendations.append("Construct dynamic 3-tier sensitivity model: Base, Bull, and Bear survival stress cases.")

        # Rule of 40 / Cash flow sanity (3 pts)
        if m.rule_of_40_val >= 0.40 or m.runway_months >= 18.0:
            p5_score += 3
        else:
            p5_score += 1

        pillar_scores["dynamic_scenarios_and_stress_testing"] = p5_score

        # Compute total
        total_score = sum(pillar_scores.values())

        # Veto check
        veto_triggered = len(veto_reasons) > 0
        if veto_triggered and total_score >= self.PASSING_THRESHOLD:
            # Force score below threshold if a critical fiduciary veto occurred
            total_score = 74

        is_certified = (total_score >= self.PASSING_THRESHOLD) and not veto_triggered

        return RubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
