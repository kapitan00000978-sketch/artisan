"""
Unit tests for Cassandra Thorne (Principal Database & Distributed Data Subsystem).
"""

import pytest
from professions.database_architect.references import (
    DatabaseReferenceLibrary,
    CANONICAL_DATA_ACCESS_CORE,
)
from professions.database_architect.inspector import DatabaseSystemInspector
from professions.database_architect.rubric import DatabaseArchitectureRubric
from professions.database_architect.blind_critic import BlindDatabaseCritic
from professions.database_architect.elevation_engine import DatabaseElevationEngine
from professions.database_architect.master import CassandraThorneMaster


def test_cassandra_references_loading():
    benchmarks = DatabaseReferenceLibrary.get_system_benchmarks()
    assert benchmarks["max_p99_query_latency_ms"] == 10.0
    assert benchmarks["max_allowed_n_plus_one_queries"] == 0
    assert benchmarks["min_cache_hit_ratio"] == 0.99

    index_standards = DatabaseReferenceLibrary.get_index_standards()
    assert "btree" in index_standards
    assert "gin" in index_standards
    assert "brin" in index_standards
    assert "O(log N)" in index_standards["btree"]["complexity"]

    anti_patterns = DatabaseReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "lazy_n_plus_one_query_loop" for ap in anti_patterns)


def test_cassandra_inspector_clean_query():
    inspector = DatabaseSystemInspector()
    report = inspector.inspect(CANONICAL_DATA_ACCESS_CORE)

    assert report.is_database_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_n_plus_one_loop is False
    assert report.metrics.has_unbounded_select_star is False
    assert report.metrics.has_explicit_projections is True
    assert report.metrics.has_query_limit_or_keyset is True
    assert report.metrics.has_eager_loading_or_joins is True
    assert report.metrics.has_blocking_ddl is False


def test_cassandra_inspector_flawed_query():
    inspector = DatabaseSystemInspector()
    flawed_code = (
        "-- Blocking migration and N+1 loop query\n"
        "CREATE INDEX idx_orders_user ON orders (user_id);\n"
        "for user in users:\n"
        "    orders = db.query('SELECT * FROM orders WHERE user_id = ' + user.id)\n"
    )
    report = inspector.inspect(flawed_code)

    assert report.is_database_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_blocking_ddl is True
    assert report.metrics.has_n_plus_one_loop is True
    assert report.metrics.has_unbounded_select_star is True


def test_cassandra_rubric_and_veto():
    inspector = DatabaseSystemInspector()
    rubric = DatabaseArchitectureRubric()

    bad_sql = (
        "CREATE INDEX idx_audit_log ON audit_logs (timestamp);\n"
        "SELECT * FROM audit_logs;\n"
    )
    report = inspector.inspect(bad_sql)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) >= 2


def test_cassandra_critic_defect_ledger():
    critic = BlindDatabaseCritic()
    flawed_sql = (
        "for org in organizations:\n"
        "    members = db.execute('SELECT * FROM members WHERE org_id = %s', org.id)\n"
    )
    ledger = critic.review(flawed_sql)

    assert ledger.verdict == "REJECTED_DATABASE_CONTROVERSY"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 1
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_cassandra_elevation_engine():
    engine = DatabaseElevationEngine()
    flawed_input = (
        "CREATE INDEX idx_users_email ON users (email);\n"
        "SELECT * FROM users;\n"
    )
    elevated_result = engine.elevate(flawed_input)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "CONCURRENTLY" in elevated_result["elevated_database"]
    assert "LIMIT 100" in elevated_result["elevated_database"]
    assert "users.email" in elevated_result["elevated_database"]


def test_cassandra_master_autonomous_cycle():
    master = CassandraThorneMaster(passing_threshold=85)
    raw_query = (
        "CREATE INDEX idx_payments_customer ON payments (customer_id);\n"
        "SELECT * FROM payments;\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_query)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE DATABASE ARCHITECTURE BRIEFING" in result["executive_briefing"]
    assert "DATABASE CORE CERTIFIED" in result["executive_briefing"]
