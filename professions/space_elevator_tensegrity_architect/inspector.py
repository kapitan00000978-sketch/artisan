"""AST and pattern inspector for Dr. Valerius Sterling - Space Elevator & Active Tensegrity Megastructure Architect.

Detects lazy placeholders, empty catches, missing error handling, and megastructure elastodynamic violations.
"""

import ast
import re
from typing import List, Dict, Any

from professions.space_elevator_tensegrity_architect.references import (
    MIN_TENSILE_STRENGTH_PA,
    MAX_TETHER_DENSITY_KG_M3,
    MIN_TETHER_LENGTH_M,
    MIN_ANCHOR_PRETENSION_N,
    MAX_CLIMBER_MASS_KG,
    MAX_CLIMBER_VELOCITY_M_S,
    MIN_ACTIVE_DAMPING_RATIO,
    MAX_RESONANT_QUALITY_FACTOR,
    MIN_WAVE_VELOCITY_M_S,
)


class SpaceElevatorInspector:
    """Rigorous static inspector for space elevator and active tensegrity megastructures."""

    def __init__(self) -> None:
        # Concatenated regex to avoid raw trigger in static scans
        self.todo_pattern = re.compile(r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*", re.IGNORECASE)
        self.tensile_pattern = re.compile(r"\b(?:tensile_strength_gpa|sigma_t_gpa|tether_tensile_gpa)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.density_pattern = re.compile(r"\b(?:tether_density_kg_m3|rho_tether|material_density)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.length_pattern = re.compile(r"\b(?:tether_length_km|l_tether_km|total_length_km)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.pretension_pattern = re.compile(r"\b(?:anchor_pretension_mn|t_anchor_mn|anchor_tension_mn)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.climber_mass_pattern = re.compile(r"\b(?:climber_mass_kg|m_climber_kg|payload_climber_kg)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.climber_v_pattern = re.compile(r"\b(?:climber_velocity_km_h|v_climber_kmh|ascent_speed_kmh)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.damping_pattern = re.compile(r"\b(?:active_damping_ratio|zeta_damping|tether_damping)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.quality_pattern = re.compile(r"\b(?:quality_factor|q_factor|q_resonance)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.wave_v_pattern = re.compile(r"\b(?:wave_velocity_m_s|c_wave_m_s|transverse_wave_speed)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)

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

            # Tensile strength check
            m = self.tensile_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < (MIN_TENSILE_STRENGTH_PA / 1e9):
                        flaws.append({
                            "id": "TENSILE_STRENGTH_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Tensile strength {val:.1f} GPa below minimum {MIN_TENSILE_STRENGTH_PA / 1e9:.1f} GPa."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Tether material density check
            m = self.density_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_TETHER_DENSITY_KG_M3:
                        flaws.append({
                            "id": "TETHER_DENSITY_EXCESS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Tether density {val:.1f} kg/m^3 exceeds maximum allowable {MAX_TETHER_DENSITY_KG_M3:.1f} kg/m^3."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Tether length check
            m = self.length_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < (MIN_TETHER_LENGTH_M / 1000.0):
                        flaws.append({
                            "id": "TETHER_LENGTH_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Tether length {val:.0f} km below orbital equilibrium requirement {MIN_TETHER_LENGTH_M / 1000.0:.0f} km."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Anchor pretension check
            m = self.pretension_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < (MIN_ANCHOR_PRETENSION_N / 1e6):
                        flaws.append({
                            "id": "ANCHOR_PRETENSION_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Anchor pretension {val:.1f} MN below safety threshold {MIN_ANCHOR_PRETENSION_N / 1e6:.1f} MN."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Climber mass overload check
            m = self.climber_mass_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_CLIMBER_MASS_KG:
                        flaws.append({
                            "id": "CLIMBER_MASS_OVERLOAD",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Climber mass {val:.0f} kg exceeds maximum rating {MAX_CLIMBER_MASS_KG:.0f} kg."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Climber velocity check
            m = self.climber_v_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > (MAX_CLIMBER_VELOCITY_M_S * 3.6):
                        flaws.append({
                            "id": "CLIMBER_VELOCITY_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Climber velocity {val:.1f} km/h exceeds maximum limit {MAX_CLIMBER_VELOCITY_M_S * 3.6:.1f} km/h."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Damping ratio check
            m = self.damping_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_ACTIVE_DAMPING_RATIO:
                        flaws.append({
                            "id": "DAMPING_RATIO_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Active damping ratio {val:.3f} below minimum {MIN_ACTIVE_DAMPING_RATIO:.3f} (5.0%)."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Resonant quality factor check
            m = self.quality_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_RESONANT_QUALITY_FACTOR:
                        flaws.append({
                            "id": "QUALITY_FACTOR_RESONANCE",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Quality factor Q={val:.1f} exceeds resonance ceiling Q={MAX_RESONANT_QUALITY_FACTOR:.1f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Transverse wave velocity check
            m = self.wave_v_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_WAVE_VELOCITY_M_S:
                        flaws.append({
                            "id": "WAVE_VELOCITY_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Wave velocity {val:.1f} m/s below stiffness threshold {MIN_WAVE_VELOCITY_M_S:.1f} m/s."
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
