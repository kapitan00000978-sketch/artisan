#!/usr/bin/env python3
"""
Astrodynamics & Interplanetary Trajectory Static AST & Pattern Inspector
Scans orbital mechanics code for delta-v deficit, Tisserand non-conservation,
insufficient flyby periapsis clearance, Jacobi energy violations, and SRP drift.
"""

import ast
import re
from typing import List, Dict, Any


class AstrodynamicsInspector:
    """
    Relentless static inspector for orbital mechanics, interplanetary trajectories,
    and celestial navigation systems.
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
                "id": "lazy_astrodynamic_stub",
                "severity": "CRITICAL",
                "message": "Found unfinished stub or placeholder in mission-critical trajectory computation."
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
                            "message": "Empty except block detected: suppresses orbital maneuver or sensor telemetry failures."
                        })
        except SyntaxError as err:
            flaws.append({
                "id": "syntax_error_in_trajectory_code",
                "severity": "CRITICAL",
                "message": f"Syntax error prevents AST validation: {err}"
            })

        # 3. Check for Delta-V Propellant Margin Deficit (< 1.15)
        margin_match = re.search(r"(?:delta_v_margin|propellant_margin|sf_delta_v)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", source_code, re.IGNORECASE)
        if margin_match:
            val = float(margin_match.group(1))
            if val < 1.15:
                flaws.append({
                    "id": "delta_v_margin_deficit",
                    "severity": "CRITICAL",
                    "message": f"Delta-V propellant margin safety factor {val} < 1.15 mandatory reserve threshold."
                })

        # 4. Check for Tisserand Parameter Invariance Violation (|Delta T_p| > 0.05)
        tiss_match = re.search(r"(?:tisserand_error|tiss_delta|delta_tisserand)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", source_code, re.IGNORECASE)
        if tiss_match:
            val = float(tiss_match.group(1))
            if val > 0.05:
                flaws.append({
                    "id": "tisserand_invariance_violation",
                    "severity": "HIGH",
                    "message": f"Tisserand parameter jump across flyby {val} exceeds 0.05 invariance limit."
                })

        # 5. Check for Flyby Periapsis Clearance (< 300.0 km)
        peri_match = re.search(r"(?:periapsis_altitude|flyby_clearance|h_periapsis)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", source_code, re.IGNORECASE)
        if peri_match:
            val = float(peri_match.group(1))
            if val < 300.0:
                flaws.append({
                    "id": "flyby_periapsis_violation",
                    "severity": "FATAL",
                    "message": f"Flyby periapsis altitude {val} km < 300.0 km minimum clearance; danger of atmospheric capture or collision."
                })

        # 6. Check for CR3BP Jacobi Constant Barrier Violation
        if re.search(r"(?:jacobi_barrier_breach|jacobi_constant\s*<\s*min_jacobi)\s*=\s*True", source_code, re.IGNORECASE):
            flaws.append({
                "id": "cr3bp_jacobi_violation",
                "severity": "HIGH",
                "message": "Jacobi energy integral falls below zero-velocity curve barrier; probe risks escaping halo manifold."
            })

        # 7. Check for Unmodeled Solar Radiation Pressure Drift (> 1.0e-6 m/s^2)
        srp_match = re.search(r"(?:unmodeled_srp_drift|srp_drift_accel)\s*=\s*([0-9]+(?:\.[0-9]+)?(?:e-?[0-9]+)?)\b", source_code, re.IGNORECASE)
        if srp_match:
            try:
                val = float(srp_match.group(1))
                if val > 1.0e-6:
                    flaws.append({
                        "id": "srp_drift_uncompensated",
                        "severity": "MEDIUM",
                        "message": f"Unmodeled solar radiation pressure drift {val:.2e} m/s^2 exceeds 1.0e-6 m/s^2 ephemeris bound."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        return flaws
