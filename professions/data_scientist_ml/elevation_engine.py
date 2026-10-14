"""
Dr. Evelyn Reed - Autonomous Machine Learning Pipeline Elevation Engine.

Transforms contaminated, leaky, or non-reproducible ML pipelines into
hermetically isolated, statistically robust, production-ready architectures.
"""

from typing import Dict, Any, List
import re
from professions.data_scientist_ml.inspector import MLPipelineInspector, MLInspectionReport
from professions.data_scientist_ml.blind_critic import BlindMLCritic, MLDefectLedger


class MLElevationEngine:
    """Elevates vulnerable or contaminated ML pipelines into Oracle-certified standards."""

    def __init__(self):
        self.inspector = MLPipelineInspector()
        self.critic = BlindMLCritic()

    def elevate(self, pipeline_input: Any, max_iterations: int = 3) -> Dict[str, Any]:
        """
        Takes raw ML code string or dict and iteratively refactors it until certified at >= 85/100.
        """
        code = str(pipeline_input)
        remediations_applied: List[str] = []

        for iteration in range(1, max_iterations + 1):
            ledger: MLDefectLedger = self.critic.review(code)
            if ledger.is_certified:
                break

            report: MLInspectionReport = self.inspector.inspect(code)
            m = report.metrics

            # 1. Remediate Preprocessing Leakage
            if m.has_preprocessing_leakage or not m.uses_pipeline_encapsulation:
                code = self._remediate_leakage_and_pipeline(code)
                remediations_applied.append(
                    f"Iteration {iteration}: Encapsulated preprocessing inside hermetic sklearn.pipeline.Pipeline to prevent data leakage."
                )

            # 2. Remediate Temporal Leakage
            if m.is_temporal_data and m.has_temporal_leakage:
                code = self._remediate_temporal_split(code)
                remediations_applied.append(
                    f"Iteration {iteration}: Replaced random split with TimeSeriesSplit to preserve historical causality."
                )

            # 3. Remediate Metric Deception
            if m.has_imbalance_accuracy_trap or m.primary_metric in ["accuracy", "unknown"]:
                code = self._remediate_evaluation_metrics(code, m.target_minority_ratio)
                remediations_applied.append(
                    f"Iteration {iteration}: Switched evaluation to PR-AUC (Average Precision) and F1-macro for class imbalance resilience."
                )

            # 4. Remediate Reproducibility
            if not m.has_deterministic_seed:
                code = self._remediate_seeds(code)
                remediations_applied.append(
                    f"Iteration {iteration}: Pinned deterministic pseudo-random seeds (random_state=42)."
                )

            # 5. Inject Baseline Benchmark
            if not m.has_baseline_comparison:
                code = self._inject_baseline_benchmark(code)
                remediations_applied.append(
                    f"Iteration {iteration}: Injected naive DummyClassifier baseline for comparative benchmarking."
                )

            # 6. Inject Drift Monitoring Guardrails
            if not m.has_drift_monitoring:
                code = self._inject_drift_monitoring(code)
                remediations_applied.append(
                    f"Iteration {iteration}: Configured Population Stability Index (PSI) drift monitoring guardrail."
                )

        final_ledger = self.critic.review(code)

        return {
            "status": "CERTIFIED" if final_ledger.is_certified else "ELEVATED_WITH_CAUTIONS",
            "score": final_ledger.score,
            "passing_threshold": final_ledger.passing_threshold,
            "verdict": final_ledger.verdict,
            "remediations_applied": remediations_applied,
            "elevated_pipeline": code,
            "final_ledger": final_ledger,
            "metrics": self.inspector.inspect(code).metrics
        }

    def _remediate_leakage_and_pipeline(self, code: str) -> str:
        # Remove premature fit_transform on full data
        cleaned = re.sub(
            r"X\s*=\s*\w+scaler\(\)\.fit_transform\(X\)",
            "# PREPROCESSING LEAKAGE ELIMINATED: Scaling moved inside Pipeline",
            code,
            flags=re.IGNORECASE
        )
        if "from sklearn.pipeline import Pipeline" not in cleaned:
            pipeline_block = (
                "\n\n# --- HERMETIC ML PIPELINE (ZERO LEAKAGE) ---\n"
                "from sklearn.pipeline import Pipeline\n"
                "from sklearn.preprocessing import StandardScaler\n"
                "from sklearn.ensemble import HistGradientBoostingClassifier\n\n"
                "ml_pipeline = Pipeline([\n"
                "    ('scaler', StandardScaler()),\n"
                "    ('classifier', HistGradientBoostingClassifier(random_state=42))\n"
                "])\n"
                "ml_pipeline.fit(X_train, y_train)\n"
            )
            cleaned = cleaned + pipeline_block
        return cleaned

    def _remediate_temporal_split(self, code: str) -> str:
        cleaned = re.sub(
            r"train_test_split\([^)]*shuffle\s*=\s*True[^)]*\)",
            "TimeSeriesSplit(n_splits=5)",
            code,
            flags=re.IGNORECASE
        )
        if "from sklearn.model_selection import TimeSeriesSplit" not in cleaned:
            ts_block = (
                "\n\n# --- TEMPORAL CAUSALITY SPLIT ---\n"
                "from sklearn.model_selection import TimeSeriesSplit\n"
                "tscv = TimeSeriesSplit(n_splits=5)\n"
            )
            cleaned = cleaned + ts_block
        return cleaned

    def _remediate_evaluation_metrics(self, code: str, minority_ratio: float) -> str:
        cleaned = re.sub(r"\baccuracy_score\b", "average_precision_score", code)
        if "from sklearn.metrics import average_precision_score" not in cleaned:
            metrics_block = (
                "\n\n# --- IMBALANCE-RESILIENT EVALUATION (PR-AUC & F1-MACRO) ---\n"
                "from sklearn.metrics import average_precision_score, f1_score, classification_report\n"
                "y_pred_proba = ml_pipeline.predict_proba(X_test)[:, 1]\n"
                "y_pred = ml_pipeline.predict(X_test)\n"
                "pr_auc = average_precision_score(y_test, y_pred_proba)\n"
                "macro_f1 = f1_score(y_test, y_pred, average='macro')\n"
                "print(f'PR-AUC: {pr_auc:.4f} | Macro-F1: {macro_f1:.4f}')\n"
            )
            cleaned = cleaned + metrics_block
        return cleaned

    def _remediate_seeds(self, code: str) -> str:
        seed_header = (
            "# --- DETERMINISTIC REPRODUCIBILITY SEEDS ---\n"
            "import numpy as np\n"
            "SEED = 42\n"
            "np.random.seed(SEED)\n\n"
        )
        return seed_header + code

    def _inject_baseline_benchmark(self, code: str) -> str:
        baseline_block = (
            "\n\n# --- NAIVE BASELINE BENCHMARK (CHAMPION VS CHALLENGER) ---\n"
            "from sklearn.dummy import DummyClassifier\n"
            "dummy_baseline = DummyClassifier(strategy='prior', random_state=42)\n"
            "dummy_baseline.fit(X_train, y_train)\n"
            "dummy_score = dummy_baseline.score(X_test, y_test)\n"
        )
        return code + baseline_block

    def _inject_drift_monitoring(self, code: str) -> str:
        drift_block = (
            "\n\n# --- PRODUCTION DATA DRIFT MONITORING (POPULATION STABILITY INDEX) ---\n"
            "def calculate_psi(expected: np.ndarray, actual: np.ndarray, num_buckets: int = 10) -> float:\n"
            "    '''Computes Population Stability Index (PSI) to detect feature distribution drift.'''\n"
            "    percentiles = np.linspace(0, 100, num_buckets + 1)\n"
            "    breakpoints = np.percentile(expected, percentiles)\n"
            "    breakpoints[0] -= 1e-5\n"
            "    breakpoints[-1] += 1e-5\n"
            "    expected_counts = np.histogram(expected, bins=breakpoints)[0] / len(expected)\n"
            "    actual_counts = np.histogram(actual, bins=breakpoints)[0] / len(actual)\n"
            "    expected_counts = np.where(expected_counts == 0, 1e-4, expected_counts)\n"
            "    actual_counts = np.where(actual_counts == 0, 1e-4, actual_counts)\n"
            "    psi = np.sum((actual_counts - expected_counts) * np.log(actual_counts / expected_counts))\n"
            "    return float(psi)\n"
        )
        return code + drift_block
