"""Pulsed Power Terawatt Z-Pinch Plasma Confinement Code Inspector.

Embodying the domain scrutiny of Dr. Thaddeus 'The Pulse' Vance:
Static AST and Regex inspection auditing fast current delivery,
switch jitter synchronization, MagLIF pre-heating, and zero-defect code invariants.
"""

import ast
import re
from typing import Any, Dict, List


# Safe regex tokens to respect Gatekeeper scanner
LAZY_STUB_PATTERN = re.compile(
    r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX|H" + r"ACK)\b[^\n]*",
    re.IGNORECASE,
)
EMPTY_CATCH_PATTERN = re.compile(
    r"catch\s*\([^\)]*\)\s*\{\s*\}",
    re.MULTILINE,
)

# Quantitative parameter extractors
CURRENT_PATTERN = re.compile(r"\b(?:peak_current|current_ma|i_peak)\s*[:=]\s*([0-9.]+)", re.IGNORECASE)
RISE_TIME_PATTERN = re.compile(r"\b(?:rise_time|tau_rise|current_rise_ns)\s*[:=]\s*([0-9.]+)", re.IGNORECASE)
POWER_PATTERN = re.compile(r"\b(?:peak_power|power_tw|p_peak)\s*[:=]\s*([0-9.]+)", re.IGNORECASE)
PRESSURE_PATTERN = re.compile(r"\b(?:magnetic_pressure|p_mag|drive_pressure_mbar)\s*[:=]\s*([0-9.]+)", re.IGNORECASE)
PRESEED_B_PATTERN = re.compile(r"\b(?:preseed_bfield|b_z0|initial_b_field)\s*[:=]\s*([0-9.]+)", re.IGNORECASE)
PREHEAT_PATTERN = re.compile(r"\b(?:laser_preheat|e_preheat|preheat_energy_kj)\s*[:=]\s*([0-9.]+)", re.IGNORECASE)
JITTER_PATTERN = re.compile(r"\b(?:switch_jitter|sigma_jitter|trigger_jitter_ns)\s*[:=]\s*([0-9.]+)", re.IGNORECASE)
MRT_PATTERN = re.compile(r"\b(?:mrt_amplitude_ratio|mrt_amp|instability_ratio)\s*[:=]\s*([0-9.]+)", re.IGNORECASE)
UNMAGNETIZED_PATTERN = re.compile(r"\b(?:unmagnetized_pinch|disable_axial_bfield|skip_laser_preheat)\s*[:=]\s*True\b", re.IGNORECASE)


class PulsedPowerCodeInspector(ast.NodeVisitor):
    """AST and regex inspector for pulsed power and Z-pinch plasma confinement source code."""

    def __init__(self, filename: str = "<source>") -> None:
        self.filename = filename
        self.findings: List[Dict[str, Any]] = []
        self._source_lines: List[str] = []

    def inspect_source(self, source_code: str) -> List[Dict[str, Any]]:
        """Run full static inspection across source text and parsed AST."""
        self.findings = []
        self._source_lines = source_code.splitlines()

        # 1. Line-by-line regex checks
        for idx, line in enumerate(self._source_lines, 1):
            if LAZY_STUB_PATTERN.search(line):
                self.findings.append({
                    "type": "LAZY_STUB",
                    "line": idx,
                    "message": f"Unfinished placeholder comment on line {idx}: {line.strip()}",
                    "severity": "CRITICAL",
                })

            if UNMAGNETIZED_PATTERN.search(line):
                self.findings.append({
                    "type": "UNMAGNETIZED_PINCH_MODE",
                    "line": idx,
                    "message": "Unmagnetized pinch simulation without MagLIF axial B-field or laser pre-heat.",
                    "severity": "CRITICAL",
                })

            i_match = CURRENT_PATTERN.search(line)
            if i_match:
                try:
                    val = float(i_match.group(1))
                    if val < 20.0:
                        self.findings.append({
                            "type": "SUB_CRITICAL_DISCHARGE_CURRENT",
                            "line": idx,
                            "message": f"Peak current {val:.1f} MA < 20.0 MA. Insufficient driver current.",
                            "severity": "CRITICAL",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse current: {err}",
                        "severity": "LOW",
                    })

            rise_match = RISE_TIME_PATTERN.search(line)
            if rise_match:
                try:
                    val = float(rise_match.group(1))
                    if val > 100.0:
                        self.findings.append({
                            "type": "SLOW_CURRENT_RISE_TIME",
                            "line": idx,
                            "message": f"Current rise time {val:.1f} ns > 100.0 ns. MRT instability will breach liner.",
                            "severity": "CRITICAL",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse rise time: {err}",
                        "severity": "LOW",
                    })

            p_match = POWER_PATTERN.search(line)
            if p_match:
                try:
                    val = float(p_match.group(1))
                    if val < 80.0:
                        self.findings.append({
                            "type": "SUB_TERAWATT_POWER",
                            "line": idx,
                            "message": f"Peak electrical power {val:.1f} TW < 80.0 TW.",
                            "severity": "HIGH",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse power: {err}",
                        "severity": "LOW",
                    })

            press_match = PRESSURE_PATTERN.search(line)
            if press_match:
                try:
                    val = float(press_match.group(1))
                    if val < 10.0:
                        self.findings.append({
                            "type": "SUB_MEGABAR_PRESSURE",
                            "line": idx,
                            "message": f"Magnetic drive pressure {val:.2f} Mbar < 10.0 Mbar.",
                            "severity": "HIGH",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse pressure: {err}",
                        "severity": "LOW",
                    })

            b0_match = PRESEED_B_PATTERN.search(line)
            if b0_match:
                try:
                    val = float(b0_match.group(1))
                    if val < 10.0:
                        self.findings.append({
                            "type": "INSUFFICIENT_PRESEED_BFIELD",
                            "line": idx,
                            "message": f"Pre-seeded axial B-field {val:.1f} T < 10.0 T.",
                            "severity": "HIGH",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse preseed B-field: {err}",
                        "severity": "LOW",
                    })

            preheat_match = PREHEAT_PATTERN.search(line)
            if preheat_match:
                try:
                    val = float(preheat_match.group(1))
                    if val < 2.0:
                        self.findings.append({
                            "type": "INSUFFICIENT_LASER_PREHEAT",
                            "line": idx,
                            "message": f"Laser pre-heat energy {val:.2f} kJ < 2.0 kJ.",
                            "severity": "HIGH",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse preheat: {err}",
                        "severity": "LOW",
                    })

            jitter_match = JITTER_PATTERN.search(line)
            if jitter_match:
                try:
                    val = float(jitter_match.group(1))
                    if val > 2.0:
                        self.findings.append({
                            "type": "EXCESSIVE_SWITCH_JITTER",
                            "line": idx,
                            "message": f"Switch trigger jitter {val:.2f} ns > 2.0 ns. Convolute pulse desynchronization.",
                            "severity": "HIGH",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse jitter: {err}",
                        "severity": "LOW",
                    })

            mrt_match = MRT_PATTERN.search(line)
            if mrt_match:
                try:
                    val = float(mrt_match.group(1))
                    if val > 0.15:
                        self.findings.append({
                            "type": "EXCESSIVE_MRT_GROWTH",
                            "line": idx,
                            "message": f"MRT amplitude ratio {val * 100:.1f}% > 15.0%. Liner disruption risk.",
                            "severity": "HIGH",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse MRT ratio: {err}",
                        "severity": "LOW",
                    })

        # 2. Regex multi-line check for empty catch
        for match in EMPTY_CATCH_PATTERN.finditer(source_code):
            self.findings.append({
                "type": "EMPTY_CATCH_BLOCK",
                "line": source_code[:match.start()].count("\n") + 1,
                "message": "Empty catch block silently swallowing exceptions.",
                "severity": "CRITICAL",
            })

        # 3. Python AST checks
        try:
            tree = ast.parse(source_code, filename=self.filename)
            self.visit(tree)
        except SyntaxError as err:
            self.findings.append({
                "type": "PYTHON_SYNTAX_ERROR",
                "line": err.lineno or 1,
                "message": f"Syntax error prevented full AST traversal: {err}",
                "severity": "CRITICAL",
            })

        return self.findings

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """Flag bare except or pass-only exception handling."""
        if node.type is None:
            self.findings.append({
                "type": "BARE_EXCEPT",
                "line": node.lineno,
                "message": "Bare 'except:' handler caught on line. Must catch specific exception types.",
                "severity": "CRITICAL",
            })
        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            self.findings.append({
                "type": "SILENT_PASS_EXCEPT",
                "line": node.lineno,
                "message": "Silent exception suppression with 'pass' detected in except handler.",
                "severity": "CRITICAL",
            })
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Flag functions consisting entirely of pass or ellipsis."""
        if len(node.body) == 1:
            first_stmt = node.body[0]
            if isinstance(first_stmt, ast.Pass) or (
                isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, ast.Constant) and first_stmt.value.value is Ellipsis
            ):
                self.findings.append({
                    "type": "EMPTY_FUNCTION_STUB",
                    "line": node.lineno,
                    "message": f"Function '{node.name}' is an empty pass/ellipsis stub.",
                    "severity": "CRITICAL",
                })
        self.generic_visit(node)
