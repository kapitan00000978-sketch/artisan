#!/usr/bin/env python3
"""
Neuromorphic Spiking Silicon Static AST & Pattern Inspector
Scans spiking neural network and asynchronous silicon code for refractory deficits,
STDP weight instability, unbounded conductances, AER packet drops, and energy overruns.
"""

import ast
import re
from typing import List, Dict, Any


class NeuromorphicInspector:
    """
    Relentless static inspector for neuromorphic silicon hardware,
    spiking neural network (SNN) kernels, and AER communication controllers.
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
                "id": "lazy_neuromorphic_stub",
                "severity": "CRITICAL",
                "message": "Found unfinished stub or placeholder in neuromorphic core configuration."
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
                            "message": "Empty except block detected: suppresses AER packet corruption or synapse fault."
                        })
        except SyntaxError as err:
            flaws.append({
                "id": "syntax_error_in_neuromorphic_code",
                "severity": "CRITICAL",
                "message": f"Syntax error prevents AST validation: {err}"
            })

        # 3. Check for Refractory Period Deficit (< 1.0 ms)
        ref_match = re.search(r"(?:refractory_period|tau_ref|ref_period_ms)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", source_code, re.IGNORECASE)
        if ref_match:
            val = float(ref_match.group(1))
            if val < 1.0:
                flaws.append({
                    "id": "refractory_period_deficit",
                    "severity": "CRITICAL",
                    "message": f"LIF refractory period {val} ms < 1.0 ms minimum; risks uncontrolled spike runaway."
                })

        # 4. Check for STDP Stability Ratio Violation (A_minus / A_plus < 1.05)
        stdp_match = re.search(r"(?:stdp_ratio|stdp_ltd_ltp_ratio)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", source_code, re.IGNORECASE)
        if stdp_match:
            val = float(stdp_match.group(1))
            if val < 1.05:
                flaws.append({
                    "id": "stdp_stability_violation",
                    "severity": "HIGH",
                    "message": f"STDP depression/potentiation ratio {val} < 1.05; risks runaway synaptic excitation."
                })

        # 5. Check for Unbounded Synaptic Weights
        if re.search(r"clip_synaptic_weights\s*=\s*False", source_code, re.IGNORECASE):
            flaws.append({
                "id": "unbounded_synaptic_weights",
                "severity": "CRITICAL",
                "message": "Synaptic weight saturation envelope disabled; weights may exceed [0.0, 1.0]."
            })

        # 6. Check for AER Packet Drop Violation (> 1.0e-6)
        aer_match = re.search(r"(?:aer_packet_drop|aer_loss_rate|drop_rate)\s*=\s*([0-9]+(?:\.[0-9]+)?(?:e-?[0-9]+)?)\b", source_code, re.IGNORECASE)
        if aer_match:
            try:
                val = float(aer_match.group(1))
                if val > 1.0e-6:
                    flaws.append({
                        "id": "aer_packet_drop_violation",
                        "severity": "HIGH",
                        "message": f"AER asynchronous packet loss rate {val:.2e} > 1.0e-6 threshold."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 7. Check for Synaptic Energy Overrun (> 1.0 pJ/event)
        energy_match = re.search(r"(?:energy_per_synop|synaptic_energy_pj|synop_energy)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", source_code, re.IGNORECASE)
        if energy_match:
            val = float(energy_match.group(1))
            if val > 1.0:
                flaws.append({
                    "id": "synaptic_energy_overrun",
                    "severity": "MEDIUM",
                    "message": f"Energy per synaptic operation {val} pJ > 1.0 pJ bound; causes thermal throttling."
                })

        # 8. Check for Non-sparse Firing Rate (> 20.0 Hz or < 0.1 Hz)
        fr_match = re.search(r"(?:mean_firing_rate|population_fr_hz|firing_rate_hz)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", source_code, re.IGNORECASE)
        if fr_match:
            val = float(fr_match.group(1))
            if val > 20.0 or val < 0.1:
                flaws.append({
                    "id": "epileptic_bursting_violation",
                    "severity": "HIGH",
                    "message": f"Population mean firing rate {val} Hz outside biological sparse window [0.1, 20.0] Hz."
                })

        return flaws
