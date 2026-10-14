#!/usr/bin/env python3
"""
Direct Fusion Rocket & Magnetoplasmadynamic Propulsion Static AST & Pattern Inspector
Scans fusion thruster flight software, magnetic nozzle field detachment solvers, and plasma controllers
for specific impulse deficits, Alfven Mach detachment failure, divergence losses, neutron flux overruns, and purity loss.
"""

import ast
import re
from typing import List, Dict, Any


class FusionRocketInspector:
    """
    Relentless static inspector for Direct Fusion Drive (DFD) engines,
    magnetic nozzles, and magnetoplasmadynamic rocket propulsion.
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
                "id": "lazy_fusion_rocket_stub",
                "severity": "CRITICAL",
                "message": "Found unfinished stub or placeholder in fusion rocket propulsion flight software."
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
                            "message": "Empty except block detected: suppresses magnetic nozzle detachment or HTS coil quench alert."
                        })
        except SyntaxError as err:
            flaws.append({
                "id": "syntax_error_in_fusion_rocket_code",
                "severity": "CRITICAL",
                "message": f"Syntax error prevents AST validation: {err}"
            })

        # 3. Check for Specific Impulse Deficit (< 10,000 s)
        isp_match = re.search(
            r"(?:specific_impulse|isp_seconds|isp_s)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if isp_match:
            try:
                val = float(isp_match.group(1))
                if val < 10000.0:
                    flaws.append({
                        "id": "specific_impulse_deficit",
                        "severity": "CRITICAL",
                        "message": f"Specific impulse {val:.0f} s < 10,000 s minimum; fails fusion-class exhaust velocity benchmark."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 4. Check for Magnetic Nozzle Detachment Deficit (< 1.50)
        mach_match = re.search(
            r"(?:alfven_mach|m_alfven|mach_alfven)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if mach_match:
            try:
                val = float(mach_match.group(1))
                if val < 1.50:
                    flaws.append({
                        "id": "magnetic_nozzle_detachment_failure",
                        "severity": "CRITICAL",
                        "message": f"Alfven Mach number M_A={val:.2f} < 1.50 limit; plasma trapped on closed field lines producing zero net thrust."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 5. Check for Nozzle Divergence Half-Angle Overrun (> 12.0 deg)
        div_match = re.search(
            r"(?:divergence_half_angle|theta_div_deg|nozzle_half_angle)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if div_match:
            try:
                val = float(div_match.group(1))
                if val > 12.0:
                    flaws.append({
                        "id": "nozzle_divergence_overrun",
                        "severity": "HIGH",
                        "message": f"Divergence half-angle {val:.1f} deg > 12.0 deg threshold; excessive cosine thrust momentum loss."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 6. Check for Neutron Wall Heat Flux Overrun (> 2.0 MW/m^2)
        flux_match = re.search(
            r"(?:neutron_wall_flux|q_wall_mw|neutron_heat_mw_m2)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if flux_match:
            try:
                val = float(flux_match.group(1))
                if val > 2.0:
                    flaws.append({
                        "id": "neutron_wall_flux_overrun",
                        "severity": "CRITICAL",
                        "message": f"Neutron wall flux {val:.2f} MW/m^2 > 2.0 MW/m^2 limit; causes HTS magnetic coil thermal quench."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 7. Check for Thrust Power Efficiency Deficit (< 65.0%)
        eff_match = re.search(
            r"(?:thrust_efficiency|eta_thrust_pct|thrust_eff)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if eff_match:
            try:
                val = float(eff_match.group(1))
                if val < 65.0:
                    flaws.append({
                        "id": "thrust_power_efficiency_deficit",
                        "severity": "HIGH",
                        "message": f"Thrust efficiency {val:.1f}% < 65.0% threshold; excessive parasitic thermal recirculation."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        # 8. Check for Plasma Ionization Purity Deficit (< 98.0%)
        pure_match = re.search(
            r"(?:plasma_purity|ionization_pct|chi_ion_pct)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b",
            source_code,
            re.IGNORECASE
        )
        if pure_match:
            try:
                val = float(pure_match.group(1))
                if val < 98.0:
                    flaws.append({
                        "id": "plasma_ionization_purity_deficit",
                        "severity": "MEDIUM",
                        "message": f"Plasma ionization purity {val:.1f}% < 98.0% threshold; unionized neutral boundary drag."
                    })
            except (ValueError, TypeError) as err:
                val = 0.0

        return flaws
