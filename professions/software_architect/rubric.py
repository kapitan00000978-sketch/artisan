"""
Marcus Sterling's Weighted Software Architecture Rubric
Mathematical, structural evaluation of cyclomatic complexity, modularity, exception discipline, and type contracts.
"""

from typing import Dict, Any, List, Optional


class MarcusArchitectureRubric:
    """Marcus Sterling's 100-point weighted software architecture evaluation rubric."""

    DIMENSIONS: Dict[str, Dict[str, Any]] = {
        "cyclomatic_complexity": {
            "title": "Cyclomatic Complexity & Control Flow",
            "weight": 0.25,
            "benchmark": "Max McCabe complexity <= 8 per function; clean linear control flow."
        },
        "function_modularity": {
            "title": "Modularity & Function Size (Single Responsibility)",
            "weight": 0.25,
            "benchmark": "Max function length <= 40 lines; zero God functions (>50 lines)."
        },
        "exception_discipline": {
            "title": "Exception Discipline & Error Propagation",
            "weight": 0.20,
            "benchmark": "Zero silent exception swallows or empty catch blocks."
        },
        "stub_integrity": {
            "title": "Code Completeness & Zero-Stub Integrity",
            "weight": 0.15,
            "benchmark": "Zero lazy TODO, FIXME, or unfinished stub placeholders."
        },
        "type_contract_safety": {
            "title": "Type Safety & Contract Clarity",
            "weight": 0.15,
            "benchmark": ">= 90% of function definitions annotated with explicit parameter & return types."
        }
    }

    def evaluate(self, metrics: Dict[str, Any], benchmark_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculates itemized and composite architecture score out of 100."""
        target_metrics = benchmark_profile.get("metrics", {}) if benchmark_profile else {}
        max_allowed_cc = target_metrics.get("max_cyclomatic_complexity", 8)
        max_allowed_fn_lines = target_metrics.get("max_function_lines", 40)
        min_type_pct = target_metrics.get("min_type_annotation_pct", 90.0)

        scores: Dict[str, Any] = {}

        # 1. Cyclomatic Complexity (0-10)
        max_cc = metrics.get("max_cyclomatic_complexity", 1)
        if max_cc <= max_allowed_cc:
            cc_score = 10.0
        elif max_cc <= max_allowed_cc + 3:
            cc_score = 7.5
        elif max_cc <= max_allowed_cc + 6:
            cc_score = 5.0
        else:
            cc_score = max(1.0, round(10.0 - (max_cc - max_allowed_cc) * 1.2, 1))

        scores["cyclomatic_complexity"] = {
            "score": cc_score,
            "measured": f"Max CC: {max_cc} (Avg: {metrics.get('avg_cyclomatic_complexity', 1.0)})",
            "benchmark": f"Max CC <= {max_allowed_cc}",
            "status": "PASS" if cc_score >= 8.0 else "FAIL"
        }

        # 2. Function Modularity (0-10)
        max_lines = metrics.get("max_function_lines", 0)
        god_fns = metrics.get("god_functions_count", 0)

        if max_lines <= max_allowed_fn_lines and god_fns == 0:
            mod_score = 10.0
        elif max_lines <= max_allowed_fn_lines * 1.4 and god_fns == 0:
            mod_score = 8.0
        elif god_fns == 1:
            mod_score = 5.5
        else:
            mod_score = max(2.0, round(8.0 - (god_fns * 2.5), 1))

        scores["function_modularity"] = {
            "score": mod_score,
            "measured": f"Max function lines: {max_lines} ({god_fns} God functions)",
            "benchmark": f"<= {max_allowed_fn_lines} lines per function",
            "status": "PASS" if mod_score >= 8.0 else "FAIL"
        }

        # 3. Exception Discipline (0-10)
        swallows = metrics.get("silent_exception_swallows", 0)
        if swallows == 0:
            exc_score = 10.0
        elif swallows == 1:
            exc_score = 4.0
        else:
            exc_score = 1.0

        scores["exception_discipline"] = {
            "score": exc_score,
            "measured": f"{swallows} silent exception swallows",
            "benchmark": "Zero silent exception swallows",
            "status": "PASS" if exc_score >= 8.0 else "FAIL"
        }

        # 4. Stub & Placeholder Integrity (0-10)
        todos = metrics.get("todo_placeholder_count", 0)
        if todos == 0:
            stub_score = 10.0
        elif todos == 1:
            stub_score = 5.0
        else:
            stub_score = 2.0

        scores["stub_integrity"] = {
            "score": stub_score,
            "measured": f"{todos} TODO/FIXME placeholders",
            "benchmark": "Zero unfinished placeholders",
            "status": "PASS" if stub_score >= 8.0 else "FAIL"
        }

        # 5. Type Contract Safety (0-10)
        type_pct = metrics.get("type_annotation_pct", 100.0)
        if type_pct >= min_type_pct:
            type_score = 10.0
        elif type_pct >= 60.0:
            type_score = 7.0
        elif type_pct >= 30.0:
            type_score = 4.5
        else:
            type_score = 2.0

        scores["type_contract_safety"] = {
            "score": type_score,
            "measured": f"{type_pct}% typed functions",
            "benchmark": f">= {min_type_pct}% type coverage",
            "status": "PASS" if type_score >= 8.0 else "FAIL"
        }

        # Composite score calculation
        total_score = round(sum(
            scores[dim]["score"] * self.DIMENSIONS[dim]["weight"]
            for dim in self.DIMENSIONS
        ) * 10, 1)

        return {
            "evaluator": "Marcus Sterling (Senior Software Architect)",
            "total_score": total_score,
            "passing_threshold": 85.0,
            "passed": total_score >= 85.0,
            "dimensions": scores
        }
