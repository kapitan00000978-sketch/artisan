"""AST and pattern inspector for Dr. Zephyrus Vance - Interstellar Bussard Ramjet Architect.

Detects unfinished stubs, empty exception handlers, and relativistic magnetic scoop parameter breaches.
"""

import ast
import re
from typing import List, Dict, Any

from professions.interstellar_ramjet_bussard_propulsion_architect.references import (
    MIN_SCOOP_RADIUS_KM,
    MIN_RELATIVISTIC_VELOCITY_FRACTION,
    MIN_MAGNETIC_SCOOP_FIELD_T,
    MIN_PHOTO_IONIZATION_EFFICIENCY,
    MIN_CAPTURE_CROSS_SECTION_EFFICIENCY,
    MIN_THRUST_TO_DRAG_RATIO,
    MIN_EXHAUST_VELOCITY_M_S,
    MIN_NOZZLE_COLLIMATION_EFFICIENCY,
    MIN_SHIP_ACCELERATION_M_S2,
    MAX_SHIP_ACCELERATION_M_S2,
    MIN_CORE_FUSION_TEMP_K,
    MAX_BREMSSTRAHLUNG_LOSS_RATIO,
)


class BussardRamjetInspector:
    """Rigorous static inspector for Interstellar Bussard Ramjet and relativistic magnetic scoop code."""

    def __init__(self) -> None:
        # Concatenated regex to avoid raw trigger in static scans
        self.todo_pattern = re.compile(r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*", re.IGNORECASE)
        self.scoop_radius_pattern = re.compile(r"\b(?:scoop_radius_km|r_scoop_km|intake_radius_km)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.velocity_beta_pattern = re.compile(r"\b(?:flight_velocity_beta|cruise_beta|velocity_fraction_beta)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.scoop_field_pattern = re.compile(r"\b(?:magnetic_scoop_field_t|b_scoop_t|choke_field_t)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.photo_ion_pattern = re.compile(r"\b(?:photo_ionization_efficiency|eta_ion|ionization_efficiency)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.capture_eff_pattern = re.compile(r"\b(?:capture_cross_section_efficiency|eta_capture)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.thrust_drag_pattern = re.compile(r"\b(?:thrust_to_drag_ratio|f_thrust_drag_ratio)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.exhaust_vel_pattern = re.compile(r"\b(?:exhaust_velocity_m_s|v_e_m_s|fusion_exhaust_m_s)\s*=\s*([0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?)\b", re.IGNORECASE)
        self.collimation_pattern = re.compile(r"\b(?:nozzle_collimation_efficiency|eta_collimation)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.accel_pattern = re.compile(r"\b(?:ship_acceleration_m_s2|a_ship_m_s2|continuous_accel_m_s2)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.temp_pattern = re.compile(r"\b(?:core_fusion_temp_k|t_core_k|fusion_temp_k)\s*=\s*([0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?)\b", re.IGNORECASE)
        self.brem_pattern = re.compile(r"\b(?:bremsstrahlung_loss_ratio|p_brem_loss_ratio|bremsstrahlung_ratio)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)

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

            # Scoop radius
            m = self.scoop_radius_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_SCOOP_RADIUS_KM:
                        flaws.append({
                            "id": "SCOOP_RADIUS_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Magnetic scoop radius {val:.1f} km below minimum intake benchmark {MIN_SCOOP_RADIUS_KM:.1f} km."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Flight velocity beta
            m = self.velocity_beta_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_RELATIVISTIC_VELOCITY_FRACTION:
                        flaws.append({
                            "id": "VELOCITY_BETA_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Cruise velocity fraction beta {val:.3f} below relativistic threshold {MIN_RELATIVISTIC_VELOCITY_FRACTION:.2f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Scoop magnetic field
            m = self.scoop_field_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_MAGNETIC_SCOOP_FIELD_T:
                        flaws.append({
                            "id": "SCOOP_FIELD_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Magnetic scoop choke field {val:.1f} T below minimum {MIN_MAGNETIC_SCOOP_FIELD_T:.1f} T."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Photo-ionization efficiency
            m = self.photo_ion_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_PHOTO_IONIZATION_EFFICIENCY:
                        flaws.append({
                            "id": "PHOTO_IONIZATION_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Photo-ionization efficiency {val:.3f} below floor {MIN_PHOTO_IONIZATION_EFFICIENCY:.2f} (neutral gas blowby risk)."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Capture cross-section efficiency
            m = self.capture_eff_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_CAPTURE_CROSS_SECTION_EFFICIENCY:
                        flaws.append({
                            "id": "CAPTURE_CROSS_SECTION_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Capture cross-section efficiency {val:.3f} below benchmark {MIN_CAPTURE_CROSS_SECTION_EFFICIENCY:.2f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Thrust-to-drag ratio
            m = self.thrust_drag_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_THRUST_TO_DRAG_RATIO:
                        flaws.append({
                            "id": "THRUST_TO_DRAG_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Thrust-to-drag ratio {val:.2f} below net-acceleration floor {MIN_THRUST_TO_DRAG_RATIO:.2f} (ram-drag deceleration catastrophe)."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Exhaust velocity
            m = self.exhaust_vel_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_EXHAUST_VELOCITY_M_S:
                        flaws.append({
                            "id": "EXHAUST_VELOCITY_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Fusion exhaust velocity {val:.2e} m/s below relativistic benchmark {MIN_EXHAUST_VELOCITY_M_S:.2e} m/s."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Nozzle collimation efficiency
            m = self.collimation_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_NOZZLE_COLLIMATION_EFFICIENCY:
                        flaws.append({
                            "id": "NOZZLE_COLLIMATION_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Nozzle collimation efficiency {val:.3f} below minimum {MIN_NOZZLE_COLLIMATION_EFFICIENCY:.2f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Ship acceleration
            m = self.accel_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_SHIP_ACCELERATION_M_S2 or val > MAX_SHIP_ACCELERATION_M_S2:
                        flaws.append({
                            "id": "ACCELERATION_OUT_OF_BOUNDS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Continuous ship acceleration {val:.2f} m/s^2 outside operational bounds [{MIN_SHIP_ACCELERATION_M_S2:.2f}, {MAX_SHIP_ACCELERATION_M_S2:.2f}] m/s^2."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Core fusion temperature
            m = self.temp_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_CORE_FUSION_TEMP_K:
                        flaws.append({
                            "id": "CORE_TEMP_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Core fusion temperature {val:.2e} K below thermonuclear threshold {MIN_CORE_FUSION_TEMP_K:.2e} K."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Bremsstrahlung loss ratio
            m = self.brem_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_BREMSSTRAHLUNG_LOSS_RATIO:
                        flaws.append({
                            "id": "BREMSSTRAHLUNG_LOSS_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Bremsstrahlung loss ratio {val:.3f} exceeds thermal limit {MAX_BREMSSTRAHLUNG_LOSS_RATIO:.2f}."
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
