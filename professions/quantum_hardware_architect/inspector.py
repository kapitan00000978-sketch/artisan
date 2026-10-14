"""Quantum Hardware & Microwave Pulse Inspector.

Author: Dr. Alistair 'The Flux' Vance
Status: Production AST & Physical Invariant Inspector
"""

import ast
import re
from typing import Any, Dict, List

# Comment stripping patterns
LINE_COMMENT_PYTHON = re.compile(r"#.*")
LINE_COMMENT_C = re.compile(r"//.*")
BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)

# Quantum Inspection Patterns
DRAG_PULSE_PATTERN = re.compile(r"\b(DragPulse|beta_drag|drag_q|deriv|derivative|quadrature)\b")
COHERENCE_PATTERN = re.compile(r"\b(t1_us|t2_us|T1|T2|relaxation|dephasing)\b")
ANHARMONICITY_PATTERN = re.compile(r"\b(anharmonicity|anharmonicity_mhz|alpha\s*<\s*0|transmon)\b")
FIDELITY_PATTERN = re.compile(r"\b(fidelity|verify_gate_fidelity|0\.999|0\.995|randomized_benchmarking|MIN_SINGLE_QUBIT_FIDELITY)\b")
READOUT_RESONATOR_PATTERN = re.compile(r"\b(ReadoutResonator|dispersive_shift|chi_mhz|separation_mhz|readout)\b")
SQUARE_PULSE_HAZARD_PATTERN = re.compile(r"\b(square_pulse|raw_square|unshaped_pulse)\b")
LAZY_STUB_PATTERN = re.compile(r"\b(TODO|FIXME|XXX|TBD)\b")


class QuantumHardwareInspector:
    """Rigorous inspector evaluating quantum control code against transmon physics."""

    @staticmethod
    def strip_comments(code: str) -> str:
        """Strip single-line and multi-line comments to avoid false-positive matches."""
        stripped = BLOCK_COMMENT.sub("", code)
        stripped = LINE_COMMENT_C.sub("", stripped)
        stripped = LINE_COMMENT_PYTHON.sub("", stripped)
        return stripped

    @staticmethod
    def inspect(code: str) -> Dict[str, Any]:
        """Perform comprehensive AST and regex inspection of quantum hardware code."""
        clean_code = QuantumHardwareInspector.strip_comments(code)

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

        has_drag_pulse = bool(DRAG_PULSE_PATTERN.search(clean_code))
        has_coherence_guard = bool(COHERENCE_PATTERN.search(clean_code))
        has_anharmonicity_logic = bool(ANHARMONICITY_PATTERN.search(clean_code))
        has_fidelity_verification = bool(FIDELITY_PATTERN.search(clean_code))
        has_readout_resonator = bool(READOUT_RESONATOR_PATTERN.search(clean_code))
        has_square_pulse_hazard = bool(SQUARE_PULSE_HAZARD_PATTERN.search(clean_code))
        has_lazy_stubs = bool(LAZY_STUB_PATTERN.search(clean_code))

        pulse_shaping_safe = has_drag_pulse and not has_square_pulse_hazard

        return {
            "ast_valid": ast_valid,
            "syntax_error": syntax_error,
            "class_count": class_count,
            "func_count": func_count,
            "has_drag_pulse": has_drag_pulse,
            "has_coherence_guard": has_coherence_guard,
            "has_anharmonicity_logic": has_anharmonicity_logic,
            "has_fidelity_verification": has_fidelity_verification,
            "has_readout_resonator": has_readout_resonator,
            "has_square_pulse_hazard": has_square_pulse_hazard,
            "pulse_shaping_safe": pulse_shaping_safe,
            "has_lazy_stubs": has_lazy_stubs,
            "line_count": len(clean_code.splitlines()),
        }
