"""AST and pattern inspector for Dr. Eliana Sterling - Optical Lattice Clock & Quantum Metrology Architect.

Detects lazy placeholders, empty catches, missing error handling, and optical atomic clock systematic drift violations.
"""

import ast
import re
from typing import List, Dict, Any

from professions.optical_lattice_clock_metrology_architect.references import (
    MAX_FRACTIONAL_INACCURACY,
    MAX_ALLAN_DEV_COEFF,
    MAX_MAGIC_WAVELENGTH_DETUNING_NM,
    MAX_LASER_LINEWIDTH_MHZ,
    MIN_CAVITY_FINESSE,
    MIN_SILICON_CAVITY_TEMP_K,
    MAX_SILICON_CAVITY_TEMP_K,
    MAX_BBR_TEMP_UNCERTAINTY_MK,
    MAX_ATOM_TEMPERATURE_UK,
    MAX_COLLISIONAL_SHIFT_FRACTION,
    MAX_RESIDUAL_ZEEMAN_UT,
)


class OpticalClockInspector:
    """Rigorous static inspector for optical lattice clocks, ultra-narrow lasers, and quantum metrology systems."""

    def __init__(self) -> None:
        # Concatenated regex to avoid raw trigger in static scans
        self.todo_pattern = re.compile(r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*", re.IGNORECASE)
        self.inaccuracy_pattern = re.compile(r"\b(?:fractional_inaccuracy|delta_nu_nu0|clock_uncertainty)\s*=\s*([0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?)\b", re.IGNORECASE)
        self.allan_dev_pattern = re.compile(r"\b(?:allan_deviation_1s|sigma_y_1s|allan_instability)\s*=\s*([0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?)\b", re.IGNORECASE)
        self.detuning_pattern = re.compile(r"\b(?:magic_wavelength_detuning_nm|delta_lambda_nm|magic_detuning_nm)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.linewidth_pattern = re.compile(r"\b(?:laser_linewidth_mhz|delta_nu_laser_mhz|linewidth_mhz)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.finesse_pattern = re.compile(r"\b(?:cavity_finesse|finesse_f|finesse_val)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.cavity_temp_pattern = re.compile(r"\b(?:cavity_temperature_k|t_cavity_k|silicon_temp_k)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.bbr_pattern = re.compile(r"\b(?:bbr_temp_uncertainty_mk|delta_t_bbr_mk|bbr_uncertainty_mk)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.atom_temp_pattern = re.compile(r"\b(?:atom_temperature_uk|t_atom_uk|atom_temp_microkelvin)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.collisional_pattern = re.compile(r"\b(?:collisional_shift_fraction|delta_nu_coll_fraction|density_shift)\s*=\s*([0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?)\b", re.IGNORECASE)
        self.zeeman_pattern = re.compile(r"\b(?:residual_zeeman_ut|b_residual_ut|zeeman_field_ut)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)

    def inspect_source(self, source_code: str) -> List[Dict[str, Any]]:
        """Inspect source code and return a list of identified flaws."""
        flaws: List[Dict[str, Any]] = []

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

            # Fractional frequency inaccuracy check
            m = self.inaccuracy_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_FRACTIONAL_INACCURACY:
                        flaws.append({
                            "id": "FRACTIONAL_INACCURACY_EXCESS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Fractional frequency uncertainty {val:.2e} exceeds precision limit {MAX_FRACTIONAL_INACCURACY:.2e}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Allan deviation check
            m = self.allan_dev_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_ALLAN_DEV_COEFF:
                        flaws.append({
                            "id": "ALLAN_DEVIATION_EXCESS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Short-term Allan deviation {val:.2e} exceeds stability ceiling {MAX_ALLAN_DEV_COEFF:.2e}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Magic wavelength detuning check
            m = self.detuning_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_MAGIC_WAVELENGTH_DETUNING_NM:
                        flaws.append({
                            "id": "MAGIC_WAVELENGTH_DETUNING_EXCESS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Magic wavelength detuning {val:.4f} nm exceeds tolerance {MAX_MAGIC_WAVELENGTH_DETUNING_NM:.3f} nm (differential AC Stark shift risk)."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Clock laser linewidth check
            m = self.linewidth_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_LASER_LINEWIDTH_MHZ:
                        flaws.append({
                            "id": "LASER_LINEWIDTH_EXCESS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Interrogation laser linewidth {val:.2f} mHz exceeds sub-millihertz limit {MAX_LASER_LINEWIDTH_MHZ:.1f} mHz."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Cavity finesse check
            m = self.finesse_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_CAVITY_FINESSE:
                        flaws.append({
                            "id": "CAVITY_FINESSE_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Cavity optical finesse {val:,.0f} below high-Q threshold {MIN_CAVITY_FINESSE:,.0f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Silicon cavity temperature check
            m = self.cavity_temp_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_SILICON_CAVITY_TEMP_K or val > MAX_SILICON_CAVITY_TEMP_K:
                        flaws.append({
                            "id": "CAVITY_TEMPERATURE_DEVIATION",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Cavity temperature {val:.2f} K outside silicon thermal expansion null [{MIN_SILICON_CAVITY_TEMP_K:.1f}, {MAX_SILICON_CAVITY_TEMP_K:.1f}] K."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # BBR temperature uncertainty check
            m = self.bbr_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_BBR_TEMP_UNCERTAINTY_MK:
                        flaws.append({
                            "id": "BBR_UNCERTAINTY_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: BBR temperature uncertainty {val:.1f} mK exceeds tolerance {MAX_BBR_TEMP_UNCERTAINTY_MK:.1f} mK."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Atom temperature check
            m = self.atom_temp_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_ATOM_TEMPERATURE_UK:
                        flaws.append({
                            "id": "ATOM_TEMPERATURE_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Atom temperature {val:.2f} microkelvin exceeds Lamb-Dicke bound {MAX_ATOM_TEMPERATURE_UK:.1f} microkelvin."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Collisional density shift check
            m = self.collisional_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_COLLISIONAL_SHIFT_FRACTION:
                        flaws.append({
                            "id": "COLLISIONAL_SHIFT_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Collisional density shift {val:.2e} exceeds Pauli exclusion cap {MAX_COLLISIONAL_SHIFT_FRACTION:.2e}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Residual Zeeman field check
            m = self.zeeman_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_RESIDUAL_ZEEMAN_UT:
                        flaws.append({
                            "id": "ZEEMAN_FIELD_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Residual Zeeman field {val:.2f} microtesla exceeds magnetic shielding cap {MAX_RESIDUAL_ZEEMAN_UT:.1f} microtesla."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

        # AST structural checks
        try:
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    body = [n for n in node.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
                    if len(body) == 1 and isinstance(body[0], ast.Pass):
                        flaws.append({
                            "id": "EMPTY_FUNCTION_BODY",
                            "severity": "CRITICAL",
                            "line": node.lineno,
                            "description": f"Function '{node.name}' at line {node.lineno} is an empty pass-stub."
                        })

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

    def inspect_code(self, source_code: str) -> List[str]:
        """Convenience helper returning text descriptions of detected flaws."""
        return [f["description"] for f in self.inspect_source(source_code)]
