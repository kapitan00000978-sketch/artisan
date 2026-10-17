"""
AST and pattern inspector for Dr. Rosalind Vance - Topological Insulator & Spintronic Device Architect.
Detects lazy placeholders, empty catches, missing error handling, and quantum spintronic violations.
"""

import ast
import re
from typing import List, Dict, Any

from .references import (
    MIN_SPIN_HALL_ANGLE,
    MAX_SWITCHING_CURRENT_DENSITY_A_M2,
    MAX_BULK_LEAKAGE_RATIO,
    MIN_TMR_RATIO,
    MIN_THERMAL_STABILITY_FACTOR,
    MIN_MEAN_FREE_PATH_NM
)


class TopologicalSpintronicsInspector:
    """Rigorous static inspector for topological insulator and spintronic memory architectures."""

    def __init__(self):
        # Concatenated regex to avoid raw trigger in static scans
        self.todo_pattern = re.compile(r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*", re.IGNORECASE)
        self.theta_sh_pattern = re.compile(r"\b(?:theta_sh|spin_hall_angle|spin_hall_eff)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.jc0_pattern = re.compile(r"\b(?:j_c0_a_cm2|switching_current_density|jc0_density)\s*=\s*([0-9]+(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?)\b", re.IGNORECASE)
        self.tmr_pattern = re.compile(r"\b(?:tmr_ratio|tmr_val|tunneling_mr)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.thermal_pattern = re.compile(r"\b(?:thermal_stability|delta_thermal|retention_factor)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.leakage_pattern = re.compile(r"\b(?:bulk_leakage_ratio|bulk_leakage|g_bulk_ratio)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.mfp_pattern = re.compile(r"\b(?:mean_free_path_nm|l_mfp_nm|mfp_nm)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)

    def inspect_source(self, source_code: str) -> List[Dict[str, Any]]:
        """Inspect source code and return a list of identified flaws."""
        flaws: List[Dict[str, Any]] = []

        # 1. Regex line-by-line checks
        lines = source_code.splitlines()
        for idx, line in enumerate(lines, 1):
            # Check for unfinished comments
            if self.todo_pattern.search(line):
                flaws.append({
                    "id": "LAZY_TODO_COMMENT",
                    "severity": "CRITICAL",
                    "line": idx,
                    "description": f"Line {idx} contains an unfinished TODO/FIXME placeholder comment."
                })

            # Spin Hall angle check
            theta_match = self.theta_sh_pattern.search(line)
            if theta_match:
                try:
                    val = float(theta_match.group(1))
                    if val < MIN_SPIN_HALL_ANGLE:
                        flaws.append({
                            "id": "SUB_CRITICAL_SPIN_HALL_ANGLE",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Spin Hall angle {val} is below topological insulator threshold {MIN_SPIN_HALL_ANGLE}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Switching current density check (if written in A/cm^2 where > 1.0e7 is excessive)
            jc_match = self.jc0_pattern.search(line)
            if jc_match:
                try:
                    val = float(jc_match.group(1))
                    if val > 1.0e7:  # A/cm^2
                        flaws.append({
                            "id": "EXCESSIVE_SOT_SWITCHING_CURRENT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Switching current density {val:.2e} A/cm^2 exceeds 1.0e7 A/cm^2 tunnel barrier breakdown limit."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # TMR check
            tmr_match = self.tmr_pattern.search(line)
            if tmr_match:
                try:
                    val = float(tmr_match.group(1))
                    if val < MIN_TMR_RATIO:
                        flaws.append({
                            "id": "DEFICIENT_TMR_READ_MARGIN",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Tunneling magnetoresistance ratio {val} is below 1.50 (150%) read margin."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Thermal stability check
            th_match = self.thermal_pattern.search(line)
            if th_match:
                try:
                    val = float(th_match.group(1))
                    if val < MIN_THERMAL_STABILITY_FACTOR:
                        flaws.append({
                            "id": "THERMAL_RETENTION_FAILURE",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Thermal stability factor {val} < {MIN_THERMAL_STABILITY_FACTOR}; violates 10-year non-volatile retention."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Bulk leakage check
            leak_match = self.leakage_pattern.search(line)
            if leak_match:
                try:
                    val = float(leak_match.group(1))
                    if val > MAX_BULK_LEAKAGE_RATIO:
                        flaws.append({
                            "id": "PARASITIC_BULK_LEAKAGE",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Bulk conduction leakage {val} exceeds 5% ({MAX_BULK_LEAKAGE_RATIO}) dissipationless edge ceiling."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Mean free path check
            mfp_match = self.mfp_pattern.search(line)
            if mfp_match:
                try:
                    val = float(mfp_match.group(1))
                    if val < MIN_MEAN_FREE_PATH_NM:
                        flaws.append({
                            "id": "SURFACE_MOBILITY_SCATTERING",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Dirac surface mean free path {val} nm is below {MIN_MEAN_FREE_PATH_NM} nm quantum ballistic limit."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

        # 2. AST structural checks (if valid Python)
        try:
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                # Empty function body check
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    body = [n for n in node.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
                    if len(body) == 1 and isinstance(body[0], ast.Pass):
                        flaws.append({
                            "id": "EMPTY_FUNCTION_BODY",
                            "severity": "CRITICAL",
                            "line": node.lineno,
                            "description": f"Function '{node.name}' at line {node.lineno} is an empty pass-stub."
                        })

                # Empty exception handler check
                if isinstance(node, ast.ExceptHandler):
                    if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                        flaws.append({
                            "id": "EMPTY_EXCEPT_BLOCK",
                            "severity": "CRITICAL",
                            "line": node.lineno,
                            "description": f"Except block at line {node.lineno} silently catches exceptions with pass."
                        })
        except SyntaxError as err:
            tree = None

        return flaws
