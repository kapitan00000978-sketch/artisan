"""
Cassandra 'The Core' Thorne - Blind Database & Distributed Data Critic.

Evaluates SQL queries, ORM code, and database migrations strictly against
zero N+1 loop tolerance, non-blocking concurrent DDL, and bounded index projections.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.database_architect.inspector import DatabaseSystemInspector, DatabaseInspectionReport
from professions.database_architect.rubric import DatabaseArchitectureRubric, DatabaseRubricEvaluation


@dataclass
class DatabaseDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    storage_impact: str
    actionable_fix: str


@dataclass
class DatabaseDefectLedger:
    verdict: str  # CERTIFIED_DATABASE_CORE or REJECTED_DATABASE_CONTROVERSY
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[DatabaseDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindDatabaseCritic:
    """Database adversary reviewing queries and migrations for catastrophic locks, leaks, and scans."""

    def __init__(self):
        self.inspector = DatabaseSystemInspector()
        self.rubric = DatabaseArchitectureRubric()

    def review(self, db_input: Any) -> DatabaseDefectLedger:
        """
        Runs objective inspection and adversarial rubric scoring, producing a Database Defect Ledger.
        """
        report: DatabaseInspectionReport = self.inspector.inspect(db_input)
        eval_result: DatabaseRubricEvaluation = self.rubric.evaluate(report)

        defects: List[DatabaseDefect] = []

        # 1. Critical violations -> FATAL defects
        for i, violation in enumerate(report.critical_violations, start=1):
            if "n+1" in violation.lower():
                title = "N+1 Query Amplification Loop"
                impact = "Exploding query count starves database connection pools and causes latency spikes under concurrency."
                fix = "Refactor loop into an eager JOIN or batched 'WHERE id IN (...)' query."
            elif "select *" in violation.lower():
                title = "Unbounded 'SELECT *' Wildcard Leak"
                impact = "Transfers unindexed columns, bloats client memory, and invalidates index-only scans."
                fix = "Project explicit columns (e.g. 'SELECT id, email, created_at') and append a 'LIMIT 100' ceiling."
            elif "blocking" in violation.lower() or "ddl" in violation.lower():
                title = "Blocking DDL Table Lock Escalation"
                impact = "Acquires ACCESS EXCLUSIVE lock on production tables, halting all read and write traffic."
                fix = "Use 'CREATE INDEX CONCURRENTLY' and add foreign keys with 'NOT VALID' followed by async validation."
            else:
                title = "Critical Database Architecture Violation"
                impact = "Violates high-performance database tier reliability."
                fix = "Refactor SQL and schema migrations to Cassandra Thorne standards."

            defects.append(
                DatabaseDefect(
                    defect_id=f"DATA-FATAL-{i:03d}",
                    severity="FATAL",
                    title=title,
                    description=violation,
                    storage_impact=impact,
                    actionable_fix=fix
                )
            )

        # 2. Veto reasons
        for j, reason in enumerate(eval_result.veto_reasons, start=len(defects) + 1):
            if not any(d.description == reason for d in defects):
                defects.append(
                    DatabaseDefect(
                        defect_id=f"DATA-FATAL-{j:03d}",
                        severity="FATAL",
                        title="Database Integrity Veto",
                        description=reason,
                        storage_impact="Disqualifies the data access code from production deployment.",
                        actionable_fix="Remediate the underlying SQL anti-pattern immediately."
                    )
                )

        # 3. Warnings -> HIGH / MEDIUM defects
        for k, warning in enumerate(report.warnings, start=len(defects) + 1):
            severity = "HIGH" if "foreign key" in warning.lower() else "MEDIUM"
            title = "Unindexed Foreign Key Risk" if "foreign key" in warning.lower() else "Suboptimal Query Design"
            impact = "Parent updates/deletions trigger sequential table locks on the child table." if "foreign key" in warning.lower() else "Causes unnecessary disk I/O."
            fix = "Create a supporting B-tree index on the child foreign key column." if "foreign key" in warning.lower() else "Optimize query plan."

            defects.append(
                DatabaseDefect(
                    defect_id=f"DATA-WARN-{k:03d}",
                    severity=severity,
                    title=title,
                    description=warning,
                    storage_impact=impact,
                    actionable_fix=fix
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = (
            "CERTIFIED_DATABASE_CORE"
            if eval_result.is_certified and fatal_count == 0
            else "REJECTED_DATABASE_CONTROVERSY"
        )

        summary = (
            f"Cassandra Thorne Database Review: Score {eval_result.total_score}/100. "
            f"Verdict: {verdict}. Fatal defects: {fatal_count}, High defects: {high_count}."
        )

        return DatabaseDefectLedger(
            verdict=verdict,
            score=eval_result.total_score,
            passing_threshold=eval_result.passing_threshold,
            is_certified=eval_result.is_certified and fatal_count == 0,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
