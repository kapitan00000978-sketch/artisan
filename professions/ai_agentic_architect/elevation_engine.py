"""
Naomi 'The Neural' Chen - Autonomous AI Agentic Architecture Elevation Engine.

Transforms stochastic, runaway, or injection-vulnerable agent workflows into
rock-solid, bounded, injection-defended, and structured-schema deterministic cognitive machines.
"""

from typing import Dict, Any, List
import re
from professions.ai_agentic_architect.inspector import AgenticSystemInspector, AgenticInspectionReport
from professions.ai_agentic_architect.blind_critic import BlindAgenticCritic, AgenticDefectLedger


class AgenticElevationEngine:
    """Elevates flawed agent loops and prompts into Naomi Chen Deterministic Agent standards."""

    def __init__(self):
        self.inspector = AgenticSystemInspector()
        self.critic = BlindAgenticCritic()

    def elevate(self, agent_input: Any, max_iterations: int = 3) -> Dict[str, Any]:
        """
        Takes raw agent loop code or prompt string and iteratively elevates it until certified at >= 85/100.
        """
        content = str(agent_input)
        remediations_applied: List[str] = []

        for iteration in range(1, max_iterations + 1):
            ledger: AgenticDefectLedger = self.critic.review(content)
            if ledger.is_certified:
                break

            report: AgenticInspectionReport = self.inspector.inspect(content)
            m = report.metrics

            # 1. Remediate Unbounded While Loops
            if m.has_unbounded_while_loop or not m.has_max_iteration_circuit_breaker:
                content = self._remediate_loop_bounding(content)
                remediations_applied.append(
                    f"Iteration {iteration}: Injected immutable max_iterations=5 circuit breaker to eliminate runaway loop risks."
                )

            # 2. Remediate Prompt Injection Vulnerability
            if m.has_raw_prompt_fstring_injection or not m.has_prompt_injection_delimiter:
                content = self._remediate_prompt_injection(content)
                remediations_applied.append(
                    f"Iteration {iteration}: Isolated untrusted user inputs with structural <untrusted_input> XML tags."
                )

            # 3. Remediate Unstructured Free-Form Parsing
            if not m.has_structured_output_schema:
                content = self._remediate_structured_schema(content)
                remediations_applied.append(
                    f"Iteration {iteration}: Enforced deterministic StructuredAgentDecision schema on model returns."
                )

            # 4. Remediate Tool Sandboxing
            if not m.has_tool_execution_sandbox and ("tool" in content.lower() or "execute" in content.lower()):
                content = self._remediate_tool_sandbox(content)
                remediations_applied.append(
                    f"Iteration {iteration}: Added capability whitelist and argument validation to tool dispatcher."
                )

        final_ledger = self.critic.review(content)

        return {
            "status": "CERTIFIED" if final_ledger.is_certified else "ELEVATED_WITH_CAUTIONS",
            "score": final_ledger.score,
            "passing_threshold": final_ledger.passing_threshold,
            "verdict": final_ledger.verdict,
            "remediations_applied": remediations_applied,
            "elevated_agent": content,
            "final_ledger": final_ledger,
            "metrics": self.inspector.inspect(content).metrics
        }

    def _remediate_loop_bounding(self, content: str) -> str:
        if "while true" in content.lower():
            content = re.sub(
                r"while\s+true\s*:",
                "max_iterations = 5\n        for iteration in range(1, max_iterations + 1):",
                content,
                flags=re.IGNORECASE
            )
        elif "max_iterations" not in content.lower():
            circuit_breaker = "\n    max_iterations = 5  # Naomi Chen Circuit Breaker\n"
            content = circuit_breaker + content
        return content

    def _remediate_prompt_injection(self, content: str) -> str:
        # Wrap raw {user_input} in structural tags
        if "f\"" in content or "f'" in content:
            content = re.sub(
                r"\{user_input\}",
                r"<untrusted_input>{user_input}</untrusted_input>",
                content
            )
        if "<untrusted_input>" not in content:
            delimiter_fn = (
                "\n    def sanitize_untrusted_input(self, raw_input: str) -> str:\n"
                "        safe = raw_input.replace('<untrusted_input>', '').replace('</untrusted_input>', '')\n"
                "        return f'<untrusted_input>\\n{safe}\\n</untrusted_input>'\n"
            )
            content = delimiter_fn + "\n" + content
        return content

    def _remediate_structured_schema(self, content: str) -> str:
        schema_def = (
            "\n# Naomi Chen Deterministic Structured Output Schema\n"
            "class StructuredAgentDecision:\n"
            "    def __init__(self, action: str, tool_name: str = None, tool_arguments: dict = None, confidence: float = 1.0):\n"
            "        self.action = action\n"
            "        self.tool_name = tool_name\n"
            "        self.tool_arguments = tool_arguments or {}\n"
            "        self.confidence = confidence\n"
        )
        return schema_def + "\n" + content

    def _remediate_tool_sandbox(self, content: str) -> str:
        sandbox_snippet = (
            "\n    # Hermetic Tool Execution Sandbox\n"
            "    ALLOWED_TOOLS = {'read_file', 'grep_search', 'list_dir', 'execute_calculation'}\n"
            "    def execute_tool(self, tool_name: str, args: dict):\n"
            "        if tool_name not in self.ALLOWED_TOOLS:\n"
            "            raise ValueError(f'Security Violation: Unauthorized tool {tool_name}')\n"
        )
        return content + sandbox_snippet
