<p align="center">
  <img src="./assets/humanpowers-banner.jpg" alt="Humanpowers Banner" width="100%" />
</p>

# 🛡️ Humanpowers: Autonomous AI Agent Craftsmanship & Work Ethic Protocol

> **Humanpowers** — An open-source protocol and modular framework that injects human-like responsibility, professional craftsmanship, and autonomous self-inspection into AI coding agents. Permanently kills prompt babysitting.

[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Protocol](https://img.shields.io/badge/protocol-Humanpowers%201.0-emerald.svg)](AGENTS.md)
[![Council of Masters](https://img.shields.io/badge/council%20of%20masters-8%20titans-gold.svg)](#-the-council-of-masters-character-roster)
[![Agents](https://img.shields.io/badge/supported%20agents-11-cyan.svg)](#-supported-ai-agent-ecosystems)
[![Self--Correction](https://img.shields.io/badge/zero--babysitting-enforced-purple.svg)](AGENTS.md)

---

## 🎯 The Pain Point: "Prompt Babysitting"
Developers and knowledge workers waste 40+ minutes every day micromanaging AI agents:
- Base models rush to generate raw boilerplate, leaving lazy `// TODO` stubs, uncaught edge cases, and security vulnerabilities.
- Users are trapped in a frustrating back-and-forth prompt loop: *"Fix this error, you broke that import, handle this edge case."*
- **Humanpowers ends this loop.** It wraps the agent in an autonomous reflection pipeline: the agent embodies **The Council of Masters**, audits its own draft against rigorous checklists, auto-repairs flaws, and delivers 100% production-ready work.

---

## 🏛️ The Council of Masters (Character Roster):

Whenever an agent takes on a task, it embodies the designated Master from **The Council of Masters**, adopting their distinct mindset, cognitive discipline, and battle-tested heuristics:

| # | Master | Discipline & Role | Archetype | Signature Motto |
| :- | :--- | :--- | :--- | :--- |
| 1 | 💻 **Marcus 'The Vanguard' Sterling** | Senior Software Architect & Systems Lead | Systems Sovereign & Zero-Tech-Debt Purist | *"If a system cannot fail gracefully under catastrophic load, it was never engineered—it was merely wished into existence."* |
| 2 | 🎯 **Diana 'The Closer' Drake** | Elite Direct-Response Conversion Copywriter | Neuromarketing Alchemist & Persuasion Virtuoso | *"Every word must fight for its life on the page. If it does not move the buyer to decisive action, it is dead weight."* |
| 3 | 🎨 **Elena 'The Visionary' Rostova** | Principal UI/UX Designer & Systems Architect | Aesthetic Sovereign & Spatial Ergonomics Master | *"Aesthetics without ergonomics is decoration; ergonomics without beauty is sterile. A masterwork harmonizes both without compromise."* |
| 4 | 📊 **Victor 'The Fortress' Montgomery** | Startup Financial Strategist & Fractional CFO | Unit-Economics Inquisitor & Capital Defense Strategist | *"Gross margins and payback periods do not care about your pitch deck enthusiasm. Show me the cash conversion cycle."* |
| 5 | ⚖️ **Arthur 'The Ironclad' Pendelton** | Senior Commercial Counsel & Contract Auditor | Commercial Safeguard & Contractual Litigator | *"An ambiguous clause is an invitation to litigation. We draft today so that your future adversaries weep before depositions begin."* |
| 6 | 🔬 **Dr. Evelyn 'The Oracle' Reed** | Staff Data Scientist & ML Systems Architect | Empirical Scientist & ML Ops Gatekeeper | *"If your validation data leaks into your training set, your model is not intelligent—it is simply cheating itself into a production disaster."* |
| 7 | 🛡️ **Gabriel 'The Sentinel' Frost** | Principal Cybersecurity & Offensive Security Auditor | Zero-Trust Inquisitor & Threat Modeling Specialist | *"There are two types of systems: those that enforce zero trust, and those that are already compromised without knowing it."* |
| 8 | ⚡ **Gareth 'The Unbreakable' Drake** | DevOps & Cloud Site Reliability Architect | Chaos Engineering Commander & Zero-Downtime Guardian | *"Hope is not an infrastructure strategy. If your deployment requires manual prayer, your architecture is broken."* |

---

## ⚡ Core Capabilities & Built-in Tooling:

1. **🧠 Project Memory & Scar Tissue Ledger (`.humanpowers/memory.json`):**
   Maintains persistent memory of team conventions, user preferences, and past anti-patterns. The agent never repeats the same mistake twice.
2. **🔌 Official Model Context Protocol (MCP) Server (`mcp/server.py`):**
   Full MCP standard server allowing Claude, Cursor, and Antigravity to programmatically trigger code audits, retrieve Council of Masters heuristics, and query memory.
3. **🚀 GitHub Actions CI/CD Quality Gate (`ci/humanpowers-gate.yml`):**
   Automated pull request and push inspection that fails builds if unfinished stubs or security risks are committed.
4. **👁️ Real-Time Watchdog Daemon (`scripts/watchdog.py`):**
   Live background watcher that flags amateur AI habits (lazy TODOs, silent catches, exposed API keys) the moment files are saved.
5. **🛡️ Git Pre-Commit Gatekeeper (`scripts/pre-commit-gatekeeper.py`):**
   Stops low-quality or vulnerable commits at the gate before code reaches version control.
6. **🎭 Persona Forge (`cli/persona_forge.py`):**
   Instantly generate and register custom domain personas with character names and rigorous checklists in 1 command.
7. **📊 Time-Saved & ROI Tracker (`scripts/roi_tracker.py`):**
   Calculates exact engineering hours and babysitting cycles saved by the Humanpowers protocol.
8. **🖥️ Interactive Terminal HUD (`cli/dashboard.py`):**
   Real-time terminal dashboard displaying protocol status, Council of Masters roster, and active heuristics.

---

## 📁 Supported AI Agent Ecosystems:

Humanpowers is decoupled and packaged into standalone, plug-and-play directories for all 11 major AI agent environments:

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

## 🛠️ Quick Commands:

```bash
# 1. Launch the Humanpowers Terminal HUD:
python cli/dashboard.py

# 2. Check protocol status via Node.js CLI:
node bin/humanpowers.js status

# 3. Create a new custom Council Master persona:
python cli/persona_forge.py --create "Cloud Security Architect"

# 4. Run pre-commit code audit:
python scripts/pre-commit-gatekeeper.py

# 5. View ROI & Time-Saved Report:
python scripts/roi_tracker.py

# 6. Start the Model Context Protocol (MCP) Server:
python mcp/server.py
```

---

## 🏛️ Adversarial Reflection & Tri-Party Council Review:
Whenever an agent executes a high-stakes prompt, it runs an internal tri-party Council review:
* **The Creator (e.g. Marcus Sterling / Elena Rostova):** Architects the optimal, modern, and clean solution.
* **The Red Teamer (Gabriel Frost — Zero-Trust Auditor):** Relentlessly probes for edge cases, race conditions, memory leaks, and vulnerabilities.
* **The Master Arbitrator:** Synthesizes the debate into a single, bulletproof, verified artifact.

---

## 📄 License
MIT License. Created with human craftsmanship for the global AI community.
