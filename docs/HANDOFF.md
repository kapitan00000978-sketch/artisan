# Hallwright Project Handover & Briefing (docs/HANDOFF.md)

## What This Project Is
Hallwright (repo `kapitan00000978-sketch/hallwright`; formerly Artisan, formerly Humanpowers) is a **GUARDRAIL LAYER** for existing AI coding agents (Claude Code, Cursor, Copilot, Antigravity, etc.). It is NOT an AI agent, NOT an operating system, and it calls no model itself. The host agent is the LLM.

### What it actually provides:
1. A deterministic pre-commit/CI gate (`scripts/detector.py`, `scripts/pre-commit-gatekeeper.py`) that blocks stubs (TODO/FIXME), silent catches, dangerous eval/exec and hardcoded secrets.
2. Project memory and cross-agent continuity (`.hallwright/`).
3. Seven subagents (architect, copywriter, critic, healer, performance, security, tester) plus skills, delivered as thin per-tool adapters.
4. An MCP server (`mcp/server.py`).

---

## Owner's Goals & Strategic Decisions
- Quality over speed and honest answers. No flattery, no unverified claims.
- Keep the project simple. The 64 'professions' (physics/space/etc. masters) are ballast: back up to branch `archive/full-v1`, then distill into ~8 software guilds (architecture, security, performance, testing, database, devops/sre, api/dx, frontend/ui-ux) as short `references/<guild>.md` files. Subagent files stay under 2 KB each. Science masters go to `packs/science/` (not loaded by default).
- One name only: Hallwright. Remove duplicate `artisan_*` files and `.artisan/`.
- Do NOT now: switch to SQLite, add tree-sitter/libcst, standalone binaries, PyPI packaging, new features, new agents.

---

## Working Rules
- One small step per commit. After EACH step print the exact command output proving it (`git status`, `pytest -q`, gate run, `grep`, `wc -c`). Never write 'fixed' without proof.
- Do not rely on conversation history: write progress to `docs/HANDOFF.md` (done / remaining / decisions) after every step so a new chat can resume.
- If something in this briefing contradicts the code, report it instead of guessing.

---

## Status Ledger

### Done
- Initialized `docs/HANDOFF.md` with project briefing, scope, rules, and known defects ledger.
- Performed initial read-only verification of known defects 1–9.
- Created git baseline backup branch `archive/full-v1`.
- **Step 1 Completed (Unified Brand & Cleanup):**
  - Synced latest state to `.hallwright/` and completely deleted `.artisan/`.
  - Removed duplicate CLI wrappers and aliases (`artisan_cli.py`, `artisan.py`, `bin/artisan.js`, `artisan.config.json`).
  - Unified runtime memory and config paths in `src/sdk/continuity.py`, `src/sdk/learning_memory.py`, `src/sdk/agent_registry.py`, `src/memory/store.py`, `src/studio/active_memory.py`, `scripts/roi_tracker.py`, `scripts/artisan_studio.py`, `hallwright_cli.py`, `bin/hallwright.js`, `tests/test_cli.py`, `tests/test_continuity.py`, `package.json`, and `index.html`.
  - Verified 100% test pass rate (`600 passed in 57.40s`) and pre-commit gate pass (`100/100`).

### Remaining
- **Step 2:** Eliminate self-exclusion (`EXCLUDED_FILES`) in `detector.py` and remediate all `except Exception: pass` silent swallowers.
- **Step 3:** Fully wire SQLite WAL memory engine (`src/memory/store.py`) to CLI and MCP server as the default store.
- **Step 4:** Safe auto-remediation (ensure AST/syntax checks, proper imports, prevent destructive code rewrites).
- **Step 5:** Distill 64 professions down to ~8 core software guilds, archive science masters to `packs/science/`.
- **Step 6:** Package & distribution refinement.
- **Step 7:** Bound and prune `.hallwright/decision_journal.json`.

### Decisions
- Single unified brand: **Hallwright**.
- Active persistent state directory: `.hallwright/`.
- Guardrail layer architecture strictly preserved; no autonomous model invocation inside the core guardrail layer.
