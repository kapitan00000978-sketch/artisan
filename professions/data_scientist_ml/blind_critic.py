"""
Dr. Evelyn Reed - Blind ML Critic & Empirical Rigor Inquisitor.

Evaluates machine learning pipelines strictly on statistical power,
leakage isolation, and distribution robustness without accepting practitioner excuses.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.data_scientist_ml.inspector import MLPipelineInspector, MLInspectionReport
from professions.data_scientist_ml.rubric import MLRubric, MLRubricEvaluation


@dataclass
class MLDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    statistical_impact: str
    actionable_remediation: str


@dataclass
class MLDefectLedger:
    verdict: str  # CERTIFIED_ORACLE_CANON or REJECTED_CONTAMINATED
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[MLDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindMLCritic:
    """Scientific adversary reviewing ML architectures strictly for empirical integrity."""

    def __init__(self):
        self.inspector = MLPipelineInspector()
        self.rubric = MLRubric()

    def review(self, pipeline_input: Any) -> MLDefectLedger:
        """
        Runs objective pipeline inspection and adversarial rubric scoring, producing an ML Defect Ledger.
        """
        report: MLInspectionReport = self.inspector.inspect(pipeline_input)
        eval_result: MLRubricEvaluation = self.rubric.evaluate(report)

        defects: List[MLDefect] = []

        # 1. Critical violations -> FATAL defects
        for i, violation in enumerate(report.critical_violations, start=1):
            if "data leakage" in violation.lower():
                title = "Fatal Preprocessing Data Contamination"
                impact = "Test set statistics leaked into training weights; real-world production performance will collapse."
                fix = "Move all feature scaling and imputation inside an sklearn.pipeline.Pipeline object fit only on X_train."
            elif "temporal" in violation.lower():
                title = "Temporal Causality Contamination"
                impact = "Model trains on future observations to predict past events, invalidating historical backtest."
                fix = "Replace random shuffle split with TimeSeriesSplit or fixed chronological cutoff date."
            elif "deceptive metric" in violation.lower():
                title = "Class Imbalance Metric Illusion"
                impact = "High reported accuracy merely reflects majority class prevalence; minority class detection is unmonitored."
                fix = "Evaluate using PR-AUC (Precision-Recall AUC), minority-class F1, and cost-weighted loss."
            elif "missing train/test" in violation.lower():
                title = "Absence of Empirical Validation Split"
                impact = "Evaluation is purely on training data; extreme memorization and zero generalization."
                fix = "Execute stratified train_test_split(test_size=0.20, random_state=42)."
            else:
                title = "Critical Empirical Violation"
                impact = "Invalidates statistical significance of model results."
                fix = "Re-architect pipeline to satisfy empirical isolation standards."

            defects.append(
                MLDefect(
                    defect_id=f"ML-FATAL-{i:03d}",
                    severity="FATAL",
                    title=title,
                    description=violation,
                    statistical_impact=impact,
                    actionable_remediation=fix
                )
            )

        # 2. Veto reasons
        for j, reason in enumerate(eval_result.veto_reasons, start=len(defects) + 1):
            if not any(d.description == reason for d in defects):
                defects.append(
                    MLDefect(
                        defect_id=f"ML-FATAL-{j:03d}",
                        severity="FATAL",
                        title="Statistical Veto Criterion",
                        description=reason,
                        statistical_impact="Unacceptable risk of silent production failure or statistical bias.",
                        actionable_remediation="Refactor ML pipeline according to Oracle benchmarks."
                    )
                )

        # 3. Warnings -> HIGH / MEDIUM defects
        for k, warning in enumerate(report.warnings, start=len(defects) + 1):
            sev = "HIGH" if "non-deterministic" in warning.lower() or "drift" in warning.lower() else "MEDIUM"
            defects.append(
                MLDefect(
                    defect_id=f"ML-WARN-{k:03d}",
                    severity=sev,
                    title="ML Reliability Deficiency",
                    description=warning,
                    statistical_impact="Diminished reproducibility, unmonitored drift, or lack of baseline benchmarking.",
                    actionable_remediation="Pin random_state seeds, add DummyClassifier baseline, and log PSI drift metrics."
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = "CERTIFIED_ORACLE_CANON" if eval_result.is_certified else "REJECTED_CONTAMINATED"

        if eval_result.is_certified:
            summary = (
                f"ORACLE CERTIFIED (Score: {eval_result.total_score}/100). "
                "Data isolation verified, class imbalance calibrated with PR-AUC, "
                "deterministic seeds pinned, and drift guardrails established. Pipeline is production-ready."
            )
        else:
            summary = (
                f"REJECTED BY THE ORACLE (Score: {eval_result.total_score}/100, Threshold: {eval_result.passing_threshold}). "
                f"Identified {fatal_count} fatal statistical leakages and {high_count} operational vulnerabilities. "
                "The pipeline is cheating on contaminated data and cannot be deployed to production."
            )

        return MLDefectLedger(
            verdict=verdict,
            score=eval_result.total_score,
            passing_threshold=eval_result.passing_threshold,
            is_certified=eval_result.is_certified,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
