"""
Naomi 'The Neural' Chen - 100-Point AI Agentic Systems & LLM Architecture Rubric.

Evaluates autonomous agent state machines, structured JSON outputs, prompt injection defenses,
and tool sandboxing safety.
Passing threshold: 85/100 points.
Veto criteria: Unbounded while loop, raw prompt f-string injection, or unstructured free-form parsing.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.ai_agentic_architect.inspector import AgenticInspectionReport, AgenticMetrics


@dataclass
class AgenticRubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class AgenticArchitectureRubric:
    """Rigorous 100-point weighted evaluation rubric for autonomous AI agents and LLM orchestration."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: AgenticInspectionReport) -> AgenticRubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Loop Bounding & Circuit Breakers (25 pts)
        # ----------------------------------------------------
        p1_score = 0
        if m.has_unbounded_while_loop:
            veto_reasons.append(
                "Unbounded While Loop: Running autonomous loops with 'while True:' without an immutable max_iterations ceiling."
            )
            recommendations.append(
                "Enforce a strict circuit breaker: 'for iteration in range(1, max_iterations + 1):' with early finish return."
            )
        elif m.has_max_iteration_circuit_breaker:
            p1_score += 25
        else:
            p1_score += 10
            recommendations.append("Explicitly declare a 'max_iterations' budget ceiling in the agent runner.")

        pillar_scores["loop_circuit_breaker"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Prompt Injection Defense (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if m.has_raw_prompt_fstring_injection:
            veto_reasons.append(
                "Prompt Injection Hazard: Untrusted user input is directly concatenated/interpolated into system instructions."
            )
            recommendations.append(
                "Wrap untrusted inputs inside clear structural tags (<untrusted_input>...</untrusted_input>) and sanitize delimiters."
            )
        elif m.has_prompt_injection_delimiter:
            p2_score += 25
        else:
            p2_score += 8
            recommendations.append("Isolate external retrieved text and user inputs using structural XML/tag wrappers.")

        pillar_scores["prompt_injection_defense"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: Structured Output & Schema Enforcement (25 pts)
        # ----------------------------------------------------
        p3_score = 0
        if not m.has_structured_output_schema:
            veto_reasons.append(
                "Unstructured Model Output: Extracting model decisions via regex or raw strings instead of Pydantic/JSON schemas."
            )
            recommendations.append(
                "Enforce a strict Pydantic BaseModel or JSON schema (Structured Outputs / function calling) for deterministic parsing."
            )
        else:
            p3_score += 25

        pillar_scores["structured_schema_enforcement"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: Tool Execution Sandboxing (15 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.has_tool_execution_sandbox:
            p4_score += 15
        else:
            p4_score += 5
            recommendations.append(
                "Validate tool names against a strict capability whitelist and sanitize arguments before execution."
            )

        pillar_scores["tool_sandboxing"] = p4_score

        # ----------------------------------------------------
        # Pillar 5: Trajectory & State Observability (10 pts)
        # ----------------------------------------------------
        p5_score = 10
        pillar_scores["state_observability"] = p5_score

        total_score = sum(pillar_scores.values())

        # Veto enforcement
        veto_triggered = len(veto_reasons) > 0
        if veto_triggered and total_score >= self.PASSING_THRESHOLD:
            total_score = 65

        is_certified = (total_score >= self.PASSING_THRESHOLD) and not veto_triggered

        return AgenticRubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
