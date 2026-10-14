#!/usr/bin/env python3
"""
Neural Interface & Biomechatronic BCI Static AST & Pattern Inspector
Scans neural implant firmware, microstimulation drivers, and real-time BCI decoding pipelines
for Shannon safety violations, tissue overheating, decoding latency lag, glial impedance degradation, CMRR deficits, and charge imbalance.
"""

import ast
import re
from typing import List, Dict, Any


class NeuralInterfaceInspector:
    """
    Relentless static inspector for intracortical neural interfaces, BCI motor decoders,
    and neuroprosthetic microstimulation controllers.
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
                "id": "lazy_neural_interface_stub",
                "severity": "CRITICAL",
                "message": "Found unfinished stub or placeholder in neural interface control firmware."
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
                            "message": "Empty except block detected: suppresses neural stimulator electrode fault or tissue thermal alert."
                        })
        except SyntaxError as err:
            flaws.append({
                "id": "syntax_error_in_bci_code",
                "severity": "CRITICAL",
                "message": f"Syntax error prevents AST validation: {err}"
            })

        # 3. Check for Shannon Safety Index Violation (> 1.75)
        shannon_match = re.search(
            r"(?:shannon_safety|shannon_k|k_shannon)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if shannon_match:
            try:
                val = float(shannon_match.group(1))
                if val > 1.75:
                    flaws.append({
                        "id": "shannon_safety_index_violation",
                        "severity": "CRITICAL",
                        "message": f"Shannon safety index k={val:.2f} > 1.75 limit; causes irreversible tissue electro-damage and electrode dissolution."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 4. Check for Cortical Tissue Heating Overrun (> 1.0 C)
        temp_match = re.search(
            r"(?:tissue_heating|temp_rise_c|tissue_temp_c)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if temp_match:
            try:
                val = float(temp_match.group(1))
                if val > 1.0:
                    flaws.append({
                        "id": "tissue_heating_overrun",
                        "severity": "CRITICAL",
                        "message": f"Cortical tissue temperature rise {val:.2f} C > 1.0 C limit; parenchymal thermal necrosis risk."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 5. Check for Closed-Loop Latency Violation (> 10.0 ms)
        lat_match = re.search(
            r"(?:decoding_latency|loop_latency_ms|latency_ms)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if lat_match:
            try:
                val = float(lat_match.group(1))
                if val > 10.0:
                    flaws.append({
                        "id": "decoding_latency_excessive",
                        "severity": "HIGH",
                        "message": f"Closed-loop BCI latency {val:.1f} ms > 10.0 ms limit; neuroprosthetic ataxia and lag."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 6. Check for Electrode Impedance Overrun (> 500.0 kohm)
        imp_match = re.search(
            r"(?:electrode_impedance|z_1khz_kohm|impedance_kohm)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if imp_match:
            try:
                val = float(imp_match.group(1))
                if val > 500.0:
                    flaws.append({
                        "id": "electrode_impedance_overrun",
                        "severity": "HIGH",
                        "message": f"1 kHz electrode impedance {val:.1f} kohm > 500.0 kohm; glial scar encapsulation and signal collapse."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 7. Check for Front-End CMRR Deficit (< 90.0 dB)
        cmrr_match = re.search(
            r"(?:front_end_cmrr|cmrr_db|analog_cmrr)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if cmrr_match:
            try:
                val = float(cmrr_match.group(1))
                if val < 90.0:
                    flaws.append({
                        "id": "front_end_cmrr_deficit",
                        "severity": "MEDIUM",
                        "message": f"Common-Mode Rejection {val:.1f} dB < 90.0 dB threshold; vulnerability to 50/60Hz and EMG artifacts."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 8. Check for Residual Charge Imbalance Violation (> 1.0 pC)
        q_match = re.search(
            r"(?:residual_charge|charge_imbalance|delta_q_pc)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if q_match:
            try:
                val = float(q_match.group(1))
                if val > 1.0:
                    flaws.append({
                        "id": "residual_charge_imbalance_violation",
                        "severity": "CRITICAL",
                        "message": f"Residual biphasic charge {val:.2f} pC > 1.0 pC limit; electrolytic tissue damage and Faradaic corrosion."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        return flaws
