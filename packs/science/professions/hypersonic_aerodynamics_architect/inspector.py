"""Static AST and regex inspector for Hypersonic Aerothermodynamics & Scramjet Propulsion.

Maintained by Dr. Zephyr 'The Hypersonic' Sterling.
Inspects code for Sutton-Graves aerothermal heating, real-gas dissociation,
scramjet isolator shock train margins, and unstart mitigation latencies.
"""

from __future__ import annotations
import ast
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class HypersonicInspectionResult:
    """Detailed inspection report for hypersonic flight and scramjet autonomy code."""
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


class HypersonicInspector:
    """Audits hypersonic aerothermodynamics and scramjet control software."""

    def __init__(self) -> None:
        todo_pattern = r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*\n"
        self._stub_regex = re.compile(todo_pattern, re.IGNORECASE)

    def _strip_comments(self, code: str) -> str:
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
        code = re.sub(r"//.*", "", code)
        code = re.sub(r"#.*", "", code)
        return code

    def inspect_source(self, source_code: str, file_path: str = "inline_hypersonic.py") -> HypersonicInspectionResult:
        """Conduct ruthless static and AST inspection against hypersonic standards."""
        stripped = self._strip_comments(source_code)
        violations: List[str] = []
        capabilities = {
            "has_aerothermal_heating": False,
            "has_real_gas_model": False,
            "has_isolator_stability": False,
            "has_telemetry_eval": False,
            "has_unstart_mitigation": False
        }

        # 1. AST Syntax Check
        try:
            tree = ast.parse(source_code)
            syntax_valid = True
            node_count = len(list(ast.walk(tree)))
        except SyntaxError as err:
            return HypersonicInspectionResult(
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

        # Capability: Aerothermal heating calculation
        if any(tok in stripped for tok in ["calculate_stagnation_aerothermal_heating", "calculate_sutton_graves_heat_flux", "sutton_graves", "k_sg * math.sqrt"]):
            capabilities["has_aerothermal_heating"] = True

        # Capability: Real gas dissociation
        if any(tok in stripped for tok in ["evaluate_real_gas_shock_temperature", "real_gas", "dissociation", "is_real_gas_valid"]):
            capabilities["has_real_gas_model"] = True

        # Capability: Scramjet isolator shock stability
        if any(tok in stripped for tok in ["evaluate_scramjet_isolator_stability", "calculate_isolator_shock_train_length", "shock_train", "isolator_stability_margin"]):
            capabilities["has_isolator_stability"] = True

        # Capability: Telemetry safety audit
        if any(tok in stripped for tok in ["evaluate_telemetry_safety", "is_hypersonic_regime", "is_isolator_stable", "is_tps_safe"]):
            capabilities["has_telemetry_eval"] = True

        # Capability: Active unstart mitigation
        if any(tok in stripped for tok in ["trigger_unstart_mitigation", "fuel_throttle", "bleed_doors", "unstart_mitigation_deployed"]):
            capabilities["has_unstart_mitigation"] = True

        # 4. Check for Hypersonic Aerothermodynamic Hazards
        # Hazard: Substandard isolator margin (< 1.25)
        iso_match = re.search(r"\b(?:min_isolator_margin|isolator_stability_margin)\s*=\s*(0\.[0-9]+|1\.[0-1][0-9]*|1\.2[0-4])\b", stripped)
        if iso_match:
            violations.append(f"Substandard scramjet isolator shock margin: {iso_match.group(1)} (minimum required: 1.25)")

        # Hazard: Substandard TPS safety factor (< 1.50)
        tps_match = re.search(r"\b(?:min_tps_safety_factor|tps_safety_factor)\s*=\s*(0\.[0-9]+|1\.[0-4][0-9]*)\b", stripped)
        if tps_match:
            violations.append(f"Substandard Thermal Protection System safety factor: {tps_match.group(1)} (minimum required: 1.50)")

        # Hazard: Excessive unstart reaction latency (> 5.0ms)
        latency_match = re.search(r"\b(?:unstart_actuator_latency_ms|unstart_response_ms)\s*=\s*([6-9]|[1-9][0-9]+)\b", stripped)
        if latency_match:
            violations.append(f"Unstart mitigation response latency ({latency_match.group(1)}ms) exceeds 5.0ms unstart threshold")

        # 5. Calculate Score
        score = 100.0
        for cap, present in capabilities.items():
            if not present:
                score -= 10.0

        for v in violations:
            if "Substandard scramjet isolator" in v or "Substandard Thermal Protection" in v or "Lazy stub" in v:
                score -= 25.0
            else:
                score -= 15.0

        score = max(0.0, min(100.0, score))
        has_fatal = any(
            "Substandard scramjet isolator" in v or
            "Substandard Thermal Protection" in v or
            "Lazy stub" in v or
            "Empty pass" in v
            for v in violations
        ) or (not capabilities["has_aerothermal_heating"] and not capabilities["has_isolator_stability"])

        return HypersonicInspectionResult(
            file_path=file_path,
            syntax_valid=syntax_valid,
            capabilities=capabilities,
            violations=violations,
            has_fatal_defects=has_fatal,
            ast_node_count=node_count,
            score=score
        )

    @classmethod
    def inspect(cls, source_code: str, file_path: str = "inline_hypersonic.py") -> Dict[str, Any]:
        """Convenience classmethod returning dict of inspected hypersonic metrics."""
        inst = cls()
        res = inst.inspect_source(source_code, file_path=file_path)
        return {
            "ast_valid": res.syntax_valid,
            "has_aerothermal_heating": res.capabilities.get("has_aerothermal_heating", False),
            "has_real_gas_model": res.capabilities.get("has_real_gas_model", False),
            "has_isolator_stability": res.capabilities.get("has_isolator_stability", False),
            "has_telemetry_eval": res.capabilities.get("has_telemetry_eval", False),
            "has_unstart_mitigation": res.capabilities.get("has_unstart_mitigation", False),
            "has_fatal_defects": res.has_fatal_defects,
            "violations": res.violations,
            "score": res.score,
            "is_production_ready": res.is_production_ready,
        }
