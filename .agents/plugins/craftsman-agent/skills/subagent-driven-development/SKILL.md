---
name: subagent-driven-development
description: Deconstructs complex architectures into independent tasks delegated to autonomous subagent workers, reviewing and merging each output.
---

# 🤖 Subagent-Driven Development

When tackling large codebases or complex multi-file features, divide and conquer by delegating bounded sub-tasks to isolated subagents while maintaining strict quality gates.

## Execution Rules:

1. **Context Isolation:**
   - Provide each subagent with only the necessary files, interfaces, and specific acceptance criteria.
   - Prevent context pollution and token exhaustion.

2. **Adversarial Output Verification:**
   - Do not trust subagent output blindly.
   - Inspect diffs against interface specifications and run automated checks.

3. **Atomic Merging:**
   - Integrate each subagent's validated contribution incrementally into the main branch.
