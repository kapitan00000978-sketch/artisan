"""Hydrodynamic Code Inspector for Extreme Non-Linear Ocean Wave Simulations.

Audits AST structures and numerical parameters against Dr. Silas Sterling's
rogue wave hydrodynamics and non-linear physical invariants.
"""

import ast
import re
from typing import Any, Dict, List, Optional


class ExtremeWaveInspector:
    """Audits Python source code for hydrodynamic violations and amateur shortcuts."""

    def __init__(self) -> None:
        self.todo_pattern = re.compile(
            r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*",
            re.IGNORECASE
        )
        self.param_patterns: Dict[str, re.Pattern] = {
            "benjamin_feir_index": re.compile(
                r"\b(benjamin_feir_index|bfi)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "rogue_height_ratio": re.compile(
                r"\b(rogue_height_ratio|h_ratio)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "crest_abnormality": re.compile(
                r"\b(crest_abnormality|alpha_crest)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "steepness": re.compile(
                r"\b(steepness|ka_steepness)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "slamming_pressure_kpa": re.compile(
                r"\b(slamming_pressure_kpa|p_slam)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "kurtosis": re.compile(
                r"\b(kurtosis|k_elevation)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "directional_spreading_deg": re.compile(
                r"\b(directional_spreading_deg|sigma_theta)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "hosm_order": re.compile(
                r"\b(hosm_order|m_hosm)\s*[:=]\s*([0-9]+)", re.IGNORECASE
            ),
            "deck_airgap_m": re.compile(
                r"\b(deck_airgap_m|airgap_margin)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
            ),
            "daf": re.compile(
                r"\b(daf|dynamic_amplification)\s*[:=]\s*([0-9.]+)", re.IGNORECASE
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
        if "benjamin_feir_index" in parsed_params and parsed_params["benjamin_feir_index"] < 1.0:
            findings.append(
                f"Benjamin-Feir Index {parsed_params['benjamin_feir_index']} < 1.0: Sub-critical modulational instability."
            )
        if "rogue_height_ratio" in parsed_params and parsed_params["rogue_height_ratio"] < 2.0:
            findings.append(
                f"Rogue Height Ratio {parsed_params['rogue_height_ratio']} < 2.0: Fails rogue wave definition."
            )
        if "crest_abnormality" in parsed_params and parsed_params["crest_abnormality"] < 1.25:
            findings.append(
                f"Crest Abnormality {parsed_params['crest_abnormality']} < 1.25: Crest elevation under threshold."
            )
        if "steepness" in parsed_params:
            if parsed_params["steepness"] > 0.44:
                findings.append(
                    f"Wave Steepness {parsed_params['steepness']} > 0.44: Exceeds kinematic wave breaking limit."
                )
            elif parsed_params["steepness"] < 0.10:
                findings.append(
                    f"Wave Steepness {parsed_params['steepness']} < 0.10: Sea state too mild for non-linear rogue focus."
                )
        if "slamming_pressure_kpa" in parsed_params and parsed_params["slamming_pressure_kpa"] < 500.0:
            findings.append(
                f"Slamming Pressure {parsed_params['slamming_pressure_kpa']} kPa < 500.0 kPa: Under-estimating wave impact."
            )
        if "kurtosis" in parsed_params and parsed_params["kurtosis"] < 3.0:
            findings.append(
                f"Kurtosis {parsed_params['kurtosis']} < 3.0: Sub-Gaussian distribution neglects heavy tails."
            )
        if "directional_spreading_deg" in parsed_params and parsed_params["directional_spreading_deg"] > 30.0:
            findings.append(
                f"Directional Spreading {parsed_params['directional_spreading_deg']} deg > 30.0 deg: Excess spreading diffuses rogue wave focus."
            )
        if "hosm_order" in parsed_params and int(parsed_params["hosm_order"]) < 3:
            findings.append(
                f"HOSM Order {int(parsed_params['hosm_order'])} < 3: Cannot capture 4-wave non-linear resonances."
            )
        if "deck_airgap_m" in parsed_params and parsed_params["deck_airgap_m"] < 2.0:
            findings.append(
                f"Deck Air Gap {parsed_params['deck_airgap_m']} m < 2.0 m: Inadequate wave-in-deck clearance."
            )
        if "daf" in parsed_params and parsed_params["daf"] > 1.80:
            findings.append(
                f"Dynamic Amplification Factor {parsed_params['daf']} > 1.80: Structural amplification exceeds safe limit."
            )

        return {
            "findings": findings,
            "parsed_parameters": parsed_params,
            "has_defects": len(findings) > 0,
        }
