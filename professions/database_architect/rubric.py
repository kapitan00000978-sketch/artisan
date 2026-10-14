"""
Cassandra 'The Core' Thorne - 100-Point Database & Distributed Data Rubric.

Evaluates SQL queries, schema migrations, ORM access patterns, and indexing strategies.
Passing threshold: 85/100 points.
Veto criteria: N+1 query loop amplification, unbounded SELECT * without limit, or blocking DDL.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.database_architect.inspector import DatabaseInspectionReport, DatabaseMetrics


@dataclass
class DatabaseRubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class DatabaseArchitectureRubric:
    """Rigorous 100-point weighted evaluation rubric for databases and distributed data access."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: DatabaseInspectionReport) -> DatabaseRubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Zero N+1 Query Immunity (25 pts)
        # ----------------------------------------------------
        p1_score = 0
        if m.has_n_plus_one_loop:
            veto_reasons.append(
                "N+1 Query Amplification: Iterating over records and issuing child queries inside a loop saturates connection pools."
            )
            recommendations.append(
                "Replace loop queries with a single INNER/LEFT JOIN or batched 'WHERE id IN (...)' eager fetching."
            )
        elif m.has_eager_loading_or_joins:
            p1_score += 25
        else:
            # Clean single-table query or batched lookup without N+1 loops
            p1_score += 20
            recommendations.append(
                "Explicitly declare eager JOIN relationships in ORM queries if multiple entities are related."
            )

        pillar_scores["n_plus_one_immunity"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Bounded Projections & LIMIT Ceilings (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if m.has_unbounded_select_star:
            veto_reasons.append(
                "Unbounded 'SELECT *': Dragging wildcard columns without explicit projection or LIMIT ceiling risks buffer pool exhaustion."
            )
            recommendations.append(
                "Project only required columns explicitly (e.g. 'SELECT id, email, created_at') and enforce 'LIMIT 100'."
            )
        else:
            if m.has_explicit_projections:
                p2_score += 15
            else:
                p2_score += 5
                recommendations.append("Specify explicit column names in the SELECT clause instead of wildcard '*'.")

            if m.has_query_limit_or_keyset:
                p2_score += 10
            else:
                p2_score += 3
                recommendations.append("Enforce a mandatory LIMIT or keyset pagination cursor on all queries.")

        pillar_scores["bounded_projections"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: Non-Blocking Concurrent DDL (20 pts)
        # ----------------------------------------------------
        p3_score = 0
        if m.has_blocking_ddl:
            veto_reasons.append(
                "Blocking Table DDL: Creating indexes without 'CONCURRENTLY' or adding constraints without 'NOT VALID' locks tables."
            )
            recommendations.append(
                "Use 'CREATE INDEX CONCURRENTLY' and add foreign keys with 'NOT VALID' followed by asynchronous validation."
            )
        else:
            p3_score += 20

        pillar_scores["concurrent_ddl"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: Foreign Key Indexing & Integrity (15 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.has_indexed_foreign_keys:
            p4_score += 15
        else:
            p4_score += 5
            recommendations.append(
                "Create supporting B-tree indexes on foreign key columns (e.g. 'CREATE INDEX CONCURRENTLY idx_child_parent_id')."
            )

        pillar_scores["foreign_key_indexing"] = p4_score

        # ----------------------------------------------------
        # Pillar 5: Execution Plan Discipline & Keysets (15 pts)
        # ----------------------------------------------------
        p5_score = 0
        if m.has_query_limit_or_keyset and (m.has_eager_loading_or_joins or m.has_explicit_projections):
            p5_score += 15
        elif m.has_query_limit_or_keyset:
            p5_score += 10
        else:
            p5_score += 6
            recommendations.append(
                "Adopt O(1) keyset pagination ('WHERE (created_at, id) < (...)') instead of high-offset OFFSET scans."
            )

        pillar_scores["execution_plan_discipline"] = p5_score

        total_score = sum(pillar_scores.values())

        # Veto enforcement
        veto_triggered = len(veto_reasons) > 0
        if veto_triggered and total_score >= self.PASSING_THRESHOLD:
            total_score = 65

        is_certified = (total_score >= self.PASSING_THRESHOLD) and not veto_triggered

        return DatabaseRubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
