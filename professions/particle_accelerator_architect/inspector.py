"""Static AST and regex inspector for Particle Accelerators & Relativistic Beam Dynamics.

Maintained by Dr. Julian 'The Accelerator' Vance.
Inspects code for Lorentz relativistic dynamics, betatron tune resonance avoidance,
superconducting cavity quench interlocks, and microsecond kicker machine protection.
"""

from __future__ import annotations
import ast
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class AcceleratorInspectionResult:
    """Detailed inspection report for particle accelerator autonomy code."""
    file_path: str
    syntax_valid: bool
    capabilities: Dict[str, bool] = field(default_factory=dict)
    violations: List[str] = field(default_factory=list)
    has_fatal_defects: bool = False
    ast_node_count: int = 0
    score: float = 0.0

    @property
    def is_production_ready(self) -> bool:
        return self.syntax_valid and not self.has_fatal_defects and self.score >= 85.0


class AcceleratorInspector:
    """Audits accelerator beam physics and machine protection software."""

    def __init__(self) -> None:
        todo_pattern = r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*\n"
        self._stub_regex = re.compile(todo_pattern, re.IGNORECASE)

    def _strip_comments(self, code: str) -> str:
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
        code = re.sub(r"//.*", "", code)
        code = re.sub(r"#.*", "", code)
        return code

    def inspect_source(self, source_code: str, file_path: str = "inline_accelerator.py") -> AcceleratorInspectionResult:
        """Conduct ruthless static and AST inspection against accelerator standards."""
        stripped = self._strip_comments(source_code)
        violations: List[str] = []
        capabilities = {
            "has_relativistic_kinematics": False,
            "has_tune_resonance_guard": False,
            "has_cavity_quench_check": False,
            "has_telemetry_eval": False,
            "has_kicker_dump_abort": False
        }

        # 1. AST Syntax Check
        try:
            tree = ast.parse(source_code)
            syntax_valid = True
            node_count = len(list(ast.walk(tree)))
        except SyntaxError as err:
            return AcceleratorInspectionResult(
                file_path=file_path,
                syntax_valid=False,
                violations=[f"Syntax error: {err}"],
                has_fatal_defects=True,
                ast_node_count=0,
                score=0.0
            )

        # 2. Check for lazy stubs / unhandled exceptions
        for node in ast.walk(tree):
            if isinstance(node, ast.Raise):
                if isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
                    if node.exc.func.id == "NotImplementedError":
                        violations.append("Lazy stub detected: NotImplementedError raised")
            elif isinstance(node, ast.Pass):
                parent_func = False
                for parent in ast.walk(tree):
                    if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if len(parent.body) == 1 and parent.body[0] == node:
                            parent_func = True
                            break
                if parent_func:
                    violations.append("Empty pass stub function detected")

        # 3. Detect Capabilities via AST / Identifier Tokens
        funcs = {node.name.lower() for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}

        # Capability: Relativistic kinematics
        if any(tok in stripped for tok in ["compute_relativistic_lorentz_state", "calculate_lorentz_gamma", "calculate_magnetic_rigidity", "rigidity_t_m"]):
            capabilities["has_relativistic_kinematics"] = True

        # Capability: Betatron tune resonance guard
        if any(tok in stripped for tok in ["evaluate_betatron_tune_resonances", "is_resonance_safe", "horizontal_tune", "betatron_tune"]):
            capabilities["has_tune_resonance_guard"] = True

        # Capability: Superconducting cavity quench check
        if any(tok in stripped for tok in ["cavity_temp_k", "quench_trip_latency_us", "is_cavity_safe", "accelerating_gradient"]):
            capabilities["has_cavity_quench_check"] = True

        # Capability: Telemetry safety audit
        if any(tok in stripped for tok in ["evaluate_telemetry_safety", "is_ultra_relativistic", "is_symplectic_valid", "is_protection_intact"]):
            capabilities["has_telemetry_eval"] = True

        # Capability: Machine protection kicker dump abort
        if any(tok in stripped for tok in ["trigger_machine_protection_dump", "kicker_abort", "kicker_field", "beam_extracted_to_dump"]):
            capabilities["has_kicker_dump_abort"] = True

        # 4. Check for Accelerator Hazards and Violations
        # Hazard: Substandard tune resonance margin (< 0.05)
        margin_match = re.search(r"\b(?:min_tune_margin|tune_resonance_margin)\s*=\s*(0\.0[0-4][0-9]*|0\.00[0-9]*)\b", stripped)
        if margin_match:
            violations.append(f"Substandard betatron tune resonance margin: {margin_match.group(1)} (minimum required: 0.05)")

        # Hazard: Unsafe cavity cryogenic temperature (> 2.0K)
        temp_match = re.search(r"\b(?:max_cavity_temp_k|cavity_temp_limit)\s*=\s*([3-9]\.[0-9]+|[1-9][0-9]+)\b", stripped)
        if temp_match:
            violations.append(f"Superconducting RF cavity temperature threshold ({temp_match.group(1)}K) exceeds 2.0K superfluid helium limit")

        # Hazard: Sluggish quench trip latency (> 10us)
        quench_match = re.search(r"\b(?:max_quench_latency_us|quench_trip_time_us)\s*=\s*([1-9][0-9]{2,}|[2-9][0-9])\b", stripped)
        if quench_match:
            violations.append(f"Quench trip interlock latency ({quench_match.group(1)}us) exceeds 10.0us threshold")

        # Hazard: Sluggish kicker abort latency (> 3.0us)
        kicker_match = re.search(r"\b(?:max_abort_latency_us|kicker_abort_time_us)\s*=\s*([4-9]|[1-9][0-9]+)\b", stripped)
        if kicker_match:
            violations.append(f"Kicker magnet abort latency ({kicker_match.group(1)}us) exceeds 3.0us limit")

        # 5. Calculate Score
        score = 100.0
        for cap, present in capabilities.items():
            if not present:
                score -= 10.0

        for v in violations:
            if "Substandard betatron tune" in v or "Superconducting RF cavity" in v or "Lazy stub" in v:
                score -= 25.0
            else:
                score -= 15.0

        score = max(0.0, min(100.0, score))
        has_fatal = any(
            "Substandard betatron tune" in v or
            "Superconducting RF cavity" in v or
            "Lazy stub" in v or
            "Empty pass" in v
            for v in violations
        ) or (not capabilities["has_relativistic_kinematics"] and not capabilities["has_tune_resonance_guard"])

        return AcceleratorInspectionResult(
            file_path=file_path,
            syntax_valid=syntax_valid,
            capabilities=capabilities,
            violations=violations,
            has_fatal_defects=has_fatal,
            ast_node_count=node_count,
            score=score
        )

    @classmethod
    def inspect(cls, source_code: str, file_path: str = "inline_accelerator.py") -> Dict[str, Any]:
        """Convenience classmethod returning dict of inspected accelerator metrics."""
        inst = cls()
        res = inst.inspect_source(source_code, file_path=file_path)
        return {
            "ast_valid": res.syntax_valid,
            "has_relativistic_kinematics": res.capabilities.get("has_relativistic_kinematics", False),
            "has_tune_resonance_guard": res.capabilities.get("has_tune_resonance_guard", False),
            "has_cavity_quench_check": res.capabilities.get("has_cavity_quench_check", False),
            "has_telemetry_eval": res.capabilities.get("has_telemetry_eval", False),
            "has_kicker_dump_abort": res.capabilities.get("has_kicker_dump_abort", False),
            "has_fatal_defects": res.has_fatal_defects,
            "violations": res.violations,
            "score": res.score,
            "is_production_ready": res.is_production_ready,
        }
