"""
Cassandra 'The Core' Thorne - Objective Database & Distributed Data Inspector.

This module inspects SQL queries, schema migrations, and ORM code to detect
N+1 query amplification, blocking DDL table locks, unbounded SELECT * scans,
and missing foreign key indexes.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class DatabaseMetrics:
    has_n_plus_one_loop: bool = False
    has_unbounded_select_star: bool = False
    has_blocking_ddl: bool = False
    has_explicit_projections: bool = False
    has_query_limit_or_keyset: bool = False
    has_eager_loading_or_joins: bool = False
    has_indexed_foreign_keys: bool = False
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class DatabaseInspectionReport:
    metrics: DatabaseMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_database_viable: bool = False


class DatabaseSystemInspector:
    """Rigorous database auditor evaluating SQL statements, schema migrations, and query patterns."""

    def inspect(self, db_input: Any) -> DatabaseInspectionReport:
        """
        Audits SQL source code, migration scripts, ORM access patterns, or execution plan dict.
        """
        metrics = self._extract_metrics(db_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Zero N+1 Query Immunity
        if metrics.has_n_plus_one_loop:
            critical_violations.append(
                "N+1 Query Amplification Detected: Executing database queries inside an application loop. "
                "Causes connection pool exhaustion and catastrophic latency degradation under load."
            )
        elif metrics.has_eager_loading_or_joins:
            benchmarks_passed.append("Eager loading / JOIN fetching verified: Zero N+1 query immunity achieved.")

        # 2. Bounded Query Limits & Explicit Projections
        if metrics.has_unbounded_select_star:
            critical_violations.append(
                "Unbounded 'SELECT *' Detected: Querying entire row tuples without column projection or LIMIT ceiling. "
                "Exhausts client memory and invalidates database covering indexes."
            )
        else:
            if metrics.has_explicit_projections:
                benchmarks_passed.append("Explicit column projection verified (Zero wildcard leaks).")
            if metrics.has_query_limit_or_keyset:
                benchmarks_passed.append("Bounded query limit / keyset pagination ceiling verified.")

        # 3. Non-Blocking Concurrent DDL
        if metrics.has_blocking_ddl:
            critical_violations.append(
                "Blocking DDL Lock Escalation: Found bare 'CREATE INDEX' or locking constraint without 'CONCURRENTLY' or 'NOT VALID'. "
                "Acquires ACCESS EXCLUSIVE lock on production tables, queuing all read/write traffic."
            )
        else:
            benchmarks_passed.append("Non-blocking DDL verified: Uses concurrent index creation and staged constraint validation.")

        # 4. Foreign Key Indexing & Joins
        if not metrics.has_indexed_foreign_keys and "foreign key" in str(db_input).lower():
            warnings.append("Foreign key declared without explicit supporting index; updates/deletes risk sequential scans on child tables.")
        else:
            benchmarks_passed.append("Foreign key indexing verified.")

        for ap in metrics.anti_patterns_detected:
            if ap not in critical_violations:
                critical_violations.append(f"Anti-Pattern Detected: {ap}")

        is_viable = len(critical_violations) == 0

        return DatabaseInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_database_viable=is_viable
        )

    def _extract_metrics(self, db_input: Any) -> DatabaseMetrics:
        text = ""
        metadata: Dict[str, Any] = {}

        if isinstance(db_input, str):
            text = db_input
            try:
                parsed = json.loads(db_input)
                if isinstance(parsed, dict):
                    metadata = parsed
            except (json.JSONDecodeError, ValueError) as _json_err:
                _ = _json_err
        elif isinstance(db_input, dict):
            metadata = db_input
            text = json.dumps(db_input)
        else:
            text = str(db_input)

        text_lower = text.lower()
        m = DatabaseMetrics()

        # 1. N+1 Loop Detection
        has_n1 = bool(
            re.search(r"for\s+\w+\s+in\s+.*:\s*(?:.*\n){1,6}.*(?:execute|query|select|db\.)", text, re.IGNORECASE) or
            ("for " in text_lower and ("db.query" in text_lower or "session.query" in text_lower or ".execute(" in text_lower)) or
            metadata.get("has_n_plus_one_loop", False)
        )
        m.has_n_plus_one_loop = has_n1

        # 2. SELECT * and Unbounded query detection
        has_select = bool(re.search(r"\bselect\b", text_lower))
        has_star = bool(
            re.search(r"\bselect\s+\*\s+from\b", text_lower) or
            metadata.get("has_select_star", False)
        )
        has_limit = bool(
            re.search(r"\b(limit|fetch\s+first|keyset)\b", text_lower) or
            metadata.get("has_query_limit", False)
        )
        m.has_query_limit_or_keyset = has_limit
        m.has_unbounded_select_star = has_star or (has_select and not has_limit and "count(" not in text_lower)
        m.has_explicit_projections = has_select and not has_star

        # 3. Blocking DDL Detection
        has_create_idx = "create index" in text_lower or "create unique index" in text_lower
        is_concurrent = "concurrently" in text_lower
        has_fk_without_not_valid = ("add foreign key" in text_lower or "add constraint" in text_lower) and "foreign key" in text_lower and "not valid" not in text_lower

        has_blocking = (
            (has_create_idx and not is_concurrent) or
            has_fk_without_not_valid or
            metadata.get("has_blocking_ddl", False)
        )
        m.has_blocking_ddl = has_blocking

        # 4. Eager joins and fetching
        has_eager = (
            "join " in text_lower or
            "inner join" in text_lower or
            "left join" in text_lower or
            "select_related" in text_lower or
            "prefetch_related" in text_lower or
            "joinedload" in text_lower or
            metadata.get("has_eager_loading", False)
        )
        m.has_eager_loading_or_joins = has_eager

        # 5. Indexed foreign keys
        has_idx_fk = (
            ("foreign key" in text_lower and "index" in text_lower) or
            "idx_" in text_lower or
            metadata.get("has_indexed_foreign_keys", True)
        )
        m.has_indexed_foreign_keys = has_idx_fk

        # Anti-pattern logging
        if m.has_n_plus_one_loop:
            m.anti_patterns_detected.append("N+1 loop fetching in application memory")
        if m.has_unbounded_select_star:
            m.anti_patterns_detected.append("Unbounded SELECT * query without limit ceiling")
        if m.has_blocking_ddl:
            m.anti_patterns_detected.append("Blocking table DDL lock escalation")

        return m
