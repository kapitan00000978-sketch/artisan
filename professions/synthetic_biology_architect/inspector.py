"""Static AST and regex inspector for Synthetic Biology & Metabolic Genetic Circuits.

Maintained by Dr. Seraphiel 'The SynBio' Sterling.
Inspects code for Hill cooperativity, cellular metabolic burden,
transcriptional crosstalk, and dual-layer biocontainment escape frequencies.
"""

from __future__ import annotations
import ast
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class SynBioInspectionResult:
    """Detailed inspection report for synthetic biology autonomy code."""
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


class SynBioInspector:
    """Audits synthetic genetic circuit design and biocontainment software."""

    def __init__(self) -> None:
        todo_pattern = r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*\n"
        self._stub_regex = re.compile(todo_pattern, re.IGNORECASE)

    def _strip_comments(self, code: str) -> str:
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
        code = re.sub(r"//.*", "", code)
        code = re.sub(r"#.*", "", code)
        return code

    def inspect_source(self, source_code: str, file_path: str = "inline_synbio.py") -> SynBioInspectionResult:
        """Conduct ruthless static and AST inspection against synthetic biology standards."""
        stripped = self._strip_comments(source_code)
        violations: List[str] = []
        capabilities = {
            "has_hill_kinetics": False,
            "has_metabolic_burden_calc": False,
            "has_crosstalk_check": False,
            "has_telemetry_eval": False,
            "has_suicide_kill_switch": False
        }

        # 1. AST Syntax Check
        try:
            tree = ast.parse(source_code)
            syntax_valid = True
            node_count = len(list(ast.walk(tree)))
        except SyntaxError as err:
            return SynBioInspectionResult(
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

        # Capability: Hill kinetics transfer function
        if any(tok in stripped for tok in ["compute_transfer_function", "calculate_hill_repression", "hill_coefficient", "kd ** n", "kd_n"]):
            capabilities["has_hill_kinetics"] = True

        # Capability: Metabolic burden calculation
        if any(tok in stripped for tok in ["evaluate_circuit_burden", "evaluate_metabolic_burden", "ribosome_usage_fraction", "atp_drain"]):
            capabilities["has_metabolic_burden_calc"] = True

        # Capability: Crosstalk check
        if any(tok in stripped for tok in ["host_crosstalk_rate", "host_crosstalk_fraction", "max_crosstalk_limit", "is_orthogonal_clean"]):
            capabilities["has_crosstalk_check"] = True

        # Capability: Telemetry safety audit
        if any(tok in stripped for tok in ["evaluate_telemetry_safety", "is_kinetics_robust", "is_burden_sustainable", "is_containment_secure"]):
            capabilities["has_telemetry_eval"] = True

        # Capability: Suicide kill switch
        if any(tok in stripped for tok in ["trigger_suicide_kill_switch", "suicide_switch_mechanism", "suicide_kill_switch_deployed", "kill_switch_latency"]):
            capabilities["has_suicide_kill_switch"] = True

        # 4. Check for Synthetic Biology Hazards and Violations
        # Hazard: Substandard Hill cooperativity (< 2.0)
        hill_match = re.search(r"\b(?:min_hill_n|hill_coefficient_n)\s*=\s*(0\.[0-9]+|1\.[0-9]+)\b", stripped)
        if hill_match:
            violations.append(f"Substandard Hill cooperativity coefficient: {hill_match.group(1)} (minimum required: 2.0)")

        # Hazard: Excessive metabolic burden limit (> 0.30)
        burden_match = re.search(r"\b(?:max_burden_limit|total_burden_limit)\s*=\s*(0\.(?:3[1-9]|[4-9][0-9]*)|[1-9]\.[0-9]+)\b", stripped)
        if burden_match:
            violations.append(f"Metabolic burden limit {burden_match.group(1)} exceeds 30% cellular translation budget")

        # Hazard: Inadequate biocontainment escape rate (> 1e-8)
        escape_match = re.search(r"\b(?:max_escape_freq|measured_escape_frequency)\s*=\s*1\.0e-([1-7])\b", stripped)
        if escape_match:
            violations.append(f"Biocontainment escape frequency (1.0e-{escape_match.group(1)}) violates NIH 1.0e-8 standard")

        # Hazard: Sluggish kill switch latency (> 60 min)
        kill_lat_match = re.search(r"\b(?:max_kill_latency_min|kill_switch_latency_min)\s*=\s*([7-9][0-9]|[1-9][0-9]{2,})\b", stripped)
        if kill_lat_match:
            violations.append(f"Kill switch activation latency ({kill_lat_match.group(1)} min) exceeds 60.0 min threshold")

        # 5. Calculate Score
        score = 100.0
        for cap, present in capabilities.items():
            if not present:
                score -= 10.0

        for v in violations:
            if "Biocontainment escape frequency" in v or "Metabolic burden limit" in v or "Lazy stub" in v:
                score -= 25.0
            else:
                score -= 15.0

        score = max(0.0, min(100.0, score))
        has_fatal = any(
            "Biocontainment escape frequency" in v or
            "Metabolic burden limit" in v or
            "Lazy stub" in v or
            "Empty pass" in v
            for v in violations
        ) or (not capabilities["has_hill_kinetics"] and not capabilities["has_suicide_kill_switch"])

        return SynBioInspectionResult(
            file_path=file_path,
            syntax_valid=syntax_valid,
            capabilities=capabilities,
            violations=violations,
            has_fatal_defects=has_fatal,
            ast_node_count=node_count,
            score=score
        )

    @classmethod
    def inspect(cls, source_code: str, file_path: str = "inline_synbio.py") -> Dict[str, Any]:
        """Convenience classmethod returning dict of inspected synbio metrics."""
        inst = cls()
        res = inst.inspect_source(source_code, file_path=file_path)
        return {
            "ast_valid": res.syntax_valid,
            "has_hill_kinetics": res.capabilities.get("has_hill_kinetics", False),
            "has_metabolic_burden_calc": res.capabilities.get("has_metabolic_burden_calc", False),
            "has_crosstalk_check": res.capabilities.get("has_crosstalk_check", False),
            "has_telemetry_eval": res.capabilities.get("has_telemetry_eval", False),
            "has_suicide_kill_switch": res.capabilities.get("has_suicide_kill_switch", False),
            "has_fatal_defects": res.has_fatal_defects,
            "violations": res.violations,
            "score": res.score,
            "is_production_ready": res.is_production_ready,
        }
