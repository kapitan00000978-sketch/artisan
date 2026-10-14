"""Genomic Codebase & High-Throughput Bioinformatics Inspector.

Author: Dr. Astrid 'The Genome' Vance
Status: Production AST & Pattern Verification Engine
"""

import ast
import re
from typing import Any, Dict, List

# Comment stripping patterns
LINE_COMMENT_PYTHON = re.compile(r"#.*")
LINE_COMMENT_C = re.compile(r"//.*")
BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)

# Genomic Inspection Patterns
STREAMING_GENERATOR_PATTERN = re.compile(r"\b(yield|Iterator|Iterable|StreamParser|parse_stream)\b")
WHOLE_FILE_SLURP_PATTERN = re.compile(r"\.(read|readlines)\(\)")
CIGAR_PATTERN = re.compile(r"(CIGAR|cigar|MIDNSHP=\s*X|\d+\[MIDNSHP=\s*X\]|parse_operations)")
MAPQ_PATTERN = re.compile(r"\b(mapq|MAPQ|mapping_quality)\b")
VARIANT_DEPTH_PATTERN = re.compile(r"\b(DP|min_depth|get_depth|sequencing_depth)\b")
PHRED_QUAL_PATTERN = re.compile(r"\b(phred|PHRED|qual|QUAL|to_phred_scores|offset\s*=\s*33)\b")
STRAND_BIAS_PATTERN = re.compile(r"\b(strand_bias|strand_bias_pvalue|SP_PVAL|Fisher)\b")
REFERENCE_BUILD_PATTERN = re.compile(r"\b(GRCh38|T2T-CHM13|hg38|reference_build|assembly|seed|sha256)\b")
PROTEOMICS_DISTANCE_PATTERN = re.compile(r"\b(ProteinResidue|distance_to|compute_contacts|cutoff_angstrom|calpha|contact_matrix)\b")
LAZY_STUB_PATTERN = re.compile(r"\b(TODO|FIXME|XXX|TBD)\b")


class BioinformaticsInspector:
    """Rigorous inspector evaluating genomics pipelines for memory safety and scientific rigor."""

    @staticmethod
    def strip_comments(code: str) -> str:
        """Strip single-line and multi-line comments to avoid false-positive metric matches."""
        stripped = BLOCK_COMMENT.sub("", code)
        stripped = LINE_COMMENT_C.sub("", stripped)
        stripped = LINE_COMMENT_PYTHON.sub("", stripped)
        return stripped

    @staticmethod
    def inspect(code: str) -> Dict[str, Any]:
        """Perform comprehensive AST and regex inspection of genomics code."""
        clean_code = BioinformaticsInspector.strip_comments(code)

        # Parse AST if valid Python
        ast_valid = False
        syntax_error = None
        has_generator = False
        class_count = 0
        func_count = 0

        try:
            tree = ast.parse(clean_code)
            ast_valid = True
            for node in ast.walk(tree):
                if isinstance(node, (ast.Yield, ast.YieldFrom)):
                    has_generator = True
                elif isinstance(node, ast.ClassDef):
                    class_count += 1
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    func_count += 1
        except SyntaxError as e:
            syntax_error = str(e)

        # Regex Metric Evaluators
        has_streaming_parser = bool(STREAMING_GENERATOR_PATTERN.search(clean_code)) or has_generator
        has_whole_file_slurp = bool(WHOLE_FILE_SLURP_PATTERN.search(clean_code))
        has_cigar_logic = bool(CIGAR_PATTERN.search(clean_code))
        has_mapq_logic = bool(MAPQ_PATTERN.search(clean_code))
        has_depth_filter = bool(VARIANT_DEPTH_PATTERN.search(clean_code))
        has_phred_logic = bool(PHRED_QUAL_PATTERN.search(clean_code))
        has_strand_bias_filter = bool(STRAND_BIAS_PATTERN.search(clean_code))
        has_reference_provenance = bool(REFERENCE_BUILD_PATTERN.search(clean_code))
        has_proteomic_structure = bool(PROTEOMICS_DISTANCE_PATTERN.search(clean_code))
        has_lazy_stubs = bool(LAZY_STUB_PATTERN.search(clean_code))

        # Memory safety check: true if streaming parser is present and no naive whole-file slurp
        memory_safe_streaming = has_streaming_parser and not has_whole_file_slurp

        return {
            "ast_valid": ast_valid,
            "syntax_error": syntax_error,
            "class_count": class_count,
            "func_count": func_count,
            "has_generator": has_generator,
            "has_streaming_parser": has_streaming_parser,
            "has_whole_file_slurp": has_whole_file_slurp,
            "memory_safe_streaming": memory_safe_streaming,
            "has_cigar_logic": has_cigar_logic,
            "has_mapq_logic": has_mapq_logic,
            "has_depth_filter": has_depth_filter,
            "has_phred_logic": has_phred_logic,
            "has_strand_bias_filter": has_strand_bias_filter,
            "has_reference_provenance": has_reference_provenance,
            "has_proteomic_structure": has_proteomic_structure,
            "has_lazy_stubs": has_lazy_stubs,
            "line_count": len(clean_code.splitlines()),
        }
