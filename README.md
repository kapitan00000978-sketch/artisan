<p align="center">
  <img src="./assets/hallwright-banner.jpg" alt="Hallwright Banner" width="800" />
</p>

# 🛡️ Hallwright: A Guardrail Layer for AI Coding Agents

> **Deterministic pre-commit gate, project memory, and subagent/skill definitions for Claude Code, Cursor, Copilot, Antigravity, and other AI coding assistants.**

[![CI](https://github.com/kapitan00000978-sketch/hallwright/actions/workflows/artisan-gate.yml/badge.svg)](https://github.com/kapitan00000978-sketch/hallwright/actions)
[![npm version](https://img.shields.io/npm/v/hallwright.svg)](https://www.npmjs.com/)
[![MCP 2.0](https://img.shields.io/badge/MCP-JSON--RPC%202.0-orange.svg)](mcp/server.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## ⚡ The 3 Core Pillars

Hallwright is not an AI model or operating system. It sits between your developer workspace and whichever AI assistant you use, providing three deterministic guardrails:

```
                  ┌─────────────────────────────────────────┐
                  │          Your Host AI Assistant         │
                  │   (Claude Code, Cursor, Copilot, etc.)  │
                  └────────────────────┬────────────────────┘
                                       │
                        ┌──────────────┴──────────────┐
                        ▼                             ▼
              ┌───────────────────┐         ┌───────────────────┐
              │  2. Project       │         │  3. Subagent &    │
              │     Memory        │         │     Skill Defs    │
              │  (.artisan/)      │         │  (.agents/, MCP)  │
              └─────────┬─────────┘         └─────────┬─────────┘
                        │                             │
                        ▼                             ▼
                  ┌─────────────────────────────────────────┐
                  │        Local Codebase & Git Stage       │
                  └────────────────────┬────────────────────┘
                                       │ git commit
                                       ▼
                        ┌─────────────────────────────┐
                        │   1. Pre-Commit AST Gate    │
                        │   (Blocks stubs & secrets)  │
                        └─────────────────────────────┘
```

| Pillar | What It Does | Key Command |
| :--- | :--- | :--- |
| **1. Deterministic Gate** | Intercepts unfinished stubs (`pass`, `// TODO`), empty catches (`except: pass`), and secret leaks before commit. | `hallwright audit --staged` |
| **2. Project Memory** | Records past bugs as persistent "scar tissue" (`.artisan/memory.json`) and provides cross-agent continuity handoffs (`.artisan/continuity.json`). | `hallwright memory` / `hallwright resume` |
| **3. Subagents & Skills** | Provides 7 specialized role definitions and domain skills that your host assistant can adopt for complex tasks. | `hallwright swarm` / `hallwright context` |

---

### ⚡ Quick Start (3 Commands)

```bash
# 1. Initialize pre-commit gate & agent configs in your repository
npx github:kapitan00000978-sketch/hallwright init

# 2. Audit staged changes for stubs, empty catches & exposed secrets
hallwright audit --staged

# 3. Automatically remediate detected silent catches & placeholder stubs
hallwright fix
```
*(Note: Both `hallwright` and `artisan` CLI aliases are fully supported).*

---

### 💡 Instant Example: What Hallwright Intercepts

```python
# ❌ Host AI Output (Blocked by Pre-Commit Gate)
def handle_webhook(payload):
    try:
        token = "sk_live_93847291834729183472"      # Secret leak!
        process_event(payload)
    except Exception:
        pass                                        # Silent error suppression!
    # Unfinished placeholder stub                   # Incomplete logic!

# ✅ After Hallwright Auto-Fix (`hallwright fix`)
import os
import logging

logger = logging.getLogger(__name__)

def handle_webhook(payload):
    token = os.environ.get("WEBHOOK_SECRET_KEY")
    if not token:
        raise ValueError("WEBHOOK_SECRET_KEY environment variable required")
    try:
        process_event(payload)
    except Exception as exc:
        logger.error("Failed to process webhook payload: %s", exc, exc_info=True)
        raise
```

---

## 🔍 How Each Pillar Works

### Pillar 1: Deterministic Pre-Commit Gate (`scripts/detector.py`)
- **AST Semantic Analysis:** Scans Python, JavaScript, TypeScript, Go, and Rust files.
- **Pattern Interception:** Catches unfinished stubs (`TODO`, `FIXME`, bare `pass`), silent error swallowers (`except: pass`, empty `catch {}`), dangerous dynamic code execution, and exposed API keys (`sk-...`, `ghp_...`).
- **Auto-Fix (`hallwright fix`):** Refactors empty catches into structured logger statements and replaces empty stubs.

### Pillar 2: Project Memory & Continuity (`.artisan/`)
- **Living Scar Tissue (`.artisan/memory.json`):** When bugs are caught and fixed, lessons are recorded. When starting new tasks, `hallwright context` injects only the matching lessons (~6x context optimization: ~2K tokens vs ~12K full rubric dump).
- **Cross-Agent Continuity (`hallwright checkpoint` & `hallwright resume`):** Checkpoints task progress, active files, and blockers so that switching between Claude Code, Cursor, or Antigravity does not lose session context.
- **Strictly Optional:** Disable anytime with `hallwright resume --no-continuity` or configuring `continuity.enabled: false`.

### Pillar 3: Subagent & Skill Definitions (`.agents/`, `skills/`)
Hallwright provides 7 structured sub-agent roles for decomposing complex engineering tasks:

> **The host agent runs the subagents; Hallwright does not call any model itself.**

| Sub-Agent | Role | Focus Area |
| :--- | :--- | :--- |
| **`hallwright-architect`** | Architecture Lead | Modular decomposition, clean APIs, zero tech-debt. |
| **`hallwright-security`** | Security Auditor | Threat modeling, OWASP Top 10 defense, credential protection. |
| **`hallwright-critic`** | Red-Team Reviewer | Objective peer review, defect ledger compilation, veto/approval. |
| **`hallwright-tester`** | Testing Lead | Edge case coverage, fuzzing, regression catch validation. |
| **`hallwright-performance`** | Performance Lead | Mechanical sympathy, zero hot-loop allocations, low latency. |
| **`hallwright-copywriter`** | Technical Writer | Clear API references, documentation, developer experience. |
| **`hallwright-healer`** | Remediation Lead | Auto-repair of silent catches, missing handlers, and stubs. |

---

## ❓ What `hallwright swarm` Actually Does

`hallwright swarm` (or `artisan swarm`) does **not** invoke an LLM or make external API calls. It is a local, deterministic planning and coordination tool:

1. **Task Decomposition:** Analyzes the task description and target files using keyword and extension heuristics.
2. **Role Selection:** Selects relevant sub-agent roles from the 7 definitions above.
3. **Memory Retrieval:** Queries `.artisan/memory.json` to attach historical lessons relevant to each role.
4. **Plan Generation:** Outputs a structured, ordered execution plan (e.g. Architect → Security → Tester → Critic) with clear directives.
5. **Session Coordination:** In execution mode, registers session locks in `.artisan/agent_sessions.json` to prevent multi-agent file collisions.
6. **Execution by Host:** Your **host AI assistant** (Claude Code, Cursor, Antigravity) receives the plan and executes the steps.

```bash
# Preview the decomposition plan for a task:
hallwright swarm "Implement JWT authentication and Stripe webhook" --plan

# Register stages and session locks for the host agent:
hallwright swarm "Implement JWT authentication and Stripe webhook"
```

---

## 📊 Synthetic Verification Suite (`bench/`)

Hallwright provides a reproducible verification harness evaluating deterministic static detection and autonomous remediation across 10 controlled fixtures containing common AI anti-patterns (`python bench/run_benchmark.py`):

| Fixture Metric | Baseline (no gate) | With Hallwright (Gatekeeper + Auto-Fix) |
| :--- | :--- | :--- |
| **Quality Gate Pass Rate** | `1 / 10` (10.0%) | **`10 / 10` (100.0%)** |
| **Defects Neutralized** | `0` (flaws leak into codebase) | **`9` anti-patterns deterministically resolved** |
| **Remediation Cycles** | Unbounded / Manual human triage | **Average `1.0` cycle auto-remediation** |

> Controlled evaluation methodology and task fixtures: [`bench/BENCHMARK_REPORT.md`](./bench/BENCHMARK_REPORT.md).  
> *Note: Hallwright's own protocol and CLI codebase is verified across 580+ automated unit, regression, and mutation tests.*

---

## 🔌 Model Context Protocol (MCP 2.0 Server)

Hallwright exposes its inspection, memory, and library suite as standard JSON-RPC 2.0 tools for Claude Desktop, Claude Code, Cursor, Windsurf, and Antigravity:

```bash
# Start MCP server over stdio:
hallwright mcp
# or: python mcp/server.py
```

### Exposed MCP Tools:
- `hallwright_select_masters` (`artisan_select_masters`) — Context-aware selection of relevant domain leads based on task keywords.
- `hallwright_inject_prompt` (`artisan_inject_prompt`) — Generates a task-targeted 2K-token prompt (~6x context optimization).
- `hallwright_inspect_code` (`artisan_inspect_code`) — Pre-commit AST-level flaw and secret leak analysis on code strings.
- `hallwright_get_lessons` (`artisan_get_lessons`) — Searches past scar tissue and mistakes to prevent repeating bugs.
- `hallwright_record_learning` (`artisan_record_learning`) — Writes lessons and success patterns into persistent storage.
- `hallwright_resume_continuity` (`artisan_resume_continuity`) — Retrieves cross-agent continuity state and checkpoints.
- `hallwright_save_checkpoint` (`artisan_save_checkpoint`) — Saves task progress and blockers across sessions.
- `hallwright_get_library` (`artisan_get_library`) — Retrieves production implementation modules (`auth`, `db`, `payments`, etc.).
- `hallwright_review_code` (`artisan_review_code`) — Runs adversarial red-team code review on diffs or source code.
- `hallwright_get_persona` (`artisan_get_persona`) — Retrieves full discipline criteria and pledge for any Council Master.
- `hallwright_list_council` (`artisan_list_council`) — Lists the Council roster.
- `hallwright_recall_memory` (`artisan_recall_memory`) — Direct query interface for memory ledger.

---

## 📦 Universal Production Libraries (`src/libraries/`)

Hallwright includes zero-dependency, production-grade building blocks ready for immediate use via `hallwright lib <domain>`:

| Domain Module | Path | Description |
| :--- | :--- | :--- |
| **Auth & Security** | [`src/libraries/auth_security.py`](./src/libraries/auth_security.py) | PBKDF2/HMAC-SHA256 password hashing, constant-time verification, cryptographic tokens, role permissions. |
| **Database Engine** | [`src/libraries/database.py`](./src/libraries/database.py) | Parameterized SQLite connection pooling, schema migrations, and transaction management with zero string interpolation. |
| **Payments & Billing** | [`src/libraries/payments.py`](./src/libraries/payments.py) | Idempotent payment intent processing, double-charge defense, webhook signature verification. |
| **Real-Time PubSub** | [`src/libraries/real_time.py`](./src/libraries/real_time.py) | In-memory pub/sub broker with regex topic matching, backpressure buffering, thread-safe delivery. |
| **Caching Layer** | [`src/libraries/caching.py`](./src/libraries/caching.py) | Thread-safe LRU/TTL cache with expiration sweeps, cache-stampede locking, cache-aside decorators. |
| **Resilient HTTP Client** | [`src/libraries/resilient_http.py`](./src/libraries/resilient_http.py) | Standard-library HTTP client with exponential backoff, jitter, circuit breaker state machine, timeouts. |

---

## 📁 Supported AI Agent Ecosystems

Hallwright configures 14 agent environments with native instructions and rule sets:

| # | Agent Environment | Target Platform | Core Config Files |
| :- | :--- | :--- | :--- |
| 1 | 🤖 [`antigravity-agent/`](./antigravity-agent/) | **Google Antigravity & Gemini CLI** | `.agents/plugins/`, `AGENTS.md`, `skills/` |
| 2 | 🧠 [`claude-code-agent/`](./claude-code-agent/) | **Anthropic Claude Code CLI** | `CLAUDE.md`, `skills/` |
| 3 | ⚡ [`cursor-agent/`](./cursor-agent/) | **Cursor AI Code Editor** | `.cursorrules`, `.cursor/rules/*.mdc`, `skills/` |
| 4 | 🐙 [`copilot-agent/`](./copilot-agent/) | **GitHub Copilot (CLI & Workspace)** | `.github/copilot-instructions.md`, `skills/` |
| 5 | 🌊 [`windsurf-agent/`](./windsurf-agent/) | **Windsurf IDE (Cascade AI)** | `.windsurfrules`, `skills/` |
| 6 | 🛠️ [`cline-agent/`](./cline-agent/) | **Cline & Roo Code (VS Code Extension)** | `.clinerules`, `skills/`, `mcp/server.py` |
| 7 | 🌙 [`kimi-agent/`](./kimi-agent/) | **Moonshot Kimi Code Agent** | `KIMI.md`, `skills/`, `mcp/server.py` |
| 8 | ⚡ [`kilo-agent/`](./kilo-agent/) | **Kilo Code Agent** | `KILO.md`, `skills/`, `mcp/server.py` |
| 9 | 🏛️ [`hermes-agent/`](./hermes-agent/) | **Nous Research Hermes Agent OS** | `HERMES.md`, `system_prompt.txt`, `skills/` |
| 10| 💻 [`codex-agent/`](./codex-agent/) | **OpenAI Codex CLI** | `CODEX.md`, `.codex/config.json`, `skills/` |
| 11| 🥧 [`pie-agent/`](./pie-agent/) | **Pi / Pie Coding Agent CLI (Rust)** | `PIE.md`, `.pie/config.json`, `skills/` |
| 12| 🖥️ [`opencode-agent/`](./opencode-agent/) | **OpenCode Terminal TUI Agent** | `OPENCODE.md`, `.opencode/agent.json`, `skills/` |
| 13| 🦅 [`openclaw-agent/`](./openclaw-agent/) | **OpenClaw Autonomous Agent Platform** | `OPENCLAW.md`, `.openclaw/agent_manifest.json`, `skills/` |
| 14| 🐍 [`universal-python-agent/`](./universal-python-agent/) | **Python, LangChain, AutoGen, CrewAI** | `craftsman/` SDK, `example.py`, `skills/` |

---

## 🚀 Reusable GitHub Action (`@v2` / `@v1`)

Audit Pull Requests and Pushes automatically in your CI workflow (`.github/workflows/artisan.yml`):

```yaml
name: Hallwright Quality Gate
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Hallwright Quality & Security Gate
        uses: kapitan00000978-sketch/hallwright@v2
```
*(Both `@v2` and `@v1` tags resolve to current stable releases).*

---

## 📚 Deep-Dive Documentation (`docs/`)

Specialized tools and extended documentation are maintained in `docs/`:

- **Complete 64-Master Council Roster:** [`docs/COUNCIL.md`](./docs/COUNCIL.md) (All 64 domain personas across 8 guilds).
- **Hallwright Studio (Visual UI Audits):** [`docs/STUDIO.md`](./docs/STUDIO.md) (Playwright headless Chromium visual capture and DOM checks).
- **AST Mutation Testing Engine:** [`docs/MUTATION_TESTING.md`](./docs/MUTATION_TESTING.md) (Test assertiveness verification via semantic mutants).
- **Adversarial Red-Team Code Review:** [`docs/RED_TEAM_REVIEW.md`](./docs/RED_TEAM_REVIEW.md) (Independent defect ledger and PR review generation).

---

## 💻 CLI Command Reference

```bash
# ⚡ Initialization & Setup
hallwright init                 # Auto-detects stack, installs pre-commit hook & agent configs
hallwright doctor               # Diagnostic check on git hooks, MCP, and agent rules

# 🛡️ Quality Audit & Auto-Fix
hallwright audit                # Audits entire repository for stubs, secrets & bad patterns
hallwright audit --staged       # Fast audit on git-staged changes only
hallwright fix                  # Automatically repairs silent catches and unfinished stubs

# 🎯 Context & Memory
hallwright context "<task>"     # Generates targeted 2K-token prompt (~6x context optimization)
hallwright memory               # Inspects living persistent memory and recorded scar tissue
hallwright memory --search "jwt" # Search historical lessons by keyword

# 🤖 Swarm Coordination (Planning for Host Agent)
hallwright swarm "<task>" --plan # Previews multi-agent decomposition plan
hallwright swarm "<task>"       # Registers session locks for the planned stages
hallwright agents               # Displays active agent concurrency and file locks

# 🔄 Cross-Agent Continuity
hallwright resume               # Resumes from last agent checkpoint
hallwright checkpoint "<msg>"   # Checkpoints active progress and blockers
hallwright resume --no-continuity # Disables continuity tracking

# 📦 Enterprise Libraries
hallwright lib auth             # Inspects and exports production auth & security library
hallwright lib db               # Inspects database connection pool & migration library
hallwright lib payments         # Inspects idempotent payment processing library
hallwright lib list             # Lists all available domain libraries

# 🌐 Protocol Server & Metrics
hallwright mcp                  # Launches Model Context Protocol JSON-RPC 2.0 server
hallwright metrics              # Prints workspace quality score and file statistics
```

---

## 🔍 Scope & Limitations

- **Pre-Commit Defense:** The gatekeeper (`scripts/pre-commit-gatekeeper.py`) inspects staged source files and AST nodes before git commits are finalized.
- **Deterministic Scope:** The gatekeeper deterministically detects unfinished stubs, bare exception catches (`except: pass`, empty `catch {}`), dangerous dynamic code execution, and hardcoded secrets. It does not replace application-specific business logic tests.
- **Host Execution:** Hallwright does not run an LLM. Your host agent executes all coding actions; Hallwright acts as the deterministic verification and memory layer.
- **Local Continuity:** Checkpoints track files, status, and notes in `.artisan/continuity.json`. It is fully local and does not transmit code to external servers.

---

## 📄 License
MIT License. Open source under the MIT License.
