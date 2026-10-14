"""
Naomi 'The Neural' Chen - AI Agentic Systems & LLM Architecture Reference Standards.

This module codifies empirical agentic evaluation thresholds, context token budget partitions,
prompt injection defense boundaries, structured tool execution schemas, and agent anti-patterns.
"""

from typing import Dict, Any, List


AGENTIC_SYSTEM_BENCHMARKS: Dict[str, Any] = {
    "max_iteration_budget": 5,
    "max_context_utilization_ratio": 0.75,
    "min_eval_faithfulness_score": 0.90,
    "min_tool_selection_accuracy": 0.95,
    "max_p95_agent_turn_latency_ms": 3500.0,
    "max_untrusted_input_length_chars": 16000,
    "max_consecutive_tool_failures": 2,
}

CONTEXT_BUDGET_PARTITIONS: Dict[str, float] = {
    "system_prompt_pct": 15.0,
    "tool_declarations_pct": 15.0,
    "retrieval_grounding_pct": 40.0,
    "scratchpad_working_pct": 30.0,
}

TOXIC_AGENTIC_ANTI_PATTERNS: List[Dict[str, str]] = [
    {
        "id": "unbounded_while_true_agent_loop",
        "indicator": "Implementing autonomous execution using 'while True:' without an immutable max_iterations ceiling.",
        "risk": "Agent enters runaway recursive hallucination loop, draining thousands of dollars in API tokens.",
        "severity": "FATAL"
    },
    {
        "id": "raw_string_prompt_interpolation",
        "indicator": "Interpolating user inputs directly into system prompts without protective structural XML/tag delimiters.",
        "risk": "Leaves system vulnerable to direct and indirect prompt injection attacks (Jailbreaks, System Overrides).",
        "severity": "FATAL"
    },
    {
        "id": "unstructured_json_regex_parsing",
        "indicator": "Requesting JSON in free-form text and parsing model outputs with regex or raw json.loads without schema validation.",
        "risk": "Produces intermittent runtime syntax crashes when models introduce markdown fences or conversational preambles.",
        "severity": "FATAL"
    },
    {
        "id": "blind_tool_execution",
        "indicator": "Executing bash, python, or database operations directly from raw LLM text without capability whitelisting or sandboxing.",
        "risk": "Rogue agents can execute destructive rm -rf, drop table, or network exfiltration commands.",
        "severity": "FATAL"
    },
    {
        "id": "context_window_flooding",
        "indicator": "Dumping full unpruned chat logs, huge DOM trees, or raw PDFs directly into LLM prompts.",
        "risk": "Induces quadratic attention latency degradation ('lost in the middle' phenomenon) and massive token costs.",
        "severity": "HIGH"
    }
]

CANONICAL_AGENTIC_LOOP_CORE: str = (
    "# Naomi Chen: Canonical Deterministic AI Agentic State Machine\n"
    "from typing import Dict, Any, List, Optional\n"
    "import json\n"
    "\n"
    "class StructuredAgentDecision:\n"
    "    def __init__(self, action: str, tool_name: Optional[str], tool_arguments: Dict[str, Any], confidence: float):\n"
    "        self.action = action  # 'call_tool' or 'finish'\n"
    "        self.tool_name = tool_name\n"
    "        self.tool_arguments = tool_arguments\n"
    "        self.confidence = confidence\n"
    "\n"
    "class DeterministicAgentStateMachine:\n"
    "    def __init__(self, max_iterations: int = 5, context_token_ceiling: int = 8000):\n"
    "        self.max_iterations = max_iterations\n"
    "        self.context_token_ceiling = context_token_ceiling\n"
    "        self.trajectory: List[Dict[str, Any]] = []\n"
    "\n"
    "    def sanitize_untrusted_input(self, user_prompt: str) -> str:\n"
    "        # Enforce structural XML boundary to prevent prompt injection\n"
    "        cleaned = user_prompt.replace('<untrusted_input>', '').replace('</untrusted_input>', '')\n"
    "        return f'<untrusted_input>\\n{cleaned}\\n</untrusted_input>'\n"
    "\n"
    "    def execute_step(self, user_prompt: str) -> Dict[str, Any]:\n"
    "        sanitized_prompt = self.sanitize_untrusted_input(user_prompt)\n"
    "        for iteration in range(1, self.max_iterations + 1):\n"
    "            decision = self.call_llm_with_schema(sanitized_prompt)\n"
    "            self.trajectory.append({'iteration': iteration, 'decision': decision})\n"
    "            if decision.action == 'finish':\n"
    "                return {'status': 'completed', 'iterations': iteration, 'result': decision.tool_arguments}\n"
    "        return {'status': 'circuit_breaker_tripped', 'iterations': self.max_iterations}\n"
    "\n"
    "    def call_llm_with_schema(self, prompt: str) -> StructuredAgentDecision:\n"
    "        # Simulated structured output enforcement\n"
    "        return StructuredAgentDecision('finish', None, {'response': 'Verified output'}, 0.98)\n"
)


class AgenticReferenceLibrary:
    """Provides empirical benchmarks, context budgets, and anti-pattern standards for AI agents."""

    @staticmethod
    def get_system_benchmarks() -> Dict[str, Any]:
        return AGENTIC_SYSTEM_BENCHMARKS

    @staticmethod
    def get_context_budgets() -> Dict[str, float]:
        return CONTEXT_BUDGET_PARTITIONS

    @staticmethod
    def get_toxic_anti_patterns() -> List[Dict[str, str]]:
        return TOXIC_AGENTIC_ANTI_PATTERNS

    @staticmethod
    def get_canonical_agent_core() -> str:
        return CANONICAL_AGENTIC_LOOP_CORE
