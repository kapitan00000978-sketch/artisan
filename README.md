<p align="center">
  <img src="./assets/artisan-banner.jpg" alt="Artisan Banner" width="100%" />
</p>

# 🛡️ Artisan: Autonomous AI Agent Craftsmanship & Quality Protocol

> **Artisan** — An open-source protocol and modular framework that brings engineering responsibility, professional craftsmanship, and automated quality gates into AI coding workflows. Designed to reduce prompt babysitting.

[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Protocol](https://img.shields.io/badge/protocol-Artisan%201.0-emerald.svg)](AGENTS.md)

[![Council of Masters](https://img.shields.io/badge/council%20of%20masters-8%20titans-gold.svg)](#-the-council-of-masters-character-roster)
[![Agents](https://img.shields.io/badge/supported%20agents-11-cyan.svg)](#-supported-ai-agent-ecosystems)
[![Self--Correction](https://img.shields.io/badge/quality--gate-enforced-purple.svg)](AGENTS.md)

---

## 🎯 The Problem: Iterative Prompt Micromanagement
Developers often spend significant time micromanaging AI coding assistants:
- Base models may rush to generate boilerplate, occasionally leaving unfinished `TODO` stubs, unhandled boundary conditions, or unparameterized queries.
- Users frequently enter an iterative correction loop: *"Fix this error, you broke that import, handle this edge case."*
- **Artisan addresses this:** By embedding structured domain rules and automated quality checks directly into agent configuration files, the assistant self-audits before presenting results.

---

## 🏛️ The Council of Masters (Domain Heuristics):

Artisan packages role-specific heuristics inspired by senior discipline leads:


| # | Master | Discipline & Role | Archetype | Core Focus |
| :- | :--- | :--- | :--- | :--- |
| 1 | 💻 **Marcus 'The Vanguard' Sterling** | Senior Software Architect & Systems Lead | Systems Sovereign & Zero-Tech-Debt Purist | SOLID architecture, zero unhandled stubs, concurrency |
| 2 | 🎯 **Diana 'The Closer' Drake** | Direct-Response Conversion Copywriter | Neuromarketing Alchemist & Persuasion Virtuoso | High-clarity hooks, value proposition, zero AI filler |
| 3 | 🎨 **Elena 'The Visionary' Rostova** | Principal UI/UX Designer & Systems Architect | Aesthetic Sovereign & Spatial Ergonomics Master | WCAG 2.1 AAA accessibility, 8pt spatial grid, design tokens |
| 4 | 📊 **Victor 'The Fortress' Montgomery** | Startup Financial Strategist & Fractional CFO | Unit-Economics Inquisitor & Capital Defense | Unit economics, burn rate, cash conversion cycles |
| 5 | ⚖️ **Arthur 'The Ironclad' Pendelton** | Senior Commercial Counsel & Contract Auditor | Commercial Safeguard & Contractual Litigator | Contract auditing, liability containment, clear definitions |
| 6 | 🔬 **Dr. Evelyn 'The Oracle' Reed** | Staff Data Scientist & ML Systems Architect | Empirical Scientist & ML Ops Gatekeeper | Data leakage prevention, statistical validation, model drift |
| 7 | 🛡️ **Gabriel 'The Sentinel' Frost** | Principal Cybersecurity & Offensive Auditor | Zero-Trust Inquisitor & Threat Modeling | OWASP Top 10, credential protection, parameterized queries |
| 8 | ⚡ **Gareth 'The Unbreakable' Drake** | DevOps & Cloud Site Reliability Architect | Chaos Engineering Commander & Reliability | Idempotent IaC, container best practices, health probes |

---

## ⚡ Core Capabilities & Built-in Tooling:

1. **🧠 Project Memory Ledger (`.humanpowers/memory.json`):**
   Maintains a structured record of team conventions, user preferences, and recorded anti-patterns to avoid repeating known mistakes.
2. **🔌 Model Context Protocol (MCP) Server (`mcp/server.py`):**
   Standard JSON-RPC 2.0 MCP server allowing Claude, Cursor, and other MCP clients to query domain personas and run static code inspections.
3. **🚀 GitHub Actions CI/CD Quality Gate (`.github/workflows/humanpowers-gate.yml`):**
   Automated pull request and push inspection that verifies test suites and checks for lazy stubs or exposed credentials.
4. **👁️ Real-Time Watchdog Daemon (`scripts/watchdog.py`):**
   Continuous background file sentinel (`--watch`) that monitors local edits and flags stubs, empty catches, and credential leaks.
5. **🛡️ Git Pre-Commit Gatekeeper (`scripts/pre-commit-gatekeeper.py`):**
   Pre-commit hook stopping unfinished stubs, silent exception suppressions, or plaintext keys before git commits.
6. **🎭 Persona Forge (`cli/persona_forge.py`):**
   CLI to create and register custom domain checklists and personas.
7. **📊 Workspace Quality & Audit Report (`scripts/roi_tracker.py`):**
   Inspects and reports real workspace metrics: active files, total lines audited, and gatekeeper compliance.
8. **🖥️ Interactive Terminal HUD (`cli/dashboard.py`):**
   Terminal dashboard displaying active protocol status, Council roster, and heuristic checklists.

---

## 📁 Supported AI Agent Ecosystems:

Artisan provides tailored configuration modules across 11 agent environments:

| # | Agent Environment | Target Platform | Core Config Files |
| :- | :--- | :--- | :--- |
| 1 | 🤖 [`antigravity-agent/`](./antigravity-agent/) | **Google Antigravity & Gemini CLI** | `.agents/plugins/`, `AGENTS.md`, `skills/` |
| 2 | 🧠 [`claude-code-agent/`](./claude-code-agent/) | **Anthropic Claude Code CLI** | `CLAUDE.md`, `skills/` |
| 3 | ⚡ [`cursor-agent/`](./cursor-agent/) | **Cursor AI Code Editor** | `.cursorrules`, `.cursor/rules/*.mdc`, `skills/` |
| 4 | 🐙 [`copilot-agent/`](./copilot-agent/) | **GitHub Copilot (CLI & Workspace)** | `.github/copilot-instructions.md`, `skills/` |
| 5 | 🌊 [`windsurf-agent/`](./windsurf-agent/) | **Windsurf IDE (Cascade AI)** | `.windsurfrules`, `skills/` |
| 6 | 🏛️ [`hermes-agent/`](./hermes-agent/) | **Nous Research Hermes Agent OS** | `HERMES.md`, `system_prompt.txt`, `skills/` |
| 7 | 💻 [`codex-agent/`](./codex-agent/) | **OpenAI Codex CLI** | `CODEX.md`, `.codex/config.json`, `skills/` |
| 8 | 🥧 [`pie-agent/`](./pie-agent/) | **Pi / Pie Coding Agent CLI (Rust)** | `PIE.md`, `.pie/config.json`, `skills/` |
| 9 | 🖥️ [`opencode-agent/`](./opencode-agent/) | **OpenCode Terminal TUI Agent** | `OPENCODE.md`, `.opencode/agent.json`, `skills/` |
| 10| 🦅 [`openclaw-agent/`](./openclaw-agent/) | **OpenClaw Autonomous Agent Platform** | `OPENCLAW.md`, `.openclaw/agent_manifest.json`, `skills/` |
| 11| 🐍 [`universal-python-agent/`](./universal-python-agent/) | **Python, LangChain, AutoGen, CrewAI** | `craftsman/` SDK, `example.py`, `skills/` |

---

## ⚡ Quick Installation:

Install Artisan configuration files into any repository:


```bash
# 🍏 Linux & macOS (curl bash installer):
curl -fsSL https://raw.githubusercontent.com/kapitan00000978-sketch/humanpowers/main/install.sh | bash

# 🪟 Windows PowerShell (1-line installer):
irm https://raw.githubusercontent.com/kapitan00000978-sketch/humanpowers/main/install.ps1 | iex

# 📦 Node.js / npx (directly from GitHub repo):
npx github:kapitan00000978-sketch/humanpowers init

# 🐍 Universal Python CLI:
python cli/installer.py --agent all
```

---

## 🛠️ Developer Commands:

```bash
# 1. Run the Automated Test Suite:
pytest tests/

# 2. Run the Pre-Commit Quality & Security Gatekeeper:
python scripts/pre-commit-gatekeeper.py

# 3. Launch the Continuous Watchdog Sentinel Daemon:
python scripts/watchdog.py --watch

# 4. View Workspace Quality & Metrics Report:
python scripts/roi_tracker.py

# 5. Launch the Terminal HUD:
python cli/dashboard.py

# 6. Start the Model Context Protocol (MCP) Server:
python mcp/server.py
```

---

## 📄 License
MIT License. Created for the global developer community.
