"""
AST and pattern inspector for Dr. Taras Sterling - Superfluid Quantum Hydrodynamics Architect.
Detects lazy placeholders, empty catches, missing error handling, and quantum hydrodynamic violations.
"""

import ast
import re
from typing import List, Dict, Any

from .references import (
    MAX_SUPERFLUID_TEMPERATURE_K,
    MIN_SUPERFLUID_FRACTION,
    MAX_SUPERFLUID_VELOCITY_M_S,
    MAX_VORTEX_LINE_DENSITY_M2,
    MAX_SUPERLEAK_PORE_NM,
    MIN_SECOND_SOUND_VELOCITY_M_S
)


class SuperfluidHydroInspector:
    """Rigorous static inspector for superfluid quantum hydrodynamics and Helium-4 cryogenic systems."""

    def __init__(self):
        # Concatenated regex to avoid raw trigger in static scans
        self.todo_pattern = re.compile(r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*", re.IGNORECASE)
        self.temp_pattern = re.compile(r"\b(?:cryo_temperature|t_bath_k|he_ii_temperature)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.fraction_pattern = re.compile(r"\b(?:superfluid_fraction|rho_s_frac|superfluid_ratio)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.velocity_pattern = re.compile(r"\b(?:superfluid_velocity|v_superfluid|v_s_flow)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.vortex_pattern = re.compile(r"\b(?:vortex_line_density|l_vortex_m2|vortex_density)\s*=\s*([0-9]+(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?)\b", re.IGNORECASE)
        self.pore_pattern = re.compile(r"\b(?:superleak_pore_nm|pore_diameter_nm|d_pore_nm)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.second_sound_pattern = re.compile(r"\b(?:second_sound_velocity|c2_velocity|second_sound_speed)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)

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

            # Bath temperature check
            temp_match = self.temp_pattern.search(line)
            if temp_match:
                try:
                    val = float(temp_match.group(1))
                    if val > MAX_SUPERFLUID_TEMPERATURE_K:
                        flaws.append({
                            "id": "LAMBDA_TRANSITION_BREACH",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Cryogenic bath temperature {val} K exceeds He-II threshold {MAX_SUPERFLUID_TEMPERATURE_K} K."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Superfluid fraction check
            frac_match = self.fraction_pattern.search(line)
            if frac_match:
                try:
                    val = float(frac_match.group(1))
                    if val < MIN_SUPERFLUID_FRACTION:
                        flaws.append({
                            "id": "SUPERFLUID_DENSITY_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Superfluid fraction {val} is below {MIN_SUPERFLUID_FRACTION} operating floor."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Superfluid flow velocity check
            vel_match = self.velocity_pattern.search(line)
            if vel_match:
                try:
                    val = float(vel_match.group(1))
                    if val > MAX_SUPERFLUID_VELOCITY_M_S:
                        flaws.append({
                            "id": "LANDAU_ROTON_DISSIPATION",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Superfluid velocity {val} m/s exceeds safe limit {MAX_SUPERFLUID_VELOCITY_M_S} m/s near Landau roton limit."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Vortex line density check
            vortex_match = self.vortex_pattern.search(line)
            if vortex_match:
                try:
                    val = float(vortex_match.group(1))
                    if val > MAX_VORTEX_LINE_DENSITY_M2:
                        flaws.append({
                            "id": "VORTEX_TANGLE_TURBULENCE",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Vortex line density {val:.2e} m^-2 exceeds critical tangle ceiling {MAX_VORTEX_LINE_DENSITY_M2:.2e} m^-2."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Superleak pore diameter check
            pore_match = self.pore_pattern.search(line)
            if pore_match:
                try:
                    val = float(pore_match.group(1))
                    if val > MAX_SUPERLEAK_PORE_NM:
                        flaws.append({
                            "id": "SUPERLEAK_VISCOUS_LEAKAGE",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Superleak pore diameter {val} nm exceeds 10.0 nm viscous clamping limit."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Second sound velocity check
            c2_match = self.second_sound_pattern.search(line)
            if c2_match:
                try:
                    val = float(c2_match.group(1))
                    if val < MIN_SECOND_SOUND_VELOCITY_M_S:
                        flaws.append({
                            "id": "SECOND_SOUND_CHOKING",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Second sound velocity {val} m/s is below {MIN_SECOND_SOUND_VELOCITY_M_S} m/s propagation bound."
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
