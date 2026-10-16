# ⚔️ Artisan Adversarial Red-Team Review

Artisan provides an objective, adversarial code review engine (`src/sdk/reviewer.py`) designed to audit code modifications without implementation bias.

---

## ⚡ Overview

When developers or AI coding assistants make modifications, self-review often suffers from confirmation bias. The red-team reviewer acts as an independent adversarial auditor checking:

- **Security & OWASP Invariants:** Parameterized queries, secret exposure, safe deserialization.
- **Architectural Cleanliness:** Boundary enforcement, separation of concerns, zero unfinished stubs.
- **Performance Budgets:** Hot-loop allocations, unclosed handles, unnecessary blocking operations.
- **Test Fidelity:** Missing boundary conditions, unchecked edge cases.

---

## 💻 CLI Usage

```bash
# Review uncommitted working tree changes:
artisan review

# Review git-staged changes before commit:
artisan review --staged

# Review a specific file:
artisan review --file src/libraries/database.py

# Format review output as GitHub PR markdown:
artisan review --staged --markdown
```

---

## 📋 Defect Ledger & Decision

The reviewer compiles an itemized Defect Ledger with:
- **Severity Classification:** `CRITICAL`, `MAJOR`, `MINOR`
- **Location & File Anchor:** File path and line numbers
- **Remediation Directive:** Concrete, actionable fix guidance
- **Final Verdict:** `APPROVED` (no critical or major defects) or `VETO` (modifications blocked until resolved).
