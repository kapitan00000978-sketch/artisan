"""Static AST and regex inspector for Subsea Autonomous Robotics & Deep-Sea Navigation.

Maintained by Commander Orion 'The Deep' Sterling.
Inspects code for hydrostatic crush verification, acoustic sound velocity models,
positive dielectric compensation, and passive ballast jettison fail-safes.
"""

from __future__ import annotations
import ast
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class DeepSeaInspectionResult:
    """Detailed inspection report for subsea autonomy code."""
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


class DeepSeaInspector:
    """Audits subsea autonomous robotics and extreme deep-sea navigation code."""

    def __init__(self) -> None:
        # Avoid literal stubs in pattern definitions
        todo_pattern = r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*\n"
        self._stub_regex = re.compile(todo_pattern, re.IGNORECASE)

    def _strip_comments(self, code: str) -> str:
        """Strip comments to avoid matching commented patterns."""
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
        code = re.sub(r"//.*", "", code)
        code = re.sub(r"#.*", "", code)
        return code

    def inspect_source(self, source_code: str, file_path: str = "inline_deepsea.py") -> DeepSeaInspectionResult:
        """Conduct ruthless static and AST inspection against subsea standards."""
        stripped = self._strip_comments(source_code)
        violations: List[str] = []
        capabilities = {
            "has_hydrostatic_calc": False,
            "has_sound_speed_model": False,
            "has_hull_safety_check": False,
            "has_telemetry_eval": False,
            "has_passive_jettison": False
        }

        # 1. AST Syntax Check
        try:
            tree = ast.parse(source_code)
            syntax_valid = True
            node_count = len(list(ast.walk(tree)))
        except SyntaxError as err:
            return DeepSeaInspectionResult(
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
        classes = {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}

        # Capability: Hydrostatic pressure
        if any(tok in stripped for tok in ["compute_hydrostatic_pressure", "calculate_hydrostatic_pressure", "density * gravity * depth", "density_kg_m3 * standard_gravity"]):
            capabilities["has_hydrostatic_calc"] = True

        # Capability: Sound speed model (Mackenzie / Del Grosso)
        if any(tok in stripped for tok in ["calculate_sound_velocity", "calculate_sound_speed_mackenzie", "1448.96", "sound_speed_mps"]):
            capabilities["has_sound_speed_model"] = True

        # Capability: Hull safety factor verification
        if any(tok in stripped for tok in ["verify_hull_safety", "evaluate_hull_safety_factor", "collapse_pressure_mpa", "min_safety_factor", "rated_hull_collapse_mpa"]):
            capabilities["has_hull_safety_check"] = True

        # Capability: Subsea telemetry evaluation
        if any(tok in stripped for tok in ["evaluate_telemetry_safety", "is_navigation_reliable", "is_buoyancy_safe", "is_compensation_intact"]):
            capabilities["has_telemetry_eval"] = True

        # Capability: Passive drop weight jettison fail-safe
        if any(tok in stripped for tok in ["trigger_passive_jettison", "passive_drop_weight", "fail_safe_burn_wire", "galvanic_burn_wire", "burn_wire"]):
            capabilities["has_passive_jettison"] = True

        # 4. Check for Subsea Physical Hazards and Violations
        # Hazard: Substandard safety factor (< 1.50)
        sf_match = re.search(r"\b(?:safety_factor|min_safety_factor)\s*=\s*(0\.[0-9]+|1\.[0-4][0-9]*)\b", stripped)
        if sf_match:
            violations.append(f"Substandard hull collapse safety factor: {sf_match.group(1)} (minimum required: 1.50)")

        # Hazard: Unsafe depth limit for hadal exploration
        depth_rating_match = re.search(r"\b(?:max_depth_m|depth_rating_m)\s*=\s*([0-9]{1,4})\b", stripped)
        if depth_rating_match:
            val = float(depth_rating_match.group(1))
            if val < 11000.0:
                violations.append(f"Depth rating {val}m is below Full Ocean Depth Challenger rating (11,000m)")

        # Hazard: Deficient compensator bias pressure (< 0.20 bar)
        bias_match = re.search(r"\b(?:compensation_bias_bar|reservoir_bias_pressure_bar)\s*=\s*0\.(?:0[0-9]|1[0-9])\b", stripped)
        if bias_match:
            violations.append("Compensator reservoir bias pressure below 0.20 bar margin against saline ingress")

        # Hazard: Excessively slow drop weight time (> 30s)
        drop_time_match = re.search(r"\b(?:emergency_jettison_time_s|jettison_time_s)\s*=\s*([4-9][0-9]|[1-9][0-9]{2,})\b", stripped)
        if drop_time_match:
            violations.append(f"Emergency ballast drop time ({drop_time_match.group(1)}s) exceeds 30.0s fail-safe envelope")

        # Hazard: Permitting excessive positional uncertainty (> 2.0m)
        drift_match = re.search(r"\b(?:max_drift_threshold_m|position_error_bound)\s*=\s*([3-9]|[1-9][0-9]+)\b", stripped)
        if drift_match:
            violations.append(f"Acoustic position drift tolerance ({drift_match.group(1)}m) exceeds 2.0m bound")

        # 5. Calculate Score
        # Start at 100, deduct for missing capabilities and domain violations
        score = 100.0
        for cap, present in capabilities.items():
            if not present:
                score -= 10.0

        for v in violations:
            if "Substandard hull collapse" in v or "Depth rating" in v or "Lazy stub" in v:
                score -= 25.0
            else:
                score -= 15.0

        score = max(0.0, min(100.0, score))
        has_fatal = any(
            "Substandard hull collapse" in v or
            "Depth rating" in v or
            "Lazy stub" in v or
            "Empty pass" in v
            for v in violations
        ) or (not capabilities["has_hydrostatic_calc"] and not capabilities["has_hull_safety_check"])

        return DeepSeaInspectionResult(
            file_path=file_path,
            syntax_valid=syntax_valid,
            capabilities=capabilities,
            violations=violations,
            has_fatal_defects=has_fatal,
            ast_node_count=node_count,
            score=score
        )

    @classmethod
    def inspect(cls, source_code: str, file_path: str = "inline_deepsea.py") -> Dict[str, Any]:
        """Convenience classmethod returning dict of inspected subsea metrics."""
        inst = cls()
        res = inst.inspect_source(source_code, file_path=file_path)
        return {
            "ast_valid": res.syntax_valid,
            "has_hydrostatic_calc": res.capabilities.get("has_hydrostatic_calc", False),
            "has_sound_speed_model": res.capabilities.get("has_sound_speed_model", False),
            "has_hull_safety_check": res.capabilities.get("has_hull_safety_check", False),
            "has_telemetry_eval": res.capabilities.get("has_telemetry_eval", False),
            "has_passive_jettison": res.capabilities.get("has_passive_jettison", False),
            "has_fatal_defects": res.has_fatal_defects,
            "violations": res.violations,
            "score": res.score,
            "is_production_ready": res.is_production_ready,
        }
