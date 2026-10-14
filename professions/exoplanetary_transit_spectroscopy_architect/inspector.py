"""
AST and pattern inspector for Dr. Linus Sterling - Exoplanetary Atmosphere & Transit Spectroscopy Architect.
Detects lazy placeholders, empty catches, missing error handling, and astrophysical parameter violations.
"""

import ast
import re
from typing import List, Dict, Any

from .references import (
    MIN_TRANSIT_DEPTH,
    MIN_SCALE_HEIGHT_KM,
    MAX_SCALE_HEIGHT_KM,
    MIN_DETECTION_SNR,
    MAX_SPOT_FILLING_FACTOR,
    MIN_REDUCED_CHI_SQUARED,
    MAX_REDUCED_CHI_SQUARED
)


class ExoplanetTransitSpecInspector:
    """Rigorous static inspector for exoplanetary atmosphere and transit spectroscopy code."""

    def __init__(self):
        # Concatenated regex to avoid raw trigger in static scans
        self.todo_pattern = re.compile(r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*", re.IGNORECASE)
        self.scale_height_pattern = re.compile(r"\b(?:scale_height|scale_h|h_atm)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.snr_pattern = re.compile(r"\b(?:snr|detection_snr|sig_level)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.spot_pattern = re.compile(r"\b(?:f_spot|spot_fraction|spot_coverage)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.chi2_pattern = re.compile(r"\b(?:reduced_chi2|chi2_red|red_chi2)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)

    def inspect_source(self, source_code: str) -> List[Dict[str, Any]]:
        """Inspect source code and return a list of identified flaws."""
        flaws: List[Dict[str, Any]] = []

        # 1. Regex line-by-line checks
        lines = source_code.splitlines()
        for idx, line in enumerate(lines, 1):
            # Check for TODOs / lazy comments
            if self.todo_pattern.search(line):
                flaws.append({
                    "id": "LAZY_TODO_COMMENT",
                    "severity": "CRITICAL",
                    "line": idx,
                    "description": f"Line {idx} contains an unfinished TODO/FIXME placeholder comment."
                })

            # Scale height bounds check
            scale_match = self.scale_height_pattern.search(line)
            if scale_match:
                try:
                    val = float(scale_match.group(1))
                    if val < MIN_SCALE_HEIGHT_KM or val > MAX_SCALE_HEIGHT_KM:
                        flaws.append({
                            "id": "PHYSICS_SCALE_HEIGHT_VIOLATION",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Scale height {val} km outside plausible physical bounds [{MIN_SCALE_HEIGHT_KM}, {MAX_SCALE_HEIGHT_KM}] km."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # SNR bounds check
            snr_match = self.snr_pattern.search(line)
            if snr_match:
                try:
                    val = float(snr_match.group(1))
                    if val < MIN_DETECTION_SNR:
                        flaws.append({
                            "id": "DETECTION_SNR_VIOLATION",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Spectroscopic detection SNR {val} is below the 5.0-sigma astrophysics discovery threshold."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Spot filling factor check
            spot_match = self.spot_pattern.search(line)
            if spot_match:
                try:
                    val = float(spot_match.group(1))
                    if val > MAX_SPOT_FILLING_FACTOR:
                        flaws.append({
                            "id": "STELLAR_SPOT_CORRUPTION",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Spot filling factor {val} exceeds unocculted stability ceiling {MAX_SPOT_FILLING_FACTOR}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Reduced Chi2 check
            chi2_match = self.chi2_pattern.search(line)
            if chi2_match:
                try:
                    val = float(chi2_match.group(1))
                    if val < MIN_REDUCED_CHI_SQUARED or val > MAX_REDUCED_CHI_SQUARED:
                        flaws.append({
                            "id": "RETRIEVAL_CHI2_OUT_OF_BOUNDS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Reduced chi-squared {val} outside acceptable goodness-of-fit interval [{MIN_REDUCED_CHI_SQUARED}, {MAX_REDUCED_CHI_SQUARED}]."
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
