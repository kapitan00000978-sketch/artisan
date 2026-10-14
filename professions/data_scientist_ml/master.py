"""
🔬 DR. EVELYN REED — STAFF DATA SCIENTIST & ML SYSTEMS ARCHITECT
Autonomous empirical conscience, leakage inspection, blind ML outcome critique,
and automated hermetic pipeline elevation engine.

Usage:
    python professions/data_scientist_ml/master.py <pipeline_file> [--elevate]
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, List, Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception as _enc_err:
        sys.stderr.write(f"Note: UTF-8 stdout reconfiguration skipped: {_enc_err}\n")

try:
    from .references import MLReferenceLibrary
    from .inspector import MLPipelineInspector, MLInspectionReport
    from .rubric import MLRubric, MLRubricEvaluation
    from .blind_critic import BlindMLCritic, MLDefectLedger
    from .elevation_engine import MLElevationEngine
except ImportError:
    from references import MLReferenceLibrary
    from inspector import MLPipelineInspector, MLInspectionReport
    from rubric import MLRubric, MLRubricEvaluation
    from blind_critic import BlindMLCritic, MLDefectLedger
    from elevation_engine import MLElevationEngine

# Import global ActiveDecisionJournal from studio engine
try:
    from src.studio.active_memory import ActiveDecisionJournal
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.studio.active_memory import ActiveDecisionJournal


class DrEvelynReedMaster:
    """
    Dr. Evelyn Reed: The living empirical conscience, ML Ops gatekeeper,
    and statistical rigor auditor. Eradicates data leakage, bans deceptive accuracy,
    and locks in deterministic pipeline lineage.
    """

    def __init__(
        self,
        target_path: Optional[str] = None,
        passing_threshold: int = 85,
        max_cycles: int = 3
    ):
        self.target_path = os.path.abspath(target_path) if target_path else None
        self.passing_threshold = passing_threshold
        self.max_cycles = max_cycles
        self.inspector = MLPipelineInspector()
        self.rubric = MLRubric()
        self.critic = BlindMLCritic()
        self.elevation_engine = MLElevationEngine()
        self.journal = ActiveDecisionJournal()

    def run_autonomous_cycle(self, input_data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes the closed-loop autonomous ML audit & elevation lifecycle.
        1. Inspect -> 2. Rubric -> 3. Critic -> 4. Elevate (if < 85) -> 5. Certify & Journal
        """
        data = input_data
        if data is None and self.target_path:
            if os.path.exists(self.target_path):
                with open(self.target_path, "r", encoding="utf-8") as f:
                    data = f.read()
            else:
                raise FileNotFoundError(f"ML target file not found: {self.target_path}")

        if data is None:
            # Baseline prototype for testing or standalone demo
            data = (
                "# Flawed Fraud Detection ML Script\n"
                "from sklearn.preprocessing import StandardScaler\n"
                "from sklearn.ensemble import RandomForestClassifier\n"
                "from sklearn.metrics import accuracy_score\n"
                "from sklearn.model_selection import train_test_split\n\n"
                "X = StandardScaler().fit_transform(X)\n"
                "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)\n"
                "clf = RandomForestClassifier().fit(X_train, y_train)\n"
                "acc = accuracy_score(y_test, clf.predict(X_test))\n"
                "print('Accuracy:', acc)\n"
            )

        # Step 1: Initial Blind Critic Review
        ledger: MLDefectLedger = self.critic.review(data)
        initial_score = ledger.score
        elevated_result: Optional[Dict[str, Any]] = None

        # Step 2: Elevate if failed
        current_data = data
        if not ledger.is_certified:
            elevated_result = self.elevation_engine.elevate(current_data, max_iterations=self.max_cycles)
            current_data = elevated_result["elevated_pipeline"]
            ledger = elevated_result["final_ledger"]

        # Step 3: Record in Journal
        self._record_journal_entry(
            initial_score=initial_score,
            final_score=ledger.score,
            is_certified=ledger.is_certified,
            fatal_defects=ledger.fatal_defects_count,
            verdict=ledger.verdict
        )

        # Step 4: Generate Executive Briefing
        briefing = self._generate_briefing(current_data, ledger)

        return {
            "is_certified": ledger.is_certified,
            "initial_score": initial_score,
            "final_score": ledger.score,
            "verdict": ledger.verdict,
            "fatal_defects_count": ledger.fatal_defects_count,
            "defects": ledger.defects,
            "elevated_pipeline": current_data,
            "executive_briefing": briefing,
            "summary": ledger.critic_verdict_summary
        }

    def _record_journal_entry(
        self,
        initial_score: int,
        final_score: int,
        is_certified: bool,
        fatal_defects: int,
        verdict: str
    ) -> None:
        try:
            self.journal.record_decision(
                iteration=1,
                target_file=self.target_path if self.target_path else "ml_pipeline.py",
                defects_before=[f"Fatal defects: {fatal_defects}"],
                actions_taken=["evelyn_ml_hermetic_pipeline_elevation"],
                score_before=float(initial_score),
                score_after=float(final_score)
            )
        except Exception as _journal_err:
            sys.stderr.write(f"Note: Decision journal record skipped: {_journal_err}\n")

    def _generate_briefing(self, pipeline_data: Any, ledger: MLDefectLedger) -> str:
        report = self.inspector.inspect(pipeline_data)
        m = report.metrics

        status_icon = "🔬 [ORACLE CERTIFIED]" if ledger.is_certified else "⚠️ [REJECTED CONTAMINATED]"

        briefing = [
            f"# {status_icon} EXECUTIVE DATA SCIENCE & ML OPS BRIEFING",
            f"**Auditor:** Dr. Evelyn 'The Oracle' Reed (Staff Data Scientist & ML Systems Architect)",
            f"**Final Score:** {ledger.score}/100 (Threshold: {ledger.passing_threshold})",
            f"**Verdict:** {ledger.verdict}",
            "",
            "## 📊 I. Statistical Rigor & Data Isolation Matrix",
            f"- **Data Preprocessing Isolation:** {'HERMETIC (Inside Pipeline)' if m.uses_pipeline_encapsulation and not m.has_preprocessing_leakage else 'CONTAMINATED (Leakage Detected)'}",
            f"- **Temporal Causality:** {'STRICT (TimeSeriesSplit / Ordered)' if not m.has_temporal_leakage else 'VIOLATED (Random Shuffle on Time Series)'}",
            f"- **Evaluation Metric:** {m.primary_metric.upper()} ({'IMBALANCE-RESILIENT' if m.primary_metric in ['pr_auc', 'f1', 'f1_macro'] else 'STANDARD / CHECK SKEW'})",
            f"- **Reproducibility State:** {f'DETERMINISTIC (Seed: {m.seed_value})' if m.has_deterministic_seed else 'NON-DETERMINISTIC (Random)'}",
            f"- **Baseline Comparison:** {'CHAMPION/CHALLENGER (Dummy Benchmark Present)' if m.has_baseline_comparison else 'MISSING'}",
            f"- **Production Drift Guardrails:** {'POPULATION STABILITY INDEX (PSI) CONFIGURED' if m.has_drift_monitoring else 'UNMONITORED'}",
            "",
            "## 🛑 II. Defect & Remediation Ledger",
        ]

        if not ledger.defects:
            briefing.append("✅ Zero statistical leakages or metric distortions identified. Model architecture satisfies institutional ML Ops criteria.")
        else:
            for d in ledger.defects:
                briefing.append(f"- **[{d.severity}] {d.title}:** {d.description}")
                briefing.append(f"  *Statistical Impact:* {d.statistical_impact}")
                briefing.append(f"  *Actionable Fix:* {d.actionable_remediation}")

        briefing.extend([
            "",
            "## 🔬 III. Dr. Evelyn Reed's Empirical Directive",
            ledger.critic_verdict_summary,
            ""
        ])

        return "\n".join(briefing)


def main():
    parser = argparse.ArgumentParser(
        description="Dr. Evelyn Reed: Staff Data Scientist & ML Systems Master Auditor"
    )
    parser.add_argument("target", nargs="?", default=None, help="Path to ML Python script or metadata file")
    parser.add_argument("--elevate", action="store_true", help="Automatically elevate flawed pipelines")
    parser.add_argument("--threshold", type=int, default=85, help="Minimum passing score")

    args = parser.parse_args()

    master = DrEvelynReedMaster(target_path=args.target, passing_threshold=args.threshold)
    result = master.run_autonomous_cycle()

    print(result["executive_briefing"])

    if not result["is_certified"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
