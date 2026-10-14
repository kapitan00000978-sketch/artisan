"""
Cassandra 'The Core' Thorne - Database & Distributed Data Architecture Reference Standards.

This module codifies empirical OLTP/OLAP database benchmarks, execution plan metrics,
index selection heuristics, non-blocking zero-downtime DDL patterns, and query anti-patterns.
"""

from typing import Dict, Any, List


DATABASE_PERFORMANCE_BENCHMARKS: Dict[str, Any] = {
    "max_p99_query_latency_ms": 10.0,
    "max_p95_query_latency_ms": 5.0,
    "max_allowed_n_plus_one_queries": 0,
    "min_cache_hit_ratio": 0.99,
    "max_default_query_limit": 100,
    "max_transaction_duration_seconds": 2.0,
    "min_index_scan_ratio": 0.95,
}

INDEX_SELECTION_STANDARDS: Dict[str, Dict[str, str]] = {
    "btree": {
        "use_case": "Primary keys, foreign keys, equality, ranges (<, <=, =, >=, >), sorting (ORDER BY).",
        "complexity": "O(log N)",
        "maintenance": "Automatic leaf rebalancing via WAL."
    },
    "hash": {
        "use_case": "Exact 32-bit equality lookups on high-cardinality scalar columns.",
        "complexity": "O(1) expected",
        "maintenance": "Crash-safe in PostgreSQL 10+."
    },
    "gin": {
        "use_case": "JSONB document key/value containment (@>), array membership, full-text tsvector search.",
        "complexity": "Fast read, slower append due to pending list compaction.",
        "maintenance": "Requires fastupdate or explicit vacuum."
    },
    "gist": {
        "use_case": "Geometric 2D/3D points, polygon overlap (PostGIS), exclusion constraints, range types.",
        "complexity": "Hierarchical bounding box R-tree structure.",
        "maintenance": "Requires periodic reindexing if fragmented."
    },
    "brin": {
        "use_case": "Massive append-only time-series or sequential log tables sorted by physical insertion order.",
        "complexity": "Block-range min/max summary; negligible disk footprint (megabytes vs gigabytes).",
        "maintenance": "Requires brin_summarize_new_values."
    }
}

NON_BLOCKING_DDL_PATTERNS: Dict[str, str] = {
    "concurrent_index": (
        "-- Non-blocking index creation\n"
        "CREATE INDEX CONCURRENTLY idx_orders_user_created ON orders (user_id, created_at DESC);"
    ),
    "safe_foreign_key": (
        "-- Safe non-locking foreign key addition\n"
        "ALTER TABLE orders ADD CONSTRAINT fk_orders_user_id FOREIGN KEY (user_id) REFERENCES users (id) NOT VALID;\n"
        "-- Validated in background without blocking concurrent writes\n"
        "ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_user_id;"
    ),
    "keyset_pagination": (
        "-- Zero-offset keyset pagination (O(1) seek)\n"
        "SELECT id, user_id, amount, created_at\n"
        "FROM orders\n"
        "WHERE (created_at, id) < ($last_created_at, $last_id)\n"
        "ORDER BY created_at DESC, id DESC\n"
        "LIMIT 50;"
    )
}

TOXIC_DATABASE_ANTI_PATTERNS: List[Dict[str, str]] = [
    {
        "id": "lazy_n_plus_one_query_loop",
        "indicator": "Iterating over parent entities and executing a SELECT query for child relations in application memory.",
        "risk": "1,000 parent records trigger 1,001 network round-trips, saturating connection pools and starving the database.",
        "severity": "FATAL"
    },
    {
        "id": "unbounded_select_star",
        "indicator": "Querying 'SELECT *' without explicit column projection or without a LIMIT ceiling.",
        "risk": "Transfers multi-megabyte payloads, bloats client memory, exhausts buffer pools, and invalidates covering index scans.",
        "severity": "FATAL"
    },
    {
        "id": "blocking_table_rewrite_ddl",
        "indicator": "Executing 'CREATE INDEX' without CONCURRENTLY or altering tables with lock-escalating constraints in production.",
        "risk": "Acquires ACCESS EXCLUSIVE lock, queuing all reads and writes until connection timeouts cascade into total site downtime.",
        "severity": "FATAL"
    },
    {
        "id": "missing_foreign_key_index",
        "indicator": "Defining child foreign key column without a supporting index.",
        "risk": "Deletions or updates to parent table trigger full table lock and sequential scans on the child table.",
        "severity": "HIGH"
    },
    {
        "id": "network_call_inside_transaction",
        "indicator": "Making HTTP, gRPC, or external API calls while holding an open database transaction lock.",
        "risk": "External network latency holds database row locks and connections open, triggering connection pool exhaustion.",
        "severity": "HIGH"
    }
]

CANONICAL_DATA_ACCESS_CORE: str = (
    "-- Cassandra Thorne: Canonical High-Performance Eager Query Pattern\n"
    "SELECT\n"
    "    u.id AS user_id,\n"
    "    u.email,\n"
    "    o.id AS order_id,\n"
    "    o.amount,\n"
    "    o.status,\n"
    "    o.created_at\n"
    "FROM users u\n"
    "INNER JOIN orders o ON o.user_id = u.id\n"
    "WHERE u.is_active = true\n"
    "  AND o.created_at >= NOW() - INTERVAL '30 days'\n"
    "ORDER BY o.created_at DESC\n"
    "LIMIT 100;\n"
)


class DatabaseReferenceLibrary:
    """Provides empirical database benchmarks, index rules, and non-blocking DDL standards."""

    @staticmethod
    def get_system_benchmarks() -> Dict[str, Any]:
        return DATABASE_PERFORMANCE_BENCHMARKS

    @staticmethod
    def get_index_standards() -> Dict[str, Dict[str, str]]:
        return INDEX_SELECTION_STANDARDS

    @staticmethod
    def get_non_blocking_ddl() -> Dict[str, str]:
        return NON_BLOCKING_DDL_PATTERNS

    @staticmethod
    def get_toxic_anti_patterns() -> List[Dict[str, str]]:
        return TOXIC_DATABASE_ANTI_PATTERNS

    @staticmethod
    def get_canonical_query_core() -> str:
        return CANONICAL_DATA_ACCESS_CORE
