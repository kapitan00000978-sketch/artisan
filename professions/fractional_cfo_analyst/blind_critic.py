"""
Victor Montgomery - Blind Financial Critic & Capital Defense Inquisitor.

Evaluates financial data with zero tolerance for founder bias, vanity metrics,
or spreadsheet optimism. Generates an adversarial Defect Ledger with prioritized remediation tasks.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.fractional_cfo_analyst.inspector import FinancialInspector, FinancialInspectionReport
from professions.fractional_cfo_analyst.rubric import FinancialRubric, RubricEvaluation


@dataclass
class FinancialDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM, LOW
    title: str
    description: str
    metric_impact: str
    actionable_fix: str


@dataclass
class DefectLedger:
    verdict: str  # CERTIFIED_FORTRESS or REJECTED_UNVIABLE
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[FinancialDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindFinancialCritic:
    """Adversarial critic examining financial models strictly by numerical evidence."""

    def __init__(self):
        self.inspector = FinancialInspector()
        self.rubric = FinancialRubric()

    def review(self, data: Any) -> DefectLedger:
        """
        Runs mathematical inspection and adversarial rubric scoring, producing a Defect Ledger.
        """
        report: FinancialInspectionReport = self.inspector.inspect(data)
        eval_result: RubricEvaluation = self.rubric.evaluate(report)

        defects: List[FinancialDefect] = []

        # 1. Critical violations -> FATAL defects
        for i, violation in enumerate(report.critical_violations, start=1):
            severity = "FATAL"
            if "gross margin" in violation.lower():
                title = "Deficient Gross Margin Structure"
                fix = "Renegotiate vendor cloud rates or raise price floor on basic subscriptions."
            elif "runway" in violation.lower() or "insolvency" in violation.lower():
                title = "Immediate Cash Insolvency Threat"
                fix = "Activate emergency spending freeze and secure bridge debt/equity within 60 days."
            elif "ltv/cac" in violation.lower() or "unit economics" in violation.lower():
                title = "Capital-Destructive Unit Economics"
                fix = "Cut low-converting paid acquisition channels; focus on organic expansion & annual contracts."
            elif "cogs" in violation.lower():
                title = "Omission of Core Infrastructure from COGS"
                fix = "Properly allocate hosting, customer support, and gateway fees into direct gross cost."
            elif "cac payback" in violation.lower():
                title = "Working Capital Strangled by Lengthy Payback"
                fix = "Shift SMB pricing to upfront annual billing with 15% discount incentive."
            else:
                title = "Fiduciary Violation"
                fix = "Address underlying financial imbalance immediately."

            defects.append(
                FinancialDefect(
                    defect_id=f"FATAL-{i:03d}",
                    severity=severity,
                    title=title,
                    description=violation,
                    metric_impact="Structural cash destruction or immediate bankruptcy risk",
                    actionable_fix=fix
                )
            )

        # 2. Veto reasons if not covered
        for j, reason in enumerate(eval_result.veto_reasons, start=len(defects) + 1):
            if not any(d.description == reason for d in defects):
                defects.append(
                    FinancialDefect(
                        defect_id=f"FATAL-{j:03d}",
                        severity="FATAL",
                        title="Fiduciary Veto Criterion Triggered",
                        description=reason,
                        metric_impact="Automatic disqualification from institutional investment/survival",
                        actionable_fix="Restructure balance sheet and reduce monthly burn immediately."
                    )
                )

        # 3. Warnings -> HIGH / MEDIUM defects
        for k, warning in enumerate(report.warnings, start=len(defects) + 1):
            sev = "HIGH" if "blended" in warning.lower() or "runway" in warning.lower() else "MEDIUM"
            defects.append(
                FinancialDefect(
                    defect_id=f"WARN-{k:03d}",
                    severity=sev,
                    title="Financial Fragility Warning",
                    description=warning,
                    metric_impact="Suboptimal capital efficiency or hidden operational risk",
                    actionable_fix="Model dynamic sensitivity scenarios and segment paid customer acquisition."
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = "CERTIFIED_FORTRESS" if eval_result.is_certified else "REJECTED_UNVIABLE"

        if eval_result.is_certified:
            summary = (
                f"FORTRESS CERTIFIED (Score: {eval_result.total_score}/100). "
                f"Gross margin at {report.metrics.gross_margin_pct * 100:.1f}%, "
                f"Runway at {report.metrics.runway_months:.1f} months, "
                f"LTV/CAC at {report.metrics.ltv_cac_ratio:.2f}x. Model withstands institutional scrutiny."
            )
        else:
            summary = (
                f"REJECTED BY THE FORTRESS (Score: {eval_result.total_score}/100, Threshold: {eval_result.passing_threshold}). "
                f"Identified {fatal_count} fatal accounting/solvency defects and {high_count} operational warnings. "
                "The business model as modeled will exhaust working capital or bleed investor reserves."
            )

        return DefectLedger(
            verdict=verdict,
            score=eval_result.total_score,
            passing_threshold=eval_result.passing_threshold,
            is_certified=eval_result.is_certified,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
