#!/usr/bin/env python3
"""
Scanning Probe Microscopy & Atomic Manipulation Static AST & Pattern Inspector
Scans SPM control firmware, piezoelectric positioning scripts, and single-atom manipulation loops
for thermal drift violations, tip vibration, UHV pressure loss, stage heating, Q-factor degradation, and placement errors.
"""

import ast
import re
from typing import List, Dict, Any


class AtomicManipulationInspector:
    """
    Relentless static inspector for scanning tunneling microscopes (STM), non-contact AFMs,
    and single-atom nanotechnology positioning systems.
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
                "id": "lazy_atomic_manipulation_stub",
                "severity": "CRITICAL",
                "message": "Found unfinished stub or placeholder in atomic manipulation control software."
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
                            "message": "Empty except block detected: suppresses tip crash warning or tunneling current overload."
                        })
        except SyntaxError as err:
            flaws.append({
                "id": "syntax_error_in_spm_code",
                "severity": "CRITICAL",
                "message": f"Syntax error prevents AST validation: {err}"
            })

        # 3. Check for Thermal Drift Violation (> 5.0 pm/h)
        drift_match = re.search(
            r"(?:thermal_drift|drift_rate|drift_pm_h)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if drift_match:
            try:
                val = float(drift_match.group(1))
                if val > 5.0:
                    flaws.append({
                        "id": "thermal_drift_violation",
                        "severity": "CRITICAL",
                        "message": f"Thermal drift rate {val:.1f} pm/h > 5.0 pm/h threshold; causes atomic lattice distortion and tip crashes."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 4. Check for Tip-Sample Vibration Amplitude (> 1.0 pm)
        vib_match = re.search(
            r"(?:vibration_amp|tip_vibration|vib_amp_pm)\s*=\s*([0-9]+(?:\.[0-9]+)?(?:e-?[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if vib_match:
            try:
                val = float(vib_match.group(1))
                if val > 1.0:
                    flaws.append({
                        "id": "tip_vibration_excessive",
                        "severity": "CRITICAL",
                        "message": f"Tip-sample vibration amplitude {val:.2f} pm > 1.0 pm limit; destroys single-atom spatial resolution."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 5. Check for UHV Base Pressure Loss (> 1.0e-10 mbar)
        vac_match = re.search(
            r"(?:base_pressure|uhv_pressure|p_uhv_mbar)\s*=\s*([0-9]+(?:\.[0-9]+)?(?:e-?[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if vac_match:
            try:
                val = float(vac_match.group(1))
                if val > 1.0e-10:
                    flaws.append({
                        "id": "uhv_pressure_degradation",
                        "severity": "HIGH",
                        "message": f"Chamber base pressure {val:.2e} mbar > 1.0e-10 mbar limit; residual gas poisons pristine surface."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 6. Check for Cryogenic Stage Temperature Spike (> 4.5 K)
        temp_match = re.search(
            r"(?:stage_temperature|stage_temp_k|sample_temp_k)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if temp_match:
            try:
                val = float(temp_match.group(1))
                if val > 4.5:
                    flaws.append({
                        "id": "cryogenic_stage_heating",
                        "severity": "HIGH",
                        "message": f"Sample stage temperature {val:.1f} K > 4.5 K limit; thermal diffusion destabilizes manipulated adatoms."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 7. Check for qPlus Resonator Q-Factor Degradation (< 25,000)
        q_match = re.search(
            r"(?:qplus_q_factor|quality_factor|q_factor)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if q_match:
            try:
                val = float(q_match.group(1))
                if val < 25000.0:
                    flaws.append({
                        "id": "qplus_quality_factor_deficit",
                        "severity": "MEDIUM",
                        "message": f"qPlus tuning fork Q-factor {val:.0f} < 25,000 minimum; force gradient sensitivity impaired."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 8. Check for Atomic Placement Accuracy Deficit (> 20.0 pm)
        acc_match = re.search(
            r"(?:placement_accuracy|positioning_accuracy|accuracy_pm)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if acc_match:
            try:
                val = float(acc_match.group(1))
                if val > 20.0:
                    flaws.append({
                        "id": "atomic_placement_inaccuracy",
                        "severity": "CRITICAL",
                        "message": f"Atomic placement accuracy {val:.1f} pm > 20.0 pm threshold; fails quantum corral atomic tolerances."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        return flaws
