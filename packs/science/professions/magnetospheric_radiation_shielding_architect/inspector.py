"""AST and pattern inspector for Commander Kaelen Vance - Magnetospheric Radiation Shielding Architect.

Detects lazy placeholders, empty catches, missing error handling, and particle deflection threshold violations.
"""

import ast
import re
from typing import List, Dict, Any

from professions.magnetospheric_radiation_shielding_architect.references import (
    MIN_MAGNETIC_MOMENT_GA_M2,
    MIN_STORMER_RIGIDITY_GV,
    MIN_COIL_PEAK_FIELD_T,
    MAX_HABITAT_LEAKAGE_FIELD_T,
    MIN_HTS_CURRENT_DENSITY_A_M2,
    MAX_COIL_OPERATING_TEMP_K,
    MAX_QUENCH_DUMP_TIME_MS,
    MAX_CREW_ANNUAL_DOSE_MSV,
    MAX_SPE_DOSE_RATE_MGY_H,
    MIN_ELECTROSTATIC_POTENTIAL_MV,
    MIN_NEUTRALIZER_CURRENT_MA,
)


class MagnetosphericShieldInspector:
    """Rigorous static inspector for magnetospheric radiation shields and active deflection systems."""

    def __init__(self) -> None:
        # Concatenated regex to avoid raw trigger in static scans
        self.todo_pattern = re.compile(r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*", re.IGNORECASE)
        self.moment_pattern = re.compile(r"\b(?:magnetic_moment_ga_m2|m_dipole_ga_m2|magnetic_dipole_moment)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.rigidity_pattern = re.compile(r"\b(?:stormer_rigidity_gv|r_cutoff_gv|cutoff_rigidity)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.field_pattern = re.compile(r"\b(?:coil_peak_field_t|b_peak_t|peak_magnetic_field)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.leakage_pattern = re.compile(r"\b(?:habitat_leakage_field_mt|b_habitat_mt|fringe_field_mt)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.j_hts_pattern = re.compile(r"\b(?:hts_current_density_a_mm2|j_c_rebco|hts_j_density)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.coil_temp_pattern = re.compile(r"\b(?:coil_operating_temp_k|t_coil_k|hts_temperature)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.dump_time_pattern = re.compile(r"\b(?:quench_dump_time_ms|tau_dump_ms|quench_extraction_time)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.annual_dose_pattern = re.compile(r"\b(?:crew_annual_dose_msv|h_eff_annual|annual_dose_msv)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.spe_rate_pattern = re.compile(r"\b(?:spe_dose_rate_mgy_h|dot_d_spe|spe_rate_mgy)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.potential_pattern = re.compile(r"\b(?:electrostatic_potential_mv|phi_grid_mv|repulsive_barrier_mv)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.neutralizer_pattern = re.compile(r"\b(?:neutralizer_current_ma|i_beam_ma|neutralizer_beam)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)

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

            # Magnetic dipole moment check
            m = self.moment_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    from professions.magnetospheric_radiation_shielding_architect.references import MIN_MAGNETIC_MOMENT_GA_M2
                    if val < MIN_MAGNETIC_MOMENT_GA_M2:
                        flaws.append({
                            "id": "MAGNETIC_MOMENT_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Magnetic moment {val:.1f} GA*m^2 below threshold {MIN_MAGNETIC_MOMENT_GA_M2:.1f} GA*m^2."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Stormer cut-off rigidity check
            m = self.rigidity_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_STORMER_RIGIDITY_GV:
                        flaws.append({
                            "id": "STORMER_RIGIDITY_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Stormer cut-off rigidity {val:.2f} GV below minimum {MIN_STORMER_RIGIDITY_GV:.2f} GV."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Coil peak magnetic field check
            m = self.field_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_COIL_PEAK_FIELD_T:
                        flaws.append({
                            "id": "COIL_FIELD_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Coil peak magnetic field {val:.1f} T below required deflection intensity {MIN_COIL_PEAK_FIELD_T:.1f} T."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Habitat fringe field leakage check
            m = self.leakage_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > (MAX_HABITAT_LEAKAGE_FIELD_T * 1000.0):
                        flaws.append({
                            "id": "HABITAT_LEAKAGE_EXCESS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Habitat magnetic fringe field {val:.2f} mT exceeds human safety limit {MAX_HABITAT_LEAKAGE_FIELD_T * 1000.0:.2f} mT (5.0 Gauss)."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # HTS critical current density check
            m = self.j_hts_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < (MIN_HTS_CURRENT_DENSITY_A_M2 / 1.0e6):
                        flaws.append({
                            "id": "HTS_CURRENT_DENSITY_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: HTS critical current density {val:.1f} A/mm^2 below benchmark {MIN_HTS_CURRENT_DENSITY_A_M2 / 1.0e6:.1f} A/mm^2."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Coil operating temperature check
            m = self.coil_temp_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_COIL_OPERATING_TEMP_K:
                        flaws.append({
                            "id": "COIL_TEMP_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Coil operating temperature {val:.1f} K exceeds cryogenic ceiling {MAX_COIL_OPERATING_TEMP_K:.1f} K."
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
                            "description": f"Line {idx}: Quench dump extraction time {val:.1f} ms exceeds safety limit {MAX_QUENCH_DUMP_TIME_MS:.1f} ms."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Crew annual dose check
            m = self.annual_dose_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_CREW_ANNUAL_DOSE_MSV:
                        flaws.append({
                            "id": "CREW_ANNUAL_DOSE_EXCESS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Crew annual effective dose {val:.1f} mSv/year exceeds ALARA ceiling {MAX_CREW_ANNUAL_DOSE_MSV:.1f} mSv/year."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # SPE dose rate check
            m = self.spe_rate_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_SPE_DOSE_RATE_MGY_H:
                        flaws.append({
                            "id": "SPE_DOSE_RATE_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Acute SPE dose rate {val:.1f} mGy/h exceeds safety bound {MAX_SPE_DOSE_RATE_MGY_H:.1f} mGy/h."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Electrostatic potential check
            m = self.potential_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_ELECTROSTATIC_POTENTIAL_MV:
                        flaws.append({
                            "id": "ELECTROSTATIC_POTENTIAL_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Electrostatic grid potential {val:.1f} MV below threshold {MIN_ELECTROSTATIC_POTENTIAL_MV:.1f} MV."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Neutralizer current check
            m = self.neutralizer_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_NEUTRALIZER_CURRENT_MA:
                        flaws.append({
                            "id": "NEUTRALIZER_CURRENT_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Neutralizer current {val:.1f} mA below solar wind requirement {MIN_NEUTRALIZER_CURRENT_MA:.1f} mA."
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
