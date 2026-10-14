<p align="center">
  <img src="./assets/artisan-banner.jpg" alt="Artisan Banner" width="800" />
</p>

# 🛡️ Artisan: Autonomous AI Agent Craftsmanship & Quality Protocol

> **Artisan** is an open-source engineering discipline and quality protocol for AI coding assistants. It enforces deterministic pre-commit & CI gates against unfinished stubs and leaked secrets, injects role-based expert personas, maintains persistent project memory across sessions, and exposes standard Model Context Protocol (MCP) tooling for Claude Code, Cursor, Copilot, Windsurf, Antigravity, and other modern agents.

[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Protocol](https://img.shields.io/badge/protocol-Artisan%201.0-emerald.svg)](AGENTS.md)
[![Council of Masters](https://img.shields.io/badge/council%20of%20masters-8%20titans-gold.svg)](#-the-council-of-masters-character-roster)
[![Agents](https://img.shields.io/badge/supported%20agents-11-cyan.svg)](#-supported-ai-agent-ecosystems)
[![Pre-Commit Quality Gate](https://img.shields.io/badge/quality--gate-pre--commit-purple.svg)](AGENTS.md)

---

## 📌 Loyiha Tasnifi (Project Description)

**Artisan nima?**  
Artisan — bu dasturchi va AI coding agentlari (Claude Code, Cursor, Copilot, Windsurf, Antigravity va boshqalar) o‘rtasidagi sifat ko‘prigi. Standart AI modellar tez va ko‘p kod yozadi, biroq ularda doimiy intizom yo‘q: kod ichida chala `TODO`lar, bo‘sh `except: pass` bloklari, xavfli `eval()` chaqiriqlari yoki tasodifan qoldirib ketilgan API kalitlar paydo bo‘ladi. 

Artisan bu muammoni 4 ta ustun orqali hal qiladi:
1. **🛡️ Mustaqil Pre-Commit & CI Filtrlari (`scripts/detector.py`):** Kod git repoga kiritilishidan oldin har bir faylni statik tahlil qiladi. Maxfiy kalitlar (`sk-...`, `ghp_...`, `AKIA...`), xavfli buyruqlar va chala stubs topilsa, commit qat'iy to‘xtatiladi.
2. **🏛️ The Council of Masters (Senior Heuristics):** AI agentiga arxitektura, xavfsizlik, SRE, ML va UI/UX bo‘yicha 8 nafar Senior darajadagi mutaxassis tajribasi va mezonlarini kontekst sifatida yuklaydi.
3. **🧠 Doimiy Loyiha Xotirasi (`.artisan/memory.json`):** Loyihaning arxitekturaviy qoidalari va o‘tmishdagi xatolarini saqlab qoladi, shunda AI agent bir xil xatoni qayta takrorlamaydi.
4. **🔌 Model Context Protocol (MCP) Serveri (`mcp/server.py`):** Standart JSON-RPC 2.0 orqali AI muhitlariga kod tahlili va rollarni to‘g‘ridan-to‘g‘ri vosita (tool) sifatida taqdim etadi.

---

## 🎯 The Problem: Iterative Prompt Micromanagement
Developers often spend significant time micromanaging AI coding assistants:
- Base models may rush to generate boilerplate, occasionally leaving unfinished `TODO` stubs, unhandled boundary conditions, or unparameterized queries.
- Users frequently enter an iterative correction loop: *"Fix this error, you broke that import, handle this edge case."*
- **Artisan addresses this:** By embedding structured domain rules and automated quality checks directly into agent configuration files, the assistant self-audits before presenting results.

---

## 🔍 How It Works & Limitations

- **Session-Based Rules:** Rules files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, etc.) load per agent session into your assistant's system instructions.
- **Local Tooling:** The file sentinel watchdog (`scripts/watchdog.py`) and pre-commit gatekeeper (`scripts/pre-commit-gatekeeper.py`) are local command-line tools that run on your machine and in CI.
- **Limitations:** The gate catches the listed patterns (stubs, dangerous eval/exec, hardcoded secrets), not all bugs.
- **Demo Simulation Module:** The web engine in `src/engine/craftsmanshipEngine.js` is a non-functional, client-side interactive DEMO simulation for UI previewing; production enforcement is carried out by `scripts/detector.py` and the MCP server.

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

1. **🧠 Project Memory Ledger (`.artisan/memory.json`):**
   Maintains a structured record of team conventions, user preferences, and recorded anti-patterns to avoid repeating known mistakes.
2. **🔌 Model Context Protocol (MCP) Server (`mcp/server.py`):**
   Standard JSON-RPC 2.0 MCP server allowing Claude, Cursor, and other MCP clients to query domain personas and run static code inspections.
3. **🚀 GitHub Actions CI/CD Quality Gate (`.github/workflows/artisan-gate.yml`):**
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
curl -fsSL https://raw.githubusercontent.com/kapitan00000978-sketch/artisan/main/install.sh | bash

# 🪟 Windows PowerShell (1-line installer):
irm https://raw.githubusercontent.com/kapitan00000978-sketch/artisan/main/install.ps1 | iex

# 📦 Node.js / npx (directly from GitHub repo):
npx github:kapitan00000978-sketch/artisan init

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

# 7. Install Automatic Git Pre-Commit Hook:
python scripts/install_git_hook.py
```

### 💻 Artisan CLI (`npx artisan`):

```bash
# Install protocol rules into current repository
npx github:kapitan00000978-sketch/artisan init

# Automatically install Git pre-commit quality gate hook
npx github:kapitan00000978-sketch/artisan hook

# Verify configuration and environment health
npx github:kapitan00000978-sketch/artisan doctor

# Run fast audit on staged changes
npx github:kapitan00000978-sketch/artisan audit --staged

# Launch the Model Context Protocol (MCP) server
npx github:kapitan00000978-sketch/artisan mcp
```

---

## 📄 License
MIT License. Created for the global developer community.
