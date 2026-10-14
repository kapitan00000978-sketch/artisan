"""
Naomi 'The Neural' Chen - Blind AI Agentic Systems Critic.

Evaluates autonomous agent code, prompt pipelines, and tool execution state machines
strictly against injection isolation, deterministic schema outputs, and loop ceilings.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.ai_agentic_architect.inspector import AgenticSystemInspector, AgenticInspectionReport
from professions.ai_agentic_architect.rubric import AgenticArchitectureRubric, AgenticRubricEvaluation


@dataclass
class AgenticDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    agentic_impact: str
    actionable_fix: str


@dataclass
class AgenticDefectLedger:
    verdict: str  # CERTIFIED_DETERMINISTIC_AGENT or REJECTED_STOCHASTIC_CHAOS
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[AgenticDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindAgenticCritic:
    """Agentic adversary reviewing LLM loops and tool dispatchers for runaway crashes, injections, and stubs."""

    def __init__(self):
        self.inspector = AgenticSystemInspector()
        self.rubric = AgenticArchitectureRubric()

    def review(self, agent_input: Any) -> AgenticDefectLedger:
        """
        Runs objective inspection and adversarial rubric scoring, producing an Agentic Defect Ledger.
        """
        report: AgenticInspectionReport = self.inspector.inspect(agent_input)
        eval_result: AgenticRubricEvaluation = self.rubric.evaluate(report)

        defects: List[AgenticDefect] = []

        # 1. Critical violations -> FATAL defects
        for i, violation in enumerate(report.critical_violations, start=1):
            if "while" in violation.lower() or "runaway" in violation.lower() or "loop" in violation.lower():
                title = "Unbounded Runaway While Loop"
                impact = "Agent risks entering an infinite recursive loop, draining API budgets and hanging processes."
                fix = "Replace unbounded while loop with bounded for loop: 'for iteration in range(1, max_iterations + 1):'."
            elif "injection" in violation.lower() or "fstring" in violation.lower():
                title = "Raw Prompt Injection Vulnerability"
                impact = "Malicious or untrusted inputs can override system directives and commandeer agent execution."
                fix = "Isolate user inputs inside '<untrusted_input>...</untrusted_input>' structural tags."
            elif "unstructured" in violation.lower() or "schema" in violation.lower():
                title = "Unstructured Free-Form Parsing Risk"
                impact = "Output deviates from expected format, triggering syntax parse crashes in production."
                fix = "Enforce a formal Pydantic BaseModel or strict JSON schema."
            else:
                title = "Critical Agentic Architecture Violation"
                impact = "Substantially compromises autonomous agent stability or security."
                fix = "Refactor agent state machine to Naomi Chen deterministic standards."

            defects.append(
                AgenticDefect(
                    defect_id=f"AGENT-FATAL-{i:03d}",
                    severity="FATAL",
                    title=title,
                    description=violation,
                    agentic_impact=impact,
                    actionable_fix=fix
                )
            )

        # 2. Veto reasons
        for j, reason in enumerate(eval_result.veto_reasons, start=len(defects) + 1):
            if not any(d.description == reason for d in defects):
                defects.append(
                    AgenticDefect(
                        defect_id=f"AGENT-FATAL-{j:03d}",
                        severity="FATAL",
                        title="Agentic Integrity Veto",
                        description=reason,
                        agentic_impact="Disqualifies agent pipeline from production deployment under Naomi Chen protocol.",
                        actionable_fix="Remediate the underlying agentic flaw immediately."
                    )
                )

        # 3. Warnings -> HIGH / MEDIUM defects
        for k, warning in enumerate(report.warnings, start=len(defects) + 1):
            severity = "HIGH" if "tool" in warning.lower() else "MEDIUM"
            title = "Unsandboxed Tool Execution" if "tool" in warning.lower() else "Suboptimal Prompt Delimitation"
            impact = "Agent can invoke unauthorized functions." if "tool" in warning.lower() else "Minor risk of model instruction bleed."
            fix = "Validate tool names against a strict capability whitelist." if "tool" in warning.lower() else "Enforce XML delimiters."

            defects.append(
                AgenticDefect(
                    defect_id=f"AGENT-WARN-{k:03d}",
                    severity=severity,
                    title=title,
                    description=warning,
                    agentic_impact=impact,
                    actionable_fix=fix
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = (
            "CERTIFIED_DETERMINISTIC_AGENT"
            if eval_result.is_certified and fatal_count == 0
            else "REJECTED_STOCHASTIC_CHAOS"
        )

        summary = (
            f"Naomi Chen Agentic Review: Score {eval_result.total_score}/100. "
            f"Verdict: {verdict}. Fatal defects: {fatal_count}, High defects: {high_count}."
        )

        return AgenticDefectLedger(
            verdict=verdict,
            score=eval_result.total_score,
            passing_threshold=eval_result.passing_threshold,
            is_certified=eval_result.is_certified and fatal_count == 0,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
