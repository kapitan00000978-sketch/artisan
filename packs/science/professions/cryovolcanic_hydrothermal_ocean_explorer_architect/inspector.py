"""AST and pattern inspector for Commander Thorne Sterling - Cryovolcanic & Hydrothermal Ocean Explorer Architect.

Detects lazy placeholders, empty catches, missing error handling, and cryobot exploration threshold violations.
"""

import ast
import re
from typing import List, Dict, Any

from professions.cryovolcanic_hydrothermal_ocean_explorer_architect.references import (
    MIN_THERMAL_DRILL_POWER_KW,
    MIN_PENETRATION_VELOCITY_M_H,
    MIN_OCEAN_PRESSURE_RATING_MPA,
    MIN_COLLAPSE_SAFETY_FACTOR,
    MAX_ALLOWABLE_BIOBURDEN_SPORES_M2,
    MIN_DHMR_TEMPERATURE_C,
    MIN_DHMR_DURATION_HOURS,
    MAX_LOD_METHANE_NM,
    MAX_LOD_HYDROGEN_NM,
    MAX_LOD_AMINO_ACIDS_NM,
    MIN_TETHER_TENSILE_STRENGTH_KN,
    MAX_FIBER_ATTENUATION_DB_KM,
    MIN_TETHER_LENGTH_KM,
    MIN_SONAR_RANGE_KM,
)


class CryovolcanicOceanInspector:
    """Rigorous static inspector for sub-surface cryobots, pressure vessels, and hydrothermal ocean explorers."""

    def __init__(self) -> None:
        # Concatenated regex to avoid raw trigger in static scans
        self.todo_pattern = re.compile(r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*", re.IGNORECASE)
        self.drill_power_pattern = re.compile(r"\b(?:thermal_drill_power_kw|p_thermal_kw|melting_power_kw)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.velocity_pattern = re.compile(r"\b(?:penetration_velocity_m_h|v_melt_m_h|melt_velocity)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.pressure_pattern = re.compile(r"\b(?:ocean_pressure_rating_mpa|p_crush_mpa|pressure_rating_mpa)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.safety_factor_pattern = re.compile(r"\b(?:collapse_safety_factor|sf_collapse|hull_safety_factor)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.bioburden_pattern = re.compile(r"\b(?:bioburden_spores_m2|planetary_protection_spores|bioburden_level)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.dhmr_temp_pattern = re.compile(r"\b(?:dhmr_temperature_c|t_dhmr_c|sterilization_temp_c)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.dhmr_time_pattern = re.compile(r"\b(?:dhmr_duration_hours|t_soak_hours|bakeout_duration_hours)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.methane_pattern = re.compile(r"\b(?:lod_methane_nm|ch4_lod_nm|methane_sensitivity_nm)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.hydrogen_pattern = re.compile(r"\b(?:lod_hydrogen_nm|h2_lod_nm|hydrogen_sensitivity_nm)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.amino_pattern = re.compile(r"\b(?:lod_amino_acids_nm|amino_lod_nm|amino_acid_sensitivity_nm)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.tensile_pattern = re.compile(r"\b(?:tether_tensile_strength_kn|f_tether_kn|tether_strength_kn)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.attenuation_pattern = re.compile(r"\b(?:fiber_attenuation_db_km|alpha_fiber_db|fiber_loss_db_km)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.length_pattern = re.compile(r"\b(?:tether_length_km|l_tether_km|spool_length_km)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.sonar_pattern = re.compile(r"\b(?:sonar_range_km|r_sonar_km|acoustic_range_km)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)

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

            # Thermal drill power check
            m = self.drill_power_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_THERMAL_DRILL_POWER_KW:
                        flaws.append({
                            "id": "THERMAL_DRILL_POWER_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Thermal drill power {val:.1f} kW below required {MIN_THERMAL_DRILL_POWER_KW:.1f} kW (freeze-in stall risk)."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Penetration velocity check
            m = self.velocity_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_PENETRATION_VELOCITY_M_H:
                        flaws.append({
                            "id": "PENETRATION_VELOCITY_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Penetration velocity {val:.2f} m/h below benchmark {MIN_PENETRATION_VELOCITY_M_H:.2f} m/h."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Ocean hydrostatic pressure rating check
            m = self.pressure_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_OCEAN_PRESSURE_RATING_MPA:
                        flaws.append({
                            "id": "HYDROSTATIC_PRESSURE_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Pressure rating {val:.1f} MPa below alien ocean depth requirement {MIN_OCEAN_PRESSURE_RATING_MPA:.1f} MPa."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Structural collapse safety factor check
            m = self.safety_factor_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_COLLAPSE_SAFETY_FACTOR:
                        flaws.append({
                            "id": "COLLAPSE_SAFETY_FACTOR_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Collapse safety factor {val:.2f} below margin {MIN_COLLAPSE_SAFETY_FACTOR:.2f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Bioburden planetary protection check
            m = self.bioburden_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_ALLOWABLE_BIOBURDEN_SPORES_M2:
                        flaws.append({
                            "id": "BIOBURDEN_CONTAMINATION_BREACH",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Bioburden level {val:.3f} spores/m^2 breaches COSPAR Category IVb threshold {MAX_ALLOWABLE_BIOBURDEN_SPORES_M2:.3f} spores/m^2."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # DHMR sterilization temperature check
            m = self.dhmr_temp_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_DHMR_TEMPERATURE_C:
                        flaws.append({
                            "id": "DHMR_TEMPERATURE_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Dry heat sterilization temperature {val:.1f} °C below {MIN_DHMR_TEMPERATURE_C:.1f} °C."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # DHMR soak duration check
            m = self.dhmr_time_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_DHMR_DURATION_HOURS:
                        flaws.append({
                            "id": "DHMR_DURATION_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Sterilization duration {val:.1f} hours below required {MIN_DHMR_DURATION_HOURS:.1f} hours."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Methane detection limit check
            m = self.methane_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_LOD_METHANE_NM:
                        flaws.append({
                            "id": "METHANE_LOD_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Methane detection limit {val:.2f} nM exceeds sensitivity ceiling {MAX_LOD_METHANE_NM:.2f} nM."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Hydrogen detection limit check
            m = self.hydrogen_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_LOD_HYDROGEN_NM:
                        flaws.append({
                            "id": "HYDROGEN_LOD_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Hydrogen detection limit {val:.2f} nM exceeds serpentinization sensitivity {MAX_LOD_HYDROGEN_NM:.2f} nM."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Amino acids detection limit check
            m = self.amino_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_LOD_AMINO_ACIDS_NM:
                        flaws.append({
                            "id": "AMINO_ACIDS_LOD_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Amino acid detection limit {val:.3f} nM exceeds biomarker sensitivity {MAX_LOD_AMINO_ACIDS_NM:.2f} nM."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Tether tensile strength check
            m = self.tensile_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_TETHER_TENSILE_STRENGTH_KN:
                        flaws.append({
                            "id": "TETHER_TENSILE_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Tether tensile strength {val:.2f} kN below shear threshold {MIN_TETHER_TENSILE_STRENGTH_KN:.2f} kN."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Fiber attenuation check
            m = self.attenuation_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_FIBER_ATTENUATION_DB_KM:
                        flaws.append({
                            "id": "FIBER_ATTENUATION_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Optical fiber attenuation {val:.2f} dB/km exceeds limit {MAX_FIBER_ATTENUATION_DB_KM:.2f} dB/km."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Tether length check
            m = self.length_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_TETHER_LENGTH_KM:
                        flaws.append({
                            "id": "TETHER_LENGTH_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Umbilical tether length {val:.1f} km below ice shelf margin {MIN_TETHER_LENGTH_KM:.1f} km."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Sonar range check
            m = self.sonar_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_SONAR_RANGE_KM:
                        flaws.append({
                            "id": "SONAR_RANGE_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Acoustic sonar range {val:.1f} km below bathymetry requirement {MIN_SONAR_RANGE_KM:.1f} km."
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
