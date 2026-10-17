"""Code-Blind Evaluator for Computational Genomics & Bioinformatics.

Author: Dr. Astrid 'The Genome' Vance
Status: Production Adversarial Critic
"""

from typing import Any, Dict, List
from professions.bioinformatics_genomics_architect.inspector import BioinformaticsInspector
from professions.bioinformatics_genomics_architect.rubric import BioinformaticsRubric


class BioinformaticsBlindCritic:
    """Impartial code-blind critic identifying genomic data hazards, memory leaks, and filter flaws."""

    @classmethod
    def evaluate(cls, code: str) -> Dict[str, Any]:
        """Perform unbiased audit of bioinformatics code and produce actionable defect ledger."""
        metrics = BioinformaticsInspector.inspect(code)
        score, breakdown, passed, veto_reason = BioinformaticsRubric.evaluate(metrics)

        defect_ledger: List[Dict[str, str]] = []

        if not metrics.get("ast_valid", False):
            defect_ledger.append({
                "rule": "AST_SYNTAX_VALIDITY",
                "severity": "FATAL",
                "description": f"Code contains invalid Python syntax: {metrics.get('syntax_error')}",
                "remediation": "Correct syntax to produce valid AST.",
            })

        if metrics.get("has_lazy_stubs", False):
            defect_ledger.append({
                "rule": "ZERO_LAZY_STUBS",
                "severity": "FATAL",
                "description": "Found placeholder stubs or TODO/FIXME markers.",
                "remediation": "Implement production logic end-to-end with zero placeholders.",
            })

        if metrics.get("has_whole_file_slurp", False):
            defect_ledger.append({
                "rule": "GENOME_STREAM_MEMORY_SAFETY",
                "severity": "FATAL",
                "description": "Detected .read() or .readlines() whole-file buffering on genomic data.",
                "remediation": "Refactor to streaming generator protocol yielding one record at a time with O(1) memory.",
            })

        if not metrics.get("has_streaming_parser", False):
            defect_ledger.append({
                "rule": "STREAMING_GENERATOR_PARSER",
                "severity": "CRITICAL",
                "description": "Missing generator-based streaming parser for high-throughput sequencing data.",
                "remediation": "Implement FastqStreamParser or generator yield parser.",
            })

        if not metrics.get("has_cigar_logic", False) or not metrics.get("has_mapq_logic", False):
            defect_ledger.append({
                "rule": "ALIGNMENT_CIGAR_INTEGRITY",
                "severity": "CRITICAL",
                "description": "Lacks CIGAR syntax validation or MAPQ alignment threshold filtering.",
                "remediation": "Add CigarParser with regex syntax validation and MAPQ >= 30 filtering.",
            })

        if not metrics.get("has_depth_filter", False) or not metrics.get("has_phred_logic", False):
            defect_ledger.append({
                "rule": "VARIANT_CALLING_RIGOR",
                "severity": "CRITICAL",
                "description": "Lacks sequencing depth (DP >= 20) or Phred quality score calculation.",
                "remediation": "Enforce clinical variant QC with minimum depth and Phred quality score calculation.",
            })

        if not metrics.get("has_reference_provenance", False):
            defect_ledger.append({
                "rule": "ASSEMBLY_PROVENANCE_PINNING",
                "severity": "WARNING",
                "description": "Reference genome assembly build (e.g., GRCh38.p14 or T2T) or seed not explicitly pinned.",
                "remediation": "Explicitly pin reference assembly build constant and random seeds.",
            })

        if not metrics.get("has_proteomic_structure", False):
            defect_ledger.append({
                "rule": "STRUCTURAL_PROTEOMICS_INTEGRITY",
                "severity": "WARNING",
                "description": "Missing 3D Cartesian residue contact map or distance matrix calculation.",
                "remediation": "Incorporate ProteinContactMap and C-alpha Euclidean distance validation.",
            })

        fatal_defects_count = sum(1 for d in defect_ledger if d["severity"] == "FATAL")
        verdict = "APPROVED" if (passed and fatal_defects_count == 0) else "REJECTED"

        return {
            "score": score,
            "breakdown": breakdown,
            "passed": passed,
            "veto_reason": veto_reason,
            "defect_ledger": defect_ledger,
            "fatal_defects_count": fatal_defects_count,
            "verdict": verdict,
        }
