"""
Unit tests for Dr. Evelyn Reed (Staff Data Scientist & ML Systems Architect Subsystem).
"""

import pytest
from professions.data_scientist_ml.references import MLReferenceLibrary
from professions.data_scientist_ml.inspector import MLPipelineInspector
from professions.data_scientist_ml.rubric import MLRubric
from professions.data_scientist_ml.blind_critic import BlindMLCritic
from professions.data_scientist_ml.elevation_engine import MLElevationEngine
from professions.data_scientist_ml.master import DrEvelynReedMaster


def test_evelyn_references_loading():
    standards = MLReferenceLibrary.get_evaluation_standards()
    assert "balanced_distribution" in standards
    assert "severely_imbalanced" in standards
    assert "pr_auc" in standards["severely_imbalanced"]["mandatory_metrics"]

    drift = MLReferenceLibrary.get_drift_thresholds()
    assert "stable" in drift
    assert drift["stable"]["max_psi"] <= 0.10

    anti_patterns = MLReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "preprocessing_leakage" for ap in anti_patterns)


def test_evelyn_inspector_hermetic_pipeline():
    inspector = MLPipelineInspector()
    hermetic_code = (
        "import numpy as np\n"
        "from sklearn.model_selection import train_test_split\n"
        "from sklearn.pipeline import Pipeline\n"
        "from sklearn.preprocessing import StandardScaler\n"
        "from sklearn.ensemble import HistGradientBoostingClassifier\n"
        "from sklearn.dummy import DummyClassifier\n"
        "from sklearn.metrics import average_precision_score\n\n"
        "SEED = 42\n"
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=SEED)\n"
        "pipeline = Pipeline([\n"
        "    ('scaler', StandardScaler()),\n"
        "    ('model', HistGradientBoostingClassifier(random_state=SEED))\n"
        "])\n"
        "pipeline.fit(X_train, y_train)\n"
        "dummy = DummyClassifier(strategy='prior', random_state=SEED).fit(X_train, y_train)\n"
        "pr_auc = average_precision_score(y_test, pipeline.predict_proba(X_test)[:, 1])\n"
        "# Production drift monitoring: psi_score = calculate_psi(X_train, X_test)\n"
    )
    report = inspector.inspect(hermetic_code)
    assert report.is_statistically_sound is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_train_test_split is True
    assert report.metrics.has_preprocessing_leakage is False
    assert report.metrics.uses_pipeline_encapsulation is True
    assert report.metrics.has_deterministic_seed is True
    assert report.metrics.has_baseline_comparison is True


def test_evelyn_inspector_leaky_pipeline():
    inspector = MLPipelineInspector()
    leaky_code = (
        "from sklearn.preprocessing import StandardScaler\n"
        "from sklearn.ensemble import RandomForestClassifier\n"
        "from sklearn.metrics import accuracy_score\n"
        "from sklearn.model_selection import train_test_split\n\n"
        "# Target: Fraud detection (imbalanced, minority < 2%)\n"
        "X = StandardScaler().fit_transform(X)\n"
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)\n"
        "clf = RandomForestClassifier().fit(X_train, y_train)\n"
        "acc = accuracy_score(y_test, clf.predict(X_test))\n"
    )
    report = inspector.inspect(leaky_code)
    assert report.is_statistically_sound is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_preprocessing_leakage is True
    assert report.metrics.has_imbalance_accuracy_trap is True
    assert report.metrics.has_deterministic_seed is False


def test_evelyn_rubric_and_veto():
    inspector = MLPipelineInspector()
    rubric = MLRubric()

    contaminated_code = (
        "# Fraud ML Model\n"
        "X = StandardScaler().fit_transform(X)\n"
        "X_train, X_test, y_train, y_test = train_test_split(X, y)\n"
        "acc = accuracy_score(y_test, y_pred)\n"
    )
    report = inspector.inspect(contaminated_code)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) > 0


def test_evelyn_critic_defect_ledger():
    critic = BlindMLCritic()
    leaky_input = (
        "X = StandardScaler().fit_transform(X)\n"
        "X_train, X_test, y_train, y_test = train_test_split(X, y)\n"
        "# Target is fraud anomaly; metric is accuracy\n"
        "acc = accuracy_score(y_test, preds)\n"
    )
    ledger = critic.review(leaky_input)
    assert ledger.verdict == "REJECTED_CONTAMINATED"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 2
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_evelyn_elevation_engine():
    engine = MLElevationEngine()
    flawed_code = (
        "# Fraud prediction pipeline\n"
        "X = StandardScaler().fit_transform(X)\n"
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)\n"
        "clf = RandomForestClassifier().fit(X_train, y_train)\n"
        "acc = accuracy_score(y_test, clf.predict(X_test))\n"
    )
    elevated_result = engine.elevate(flawed_code)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "HERMETIC ML PIPELINE" in elevated_result["elevated_pipeline"]
    assert "IMBALANCE-RESILIENT EVALUATION" in elevated_result["elevated_pipeline"]
    assert "calculate_psi" in elevated_result["elevated_pipeline"]
    assert "dummy_baseline" in elevated_result["elevated_pipeline"]


def test_evelyn_master_autonomous_cycle():
    master = DrEvelynReedMaster(passing_threshold=85)
    raw_script = (
        "X = StandardScaler().fit_transform(X)\n"
        "X_train, X_test, y_train, y_test = train_test_split(X, y)\n"
        "acc = accuracy_score(y_test, preds)\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_script)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE DATA SCIENCE & ML OPS BRIEFING" in result["executive_briefing"]
    assert "ORACLE CERTIFIED" in result["executive_briefing"]
