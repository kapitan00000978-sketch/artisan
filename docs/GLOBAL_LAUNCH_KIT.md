# 🚀 HALLWRIGHT: Real-World Distribution & Promotion Playbook

> **Goal:** How to organically introduce Hallwright to real software engineers across Hacker News, Reddit, Twitter/X, and developer communities worldwide without bots, spam, or friction.

---

## 🎯 1. HACKER NEWS (Show HN) — STEP-BY-STEP

Hacker News ([news.ycombinator.com](https://news.ycombinator.com)) is the most respected community of software engineers. Anyone can post a "Show HN" without requiring approval or bots.

### 📅 Optimal Submission Timing:
- **Best Days:** Tuesday, Wednesday, or Thursday.
- **Best Time:** 8:00 AM – 9:00 AM EST (1:00 PM – 2:00 PM UTC). This catches both European afternoon and US morning traffic.

### 📝 Title to use:
```text
Show HN: Hallwright – Pre-commit guardrails and living memory for AI coding agents
```

### 💬 Submission Text / First Comment (Copy & Paste):
```markdown
Hey HN,

Over the past year, our team has been relying heavily on AI coding assistants (Claude Code, Cursor, Copilot, Antigravity). While their speed is astonishing, we kept running into the same 3 failure modes:

1. The "TODO: implement later" trap: The model outputs 90% of a function, leaves the critical 10% as an unfinished stub (`pass` or `// TODO`), and claims the task is complete.
2. Silent error suppression: Converting difficult edge cases into `except: pass` or empty `catch {}` blocks, silently hiding bugs.
3. Total session amnesia: Every new session forgets the architectural constraints and bug fixes learned yesterday.

We realized prompt engineering ("please don't leave TODOs") is unreliable because LLMs are probabilistic token predictors. What developer workflows actually need is a **deterministic pre-commit gate and persistent memory layer**.

So we built Hallwright: https://github.com/kapitan00000978-sketch/hallwright

### What Hallwright actually does:
- **Deterministic AST Pre-Commit Gate:** Inspects Abstract Syntax Trees and git-staged changes in < 3 seconds. If an AI generates unfinished stubs, bare exception catches, or leaks API keys, the commit is intercepted automatically (`hallwright audit --staged`).
- **Living Project Memory (`.artisan/memory.json`):** A persistent ledger that records caught bugs as "scar tissue". When your assistant starts a new task, `hallwright context` dynamically injects only the matching past lessons (~6x context optimization: ~2K tokens vs ~12K monolithic rubric dump).
- **Auto-Fix (`hallwright fix`):** Refactors empty catches into structured logger statements and replaces empty stubs.
- **Multi-Agent Coordination (`hallwright swarm`):** Generates structured execution plans and sets session locks so concurrent agent sessions don't collide.
- **MCP 2.0 JSON-RPC Server:** Direct integration into Claude Desktop, Claude Code, Cursor, Windsurf, and Antigravity.

### 3-Command Quickstart:
```bash
# Initialize pre-commit gate & agent configs in your repository
npx github:kapitan00000978-sketch/hallwright init

# Audit staged changes for stubs & secrets
hallwright audit --staged

# Automatically remediate detected defects
hallwright fix
```

The core is zero-dependency, works with 14 agent environments, and is fully open-source (MIT).

We'd love your feedback on our AST detection rules, memory format, and whether this helps your daily AI workflow!
```

---

## ⚡ 2. REDDIT DISTRIBUTION POSTS

Post these to the subreddits below. These communities welcome open-source tools that solve real day-to-day developer annoyances.

### Post A: `r/ClaudeAI` & `r/Cursor`
- **Title:** `I got tired of Claude & Cursor writing "TODO: implement later" stubs and swallowing errors with except: pass, so I built a deterministic pre-commit guardrail`
- **Body (Copy & Paste):**
```markdown
Like many of you, I use Claude Code and Cursor daily. They're incredible for velocity, but they have two habits that constantly bit me in production:

1. **Unfinished stubs:** Writing the boilerplate, and leaving `# TODO: implement error recovery` or `pass` in the most critical branch.
2. **Silent error suppression:** When wrapping logic in try/except, writing `except Exception: pass` so the script doesn't crash during generation.

Telling the prompt "do not leave TODOs" only works half the time. 

So I built **Hallwright** — a lightweight, deterministic pre-commit gatekeeper and project memory layer:
👉 https://github.com/kapitan00000978-sketch/hallwright

### How it works:
- It hooks into your git pre-commit workflow.
- In < 2 seconds, it parses the AST of staged files (Python, JS/TS, Go, Rust).
- If it detects bare exception catches, unfinished stubs, or accidental API key leaks, it blocks the commit.
- Running `hallwright fix` automatically converts bare catches into structured logging and alerts you to complete stubs.
- It also maintains a local `.artisan/memory.json` file so that when an AI makes a mistake once, it records the lesson and warns future agent sessions.

You can try it in any repo with:
```bash
npx github:kapitan00000978-sketch/hallwright init
```

Fully open-source under MIT. Would love to hear what other patterns you'd like it to catch!
```

---

### Post B: `r/LocalLLaMA` & `r/Python`
- **Title:** `Hallwright: Deterministic AST pre-commit gate & living memory protocol for coding assistants (Zero Dependencies)`
- **Body (Copy & Paste):**
```markdown
Hi everyone,

When using local models (like Qwen 2.5 Coder, DeepSeek Coder, or Llama 3) for coding, a common issue is defect leakage — smaller models frequently generate lazy placeholders (`# implement later`), swallow exceptions with bare `except: pass`, or hallucinate incomplete blocks.

I open-sourced **Hallwright**, a deterministic craftsmanship protocol and quality gate designed to run entirely locally:
👉 https://github.com/kapitan00000978-sketch/hallwright

### Architecture Highlights:
- **Zero Heavy Dependencies:** Written with standard library AST analysis and Python/Node CLI wrappers.
- **AST Semantic Analysis:** Detects unfinished AST nodes, bare Exception swallowers, dangerous eval/exec calls, and credential patterns before `git commit`.
- **Scar-Tissue Memory (`.artisan/memory.json`):** Living ledger that stores failure patterns and injects targeted warning prompts (~2K tokens) instead of blowing out context windows with 12K+ tokens of generic system prompts.
- **Model Context Protocol (MCP 2.0):** Exposes inspection tools (`hallwright_inspect_code`, `hallwright_get_lessons`) over stdio for any MCP-compliant agent.

Works offline, requires no API keys, and installs into any git repo via `npx github:kapitan00000978-sketch/hallwright init` or `python artisan_cli.py init`.

Feedback and PRs on the AST rule definitions are very welcome!
```

---

## 🐦 3. TWITTER / X VIRAL THREAD (5 TWEETS)

### Tweet 1 (Hook):
> AI coding assistants are incredible at writing code fast.
> 
> But they have 3 annoying habits:
> 1. Writing `// TODO: implement later`
> 2. Hiding errors with `except: pass`
> 3. Forgetting yesterday's bug fixes
> 
> So we built Hallwright: a deterministic pre-commit guardrail & project memory protocol for AI agents. 🧵👇

### Tweet 2:
> Why prompt engineering fails:
> 
> LLMs are probabilistic token predictors. Telling a prompt *"please don't leave stubs"* is a suggestion, not a guarantee.
> 
> Hallwright enforces a deterministic AST gate at `git commit`. If code has stubs or silent swallowers, it gets blocked before touching your branch.

### Tweet 3:
> It also features **Living Project Memory** (`.artisan/memory.json`).
> 
> When your AI agent makes a mistake, Hallwright records it as "scar tissue".
> 
> On future tasks, `hallwright context` injects only the relevant past lessons (~6x context optimization: ~2K tokens instead of 12K+ dumps).

### Tweet 4:
> Works with your existing stack:
> • Claude Code CLI & Cursor AI
> • GitHub Copilot & Windsurf
> • Python, Node, TypeScript, Go, Rust
> • Full MCP 2.0 JSON-RPC server support
> 
> Run it in any repo:
> `npx github:kapitan00000978-sketch/hallwright init`

### Tweet 5:
> Hallwright is 100% open-source under MIT.
> 
> ⭐ Star the repo on GitHub:
> https://github.com/kapitan00000978-sketch/hallwright
> 
> RT if you want AI to stop swallowing errors in production! 🔁

---

## 📈 4. SUMMARY OF RECOMMENDED SCHEDULE

| Channel | Platform | Action | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Day 1** | **Reddit** (`r/ClaudeAI`, `r/Cursor`) | Post Post A above | 5 minutes |
| **Day 2** | **Hacker News** | Submit Show HN above at 8:30 AM EST | 5 minutes |
| **Day 3** | **Twitter / X** | Post the 5-tweet thread | 5 minutes |
| **Day 4** | **Reddit** (`r/LocalLLaMA`, `r/Python`) | Post Post B above | 5 minutes |
