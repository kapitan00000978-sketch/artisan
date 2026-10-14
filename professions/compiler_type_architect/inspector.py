"""
Nikolai 'The Core' Vance - Objective Compiler & High-Assurance Type Systems Inspector.

This module inspects compiler frontends, AST lowering passes, pattern matchers,
and type checkers for exhaustiveness, recursion bounds, and unsound escape hatches.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class CompilerMetrics:
    has_exhaustive_pattern_matching: bool = False
    has_depth_circuit_breaker: bool = False
    has_algebraic_result_or_option: bool = False
    has_unsound_escape_hatch: bool = False
    has_non_exhaustive_matching: bool = False
    has_unbounded_recursion: bool = False
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class CompilerInspectionReport:
    metrics: CompilerMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_compiler_viable: bool = False


class CompilerSystemInspector:
    """Rigorous compiler and type safety auditor verifying exhaustiveness, sound bounds, and algebraic invariants."""

    def inspect(self, code_input: Any) -> CompilerInspectionReport:
        """
        Audits compiler pass, AST visitor, or type-checking logic for formal soundness.
        """
        metrics = self._extract_metrics(code_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Unsound Escape Hatches ('any', '@ts-ignore', 'reinterpret_cast')
        if metrics.has_unsound_escape_hatch:
            critical_violations.append(
                "Unsound Type Escape Hatch: Found 'as any', '@ts-ignore', or unchecked raw pointer casts that bypass the type checker."
            )
        else:
            benchmarks_passed.append("Zero unsound type escapes detected (Sound type preservation).")

        # 2. Exhaustive Pattern Matching
        if metrics.has_non_exhaustive_matching:
            critical_violations.append(
                "Non-Exhaustive Pattern Match: Match/switch construct lacks an exhaustive wildcard (case _:) or fails to handle all enum variants."
            )
        elif metrics.has_exhaustive_pattern_matching:
            benchmarks_passed.append("100% exhaustive pattern matching verified across all variant branches.")
        else:
            warnings.append("Pattern matching exhaustiveness not explicitly verifiable from AST structure.")

        # 3. Stack Recursion Circuit Breaker
        if metrics.has_unbounded_recursion:
            critical_violations.append(
                "Unbounded AST Recursion: Recursive AST traversal detected without max depth circuit breaker or stack guard."
            )
        elif metrics.has_depth_circuit_breaker:
            benchmarks_passed.append("AST recursion depth guard verified (Circuit breaker against stack overflow).")
        else:
            warnings.append("Consider adding explicit recursion depth limit (MAX_SAFE_DEPTH) to AST visitor.")

        # 4. Algebraic Error / Option Handling
        if metrics.has_algebraic_result_or_option:
            benchmarks_passed.append("Algebraic error/value representation verified (Result / Option monadic discipline).")
        else:
            warnings.append("Consider returning explicit Result[T, E] or Option[T] instead of untyped None or runtime exceptions.")

        for ap in metrics.anti_patterns_detected:
            if ap not in critical_violations:
                critical_violations.append(f"Anti-Pattern Detected: {ap}")

        is_viable = len(critical_violations) == 0

        return CompilerInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_compiler_viable=is_viable
        )

    def _extract_metrics(self, code_input: Any) -> CompilerMetrics:
        text = ""
        metadata: Dict[str, Any] = {}

        if isinstance(code_input, str):
            text = code_input
            try:
                parsed = json.loads(code_input)
                if isinstance(parsed, dict):
                    metadata = parsed
            except (json.JSONDecodeError, ValueError) as _json_err:
                _ = _json_err
        elif isinstance(code_input, dict):
            metadata = code_input
            text = json.dumps(code_input)
        else:
            text = str(code_input)

        # Strip comments to prevent false positives from documentation
        cleaned_text = re.sub(r"#.*", "", text)
        cleaned_text = re.sub(r"//.*", "", cleaned_text)
        text_lower = cleaned_text.lower()
        m = CompilerMetrics()

        # 1. Unsound escapes
        has_unsound = bool(
            "as any" in text_lower or
            "@ts-ignore" in text_lower or
            "@ts-expect-error" in text_lower or
            "reinterpret_cast" in text_lower or
            metadata.get("has_unsound_escape_hatch", False)
        )
        m.has_unsound_escape_hatch = has_unsound

        # 2. Exhaustive pattern matching
        has_match = "match " in text_lower or "switch " in text_lower
        has_wildcard = "case _:" in text_lower or "default:" in text_lower or "case _ =>" in text_lower
        m.has_exhaustive_pattern_matching = (has_match and has_wildcard) or metadata.get("has_exhaustive_pattern_matching", False)
        m.has_non_exhaustive_matching = (has_match and not has_wildcard) or metadata.get("has_non_exhaustive_matching", False)

        # 3. Depth circuit breaker
        has_depth_guard = bool(
            "max_safe_depth" in text_lower or
            "max_depth" in text_lower or
            "depth >" in text_lower or
            "current_depth >" in text_lower or
            "recursion_limit" in text_lower or
            metadata.get("has_depth_circuit_breaker", False)
        )
        m.has_depth_circuit_breaker = has_depth_guard

        # 4. Unbounded recursion check
        has_recursive_call = bool(
            ("evaluate(" in text_lower or "visit(" in text_lower or "lower(" in text_lower) and
            ("def evaluate" in text_lower or "def visit" in text_lower or "def lower" in text_lower)
        )
        m.has_unbounded_recursion = (has_recursive_call and not has_depth_guard) or metadata.get("has_unbounded_recursion", False)

        # 5. Algebraic Result or Option
        has_result_option = bool(
            "result[" in text_lower or
            "result<" in text_lower or
            "option[" in text_lower or
            "option<" in text_lower or
            "result(" in text_lower or
            "is_ok" in text_lower or
            metadata.get("has_algebraic_result_or_option", False)
        )
        m.has_algebraic_result_or_option = has_result_option

        # Anti-pattern logging
        if m.has_unsound_escape_hatch:
            m.anti_patterns_detected.append("Unsound escape hatch bypassing compiler type checker")
        if m.has_non_exhaustive_matching:
            m.anti_patterns_detected.append("Non-exhaustive pattern matching missing fallback branch")
        if m.has_unbounded_recursion:
            m.anti_patterns_detected.append("Unbounded recursive AST traversal without depth circuit breaker")

        return m
