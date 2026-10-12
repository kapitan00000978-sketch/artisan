# 🛡️ Humanpowers: AI Agent Kasbiy Xulq-Atvor & Mas'uliyat Tizimi

> **Humanpowers** — AI agentlarga insoniy mas'uliyat, kasbiy vijdon va "Zero Babysitting" (orqadan poylashni yo'qotish) falsafasini beruvchi to'liq ekotizim.

---

## ⚡ Asosiy Imkoniyatlar:

1. **🧠 Doimiy Xotira & Scar Tissue (`.humanpowers/memory.json`):**
   Agent loyihadagi xatolar va foydalanuvchi didini doimiy eslab qoladi. Bir xil xato 0% takrorlanadi.
2. **🔌 Model Context Protocol (MCP) Server (`mcp/server.py`):**
   Cursor, Claude, Antigravity va boshqa agentlar uchun rasmiy MCP server. Agentlar sifat nazorati vositalarini to'g'ridan-to'g'ri chaqira oladi.
3. **🚀 GitHub Actions CI/CD Quality Gate (`.github/workflows/humanpowers-gate.yml`):**
   GitHub'dagi har bir Pull Request va Push'ni avtomatik tekshirib, sifat muhri bosuvchi avtonom quvur.
4. **👁️ Real-Vaqt Watchdog Qo'riqchisi (`scripts/watchdog.py`):**
   Kodni yozayotganingizda chala `// TODO`, ochiq API kalitlar yoki yashirin xatolarni shu zahotiyoq aniqlaydi.
5. **🛡️ Git Pre-Commit Gatekeeper (`scripts/pre-commit-gatekeeper.py`):**
   Commitdan oldin sifat darajasi 95 balldan past bo'lgan kodlarni bloklaydi va tuzatishni talab qiladi.
6. **🎭 Persona Forge (`cli/persona_forge.py`):**
   Istalgan yangi kasbni bitta buyruq bilan yaratish.
7. **📊 Tejalgan Vaqt & ROI Hisoblagichi (`scripts/roi_tracker.py`):**
   Qancha soat va asab tejalganini aniq raqamlarda ko'rsatadi.
8. **🖥️ Interaktiv Terminal Boshqaruv Markazi (`cli/dashboard.py`):**
   Loyihaning barcha holati va agentlar matritsasini ko'rsatuvchi vizual HUD.

---

## 📁 11 Ta AI Agent Uchun Alohida Papkalar:

| # | AI Agent Papkasi | Qaysi Platforma Uchun |
| :- | :--- | :--- |
| 1 | 🤖 [`antigravity-agent/`](./antigravity-agent/) | **Google Antigravity & Gemini CLI** |
| 2 | 🧠 [`claude-code-agent/`](./claude-code-agent/) | **Anthropic Claude Code CLI** |
| 3 | ⚡ [`cursor-agent/`](./cursor-agent/) | **Cursor AI Code Editor** |
| 4 | 🐙 [`copilot-agent/`](./copilot-agent/) | **GitHub Copilot (CLI & Workspace)** |
| 5 | 🌊 [`windsurf-agent/`](./windsurf-agent/) | **Windsurf IDE (Cascade AI)** |
| 6 | 🏛️ [`hermes-agent/`](./hermes-agent/) | **Nous Research Hermes Agent OS** |
| 7 | 💻 [`codex-agent/`](./codex-agent/) | **OpenAI Codex CLI** |
| 8 | 🥧 [`pie-agent/`](./pie-agent/) | **Pi / Pie Coding Agent CLI (Rust)** |
| 9 | 🖥️ [`opencode-agent/`](./opencode-agent/) | **OpenCode Terminal TUI Agent** |
| 10| 🦅 [`openclaw-agent/`](./openclaw-agent/) | **OpenClaw Autonomous Agent Platform** |
| 11| 🐍 [`universal-python-agent/`](./universal-python-agent/) | **Python, LangChain, AutoGen, CrewAI** |

---

## 🛠️ Tezkor Buyruqlar:
```bash
# Boshqaruv HUD markazini ochish:
python cli/dashboard.py

# Real-vaqt Watchdog skanerini yurgizish:
python scripts/watchdog.py

# Tejalgan vaqt va ROI hisobotini ko'rish:
python scripts/roi_tracker.py

# MCP serverni ishga tushirish:
python mcp/server.py
```
