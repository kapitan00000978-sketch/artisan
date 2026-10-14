"""Nuclear Physics & Criticality Safety Inspector.

Author: Dr. Magnus 'The Core' Sterling
Status: Production AST & Reactor Kinetics Inspector
"""

import ast
import re
from typing import Any, Dict, List

# Comment stripping patterns
LINE_COMMENT_PYTHON = re.compile(r"#.*")
LINE_COMMENT_C = re.compile(r"//.*")
BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)

# Nuclear Safety Inspection Patterns
PRKE_KINETICS_PATTERN = re.compile(r"\b(PointReactorKinetics|precursor|precursors|prompt_lifetime|PROMPT_LIFETIME|dn_dt)\b")
REACTIVITY_DOLLARS_PATTERN = re.compile(r"\b(reactivity_dollars|BETA_EFF|beta_eff|keff|reactivity)\b")
DOPPLER_FEEDBACK_PATTERN = re.compile(r"\b(doppler|doppler_pcm_k|alpha_f|fuel_temp|MAX_DOPPLER_COEFF)\b")
DNBR_SAFETY_PATTERN = re.compile(r"\b(dnbr|DNBR|critical_heat_flux|local_heat_flux|MIN_DNBR)\b")
SCRAM_CONTROL_PATTERN = re.compile(r"\b(scram|SCRAM|insertion_time|is_stuck|ControlRod|MAX_SCRAM_TIME)\b")
POSITIVE_DOPPLER_HAZARD_PATTERN = re.compile(r"\b(doppler[a-zA-Z0-9_]*\s*>\s*0|alpha_f\s*>\s*0)\b")
PROMPT_CRITICAL_HAZARD_PATTERN = re.compile(r"\b(reactivity_dollars\s*>=\s*1\.0|prompt_critical_runaway)\b")
LAZY_STUB_PATTERN = re.compile(r"\b(TODO|FIXME|XXX|TBD)\b")


class NuclearCriticalityInspector:
    """Rigorous inspector evaluating reactor physics code against criticality safety standards."""

    @staticmethod
    def strip_comments(code: str) -> str:
        """Strip single-line and multi-line comments to avoid false-positive matches."""
        stripped = BLOCK_COMMENT.sub("", code)
        stripped = LINE_COMMENT_C.sub("", stripped)
        stripped = LINE_COMMENT_PYTHON.sub("", stripped)
        return stripped

    @staticmethod
    def inspect(code: str) -> Dict[str, Any]:
        """Perform comprehensive AST and regex inspection of nuclear reactor code."""
        clean_code = NuclearCriticalityInspector.strip_comments(code)

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

        has_prke_kinetics = bool(PRKE_KINETICS_PATTERN.search(clean_code))
        has_reactivity_dollars = bool(REACTIVITY_DOLLARS_PATTERN.search(clean_code))
        has_doppler_feedback = bool(DOPPLER_FEEDBACK_PATTERN.search(clean_code))
        has_dnbr_safety = bool(DNBR_SAFETY_PATTERN.search(clean_code))
        has_scram_control = bool(SCRAM_CONTROL_PATTERN.search(clean_code))
        has_positive_doppler_hazard = bool(POSITIVE_DOPPLER_HAZARD_PATTERN.search(clean_code))
        has_prompt_critical_hazard = bool(PROMPT_CRITICAL_HAZARD_PATTERN.search(clean_code))
        has_lazy_stubs = bool(LAZY_STUB_PATTERN.search(clean_code))

        doppler_safe = has_doppler_feedback and not has_positive_doppler_hazard
        reactivity_safe = has_reactivity_dollars and not has_prompt_critical_hazard

        return {
            "ast_valid": ast_valid,
            "syntax_error": syntax_error,
            "class_count": class_count,
            "func_count": func_count,
            "has_prke_kinetics": has_prke_kinetics,
            "has_reactivity_dollars": has_reactivity_dollars,
            "has_doppler_feedback": has_doppler_feedback,
            "has_dnbr_safety": has_dnbr_safety,
            "has_scram_control": has_scram_control,
            "has_positive_doppler_hazard": has_positive_doppler_hazard,
            "has_prompt_critical_hazard": has_prompt_critical_hazard,
            "doppler_safe": doppler_safe,
            "reactivity_safe": reactivity_safe,
            "has_lazy_stubs": has_lazy_stubs,
            "line_count": len(clean_code.splitlines()),
        }
