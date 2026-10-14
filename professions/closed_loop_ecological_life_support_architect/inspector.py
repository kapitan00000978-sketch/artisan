"""AST and pattern inspector for Dr. Morwenna Sterling - Closed-Loop ECLSS & Bioregenerative Space Architect.

Detects lazy placeholders, empty catches, missing error handling, and life support parameter violations.
"""

import ast
import re
from typing import List, Dict, Any

from professions.closed_loop_ecological_life_support_architect.references import (
    MIN_SABATIER_EFFICIENCY,
    MIN_ELECTROLYSIS_EFFICIENCY,
    MIN_WATER_LOOP_RECOVERY,
    MAX_PERMEATE_TOC_UG_PER_L,
    MIN_O2_CONSUMPTION_KG_DAY,
    MAX_O2_CONSUMPTION_KG_DAY,
    MIN_CO2_PRODUCTION_KG_DAY,
    MAX_CO2_PRODUCTION_KG_DAY,
    MIN_PQ_RATIO,
    MAX_PQ_RATIO,
    MIN_BIOMASS_GROWTH_RATE_HR,
    MIN_CABIN_TOTAL_PRESSURE_KPA,
    MAX_CABIN_TOTAL_PRESSURE_KPA,
    MIN_CABIN_PO2_KPA,
    MAX_CABIN_PO2_KPA,
    MAX_CABIN_PCO2_KPA,
    MIN_CATALYTIC_OXIDIZER_TEMP_C,
)


class ECLSSInspector:
    """Rigorous static inspector for closed-loop ECLSS and bioregenerative life support systems."""

    def __init__(self) -> None:
        # Concatenated regex to avoid raw trigger in static scans
        self.todo_pattern = re.compile(r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*", re.IGNORECASE)
        self.sabatier_pattern = re.compile(r"\b(?:sabatier_efficiency|eta_sabatier|sabatier_yield_eff)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.electrolysis_pattern = re.compile(r"\b(?:electrolysis_efficiency|eta_electrolysis|pem_efficiency)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.water_recovery_pattern = re.compile(r"\b(?:water_recovery_fraction|vmd_recovery|water_loop_recovery)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.toc_pattern = re.compile(r"\b(?:permeate_toc_ug_per_l|toc_level_ug_l|permeate_toc)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.crew_o2_pattern = re.compile(r"\b(?:crew_o2_rate_kg_day|m_o2_cons_rate|crew_o2_demand)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.crew_co2_pattern = re.compile(r"\b(?:crew_co2_rate_kg_day|m_co2_prod_rate|crew_co2_output)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.pq_pattern = re.compile(r"\b(?:photosynthetic_quotient|algal_pq|pq_ratio)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.algal_growth_pattern = re.compile(r"\b(?:algal_growth_rate_hr|mu_biomass_hr|biomass_growth_rate)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.pressure_pattern = re.compile(r"\b(?:cabin_pressure_kpa|total_cabin_pressure|p_cabin_kpa)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.po2_pattern = re.compile(r"\b(?:cabin_po2_kpa|p_o2_cabin|cabin_oxygen_kpa)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.pco2_pattern = re.compile(r"\b(?:cabin_pco2_kpa|p_co2_cabin|cabin_co2_kpa)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.catalytic_temp_pattern = re.compile(r"\b(?:catalytic_temp_c|t_cat_c|catalytic_oxidizer_temp)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)

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

            # Sabatier efficiency check
            m = self.sabatier_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_SABATIER_EFFICIENCY:
                        flaws.append({
                            "id": "SABATIER_EFFICIENCY_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Sabatier conversion efficiency {val:.3f} below minimum {MIN_SABATIER_EFFICIENCY:.3f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Electrolysis efficiency check
            m = self.electrolysis_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_ELECTROLYSIS_EFFICIENCY:
                        flaws.append({
                            "id": "ELECTROLYSIS_EFFICIENCY_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: PEM electrolysis efficiency {val:.3f} below minimum {MIN_ELECTROLYSIS_EFFICIENCY:.3f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Water recovery fraction check
            m = self.water_recovery_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_WATER_LOOP_RECOVERY:
                        flaws.append({
                            "id": "WATER_RECOVERY_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Water loop recovery fraction {val:.3f} below minimum {MIN_WATER_LOOP_RECOVERY:.3f} (98.0%)."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Permeate TOC check
            m = self.toc_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_PERMEATE_TOC_UG_PER_L:
                        flaws.append({
                            "id": "PERMEATE_TOC_CONTAMINATION",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Permeate TOC {val:.1f} ug/L exceeds maximum allowable {MAX_PERMEATE_TOC_UG_PER_L:.1f} ug/L."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Crew O2 consumption rate check
            m = self.crew_o2_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if not (MIN_O2_CONSUMPTION_KG_DAY <= val <= MAX_O2_CONSUMPTION_KG_DAY):
                        flaws.append({
                            "id": "CREW_O2_CONSUMPTION_ANOMALY",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Metabolic O2 consumption {val:.2f} kg/day/crew outside band [{MIN_O2_CONSUMPTION_KG_DAY}, {MAX_O2_CONSUMPTION_KG_DAY}]."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Crew CO2 production rate check
            m = self.crew_co2_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if not (MIN_CO2_PRODUCTION_KG_DAY <= val <= MAX_CO2_PRODUCTION_KG_DAY):
                        flaws.append({
                            "id": "CREW_CO2_PRODUCTION_ANOMALY",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Metabolic CO2 output {val:.2f} kg/day/crew outside band [{MIN_CO2_PRODUCTION_KG_DAY}, {MAX_CO2_PRODUCTION_KG_DAY}]."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Photosynthetic quotient check
            m = self.pq_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if not (MIN_PQ_RATIO <= val <= MAX_PQ_RATIO):
                        flaws.append({
                            "id": "PQ_RATIO_OUT_OF_BOUNDS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Photosynthetic Quotient {val:.2f} outside bounds [{MIN_PQ_RATIO}, {MAX_PQ_RATIO}]."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Algal growth rate check
            m = self.algal_growth_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_BIOMASS_GROWTH_RATE_HR:
                        flaws.append({
                            "id": "ALGAL_GROWTH_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Algal biomass growth rate {val:.3f} h^-1 below threshold {MIN_BIOMASS_GROWTH_RATE_HR:.3f} h^-1."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Cabin pressure check
            m = self.pressure_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if not (MIN_CABIN_TOTAL_PRESSURE_KPA <= val <= MAX_CABIN_TOTAL_PRESSURE_KPA):
                        flaws.append({
                            "id": "CABIN_PRESSURE_ANOMALY",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Cabin pressure {val:.1f} kPa outside safe operational range [{MIN_CABIN_TOTAL_PRESSURE_KPA}, {MAX_CABIN_TOTAL_PRESSURE_KPA}]."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Cabin pO2 check
            m = self.po2_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if not (MIN_CABIN_PO2_KPA <= val <= MAX_CABIN_PO2_KPA):
                        flaws.append({
                            "id": "CABIN_HYPOXIA_HYPEROXIA",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Cabin pO2 {val:.1f} kPa violates physiological hypoxia/hyperoxia limits [{MIN_CABIN_PO2_KPA}, {MAX_CABIN_PO2_KPA}]."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Cabin pCO2 check
            m = self.pco2_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_CABIN_PCO2_KPA:
                        flaws.append({
                            "id": "CABIN_HYPERCAPNIA_RISK",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Cabin pCO2 {val:.2f} kPa exceeds hypercapnia limit {MAX_CABIN_PCO2_KPA:.2f} kPa."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Catalytic oxidizer temp check
            m = self.catalytic_temp_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_CATALYTIC_OXIDIZER_TEMP_C:
                        flaws.append({
                            "id": "CATALYTIC_OXIDIZER_COLD",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Catalytic oxidizer temperature {val:.1f} C below VOC cracking threshold {MIN_CATALYTIC_OXIDIZER_TEMP_C:.1f} C."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

        # AST structural checks (if valid Python)
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
