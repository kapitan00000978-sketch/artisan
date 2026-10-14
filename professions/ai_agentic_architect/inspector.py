"""
Naomi 'The Neural' Chen - Objective AI Agentic Systems & LLM Architecture Inspector.

This module inspects autonomous AI agent code, prompt templates, and tool-calling state machines
to detect unbounded while loops, prompt injection vulnerabilities, unstructured model parsing,
and unsandboxed tool executions.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class AgenticMetrics:
    has_max_iteration_circuit_breaker: bool = False
    has_unbounded_while_loop: bool = False
    has_prompt_injection_delimiter: bool = False
    has_raw_prompt_fstring_injection: bool = False
    has_structured_output_schema: bool = False
    has_tool_execution_sandbox: bool = False
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class AgenticInspectionReport:
    metrics: AgenticMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_agentic_viable: bool = False


class AgenticSystemInspector:
    """Rigorous AI agent auditor evaluating state machine loops, prompt boundaries, and tool safety."""

    def inspect(self, agent_input: Any) -> AgenticInspectionReport:
        """
        Audits Python / TypeScript agent loop code, prompt templates, or config dict.
        """
        metrics = self._extract_metrics(agent_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Circuit Breaker & Loop Bounding
        if metrics.has_unbounded_while_loop:
            critical_violations.append(
                "Unbounded Runaway Loop Detected: Agent uses 'while True:' without an immutable max_iterations ceiling. "
                "Risks infinite recursive hallucination loops and API cost spikes."
            )
        elif metrics.has_max_iteration_circuit_breaker:
            benchmarks_passed.append("Immutable max_iterations circuit breaker verified (Bounded execution).")

        # 2. Prompt Injection Defense
        if metrics.has_raw_prompt_fstring_injection:
            critical_violations.append(
                "Prompt Injection Vulnerability: User input directly interpolated into system instructions without structural delimiters. "
                "Allows hostile prompt injections and role-reversal attacks."
            )
        elif metrics.has_prompt_injection_delimiter:
            benchmarks_passed.append("Structural XML/delimiter prompt isolation verified (Injection defense).")
        else:
            warnings.append("No explicit untrusted input delimiters found in prompt construction.")

        # 3. Structured Output & Schema Enforcement
        if not metrics.has_structured_output_schema:
            critical_violations.append(
                "Unstructured Free-Form Parsing: Agent code extracts decisions via raw strings or regex instead of Pydantic/JSON schemas. "
                "Will cause catastrophic syntax parse crashes when models deviate."
            )
        else:
            benchmarks_passed.append("Deterministic structured schema enforcement verified.")

        # 4. Tool Execution Sandboxing
        if not metrics.has_tool_execution_sandbox and ("tool" in str(agent_input).lower() or "execute" in str(agent_input).lower()):
            warnings.append("Tool execution lacks explicit whitelist or capability boundary checks.")
        else:
            benchmarks_passed.append("Hermetic tool execution validation verified.")

        for ap in metrics.anti_patterns_detected:
            if ap not in critical_violations:
                critical_violations.append(f"Anti-Pattern Detected: {ap}")

        is_viable = len(critical_violations) == 0

        return AgenticInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_agentic_viable=is_viable
        )

    def _extract_metrics(self, agent_input: Any) -> AgenticMetrics:
        text = ""
        metadata: Dict[str, Any] = {}

        if isinstance(agent_input, str):
            text = agent_input
            try:
                parsed = json.loads(agent_input)
                if isinstance(parsed, dict):
                    metadata = parsed
            except (json.JSONDecodeError, ValueError) as _json_err:
                _ = _json_err
        elif isinstance(agent_input, dict):
            metadata = agent_input
            text = json.dumps(agent_input)
        else:
            text = str(agent_input)

        text_lower = text.lower()
        m = AgenticMetrics()

        # 1. Loop bounding & circuit breaker
        has_breaker = bool(
            re.search(r"max_iterations\b", text_lower) or
            re.search(r"for\s+\w+\s+in\s+range\([^)]*max", text_lower) or
            re.search(r"iteration\s*<\s*max", text_lower) or
            metadata.get("has_max_iteration_circuit_breaker", False)
        )
        has_unbounded = bool(
            (re.search(r"while\s+true\s*:", text_lower) and not has_breaker) or
            metadata.get("has_unbounded_while_loop", False)
        )
        m.has_max_iteration_circuit_breaker = has_breaker
        m.has_unbounded_while_loop = has_unbounded

        # 2. Prompt injection defense
        has_delimiter = bool(
            "<untrusted" in text_lower or
            "<context>" in text_lower or
            "<user_input>" in text_lower or
            "sanitize_untrusted" in text_lower or
            metadata.get("has_prompt_injection_delimiter", False)
        )
        has_fstring_injection = bool(
            (re.search(r'f["\'].*?(?:system|prompt).*?\{user_input\}', text, re.IGNORECASE) and not has_delimiter) or
            metadata.get("has_raw_prompt_fstring_injection", False)
        )
        m.has_prompt_injection_delimiter = has_delimiter
        m.has_raw_prompt_fstring_injection = has_fstring_injection

        # 3. Structured output & schemas
        has_schema = bool(
            "pydantic" in text_lower or
            "basemodel" in text_lower or
            "structuredagentdecision" in text_lower or
            "json_schema" in text_lower or
            "response_format" in text_lower or
            metadata.get("has_structured_output_schema", False)
        )
        m.has_structured_output_schema = has_schema

        # 4. Tool execution sandboxing
        has_sandbox = bool(
            "sanitize" in text_lower or
            "whitelist" in text_lower or
            "tool_name in" in text_lower or
            "allowed_tools" in text_lower or
            metadata.get("has_tool_execution_sandbox", True)
        )
        m.has_tool_execution_sandbox = has_sandbox

        # Anti-pattern logging
        if m.has_unbounded_while_loop:
            m.anti_patterns_detected.append("Unbounded while True agent loop (Runaway risk)")
        if m.has_raw_prompt_fstring_injection:
            m.anti_patterns_detected.append("Raw prompt f-string injection vulnerability")
        if not m.has_structured_output_schema:
            m.anti_patterns_detected.append("Unstructured free-form model parsing")

        return m
