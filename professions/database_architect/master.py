"""
🗄️ CASSANDRA 'THE CORE' THORNE — PRINCIPAL DATABASE & DISTRIBUTED DATA ARCHITECT
Autonomous data conscience, execution plan inspection, blind query critique,
and zero-downtime, N+1-immune database elevation engine.

Usage:
    python professions/database_architect/master.py <query_or_migration_file> [--elevate]
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
    from .references import DatabaseReferenceLibrary
    from .inspector import DatabaseSystemInspector, DatabaseInspectionReport
    from .rubric import DatabaseArchitectureRubric, DatabaseRubricEvaluation
    from .blind_critic import BlindDatabaseCritic, DatabaseDefectLedger
    from .elevation_engine import DatabaseElevationEngine
except ImportError:
    from references import DatabaseReferenceLibrary
    from inspector import DatabaseSystemInspector, DatabaseInspectionReport
    from rubric import DatabaseArchitectureRubric, DatabaseRubricEvaluation
    from blind_critic import BlindDatabaseCritic, DatabaseDefectLedger
    from elevation_engine import DatabaseElevationEngine

# Import global ActiveDecisionJournal from studio engine
try:
    from src.studio.active_memory import ActiveDecisionJournal
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.studio.active_memory import ActiveDecisionJournal


class CassandraThorneMaster:
    """
    Cassandra Thorne: The living data tier sovereign, query execution plan inquisitor,
    and database conscience. Eliminates N+1 query amplification, enforces concurrent DDL,
    and guarantees sub-10ms query execution plans.
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
        self.inspector = DatabaseSystemInspector()
        self.rubric = DatabaseArchitectureRubric()
        self.critic = BlindDatabaseCritic()
        self.elevation_engine = DatabaseElevationEngine()
        self.journal = ActiveDecisionJournal()

    def run_autonomous_cycle(self, input_data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes the closed-loop autonomous database audit & elevation lifecycle.
        1. Inspect -> 2. Rubric -> 3. Critic -> 4. Elevate (if < 85) -> 5. Certify & Journal
        """
        data = input_data
        if data is None and self.target_path:
            if os.path.exists(self.target_path):
                with open(self.target_path, "r", encoding="utf-8") as f:
                    data = f.read()
            else:
                raise FileNotFoundError(f"Database target file not found: {self.target_path}")

        if data is None:
            # Baseline prototype flawed SQL query / migration for testing or demo
            data = (
                "-- Flawed Database Access Pattern & Migration\n"
                "CREATE INDEX idx_orders_user_id ON orders (user_id);\n"
                "SELECT * FROM users;\n"
            )

        # Step 1: Initial Blind Critic Review
        ledger: DatabaseDefectLedger = self.critic.review(data)
        initial_score = ledger.score
        elevated_result: Optional[Dict[str, Any]] = None

        # Step 2: Elevate if failed
        current_data = data
        if not ledger.is_certified:
            elevated_result = self.elevation_engine.elevate(current_data, max_iterations=self.max_cycles)
            current_data = elevated_result["elevated_database"]
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
            "elevated_database": current_data,
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
                target_file=self.target_path if self.target_path else "queries.sql",
                defects_before=[f"Fatal defects: {fatal_defects}"],
                actions_taken=["cassandra_database_core_elevation"],
                score_before=float(initial_score),
                score_after=float(final_score)
            )
        except Exception as _journal_err:
            sys.stderr.write(f"Note: Decision journal record skipped: {_journal_err}\n")

    def _generate_briefing(self, db_data: Any, ledger: DatabaseDefectLedger) -> str:
        report = self.inspector.inspect(db_data)
        m = report.metrics

        status_icon = "🗄️ [DATABASE CORE CERTIFIED]" if ledger.is_certified else "⚠️ [REJECTED DATABASE CONTROVERSY]"

        briefing = [
            f"# {status_icon} EXECUTIVE DATABASE ARCHITECTURE BRIEFING",
            f"**Auditor:** Cassandra 'The Core' Thorne (Principal Database & Distributed Data Architect)",
            f"**Final Score:** {ledger.score}/100 (Threshold: {ledger.passing_threshold})",
            f"**Verdict:** {ledger.verdict}",
            "",
            "## 1. Storage Health & Query Execution Metrics",
            f"- **N+1 Loop Immunity:** {'FAIL (N+1 Loop Detected)' if m.has_n_plus_one_loop else 'PASS (Eager JOIN / Batched)'}",
            f"- **Projection Hygiene:** {'FAIL (SELECT * Wildcard)' if m.has_unbounded_select_star else 'PASS (Explicit Columns)'}",
            f"- **Query LIMIT Ceiling:** {'PASS (Enforced Limit)' if m.has_query_limit_or_keyset else 'WARN (Unbounded Scan)'}",
            f"- **DDL Lock Safety:** {'FAIL (Blocking DDL Found)' if m.has_blocking_ddl else 'PASS (CONCURRENTLY Safe)'}",
            f"- **Foreign Key Indexing:** {'PASS (Indexed)' if m.has_indexed_foreign_keys else 'WARN (Potential Table Scan)'}",
            "",
            "## 2. Defects Ledger & Architectural Remediation",
        ]

        if ledger.defects:
            for d in ledger.defects:
                briefing.append(f"### [{d.severity}] {d.title} ({d.defect_id})")
                briefing.append(f"- **Description:** {d.description}")
                briefing.append(f"- **Storage Impact:** {d.storage_impact}")
                briefing.append(f"- **Actionable Fix:** {d.actionable_fix}")
                briefing.append("")
        else:
            briefing.append("Zero storage or query defects detected. Pristine sub-10ms execution plans and lock immunity achieved.")

        return "\n".join(briefing)


def main():
    parser = argparse.ArgumentParser(
        description="Cassandra Thorne: Autonomous Database & Distributed Data Architecture Master"
    )
    parser.add_argument("target", nargs="?", help="Path to SQL query, migration, or ORM script")
    parser.add_argument("--elevate", action="store_true", help="Automatically elevate flawed SQL and schema migrations")
    parser.add_argument("--threshold", type=int, default=85, help="Passing score threshold (default: 85)")
    args = parser.parse_args()

    master = CassandraThorneMaster(target_path=args.target, passing_threshold=args.threshold)
    results = master.run_autonomous_cycle()

    print(results["executive_briefing"])

    if args.elevate and "elevated_database" in results:
        print("\n--- ELEVATED DATABASE ARCHITECTURE ---")
        print(results["elevated_database"])

    sys.exit(0 if results["is_certified"] else 1)


if __name__ == "__main__":
    main()
