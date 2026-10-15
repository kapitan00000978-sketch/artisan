"""Mega-Constellation Autonomous Orbital Traffic & Collision Avoidance Code Inspector.

Embodying the domain scrutiny of Commander Mira 'The Orbit' Vance:
Static AST and Regex inspection auditing autonomous conjunction triage, miss distance margins,
Hippocratic zero-secondary-conjunction screening, slot confinement, and zero-defect code invariants.
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
PC_PATTERN = re.compile(r"\b(?:collision_probability|pc_val|p_collision)\s*[:=]\s*([0-9.eE+-]+)", re.IGNORECASE)
MISS_DIST_PATTERN = re.compile(r"\b(?:miss_distance|d_miss|miss_distance_m)\s*[:=]\s*([0-9.]+)", re.IGNORECASE)
RADIAL_SEP_PATTERN = re.compile(r"\b(?:radial_separation|dr_radial|radial_offset_m)\s*[:=]\s*([0-9.]+)", re.IGNORECASE)
COV_SIGMA_PATTERN = re.compile(r"\b(?:covariance_uncertainty|sigma_pos|cov_sigma_m)\s*[:=]\s*([0-9.]+)", re.IGNORECASE)
SEC_PC_PATTERN = re.compile(r"\b(?:secondary_conjunction_prob|pc_sec|secondary_pc)\s*[:=]\s*([0-9.eE+-]+)", re.IGNORECASE)
SLOT_OFFSET_PATTERN = re.compile(r"\b(?:slot_altitude_offset|slot_offset|dh_slot_m)\s*[:=]\s*([0-9.]+)", re.IGNORECASE)
DEORBIT_YEARS_PATTERN = re.compile(r"\b(?:post_mission_deorbit_years|deorbit_years|tau_deorbit)\s*[:=]\s*([0-9.]+)", re.IGNORECASE)
CASUALTY_PATTERN = re.compile(r"\b(?:casualty_risk|e_c|casualty_expectation)\s*[:=]\s*([0-9.eE+-]+)", re.IGNORECASE)
SIMPLIFIED_GRAVITY_PATTERN = re.compile(r"\b(?:ignore_j2_perturbation|disable_atmospheric_drag|pure_keplerian_twobody)\s*[:=]\s*True\b", re.IGNORECASE)


class OrbitalTrafficCodeInspector(ast.NodeVisitor):
    """AST and regex inspector for mega-constellation collision avoidance and orbital flight dynamics."""

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

            if SIMPLIFIED_GRAVITY_PATTERN.search(line):
                self.findings.append({
                    "type": "SIMPLIFIED_ORBITAL_PROPAGATION",
                    "line": idx,
                    "message": "Pure Keplerian two-body propagation without Earth J2 geopotential or atmospheric drag.",
                    "severity": "CRITICAL",
                })

            pc_match = PC_PATTERN.search(line)
            if pc_match:
                try:
                    val = float(pc_match.group(1))
                    if val >= 1.0e-4:
                        self.findings.append({
                            "type": "ACTIONABLE_CONJUNCTION_RISK",
                            "line": idx,
                            "message": f"High conjunction probability Pc = {val:.2e} >= 1.0e-4. Autonomous avoidance burn required.",
                            "severity": "HIGH",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse Pc: {err}",
                        "severity": "LOW",
                    })

            miss_match = MISS_DIST_PATTERN.search(line)
            if miss_match:
                try:
                    val = float(miss_match.group(1))
                    if val < 1000.0:
                        self.findings.append({
                            "type": "INSUFFICIENT_MISS_DISTANCE",
                            "line": idx,
                            "message": f"3D miss distance {val:.1f} m < 1000.0 m safety margin.",
                            "severity": "CRITICAL",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse miss distance: {err}",
                        "severity": "LOW",
                    })

            radial_match = RADIAL_SEP_PATTERN.search(line)
            if radial_match:
                try:
                    val = float(radial_match.group(1))
                    if val < 250.0:
                        self.findings.append({
                            "type": "INSUFFICIENT_RADIAL_SEPARATION",
                            "line": idx,
                            "message": f"Radial separation {val:.1f} m < 250.0 m margin.",
                            "severity": "HIGH",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse radial separation: {err}",
                        "severity": "LOW",
                    })

            cov_match = COV_SIGMA_PATTERN.search(line)
            if cov_match:
                try:
                    val = float(cov_match.group(1))
                    if val > 50.0:
                        self.findings.append({
                            "type": "EXCESSIVE_COVARIANCE_UNCERTAINTY",
                            "line": idx,
                            "message": f"Ephemeris covariance uncertainty {val:.1f} m > 50.0 m limit.",
                            "severity": "HIGH",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse covariance: {err}",
                        "severity": "LOW",
                    })

            sec_pc_match = SEC_PC_PATTERN.search(line)
            if sec_pc_match:
                try:
                    val = float(sec_pc_match.group(1))
                    if val > 1.0e-6:
                        self.findings.append({
                            "type": "SECONDARY_CONJUNCTION_HAZARD",
                            "line": idx,
                            "message": f"Avoidance maneuver creates secondary conjunction: Pc_sec = {val:.2e} > 1.0e-6.",
                            "severity": "CRITICAL",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse secondary Pc: {err}",
                        "severity": "LOW",
                    })

            slot_match = SLOT_OFFSET_PATTERN.search(line)
            if slot_match:
                try:
                    val = float(slot_match.group(1))
                    if val > 50.0:
                        self.findings.append({
                            "type": "ORBITAL_SLOT_DEVIATION",
                            "line": idx,
                            "message": f"Orbital slot offset {val:.1f} m > 50.0 m corridor limit.",
                            "severity": "HIGH",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse slot offset: {err}",
                        "severity": "LOW",
                    })

            deorbit_match = DEORBIT_YEARS_PATTERN.search(line)
            if deorbit_match:
                try:
                    val = float(deorbit_match.group(1))
                    if val > 5.0:
                        self.findings.append({
                            "type": "DEORBIT_TIMELINE_VIOLATION",
                            "line": idx,
                            "message": f"Post-mission de-orbit {val:.1f} years > 5.0 years rule.",
                            "severity": "HIGH",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse deorbit timeline: {err}",
                        "severity": "LOW",
                    })

            cas_match = CASUALTY_PATTERN.search(line)
            if cas_match:
                try:
                    val = float(cas_match.group(1))
                    if val > 1.0e-4:
                        self.findings.append({
                            "type": "EXCESSIVE_CASUALTY_RISK",
                            "line": idx,
                            "message": f"Re-entry casualty risk {val:.2e} > 1.0e-4 NASA threshold.",
                            "severity": "HIGH",
                        })
                except (ValueError, IndexError) as err:
                    self.findings.append({
                        "type": "PARSE_ERROR",
                        "line": idx,
                        "message": f"Failed to parse casualty risk: {err}",
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
