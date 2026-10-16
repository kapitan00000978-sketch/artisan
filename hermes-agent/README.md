# 🏛️ Artisan for Nous Research Hermes Agent

Empowered by the Artisan Autonomous Quality & Craftsmanship Protocol.

This directory configures **Nous Research Hermes Agent OS** and local Hermes LLMs (Hermes 2 Pro, Hermes 3, OpenHermes) with deterministic quality enforcement, defensive architecture, and persistent memory.

---

## 📦 Contents:
- **`HERMES.md`** — Universal Hermes agent configuration and craftsmanship protocol. Copied into project roots via `artisan init`.
- **`system_prompt.txt`** — Direct system prompt block ready for insertion into local Hermes inference runners (vLLM, Ollama, LM Studio, TGI).
- **`skills/`** — Artisan domain skills for sub-agents and tool-calling execution.

---

## ⚡ Quick Start:

### Option 1: 1-Click CLI Setup (Recommended)
```bash
# In your target project root:
artisan init
```
This automatically deploys `HERMES.md` alongside your Git pre-commit quality gate and `.artisan/memory.json`.

### Option 2: Local LLM Inference Runner
When invoking OpenHermes or Hermes 3 via Ollama, llama.cpp, or vLLM, load `system_prompt.txt` as the system directive:
```python
system_prompt = open("hermes-agent/system_prompt.txt", "r", encoding="utf-8").read()
# Inject into your chat completion request
```

### Option 3: Hermes Agent OS
Place `HERMES.md` in the working directory of Hermes Agent OS or register it in your agent runtime settings.

---

## 🎯 Enforced Standards:
1. **Zero-Defect Self-Inspection:** Zero stubs (`TODO`, `FIXME`, `pass`), zero silent error suppressions, zero hardcoded secrets.
2. **Defensive Architecture:** Built-in defenses against SQLi, XSS, SSRF, memory leaks, and race conditions.
3. **Background Auto-Correction:** Silently repairs any defect or test regression before user reporting.
4. **Persistent Learning:** Seamlessly accesses `.artisan/memory.json` to avoid past project mistakes.
5. **Cross-Agent Continuity (Optional):** Check `.artisan/agent_handoff.md` or run `artisan resume` to pick up work precisely where Cursor, Claude, or Copilot left off. Use `artisan checkpoint` to leave notes for the next agent.
6. **Universal Domain Libraries:** Ready-to-connect toolkits in `src/libraries/` (Architecture FSM/CircuitBreaker, Security Sanitizer/JWT, Performance RingBuffer/Cache, Testing Fuzzers, Standalone 3D Canvas).
7. **Swarm & Adversarial Review:** Run `artisan swarm "<task>"` for multi-agent decomposition and `artisan review` for Gabriel Frost & Marcus Sterling PR review.
