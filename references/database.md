# 💾 Database Guild Reference
**Lead:** Cassandra 'The Core' Thorne (`database_architect`)  
**Domain:** ACID Transactions, Zero-Downtime Migrations, Index Coverage & N+1 Prevention

---

## 🎯 Core Invariants
1. **Explicit Projections:** Wildcard `SELECT *` queries in application hot paths are strictly forbidden; declare required columns explicitly.
2. **Zero Table Locks in Production:** Schema changes must execute non-blockingly (`CREATE INDEX CONCURRENTLY`, `ADD COLUMN DEFAULT NULL`).
3. **Mandatory Index Coverage:** Every foreign key column and high-cardinality filter column must have a supporting B-tree or BRIN index.
4. **Pagination Ceilings:** Every listing endpoint must enforce a strict maximum LIMIT ceiling to prevent full table scans.

---

## 📋 Quality & Security Checklist
- [ ] No N+1 query loops; multi-row relationships fetched via eager JOINs or batched IN clauses.
- [ ] Database transactions are scoped tightly around state changes, never held open during remote HTTP calls.
- [ ] Migrations are idempotent and reversible with clean down/rollback scripts.
- [ ] Connection pool limits configured with realistic acquire timeouts.
- [ ] Soft deletion filters accompanied by composite indexes including the deletion marker.

---

## 🚫 Forbidden Anti-Patterns
- **Long-Running Transactions:** Holding database locks across slow external API requests.
- **Unbounded SELECT Loops:** Iterating over parent rows and issuing single SQL queries inside loop iterations.
- **Unsafe In-Place Column Drops:** Dropping production columns without multi-phase deprecation cycles.
