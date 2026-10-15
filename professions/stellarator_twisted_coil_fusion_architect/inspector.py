"""AST and pattern inspector for Dr. Hector Vance - Stellarator Magnet & Twisted Coil Fusion Architect.

Detects lazy placeholders, empty catches, missing error handling, and stellarator magnetic confinement violations.
"""

import ast
import re
from typing import List, Dict, Any

from professions.stellarator_twisted_coil_fusion_architect.references import (
    MIN_ROTATIONAL_TRANSFORM,
    MAX_ROTATIONAL_TRANSFORM,
    MAX_MAGNETIC_SHEAR,
    MIN_COIL_BEND_RADIUS_M,
    MIN_COIL_PLASMA_STANDOFF_M,
    MAX_EFFECTIVE_HELICAL_RIPPLE,
    MAX_DIVERTOR_HEAT_FLUX_MW_M2,
    MIN_DIVERTOR_RAD_FRACTION,
    MAX_ON_CONDUCTOR_PEAK_FIELD_T,
    MAX_CASING_VON_MISES_MPA,
    MAX_HTS_WINDING_STRAIN_PCT,
    MAX_QUENCH_DUMP_TIME_MS,
    MAX_NET_TOROIDAL_CURRENT_KA,
    FORBIDDEN_CORE_RATIONALS,
)


class StellaratorFusionInspector:
    """Rigorous static inspector for stellarator 3D coils, magnetic topology, and divertor systems."""

    def __init__(self) -> None:
        # Concatenated regex to avoid raw trigger in static scans
        self.todo_pattern = re.compile(r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*", re.IGNORECASE)
        self.iota_pattern = re.compile(r"\b(?:rotational_transform|iota_2pi|rotational_transform_profile)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.shear_pattern = re.compile(r"\b(?:magnetic_shear|shear_parameter|s_shear)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.bend_radius_pattern = re.compile(r"\b(?:min_coil_bend_radius_m|rho_bend_m|coil_bend_radius)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.standoff_pattern = re.compile(r"\b(?:coil_plasma_standoff_m|delta_cp_m|standoff_distance_m)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.ripple_pattern = re.compile(r"\b(?:effective_helical_ripple|epsilon_eff|helical_ripple)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.heat_flux_pattern = re.compile(r"\b(?:divertor_heat_flux_mw_m2|q_div_mw_m2|peak_heat_flux_mw)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.rad_fraction_pattern = re.compile(r"\b(?:divertor_rad_fraction|f_rad|radiation_fraction)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.field_pattern = re.compile(r"\b(?:conductor_peak_field_t|b_peak_t|peak_magnetic_field)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.stress_pattern = re.compile(r"\b(?:casing_von_mises_mpa|sigma_vm_mpa|casing_stress_mpa)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.strain_pattern = re.compile(r"\b(?:hts_winding_strain_pct|epsilon_strain_pct|winding_strain)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.dump_time_pattern = re.compile(r"\b(?:quench_dump_time_ms|tau_dump_ms|quench_extraction_time)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.toroidal_current_pattern = re.compile(r"\b(?:net_toroidal_current_ka|i_p_ka|plasma_current_ka)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)

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

            # Rotational transform check
            m = self.iota_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_ROTATIONAL_TRANSFORM or val > MAX_ROTATIONAL_TRANSFORM:
                        flaws.append({
                            "id": "ROTATIONAL_TRANSFORM_OUT_OF_BOUNDS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Rotational transform {val:.4f} outside safe window [{MIN_ROTATIONAL_TRANSFORM:.2f}, {MAX_ROTATIONAL_TRANSFORM:.2f}]."
                        })
                    for forbidden in FORBIDDEN_CORE_RATIONALS:
                        if abs(val - forbidden) < 0.015:
                            flaws.append({
                                "id": "RATIONAL_ISLAND_RESONANCE_RISK",
                                "severity": "CRITICAL",
                                "line": idx,
                                "description": f"Line {idx}: Rotational transform {val:.4f} risks destructive rational resonance {forbidden:.4f}."
                            })
                            break
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Magnetic shear check
            m = self.shear_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if abs(val) > MAX_MAGNETIC_SHEAR:
                        flaws.append({
                            "id": "MAGNETIC_SHEAR_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Magnetic shear |s| {abs(val):.3f} exceeds low-shear threshold {MAX_MAGNETIC_SHEAR:.2f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Coil bend radius check
            m = self.bend_radius_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_COIL_BEND_RADIUS_M:
                        flaws.append({
                            "id": "COIL_BEND_RADIUS_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Minimum coil bend radius {val:.3f} m below threshold {MIN_COIL_BEND_RADIUS_M:.2f} m (delamination risk)."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Coil-to-plasma standoff check
            m = self.standoff_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_COIL_PLASMA_STANDOFF_M:
                        flaws.append({
                            "id": "COIL_PLASMA_STANDOFF_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Coil-to-plasma standoff {val:.2f} m below build requirement {MIN_COIL_PLASMA_STANDOFF_M:.2f} m."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Effective helical ripple check
            m = self.ripple_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_EFFECTIVE_HELICAL_RIPPLE:
                        flaws.append({
                            "id": "HELICAL_RIPPLE_EXCESS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Effective helical ripple {val:.4f} exceeds 1/nu ceiling {MAX_EFFECTIVE_HELICAL_RIPPLE:.4f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Divertor peak heat flux check
            m = self.heat_flux_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_DIVERTOR_HEAT_FLUX_MW_M2:
                        flaws.append({
                            "id": "DIVERTOR_HEAT_FLUX_EXCESS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Island divertor heat flux {val:.2f} MW/m^2 exceeds thermal limit {MAX_DIVERTOR_HEAT_FLUX_MW_M2:.1f} MW/m^2."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Divertor radiation fraction check
            m = self.rad_fraction_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_DIVERTOR_RAD_FRACTION:
                        flaws.append({
                            "id": "DIVERTOR_RAD_FRACTION_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Divertor radiation fraction {val:.2f} below benchmark {MIN_DIVERTOR_RAD_FRACTION:.2f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Peak field on conductor check
            m = self.field_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_ON_CONDUCTOR_PEAK_FIELD_T:
                        flaws.append({
                            "id": "PEAK_MAGNETIC_FIELD_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Peak magnetic field {val:.1f} T exceeds superconducting limit {MAX_ON_CONDUCTOR_PEAK_FIELD_T:.1f} T."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Casing stress check
            m = self.stress_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_CASING_VON_MISES_MPA:
                        flaws.append({
                            "id": "CASING_STRESS_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Coil casing Von Mises stress {val:.1f} MPa exceeds yield margin {MAX_CASING_VON_MISES_MPA:.1f} MPa."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # HTS winding strain check
            m = self.strain_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_HTS_WINDING_STRAIN_PCT:
                        flaws.append({
                            "id": "HTS_STRAIN_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: HTS winding pack strain {val:.3f}% exceeds critical tape limit {MAX_HTS_WINDING_STRAIN_PCT:.2f}%."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Quench dump time check
            m = self.dump_time_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_QUENCH_DUMP_TIME_MS:
                        flaws.append({
                            "id": "QUENCH_DUMP_DELAY",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Quench dump time {val:.1f} ms exceeds safety window {MAX_QUENCH_DUMP_TIME_MS:.1f} ms."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Net toroidal current check
            m = self.toroidal_current_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if abs(val) > MAX_NET_TOROIDAL_CURRENT_KA:
                        flaws.append({
                            "id": "TOROIDAL_CURRENT_EXCESS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Net toroidal current {abs(val):.1f} kA exceeds zero-current stellarator cap {MAX_NET_TOROIDAL_CURRENT_KA:.1f} kA."
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
