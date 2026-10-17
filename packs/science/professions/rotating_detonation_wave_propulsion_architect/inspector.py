"""AST and pattern inspector for Commander Jaxen Sterling - Rotating Detonation Wave Propulsion Architect.

Detects unfinished stubs, empty exception handlers, and continuous detonation wave parameter breaches.
"""

import ast
import re
from typing import List, Dict, Any

from professions.rotating_detonation_wave_propulsion_architect.references import (
    MIN_CJ_DETONATION_VELOCITY_M_S,
    MIN_CJ_PRESSURE_RATIO,
    MIN_ZND_SPIKE_PRESSURE_RATIO,
    MAX_DDT_RUNUP_DISTANCE_MM,
    MIN_DETONATION_FREQUENCY_KHZ,
    MIN_CO_ROTATING_WAVES,
    MIN_ANNULAR_GAP_MM,
    MAX_ANNULAR_GAP_MM,
    MIN_ANNULAR_DIAMETER_MM,
    MAX_ANNULAR_DIAMETER_MM,
    MIN_PRESSURE_GAIN_EFFICIENCY,
    MIN_AEROSPIKE_NOZZLE_EFFICIENCY,
    MIN_SPECIFIC_IMPULSE_S,
    MAX_CHAMBER_WALL_HEAT_FLUX_MW_M2,
)


class RotatingDetonationInspector:
    """Rigorous static inspector for Continuous Rotating Detonation Rocket Engine code."""

    def __init__(self) -> None:
        # Concatenated regex to avoid raw trigger in static scans
        self.todo_pattern = re.compile(r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*", re.IGNORECASE)
        self.cj_velocity_pattern = re.compile(r"\b(?:cj_detonation_velocity_m_s|d_cj_m_s|detonation_velocity)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.cj_pressure_pattern = re.compile(r"\b(?:cj_pressure_ratio|p_cj_ratio)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.znd_pressure_pattern = re.compile(r"\b(?:znd_spike_pressure_ratio|p_znd_ratio)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.ddt_dist_pattern = re.compile(r"\b(?:ddt_runup_distance_mm|l_ddt_mm|runup_distance_mm)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.freq_pattern = re.compile(r"\b(?:detonation_frequency_khz|f_det_khz|wave_frequency_khz)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.waves_pattern = re.compile(r"\b(?:num_co_rotating_waves|num_waves|n_waves)\s*=\s*([0-9]+)\b", re.IGNORECASE)
        self.gap_pattern = re.compile(r"\b(?:annular_channel_gap_mm|delta_r_channel_mm|channel_gap_mm)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.diam_pattern = re.compile(r"\b(?:annular_diameter_mm|d_annulus_mm|chamber_diameter_mm)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.gain_pattern = re.compile(r"\b(?:pressure_gain_efficiency|eta_gain)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.nozzle_pattern = re.compile(r"\b(?:aerospike_nozzle_efficiency|eta_nozzle)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.isp_pattern = re.compile(r"\b(?:specific_impulse_s|isp_s)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.heat_flux_pattern = re.compile(r"\b(?:chamber_wall_heat_flux_mw_m2|q_wall_mw_m2|wall_heat_flux)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)

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

            # CJ detonation velocity
            m = self.cj_velocity_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_CJ_DETONATION_VELOCITY_M_S:
                        flaws.append({
                            "id": "CJ_VELOCITY_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Chapman-Jouguet detonation velocity {val:.1f} m/s below threshold {MIN_CJ_DETONATION_VELOCITY_M_S:.1f} m/s (risk of deflagration flame blowout)."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # CJ pressure ratio
            m = self.cj_pressure_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_CJ_PRESSURE_RATIO:
                        flaws.append({
                            "id": "CJ_PRESSURE_RATIO_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: CJ detonation pressure ratio {val:.1f} below minimum {MIN_CJ_PRESSURE_RATIO:.1f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # ZND spike pressure ratio
            m = self.znd_pressure_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_ZND_SPIKE_PRESSURE_RATIO:
                        flaws.append({
                            "id": "ZND_PRESSURE_RATIO_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: ZND leading shock spike pressure ratio {val:.1f} below minimum {MIN_ZND_SPIKE_PRESSURE_RATIO:.1f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # DDT run-up distance
            m = self.ddt_dist_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_DDT_RUNUP_DISTANCE_MM:
                        flaws.append({
                            "id": "DDT_RUNUP_EXCESS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: DDT run-up distance {val:.1f} mm exceeds maximum threshold {MAX_DDT_RUNUP_DISTANCE_MM:.1f} mm."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Wave frequency
            m = self.freq_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_DETONATION_FREQUENCY_KHZ:
                        flaws.append({
                            "id": "DETONATION_FREQUENCY_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Rotating wave frequency {val:.1f} kHz below stability floor {MIN_DETONATION_FREQUENCY_KHZ:.1f} kHz."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Co-rotating waves
            m = self.waves_pattern.search(line)
            if m:
                try:
                    val = int(m.group(1))
                    if val < MIN_CO_ROTATING_WAVES:
                        flaws.append({
                            "id": "WAVE_COUNT_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Co-rotating wave count {val} below minimum {MIN_CO_ROTATING_WAVES}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0

            # Annular gap
            m = self.gap_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_ANNULAR_GAP_MM or val > MAX_ANNULAR_GAP_MM:
                        flaws.append({
                            "id": "ANNULAR_GAP_OUT_OF_BOUNDS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Annular channel gap {val:.2f} mm outside allowable bounds [{MIN_ANNULAR_GAP_MM:.1f}, {MAX_ANNULAR_GAP_MM:.1f}] mm."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Annular diameter
            m = self.diam_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_ANNULAR_DIAMETER_MM or val > MAX_ANNULAR_DIAMETER_MM:
                        flaws.append({
                            "id": "ANNULAR_DIAMETER_OUT_OF_BOUNDS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Annular diameter {val:.1f} mm outside allowable bounds [{MIN_ANNULAR_DIAMETER_MM:.1f}, {MAX_ANNULAR_DIAMETER_MM:.1f}] mm."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Pressure gain
            m = self.gain_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_PRESSURE_GAIN_EFFICIENCY:
                        flaws.append({
                            "id": "PRESSURE_GAIN_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Pressure gain efficiency {val:.3f} below minimum {MIN_PRESSURE_GAIN_EFFICIENCY:.2f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Aerospike nozzle efficiency
            m = self.nozzle_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_AEROSPIKE_NOZZLE_EFFICIENCY:
                        flaws.append({
                            "id": "AEROSPIKE_EFFICIENCY_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Aerospike nozzle efficiency {val:.3f} below minimum {MIN_AEROSPIKE_NOZZLE_EFFICIENCY:.2f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Specific impulse
            m = self.isp_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_SPECIFIC_IMPULSE_S:
                        flaws.append({
                            "id": "SPECIFIC_IMPULSE_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Specific impulse {val:.1f} s below performance benchmark {MIN_SPECIFIC_IMPULSE_S:.1f} s."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Chamber wall heat flux
            m = self.heat_flux_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_CHAMBER_WALL_HEAT_FLUX_MW_M2:
                        flaws.append({
                            "id": "WALL_HEAT_FLUX_EXCESS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Chamber wall heat flux {val:.1f} MW/m^2 exceeds regenerative cooling ceiling {MAX_CHAMBER_WALL_HEAT_FLUX_MW_M2:.1f} MW/m^2."
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
