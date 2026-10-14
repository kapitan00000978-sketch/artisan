#!/usr/bin/env python3
"""
Cryogenic Superconducting & Dilution Refrigerator Static AST & Pattern Inspector
Scans dilution refrigerator control scripts, thermal heat-sinking models, and superconducting
circuits for base temperature elevations, critical current deficits, heat leaks, and vacuum degradation.
"""

import ast
import re
from typing import List, Dict, Any


class CryogenicInspector:
    """
    Relentless static inspector for millikelvin cryostats, dilution refrigerators,
    and superconducting quantum computing hardware.
    """

    def __init__(self):
        self.todo_pattern = re.compile(
            r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*\n",
            re.IGNORECASE
        )

    def inspect_code(self, source_code: str) -> List[Dict[str, Any]]:
        flaws = []

        # 1. Check for lazy stubs / comments
        if self.todo_pattern.search(source_code):
            flaws.append({
                "id": "lazy_cryogenic_stub",
                "severity": "CRITICAL",
                "message": "Found unfinished stub or placeholder in cryogenic cooling control software."
            })

        # 2. Check for empty catch blocks via AST
        try:
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                        flaws.append({
                            "id": "empty_exception_handler",
                            "severity": "CRITICAL",
                            "message": "Empty except block detected: suppresses cryogenic temperature sensor fault."
                        })
        except SyntaxError as err:
            flaws.append({
                "id": "syntax_error_in_cryogenic_code",
                "severity": "CRITICAL",
                "message": f"Syntax error prevents AST validation: {err}"
            })

        # 3. Check for Base Temperature Elevation (> 15.0 mK)
        temp_match = re.search(r"(?:base_temperature|t_mix_mk|base_temp_mk)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", source_code, re.IGNORECASE)
        if temp_match:
            val = float(temp_match.group(1))
            if val > 15.0:
                flaws.append({
                    "id": "base_temperature_elevation",
                    "severity": "CRITICAL",
                    "message": f"Mixing chamber base temperature {val} mK > 15.0 mK limit; causes severe thermal dephasing."
                })

        # 4. Check for Superconducting Margin Deficit (< 1.30)
        sf_match = re.search(r"(?:superconducting_margin|sf_superconducting|sc_safety_factor)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", source_code, re.IGNORECASE)
        if sf_match:
            val = float(sf_match.group(1))
            if val < 1.30:
                flaws.append({
                    "id": "superconducting_margin_deficit",
                    "severity": "CRITICAL",
                    "message": f"Superconducting critical current margin {val} < 1.30 minimum safety threshold."
                })

        # 5. Check for Parasitic Heat Leak Overrun (> 1.0 uW)
        heat_match = re.search(r"(?:parasitic_heat_leak|heat_leak_uw|mixing_heat_leak)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", source_code, re.IGNORECASE)
        if heat_match:
            val = float(heat_match.group(1))
            if val > 1.0:
                flaws.append({
                    "id": "parasitic_heat_leak_overrun",
                    "severity": "HIGH",
                    "message": f"Parasitic heat leak {val} uW > 1.0 uW budget at the mixing chamber."
                })

        # 6. Check for Cryostat Vibration Violation (> 1.0e-4 g)
        vib_match = re.search(r"(?:vibration_amplitude|accel_vib_g|vib_amp_g)\s*=\s*([0-9]+(?:\.[0-9]+)?(?:e-?[0-9]+)?)\b", source_code, re.IGNORECASE)
        if vib_match:
            try:
                val = float(vib_match.group(1))
                if val > 1.0e-4:
                    flaws.append({
                        "id": "cryostat_vibration_violation",
                        "severity": "HIGH",
                        "message": f"Pulse-tube vibration amplitude {val:.2e} g > 1.0e-4 g limit; microphonics dephasing."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 7. Check for Vacuum Insulation Loss (> 1.0e-6 mbar)
        vac_match = re.search(r"(?:insulation_vacuum|cryostat_pressure|p_vac_mbar)\s*=\s*([0-9]+(?:\.[0-9]+)?(?:e-?[0-9]+)?)\b", source_code, re.IGNORECASE)
        if vac_match:
            try:
                val = float(vac_match.group(1))
                if val > 1.0e-6:
                    flaws.append({
                        "id": "vacuum_insulation_loss",
                        "severity": "FATAL",
                        "message": f"Cryostat insulation vacuum {val:.2e} mbar > 1.0e-6 mbar limit; thermal short circuit."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        return flaws
