"""
Nikolai 'The Core' Vance - Blind Compiler & High-Assurance Type Systems Critic.

Evaluates compiler frontends, AST lowering passes, and type systems strictly against
unsound escape hatches, non-exhaustive match statements, and unbounded recursion.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.compiler_type_architect.inspector import CompilerSystemInspector, CompilerInspectionReport
from professions.compiler_type_architect.rubric import CompilerTypeRubric, CompilerRubricEvaluation


@dataclass
class CompilerDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    compiler_risk: str
    actionable_fix: str


@dataclass
class CompilerDefectLedger:
    verdict: str  # CERTIFIED_TYPE_SOUNDNESS or REJECTED_UNSOUND_TYPE_AMBIGUITY
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[CompilerDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindCompilerCritic:
    """Compiler adversary auditing type passes for soundness leaks, unhandled variants, and stack overflows."""

    def __init__(self):
        self.inspector = CompilerSystemInspector()
        self.rubric = CompilerTypeRubric()

    def review(self, code_input: Any) -> CompilerDefectLedger:
        """
        Runs objective inspection and adversarial rubric scoring, producing a Compiler Defect Ledger.
        """
        report: CompilerInspectionReport = self.inspector.inspect(code_input)
        evaluation: CompilerRubricEvaluation = self.rubric.evaluate(report)

        defects: List[CompilerDefect] = []

        # Map critical violations to FATAL / HIGH defects
        for i, violation in enumerate(report.critical_violations, 1):
            if "Unsound" in violation:
                defects.append(
                    CompilerDefect(
                        defect_id=f"COMP-FATAL-00{i}",
                        severity="FATAL",
                        title="Unsound Type Escape Hatch Detected",
                        description=violation,
                        compiler_risk="Disables compiler type guarantees, causing runtime memory corruption or segmentation faults.",
                        actionable_fix="Remove unsound escape hatch ('as any', '@ts-ignore', unchecked casts). Enforce strict generic algebraic types."
                    )
                )
            elif "Non-Exhaustive" in violation:
                defects.append(
                    CompilerDefect(
                        defect_id=f"COMP-FATAL-00{i}",
                        severity="FATAL",
                        title="Non-Exhaustive Pattern Matching",
                        description=violation,
                        compiler_risk="Missing enum variants produce silent unhandled execution branches or undefined compiler behavior.",
                        actionable_fix="Add wildcard branch (case _:) or explicitly handle 100% of defined enum variants."
                    )
                )
            elif "Unbounded" in violation:
                defects.append(
                    CompilerDefect(
                        defect_id=f"COMP-FATAL-00{i}",
                        severity="FATAL",
                        title="Unbounded AST Recursion",
                        description=violation,
                        compiler_risk="Deeply nested or circular ASTs cause host stack overflow and catastrophic compiler crash.",
                        actionable_fix="Enforce MAX_SAFE_DEPTH (e.g. 512) circuit breaker check on recursive visitor calls."
                    )
                )
            else:
                defects.append(
                    CompilerDefect(
                        defect_id=f"COMP-HIGH-00{i}",
                        severity="HIGH",
                        title="Compiler Protocol Violation",
                        description=violation,
                        compiler_risk="Severe risk to compiler stability or type soundness.",
                        actionable_fix="Remediate against Nikolai Vance type soundness standards."
                    )
                )

        # Map warnings
        for j, warning in enumerate(report.warnings, 1):
            defects.append(
                CompilerDefect(
                    defect_id=f"COMP-WARN-00{j}",
                    severity="MEDIUM",
                    title="Type Hygiene Warning",
                    description=warning,
                    compiler_risk="Sub-optimal compiler ergonomics and potential runtime type ambiguities.",
                    actionable_fix="Adopt Nikolai Vance canonical Result/Option pattern and depth circuit breakers."
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = (
            "CERTIFIED_TYPE_SOUNDNESS"
            if evaluation.is_certified and fatal_count == 0
            else "REJECTED_UNSOUND_TYPE_AMBIGUITY"
        )

        summary = (
            f"Nikolai Vance Compiler Review: Score {evaluation.total_score}/100. "
            f"Verdict: {verdict}. Fatal defects: {fatal_count}, High defects: {high_count}."
        )

        return CompilerDefectLedger(
            verdict=verdict,
            score=evaluation.total_score,
            passing_threshold=evaluation.passing_threshold,
            is_certified=evaluation.is_certified and fatal_count == 0,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
