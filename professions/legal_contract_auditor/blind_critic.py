"""
Arthur Pendelton - Blind Legal Critic & Commercial Litigation Inquisitor.

Evaluates contract drafts purely on legal exposure, enforceable title transfer,
and liability defense without hearing business optimism or commercial excuses.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.legal_contract_auditor.inspector import ContractInspector, LegalInspectionReport
from professions.legal_contract_auditor.rubric import ContractRubric, LegalRubricEvaluation


@dataclass
class LegalDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    exposure_impact: str
    actionable_redline: str


@dataclass
class LegalDefectLedger:
    verdict: str  # CERTIFIED_IRONCLAD or REJECTED_HIGH_RISK
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[LegalDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindLegalCritic:
    """Adversarial commercial counsel reviewing agreements strictly for courtroom resilience."""

    def __init__(self):
        self.inspector = ContractInspector()
        self.rubric = ContractRubric()

    def review(self, contract_input: Any) -> LegalDefectLedger:
        """
        Runs objective clause inspection and adversarial rubric scoring, producing a Defect Ledger.
        """
        report: LegalInspectionReport = self.inspector.inspect(contract_input)
        eval_result: LegalRubricEvaluation = self.rubric.evaluate(report)

        defects: List[LegalDefect] = []

        # 1. Critical violations -> FATAL defects
        for i, violation in enumerate(report.critical_violations, start=1):
            if "uncapped liability" in violation.lower() or "liability exposure" in violation.lower():
                title = "Existential Uncapped Liability"
                impact = "Company faces unlimited bankruptcy damages in event of catastrophic breach or lost data."
                redline = "Cap aggregate liability to fees paid in preceding 12 months; waive consequential damages."
            elif "future ip assignment" in violation.lower() or "vague future" in violation.lower():
                title = "Defective Title Transfer (Stanford v. Roche Trap)"
                impact = "Contractor retains underlying patent/copyright ownership; investor title is clouded."
                redline = "Replace 'agrees to assign' with present conveyance: 'hereby irrevocably assigns, transfers, and conveys'."
            elif "unilateral indemnification" in violation.lower():
                title = "Asymmetric Indemnification Black Hole"
                impact = "Company is bound to pay adversary's third-party defense fees with zero reciprocal protection."
                redline = "Convert into mutual indemnification strictly bounded to third-party IP infringement."
            elif "consequential damages" in violation.lower():
                title = "Missing Consequential Damages Waiver"
                impact = "Opens courtroom discovery to speculative lost profits and punitive multipliers."
                redline = "Insert mutual waiver of indirect, incidental, consequential, and punitive damages."
            else:
                title = "Critical Contractual Flaw"
                impact = "High litigation vulnerability upon dispute."
                redline = "Remediate clause to institutional commercial standards."

            defects.append(
                LegalDefect(
                    defect_id=f"LEGAL-FATAL-{i:03d}",
                    severity="FATAL",
                    title=title,
                    description=violation,
                    exposure_impact=impact,
                    actionable_redline=redline
                )
            )

        # 2. Veto reasons
        for j, reason in enumerate(eval_result.veto_reasons, start=len(defects) + 1):
            if not any(d.description == reason for d in defects):
                defects.append(
                    LegalDefect(
                        defect_id=f"LEGAL-FATAL-{j:03d}",
                        severity="FATAL",
                        title="Fiduciary Legal Veto",
                        description=reason,
                        exposure_impact="Disqualifying contractual imbalance.",
                        actionable_redline="Execute standard institutional clause replacement."
                    )
                )

        # 3. Warnings -> HIGH / MEDIUM defects
        for k, warning in enumerate(report.warnings, start=len(defects) + 1):
            sev = "HIGH" if "cure" in warning.lower() or "termination" in warning.lower() else "MEDIUM"
            defects.append(
                LegalDefect(
                    defect_id=f"LEGAL-WARN-{k:03d}",
                    severity=sev,
                    title="Contractual Deficiency Warning",
                    description=warning,
                    exposure_impact="Procedural disadvantage or legal friction during termination.",
                    actionable_redline="Add formal notice, cure period, and customary confidentiality exclusions."
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = "CERTIFIED_IRONCLAD" if eval_result.is_certified else "REJECTED_HIGH_RISK"

        if eval_result.is_certified:
            summary = (
                f"IRONCLAD CERTIFIED (Score: {eval_result.total_score}/100). "
                "Mutual 12-month liability cap verified, present IP assignment perfected, "
                "and reciprocal indemnification bounded. Contract provides bulletproof defense in litigation."
            )
        else:
            summary = (
                f"REJECTED BY THE IRONCLAD COUNSEL (Score: {eval_result.total_score}/100, Threshold: {eval_result.passing_threshold}). "
                f"Detected {fatal_count} fatal exposures and {high_count} substantive defects. "
                "Signing this agreement in its current form represents gross legal negligence."
            )

        return LegalDefectLedger(
            verdict=verdict,
            score=eval_result.total_score,
            passing_threshold=eval_result.passing_threshold,
            is_certified=eval_result.is_certified,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
