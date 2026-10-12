---
name: using-craftsman
description: The primary meta-skill invoked at the start of any task or session. Ensures the agent never rushes into writing code without first selecting the right workflow, domain persona, and execution plan.
---

# 🛡️ Using Craftsman & Humanpowers Meta-Skill

The cardinal rule of the Humanpowers framework: **The agent never rushes blindly into writing raw code.**

## Ironclad Directives:

1. **Always Check and Select Appropriate Skills First:**
   When receiving any user prompt or task, pause and activate the dedicated workflow skill:
   - Creating a new feature or project ➔ `brainstorming` and `writing-plans`.
   - Fixing a bug, regression, or failure ➔ `systematic-debugging`.
   - Implementation phase ➔ `test-driven-development`.
   - Verification and sign-off ➔ `adversarial-code-review` and `craftsman-evaluator`.
   - Complex multi-step task ➔ `subagent-driven-development`.

2. **User Directives Take Absolute Precedence:**
   Workspace instructions (`AGENTS.md`, `.cursorrules`, etc.) permanently override default model tendencies.

3. **Anti-Impatience (Zero Guesswork):**
   When asked to "fix X" or "build Y", never jump into speculative code changes. Always diagnose the root cause and align on architectural design first.
