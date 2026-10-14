"""
Dr. Evelyn Reed - Machine Learning & Statistical Rigor Reference Standards.

This module codifies empirical data science standards, leakage detection rules,
class-imbalance evaluation metrics, and production drift thresholds.
"""

from typing import Dict, Any, List


ML_EVALUATION_STANDARDS: Dict[str, Dict[str, Any]] = {
    "balanced_distribution": {
        "imbalance_ratio_threshold": 0.40,  # Minority class >= 40%
        "mandatory_metrics": ["accuracy", "roc_auc", "f1_macro"],
        "recommended_cv": "StratifiedKFold"
    },
    "moderately_imbalanced": {
        "imbalance_ratio_threshold": 0.10,  # Minority class 10% - 40%
        "mandatory_metrics": ["balanced_accuracy", "roc_auc", "f1_weighted"],
        "recommended_cv": "StratifiedKFold"
    },
    "severely_imbalanced": {
        "imbalance_ratio_threshold": 0.0,   # Minority class < 10% (Fraud, Anomaly, Medical)
        "mandatory_metrics": ["pr_auc", "average_precision", "f1_minority", "mcc"],
        "prohibited_primary_metrics": ["raw_accuracy"],
        "recommended_loss": ["focal_loss", "cost_sensitive_weighting"]
    }
}

DRIFT_THRESHOLDS_PSI: Dict[str, Dict[str, Any]] = {
    "stable": {
        "max_psi": 0.10,
        "action": "Model distribution stable. Production inference approved."
    },
    "moderate_shift": {
        "max_psi": 0.25,
        "action": "Warning: Marginal feature drift observed. Queue scheduled model retraining."
    },
    "critical_drift": {
        "max_psi": 999.0,
        "action": "CRITICAL: Severe distribution shift detected. Fallback to heuristic baseline and trigger emergency alert."
    }
}

TOXIC_ML_ANTI_PATTERNS: List[Dict[str, str]] = [
    {
        "id": "preprocessing_leakage",
        "indicator": "Calling fit() or fit_transform() on preprocessors before train_test_split.",
        "risk": "Validation metrics are contaminated by test data distribution; severe production degradation.",
        "severity": "FATAL"
    },
    {
        "id": "temporal_shuffling",
        "indicator": "Using random train_test_split(shuffle=True) or standard KFold on sequential/time-series data.",
        "risk": "Future information leaks into training folds; invalidates causality and real-world backtest.",
        "severity": "FATAL"
    },
    {
        "id": "imbalance_accuracy_illusion",
        "indicator": "Reporting standard accuracy on imbalanced targets where minority class is < 15%.",
        "risk": "A trivial majority-class predictor masks total model failure on the critical minority class.",
        "severity": "FATAL"
    },
    {
        "id": "non_deterministic_randomness",
        "indicator": "Training models, splitting data, or initializing weights without fixed random_state / seeds.",
        "risk": "Unreproducible results; impossible to debug regression across pipeline runs.",
        "severity": "HIGH"
    },
    {
        "id": "missing_baseline_comparison",
        "indicator": "Evaluating complex neural/tree models without comparing against DummyClassifier / simple heuristic.",
        "risk": "Over-engineered complexity that performs worse than naive business rules.",
        "severity": "MEDIUM"
    }
]

CANONICAL_LEAK_FREE_TEMPLATE: str = (
    "# Deterministic Seed Initialization\n"
    "SEED = 42\n"
    "np.random.seed(SEED)\n\n"
    "# Strict Train / Test Split Before ANY Transformation\n"
    "X_train, X_test, y_train, y_test = train_test_split(\n"
    "    X, y, test_size=0.20, random_state=SEED, stratify=y\n"
    ")\n\n"
    "# Leak-Free Pipeline Execution\n"
    "from sklearn.pipeline import Pipeline\n"
    "from sklearn.preprocessing import StandardScaler\n"
    "from sklearn.ensemble import HistGradientBoostingClassifier\n\n"
    "pipeline = Pipeline([\n"
    "    ('scaler', StandardScaler()),\n"
    "    ('classifier', HistGradientBoostingClassifier(random_state=SEED))\n"
    "])\n"
    "pipeline.fit(X_train, y_train)\n"
)


class MLReferenceLibrary:
    """Provides empirical ML benchmarks and statistical standards."""

    @staticmethod
    def get_evaluation_standards() -> Dict[str, Dict[str, Any]]:
        return ML_EVALUATION_STANDARDS

    @staticmethod
    def get_drift_thresholds() -> Dict[str, Dict[str, Any]]:
        return DRIFT_THRESHOLDS_PSI

    @staticmethod
    def get_toxic_anti_patterns() -> List[Dict[str, str]]:
        return TOXIC_ML_ANTI_PATTERNS

    @staticmethod
    def get_leak_free_template() -> str:
        return CANONICAL_LEAK_FREE_TEMPLATE
