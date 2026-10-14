"""
Nikolai 'The Core' Vance - 100-Point Compiler & High-Assurance Type Systems Rubric.

Evaluates compiler frontends, AST lowering pipelines, pattern matching exhaustiveness,
and formal type safety invariants.
Passing threshold: 85/100 points.
Veto criteria: Unsound escape hatches, non-exhaustive variant branches, or unbounded AST recursion.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.compiler_type_architect.inspector import CompilerInspectionReport, CompilerMetrics


@dataclass
class CompilerRubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class CompilerTypeRubric:
    """Rigorous 100-point weighted evaluation rubric for compiler architecture and type soundness."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: CompilerInspectionReport) -> CompilerRubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Type Soundness & Zero Escape Hatches (30 pts)
        # ----------------------------------------------------
        p1_score = 0
        if m.has_unsound_escape_hatch:
            veto_reasons.append(
                "Unsound Type Escape Hatch: Bypassing type checking via 'as any', '@ts-ignore', or unchecked casts introduces undefined behavior."
            )
            recommendations.append(
                "Eliminate all 'as any', '@ts-ignore', and raw casts. Model domain types strictly using algebraic unions and generics."
            )
        else:
            p1_score = 30
        pillar_scores["type_soundness_preservation"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Exhaustive Pattern Matching (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if m.has_non_exhaustive_matching:
            veto_reasons.append(
                "Non-Exhaustive Pattern Matching: Match or switch construct lacks an exhaustive fallback (case _:) or misses enum variants."
            )
            recommendations.append(
                "Add an exhaustive wildcard case (case _:) or handle 100% of defined enum variants explicitly."
            )
        elif m.has_exhaustive_pattern_matching:
            p2_score = 25
        else:
            p2_score = 15
            recommendations.append("Explicitly annotate pattern matching structures with exhaustive variant coverage.")
        pillar_scores["exhaustive_pattern_matching"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: Recursion Depth & Stack Defense (25 pts)
        # ----------------------------------------------------
        p3_score = 0
        if m.has_unbounded_recursion:
            veto_reasons.append(
                "Unbounded AST Recursion: Recursive tree evaluation detected without an explicit depth guard or stack overflow circuit breaker."
            )
            recommendations.append(
                "Inject MAX_SAFE_DEPTH recursion check (e.g., if current_depth > 512: return Error) to prevent compiler stack overflows."
            )
        elif m.has_depth_circuit_breaker:
            p3_score = 25
        else:
            p3_score = 15
            recommendations.append("Add explicit recursion depth parameter to tree visitors.")
        pillar_scores["recursion_stack_defense"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: Algebraic Error & Monadic Modeling (20 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.has_algebraic_result_or_option:
            p4_score = 20
        else:
            p4_score = 10
            recommendations.append(
                "Adopt Result[T, E] or Option[T] algebraic types for errors instead of silent None or runtime exception throwing."
            )
        pillar_scores["algebraic_monadic_modeling"] = p4_score

        total_score = sum(pillar_scores.values())
        veto_triggered = len(veto_reasons) > 0

        if veto_triggered:
            total_score = min(total_score, 50)
            is_certified = False
        else:
            is_certified = total_score >= self.PASSING_THRESHOLD

        return CompilerRubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
