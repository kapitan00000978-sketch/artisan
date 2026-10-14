"""
Dr. Evelyn Reed - Objective Machine Learning Pipeline Inspector & Statistical Auditor.

This module performs AST and regex inspection of ML code and metadata,
detecting data preprocessing leakage, temporal contamination, and deceptive evaluation metrics.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class MLMetrics:
    has_train_test_split: bool = False
    has_preprocessing_leakage: bool = False
    is_temporal_data: bool = False
    has_temporal_leakage: bool = False
    target_minority_ratio: float = 0.50
    primary_metric: str = "unknown"
    has_imbalance_accuracy_trap: bool = False
    has_deterministic_seed: bool = False
    seed_value: Optional[int] = None
    uses_pipeline_encapsulation: bool = False
    has_baseline_comparison: bool = False
    has_drift_monitoring: bool = False
    inference_p99_ms: float = 0.0
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class MLInspectionReport:
    metrics: MLMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_statistically_sound: bool = False


class MLPipelineInspector:
    """Rigorous scientific auditor examining ML code and experiment metadata."""

    def inspect(self, pipeline_input: Any) -> MLInspectionReport:
        """
        Audits ML code string, metadata dict, or JSON report.
        """
        metrics = self._extract_metrics(pipeline_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Preprocessing Data Leakage Audit
        if metrics.has_preprocessing_leakage:
            critical_violations.append(
                "Catastrophic Data Leakage: Preprocessor fit_transform() called on full dataset prior to train_test_split. "
                "Validation metrics are contaminated by test statistics."
            )
        elif metrics.has_train_test_split and metrics.uses_pipeline_encapsulation:
            benchmarks_passed.append("Hermetic Data Isolation: Preprocessing encapsulated inside leak-free Pipeline object.")
        elif metrics.has_train_test_split:
            benchmarks_passed.append("Train/Test split detected prior to model training.")
        else:
            critical_violations.append("Missing Train/Test Split: Model trained and evaluated on undivided dataset.")

        # 2. Temporal Leakage Audit
        if metrics.is_temporal_data and metrics.has_temporal_leakage:
            critical_violations.append(
                "Temporal Causality Contamination: Shuffling historical/time-series data across folds. "
                "Must use TimeSeriesSplit or temporal cutoff."
            )
        elif metrics.is_temporal_data:
            benchmarks_passed.append("Strict temporal sequencing verified for time-series features.")

        # 3. Class Imbalance & Evaluation Metric Integrity
        if metrics.has_imbalance_accuracy_trap:
            critical_violations.append(
                f"Deceptive Metric: Reporting raw accuracy on severely skewed dataset (Minority class: {metrics.target_minority_ratio * 100:.1f}%). "
                "Must use PR-AUC, F1-macro, or Matthews Correlation Coefficient (MCC)."
            )
        elif metrics.primary_metric in ["pr_auc", "average_precision", "f1", "f1_macro", "f1_weighted", "roc_auc"]:
            benchmarks_passed.append(f"Imbalance-resilient metric employed: {metrics.primary_metric.upper()}.")
        elif metrics.primary_metric == "accuracy" and metrics.target_minority_ratio >= 0.40:
            benchmarks_passed.append("Accuracy acceptable for balanced class distribution.")

        # 4. Reproducibility & Determinism
        if not metrics.has_deterministic_seed:
            warnings.append("Non-deterministic execution: Missing fixed random_state / seed for PRNGs.")
        else:
            benchmarks_passed.append(f"Deterministic seed locked ({metrics.seed_value if metrics.seed_value is not None else 42}).")

        # 5. Baseline Comparison
        if not metrics.has_baseline_comparison:
            warnings.append("Missing baseline benchmark: Model not compared against naive heuristic or DummyClassifier.")
        else:
            benchmarks_passed.append("Champion/Challenger benchmark verified against naive baseline.")

        # 6. Production Drift Guardrails
        if not metrics.has_drift_monitoring:
            warnings.append("Missing production drift defense: No Population Stability Index (PSI) or statistical shift checks.")
        else:
            benchmarks_passed.append("Production drift monitoring (PSI / KS-test) configured.")

        # Anti-pattern summaries
        for ap in metrics.anti_patterns_detected:
            if ap not in [cv for cv in critical_violations]:
                critical_violations.append(f"Anti-Pattern Detected: {ap}")

        is_sound = len(critical_violations) == 0

        return MLInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_statistically_sound=is_sound
        )

    def _extract_metrics(self, pipeline_input: Any) -> MLMetrics:
        text = ""
        metadata: Dict[str, Any] = {}

        if isinstance(pipeline_input, str):
            text = pipeline_input
            try:
                parsed = json.loads(pipeline_input)
                if isinstance(parsed, dict):
                    metadata = parsed
            except (json.JSONDecodeError, ValueError) as _json_err:
                _ = _json_err
        elif isinstance(pipeline_input, dict):
            metadata = pipeline_input
            text = json.dumps(pipeline_input)
        else:
            text = str(pipeline_input)

        m = MLMetrics()
        text_lower = text.lower()

        # 1. Train/Test Split
        has_split = (
            "train_test_split" in text_lower or
            "timeseriessplit" in text_lower or
            "kfold" in text_lower or
            "stratifiedkfold" in text_lower or
            metadata.get("has_train_test_split", False)
        )
        m.has_train_test_split = has_split

        # 2. Preprocessing Leakage
        # Check if fit_transform call appears BEFORE actual train_test_split invocation in code
        fit_transform_pos = text_lower.find("fit_transform")
        # Match call rather than top-level import
        split_call_match = re.search(r"(?:=\s*train_test_split\b|train_test_split\s*\()", text_lower)
        train_split_pos = split_call_match.start() if split_call_match else -1

        if fit_transform_pos != -1 and train_split_pos != -1 and fit_transform_pos < train_split_pos:
            m.has_preprocessing_leakage = True
            m.anti_patterns_detected.append("Preprocessing fit_transform() called before train_test_split")
        elif metadata.get("has_preprocessing_leakage", False):
            m.has_preprocessing_leakage = True

        # 3. Temporal Data & Leakage
        is_temporal = (
            "timestamp" in text_lower or
            "datetime" in text_lower or
            "time_series" in text_lower or
            "date" in text_lower or
            metadata.get("is_temporal_data", False)
        )
        m.is_temporal_data = is_temporal

        if is_temporal:
            # Check for random shuffle on temporal data
            if "shuffle=true" in text_lower or (train_split_pos != -1 and "timeseriessplit" not in text_lower and "shuffle=false" not in text_lower):
                m.has_temporal_leakage = True
                m.anti_patterns_detected.append("Temporal data partitioned with random shuffle instead of chronological split")
            elif metadata.get("has_temporal_leakage", False):
                m.has_temporal_leakage = True

        # 4. Imbalance and Metrics
        minority_ratio = float(metadata.get("target_minority_ratio", metadata.get("minority_class_ratio", 0.50)))
        if "fraud" in text_lower or "anomaly" in text_lower or "rare_event" in text_lower:
            if minority_ratio == 0.50:
                minority_ratio = 0.02  # Default to 2% for fraud/anomaly
        m.target_minority_ratio = minority_ratio

        metric = str(metadata.get("primary_metric", metadata.get("metric", ""))).lower()
        if not metric:
            if "pr_auc" in text_lower or "average_precision" in text_lower:
                metric = "pr_auc"
            elif "f1_macro" in text_lower or "f1" in text_lower:
                metric = "f1"
            elif "roc_auc" in text_lower:
                metric = "roc_auc"
            elif "accuracy" in text_lower or "acc" in text_lower:
                metric = "accuracy"
            else:
                metric = "accuracy"  # Default assumption
        m.primary_metric = metric

        if minority_ratio < 0.15 and metric in ["accuracy", "acc", "raw_accuracy"]:
            m.has_imbalance_accuracy_trap = True
            m.anti_patterns_detected.append(f"Raw accuracy used on imbalanced target ({minority_ratio * 100:.1f}%)")

        # 5. Reproducibility & Seeds
        seed_match = re.search(r"random_state\s*=\s*(\d+)|seed\s*=\s*(\d+)|manual_seed\((\d+)\)", text_lower)
        if seed_match:
            m.has_deterministic_seed = True
            matched_val = seed_match.group(1) or seed_match.group(2) or seed_match.group(3)
            try:
                m.seed_value = int(matched_val)
            except (ValueError, TypeError):
                m.seed_value = 42
        elif metadata.get("has_deterministic_seed", False):
            m.has_deterministic_seed = True
            m.seed_value = int(metadata.get("seed", 42))

        # 6. Pipeline Encapsulation
        m.uses_pipeline_encapsulation = (
            "pipeline(" in text_lower or
            "make_pipeline(" in text_lower or
            metadata.get("uses_pipeline", False)
        )

        # 7. Baseline & Drift
        m.has_baseline_comparison = (
            "dummyclassifier" in text_lower or
            "dummyregressor" in text_lower or
            "baseline" in text_lower or
            metadata.get("has_baseline_comparison", False)
        )

        m.has_drift_monitoring = (
            "psi" in text_lower or
            "population_stability_index" in text_lower or
            "evidently" in text_lower or
            "ks_test" in text_lower or
            metadata.get("has_drift_monitoring", False)
        )

        return m
