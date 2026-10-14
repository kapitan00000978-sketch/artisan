"""
Dr. Evelyn Reed - 100-Point Machine Learning & Statistical Rigor Rubric.

Evaluates ML pipelines against empirical data science standards.
Passing threshold: 85/100 points.
Veto criteria: Preprocessing data leakage, temporal shuffling, or deceptive accuracy on imbalanced data.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.data_scientist_ml.inspector import MLInspectionReport, MLMetrics


@dataclass
class MLRubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class MLRubric:
    """Rigorous 100-point weighted evaluation rubric for ML architectures."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: MLInspectionReport) -> MLRubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Data Hygiene & Leakage Isolation (25 pts)
        # ----------------------------------------------------
        p1_score = 0
        if not m.has_train_test_split:
            veto_reasons.append("Model evaluated without formal train/test partitioning.")
            recommendations.append("Implement strict train_test_split(test_size=0.20, random_state=42).")
        elif m.has_preprocessing_leakage:
            veto_reasons.append("Catastrophic Data Leakage: fit_transform() called on full dataset before splitting.")
            recommendations.append("Encapsulate feature transformations inside sklearn.pipeline.Pipeline.")
        else:
            p1_score += 15

        if m.is_temporal_data:
            if m.has_temporal_leakage:
                veto_reasons.append("Temporal Contamination: Random shuffling applied to chronological time-series data.")
                recommendations.append("Replace random split with TimeSeriesSplit or chronological cutoff date.")
            else:
                p1_score += 10
        else:
            p1_score += 10  # Non-temporal, full credit if no leakage

        pillar_scores["data_hygiene_and_leakage"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Evaluation Metric Rigor (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if m.has_imbalance_accuracy_trap:
            veto_reasons.append(
                f"Deceptive Metric: Raw accuracy masks failure on minority class ({m.target_minority_ratio * 100:.1f}%)."
            )
            recommendations.append("Switch primary evaluation metric to PR-AUC (Average Precision) and F1-macro.")
        elif m.primary_metric in ["pr_auc", "average_precision", "f1_macro", "mcc"]:
            p2_score += 15
        elif m.primary_metric in ["roc_auc", "f1_weighted", "balanced_accuracy"]:
            p2_score += 12
        elif m.primary_metric == "accuracy" and m.target_minority_ratio >= 0.40:
            p2_score += 15
        else:
            p2_score += 5
            recommendations.append("Specify explicit probabilistic evaluation metric (PR-AUC, ROC-AUC, or Log-Loss).")

        # Stratified / Cross-validation rigor (10 pts)
        if m.has_train_test_split and not m.has_temporal_leakage:
            p2_score += 10
        else:
            p2_score += 4

        pillar_scores["metric_selection_and_rigor"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: Reproducibility & Pipeline Lineage (20 pts)
        # ----------------------------------------------------
        p3_score = 0
        if m.has_deterministic_seed:
            p3_score += 10
        else:
            recommendations.append("Set deterministic random seeds (random_state=42, np.random.seed(42)).")

        if m.uses_pipeline_encapsulation:
            p3_score += 10
        else:
            recommendations.append("Wrap preprocessors and estimators into sklearn.pipeline.Pipeline to prevent leakages.")

        pillar_scores["reproducibility_and_lineage"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: Baseline Benchmark & Overfitting Defense (15 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.has_baseline_comparison:
            p4_score += 10
        else:
            p4_score += 3
            recommendations.append("Benchmark trained model against DummyClassifier(strategy='prior') to verify incremental value.")

        p4_score += 5  # Standard regularization & capacity credit

        pillar_scores["baseline_and_overfitting"] = p4_score

        # ----------------------------------------------------
        # Pillar 5: Production Survivability & Drift Defense (15 pts)
        # ----------------------------------------------------
        p5_score = 0
        if m.has_drift_monitoring:
            p5_score += 10
        else:
            p5_score += 3
            recommendations.append("Implement Population Stability Index (PSI) drift monitoring for production inference.")

        p5_score += 5  # Input bounds validation credit

        pillar_scores["production_and_drift_defense"] = p5_score

        total_score = sum(pillar_scores.values())

        # Veto enforcement
        veto_triggered = len(veto_reasons) > 0
        if veto_triggered and total_score >= self.PASSING_THRESHOLD:
            total_score = 70

        is_certified = (total_score >= self.PASSING_THRESHOLD) and not veto_triggered

        return MLRubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
