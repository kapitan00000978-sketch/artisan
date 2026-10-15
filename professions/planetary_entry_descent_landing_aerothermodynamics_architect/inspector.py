"""Planetary Atmospheric Entry, Descent & Landing (EDL) Code Inspector.

Audits AST syntax and numerical parameters against Dr. Caelum Sterling's
planetary EDL aerothermodynamics invariants and touchdown safety envelopes.
"""

import ast
import re
from typing import Any, Dict, List, Optional


class EDLAerothermodynamicsInspector:
    """Audits Python source code for EDL trajectory defects and amateur software stubs."""

    def __init__(self) -> None:
        self.todo_pattern = re.compile(
            r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*",
            re.IGNORECASE
        )
        self.param_patterns: Dict[str, re.Pattern] = {
            "entry_velocity_km_s": re.compile(
                r"\b(entry_velocity_km_s|v_entry|entry_speed)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "stagnation_heat_flux_mw_m2": re.compile(
                r"\b(stagnation_heat_flux_mw_m2|q_stag|heat_flux_mw)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "total_heat_load_mj_m2": re.compile(
                r"\b(total_heat_load_mj_m2|q_total|total_heat_load)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "tps_safety_factor": re.compile(
                r"\b(tps_safety_factor|sf_tps)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "bondline_temp_c": re.compile(
                r"\b(bondline_temp_c|t_bond|bond_temp)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "peak_deceleration_g": re.compile(
                r"\b(peak_deceleration_g|g_load|max_deceleration)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "parachute_deploy_mach": re.compile(
                r"\b(parachute_deploy_mach|m_deploy|chute_mach)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "parachute_dynamic_pressure_pa": re.compile(
                r"\b(parachute_dynamic_pressure_pa|q_deploy|chute_q)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "landing_ellipse_semi_major_m": re.compile(
                r"\b(landing_ellipse_semi_major_m|landing_ellipse|delta_r_landing)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "touchdown_vz_m_s": re.compile(
                r"\b(touchdown_vz_m_s|v_touchdown|touchdown_speed)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
        }

    def inspect_code(self, source_code: str) -> Dict[str, Any]:
        """Perform comprehensive AST and regex inspection on Python source code."""
        findings: List[str] = []
        parsed_params: Dict[str, float] = {}

        # 1. Regex check for lazy placeholder comments
        for line_num, line in enumerate(source_code.splitlines(), start=1):
            if self.todo_pattern.search(line):
                findings.append(f"Line {line_num}: Unfinished placeholder comment detected.")

        # 2. Regex parameter scanning
        for param_key, pattern in self.param_patterns.items():
            match = pattern.search(source_code)
            if match:
                try:
                    val = float(match.group(2))
                    parsed_params[param_key] = val
                except (ValueError, IndexError):
                    findings.append(f"Invalid numeric format for parameter '{param_key}'.")

        # 3. AST semantic checks
        try:
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                # Detect empty except blocks
                if isinstance(node, ast.ExceptHandler):
                    if not node.body or all(isinstance(stmt, ast.Pass) for stmt in node.body):
                        findings.append(
                            f"Line {getattr(node, 'lineno', '?')}: Silent exception suppression (empty catch)."
                        )
                # Detect pass-only function stubs
                elif isinstance(node, ast.FunctionDef):
                    if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                        findings.append(
                            f"Line {node.lineno}: Function '{node.name}' is an empty pass stub."
                        )
        except SyntaxError as err:
            findings.append(f"Syntax error during AST inspection: {err}")

        # 4. Check extracted numerical parameters against physical invariants
        if "entry_velocity_km_s" in parsed_params:
            v_entry = parsed_params["entry_velocity_km_s"]
            if v_entry < 5.5 or v_entry > 12.5:
                findings.append(
                    f"Entry Velocity {v_entry} km/s outside certified planetary envelope [5.5, 12.5] km/s."
                )
        if "stagnation_heat_flux_mw_m2" in parsed_params and parsed_params["stagnation_heat_flux_mw_m2"] < 4.50:
            findings.append(
                f"Stagnation Heat Flux {parsed_params['stagnation_heat_flux_mw_m2']} MW/m^2 < 4.50 MW/m^2: Underestimating shock heating."
            )
        if "total_heat_load_mj_m2" in parsed_params and parsed_params["total_heat_load_mj_m2"] < 120.0:
            findings.append(
                f"Total Heat Load {parsed_params['total_heat_load_mj_m2']} MJ/m^2 < 120.0 MJ/m^2: Integrated pulse too low."
            )
        if "tps_safety_factor" in parsed_params and parsed_params["tps_safety_factor"] < 1.50:
            findings.append(
                f"TPS Safety Factor {parsed_params['tps_safety_factor']} < 1.50: Heatshield safety margin breached."
            )
        if "bondline_temp_c" in parsed_params and parsed_params["bondline_temp_c"] > 250.0:
            findings.append(
                f"Bondline Temperature {parsed_params['bondline_temp_c']} C > 250.0 C: Risk of structural bondline failure."
            )
        if "peak_deceleration_g" in parsed_params and parsed_params["peak_deceleration_g"] > 15.0:
            findings.append(
                f"Peak Deceleration {parsed_params['peak_deceleration_g']} g > 15.0 g: G-load exceeds capsule ceiling."
            )
        if "parachute_deploy_mach" in parsed_params:
            m_dep = parsed_params["parachute_deploy_mach"]
            if m_dep < 1.40 or m_dep > 2.20:
                findings.append(
                    f"Parachute Deploy Mach {m_dep} outside certified window [1.40, 2.20]."
                )
        if "parachute_dynamic_pressure_pa" in parsed_params:
            q_dep = parsed_params["parachute_dynamic_pressure_pa"]
            if q_dep < 300.0 or q_dep > 950.0:
                findings.append(
                    f"Parachute Dynamic Pressure {q_dep} Pa outside certified limits [300.0, 950.0] Pa."
                )
        if "landing_ellipse_semi_major_m" in parsed_params and parsed_params["landing_ellipse_semi_major_m"] > 50.0:
            findings.append(
                f"Landing Ellipse {parsed_params['landing_ellipse_semi_major_m']} m > 50.0 m: Fails pinpoint landing standard."
            )
        if "touchdown_vz_m_s" in parsed_params and parsed_params["touchdown_vz_m_s"] > 0.75:
            findings.append(
                f"Touchdown Velocity {parsed_params['touchdown_vz_m_s']} m/s > 0.75 m/s: Hard landing risks gear collapse."
            )

        return {
            "findings": findings,
            "parsed_parameters": parsed_params,
            "has_defects": len(findings) > 0,
        }
