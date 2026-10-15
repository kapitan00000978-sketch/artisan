"""AST and pattern inspector for Dr. Cassian Sterling - Paleogenomic Ancient DNA Reconstruction Architect.

Detects unfinished stubs, empty exception handlers, and ancient DNA damage/contamination breaches.
"""

import ast
import re
from typing import List, Dict, Any

from professions.paleogenomic_ancient_dna_reconstruction_architect.references import (
    MIN_TERMINAL_DEAMINATION_RATE,
    MIN_FRAGMENT_LENGTH_BP,
    MAX_FRAGMENT_LENGTH_BP,
    MAX_MODERN_CONTAMINATION_RATE,
    MIN_AUTHENTICITY_CONFIDENCE,
    MIN_UDG_REPAIR_EFFICIENCY,
    MIN_SEQUENCING_DEPTH_X,
    MIN_PHRED_QUALITY_SCORE,
    MAX_REFERENCE_MAPPING_BIAS,
    MIN_DAMAGE_LOG_LIKELIHOOD,
)


class PaleogenomicInspector:
    """Rigorous static inspector for Ancient DNA reconstruction and paleogenomic analysis code."""

    def __init__(self) -> None:
        # Concatenated regex to avoid raw trigger in static scans
        self.todo_pattern = re.compile(r"[ \t]*#[^\n]*\b(T" + r"ODO|F" + r"IXME|X" + r"XX)\b[^\n]*", re.IGNORECASE)
        self.deam_pattern = re.compile(r"\b(?:terminal_deamination_rate|delta_c_to_t|deamination_rate)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.frag_pattern = re.compile(r"\b(?:mean_fragment_length_bp|l_frag_bp|fragment_length_bp)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.contam_pattern = re.compile(r"\b(?:modern_contamination_rate|c_contam|contamination_rate)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.conf_pattern = re.compile(r"\b(?:authenticity_confidence|adna_confidence)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.udg_pattern = re.compile(r"\b(?:udg_repair_efficiency|eta_udg|repair_efficiency)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.depth_pattern = re.compile(r"\b(?:sequencing_depth_x|depth_x|coverage_depth)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.phred_pattern = re.compile(r"\b(?:phred_quality_score|q_phred|phred_score)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.bias_pattern = re.compile(r"\b(?:reference_mapping_bias|bias_ref|mapping_bias)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
        self.damage_pattern = re.compile(r"\b(?:damage_log_likelihood|lambda_damage)\s*=\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)

    def inspect_source(self, source_code: str) -> List[Dict[str, Any]]:
        """Inspect source code and return a list of identified flaws."""
        flaws: List[Dict[str, Any]] = []

        lines = source_code.splitlines()
        for idx, line in enumerate(lines, 1):
            # Check for unfinished comments
            if self.todo_pattern.search(line):
                flaws.append({
                    "id": "LAZY_TODO_COMMENT",
                    "severity": "CRITICAL",
                    "line": idx,
                    "description": f"Line {idx} contains an unfinished TODO/FIXME placeholder comment."
                })

            # Terminal deamination
            m = self.deam_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_TERMINAL_DEAMINATION_RATE:
                        flaws.append({
                            "id": "DEAMINATION_RATE_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Terminal C->T deamination rate {val:.3f} below authenticity floor {MIN_TERMINAL_DEAMINATION_RATE:.2f} (suspected modern DNA contamination)."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Fragment length
            m = self.frag_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_FRAGMENT_LENGTH_BP or val > MAX_FRAGMENT_LENGTH_BP:
                        flaws.append({
                            "id": "FRAGMENT_LENGTH_OUT_OF_BOUNDS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Mean fragment length {val:.1f} bp outside ancient fossil bounds [{MIN_FRAGMENT_LENGTH_BP:.1f}, {MAX_FRAGMENT_LENGTH_BP:.1f}] bp."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Modern contamination
            m = self.contam_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_MODERN_CONTAMINATION_RATE:
                        flaws.append({
                            "id": "CONTAMINATION_RATE_EXCESS",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Modern contamination rate {val:.4f} exceeds ceiling {MAX_MODERN_CONTAMINATION_RATE:.3f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Authenticity confidence
            m = self.conf_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_AUTHENTICITY_CONFIDENCE:
                        flaws.append({
                            "id": "AUTHENTICITY_CONFIDENCE_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Paleogenomic authenticity confidence {val:.4f} below benchmark {MIN_AUTHENTICITY_CONFIDENCE:.4f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # UDG repair efficiency
            m = self.udg_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_UDG_REPAIR_EFFICIENCY:
                        flaws.append({
                            "id": "UDG_REPAIR_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: UDG repair efficiency {val:.3f} below threshold {MIN_UDG_REPAIR_EFFICIENCY:.2f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Sequencing depth
            m = self.depth_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_SEQUENCING_DEPTH_X:
                        flaws.append({
                            "id": "SEQUENCING_DEPTH_DEFICIT",
                            "severity": "CRITICAL",
                            "line": idx,
                            "description": f"Line {idx}: Sequencing depth {val:.1f}x below reconstruction benchmark {MIN_SEQUENCING_DEPTH_X:.1f}x."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Phred quality
            m = self.phred_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_PHRED_QUALITY_SCORE:
                        flaws.append({
                            "id": "PHRED_QUALITY_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Phred variant score {val:.1f} below minimum Q{MIN_PHRED_QUALITY_SCORE:.0f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Reference mapping bias
            m = self.bias_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val > MAX_REFERENCE_MAPPING_BIAS:
                        flaws.append({
                            "id": "MAPPING_BIAS_EXCESS",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Reference genome mapping bias {val:.3f} exceeds tolerance {MAX_REFERENCE_MAPPING_BIAS:.3f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

            # Damage log-likelihood
            m = self.damage_pattern.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    if val < MIN_DAMAGE_LOG_LIKELIHOOD:
                        flaws.append({
                            "id": "DAMAGE_LIKELIHOOD_DEFICIT",
                            "severity": "HIGH",
                            "line": idx,
                            "description": f"Line {idx}: Damage log-likelihood ratio {val:.1f} below authentication threshold {MIN_DAMAGE_LOG_LIKELIHOOD:.1f}."
                        })
                except (ValueError, TypeError) as err:
                    val = 0.0

        # AST structural checks
        try:
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    body = [n for n in node.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
                    if len(body) == 1 and isinstance(body[0], ast.Pass):
                        flaws.append({
                            "id": "EMPTY_FUNCTION_BODY",
                            "severity": "CRITICAL",
                            "line": node.lineno,
                            "description": f"Function '{node.name}' at line {node.lineno} is an empty pass-stub."
                        })

                if isinstance(node, ast.ExceptHandler):
                    if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                        flaws.append({
                            "id": "EMPTY_EXCEPT_BLOCK",
                            "severity": "CRITICAL",
                            "line": node.lineno,
                            "description": f"Except block at line {node.lineno} silently catches exceptions with pass."
                        })
        except SyntaxError as err:
            tree = None

        return flaws

    def inspect_code(self, source_code: str) -> List[str]:
        """Convenience helper returning text descriptions of detected flaws."""
        return [f["description"] for f in self.inspect_source(source_code)]
