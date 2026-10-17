"""Tokamak Physics & Fusion Plasma Stability Inspector.

Author: Dr. Silas 'The Plasma' Vance
Status: Production AST & MHD Invariant Inspector
"""

import ast
import re
from typing import Any, Dict, List

# Comment stripping patterns
LINE_COMMENT_PYTHON = re.compile(r"#.*")
LINE_COMMENT_C = re.compile(r"//.*")
BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)

# Tokamak Inspection Patterns
SAFETY_FACTOR_PATTERN = re.compile(r"\b(SafetyFactorProfile|is_kink_stable|MIN_Q95|is_kruskal_shafranov_stable)\b")
TROYON_BETA_PATTERN = re.compile(r"\b(beta_n|TroyonBetaMonitor|MAX_BETA_N|troyon|normalized_beta)\b")
GREENWALD_PATTERN = re.compile(r"\b(greenwald_limit|greenwald_fraction|GreenwaldDensityMonitor|MAX_GREENWALD_FRAC)\b")
NTM_PATTERN = re.compile(r"\b(verify_ntm_stabilization|eccd_power|island_width|NeoclassicalTearingMode|mre)\b")
DIVERTOR_PATTERN = re.compile(r"\b(verify_divertor_safety|MAX_DIVERTOR_FLUX|radiative_fraction|DivertorThermalProtection)\b")
KINK_HAZARD_PATTERN = re.compile(r"\b(q95\s*<\s*2\.0|q95\s*=\s*[01]\.[0-9]+|kruskal_shafranov_breach)\b")
DENSITY_HAZARD_PATTERN = re.compile(r"\b(greenwald_fraction\s*>=\s*1\.0|density_limit_collapse)\b")
LAZY_STUB_PATTERN = re.compile(r"\b(TODO|FIXME|XXX|TBD)\b")


class FusionPlasmaInspector:
    """Rigorous inspector evaluating fusion plasma code against MHD stability and disruption limits."""

    @staticmethod
    def strip_comments(code: str) -> str:
        """Strip single-line and multi-line comments to avoid false-positive matches."""
        stripped = BLOCK_COMMENT.sub("", code)
        stripped = LINE_COMMENT_C.sub("", stripped)
        stripped = LINE_COMMENT_PYTHON.sub("", stripped)
        return stripped

    @staticmethod
    def inspect(code: str) -> Dict[str, Any]:
        """Perform comprehensive AST and regex inspection of fusion plasma code."""
        clean_code = FusionPlasmaInspector.strip_comments(code)

        ast_valid = False
        syntax_error = None
        class_count = 0
        func_count = 0

        try:
            tree = ast.parse(clean_code)
            ast_valid = True
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_count += 1
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    func_count += 1
        except SyntaxError as e:
            syntax_error = str(e)

        has_safety_factor_logic = bool(SAFETY_FACTOR_PATTERN.search(clean_code))
        has_troyon_beta_logic = bool(TROYON_BETA_PATTERN.search(clean_code))
        has_greenwald_logic = bool(GREENWALD_PATTERN.search(clean_code))
        has_ntm_stabilization = bool(NTM_PATTERN.search(clean_code))
        has_divertor_protection = bool(DIVERTOR_PATTERN.search(clean_code))
        has_kink_disruption_hazard = bool(KINK_HAZARD_PATTERN.search(clean_code))
        has_density_limit_hazard = bool(DENSITY_HAZARD_PATTERN.search(clean_code))
        has_lazy_stubs = bool(LAZY_STUB_PATTERN.search(clean_code))

        q95_safe = has_safety_factor_logic and not has_kink_disruption_hazard
        density_safe = has_greenwald_logic and not has_density_limit_hazard

        return {
            "ast_valid": ast_valid,
            "syntax_error": syntax_error,
            "class_count": class_count,
            "func_count": func_count,
            "has_safety_factor_logic": has_safety_factor_logic,
            "has_troyon_beta_logic": has_troyon_beta_logic,
            "has_greenwald_logic": has_greenwald_logic,
            "has_ntm_stabilization": has_ntm_stabilization,
            "has_divertor_protection": has_divertor_protection,
            "has_kink_disruption_hazard": has_kink_disruption_hazard,
            "has_density_limit_hazard": has_density_limit_hazard,
            "q95_safe": q95_safe,
            "density_safe": density_safe,
            "has_lazy_stubs": has_lazy_stubs,
            "line_count": len(clean_code.splitlines()),
        }
