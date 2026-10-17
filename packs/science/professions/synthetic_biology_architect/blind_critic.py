"""Code-blind adversarial critic for Synthetic Biology & Metabolic Genetic Circuits.

Maintained by Dr. Seraphiel 'The SynBio' Sterling.
Delivers an unsparing audit of genetic circuit Hill kinetics,
cellular metabolic burden limits, and biocontainment escape frequencies.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
from .inspector import SynBioInspector, SynBioInspectionResult
from .rubric import SynBioRubric, SynBioRubricEvaluation


@dataclass
class SynBioDefectLedger:
    """Actionable defect ledger emitted by the blind critic."""
    target_file: str
    fatal_defects_count: int
    warnings_count: int
    defect_ledger: List[Dict[str, Any]] = field(default_factory=list)
    score: float = 0.0
    grade: str = "F"
    verdict: str = "REJECT"
    executive_summary: str = ""


class SynBioBlindCritic:
    """Adversarial evaluator with zero tolerance for biocontainment escape or circuit burden failure."""

    def __init__(self) -> None:
        self.inspector = SynBioInspector()

    def audit(self, source_code: str, file_path: str = "synbio_core.py") -> SynBioDefectLedger:
        """Ruthlessly audit source code and build actionable defect ledger."""
        inspection = self.inspector.inspect_source(source_code, file_path=file_path)
        rubric_eval = SynBioRubric.evaluate(inspection)

        defects: List[Dict[str, Any]] = []

        if not inspection.syntax_valid:
            defects.append({
                "type": "SYNTAX_FATAL",
                "description": "Code fails Python AST parsing; cannot be deployed to genetic control chassis",
                "fatal": True,
                "remediation": "Correct syntax errors immediately"
            })

        if not inspection.capabilities.get("has_hill_kinetics"):
            defects.append({
                "type": "MISSING_HILL_KINETICS",
                "description": "Missing Hill transfer function modeling promoter repression/activation",
                "fatal": True,
                "remediation": "Implement compute_transfer_function with non-linear Hill cooperativity (n >= 2.0)"
            })

        if not inspection.capabilities.get("has_metabolic_burden_calc"):
            defects.append({
                "type": "MISSING_METABOLIC_BURDEN",
                "description": "Missing cellular metabolic burden evaluation against translation budget",
                "fatal": False,
                "remediation": "Implement evaluate_circuit_burden enforcing composite burden <= 30%"
            })

        if not inspection.capabilities.get("has_crosstalk_check"):
            defects.append({
                "type": "MISSING_CROSSTALK_CHECK",
                "description": "Missing host transcriptome crosstalk verification",
                "fatal": False,
                "remediation": "Implement crosstalk rate monitoring enforcing <= 5% leakage"
            })

        if not inspection.capabilities.get("has_telemetry_eval"):
            defects.append({
                "type": "MISSING_TELEMETRY_EVAL",
                "description": "Missing real-time genetic circuit telemetry safety auditor",
                "fatal": False,
                "remediation": "Implement evaluate_telemetry_safety auditing escape frequency and burden"
            })

        if not inspection.capabilities.get("has_suicide_kill_switch"):
            defects.append({
                "type": "MISSING_SUICIDE_KILL_SWITCH",
                "description": "Missing active genomic suicide kill-switch mechanism",
                "fatal": True,
                "remediation": "Implement trigger_suicide_kill_switch guaranteeing sub-60min chassis lysis"
            })

        for v in inspection.violations:
            is_fatal = any(k in v for k in ["Biocontainment escape frequency", "Metabolic burden limit", "Lazy stub", "Empty pass"])
            defects.append({
                "type": "DOMAIN_VIOLATION",
                "description": v,
                "fatal": is_fatal,
                "remediation": f"Remediate domain invariant: {v}"
            })

        for veto in rubric_eval.veto_reasons:
            if not any(d["description"] == veto for d in defects):
                defects.append({
                    "type": "RUBRIC_VETO",
                    "description": veto,
                    "fatal": True,
                    "remediation": f"Resolve veto condition: {veto}"
                })

        fatal_count = sum(1 for d in defects if d["fatal"])
        warnings_count = sum(1 for d in defects if not d["fatal"])

        verdict = "PASS" if (rubric_eval.passed and fatal_count == 0) else "REJECT"

        summary = (
            f"Dr. Seraphiel Sterling Audit: Score {rubric_eval.total_score:.1f}/100 [{rubric_eval.grade}]. "
            f"Fatal defects: {fatal_count}, Warnings: {warnings_count}. Verdict: {verdict}."
        )

        return SynBioDefectLedger(
            target_file=file_path,
            fatal_defects_count=fatal_count,
            warnings_count=warnings_count,
            defect_ledger=defects,
            score=rubric_eval.total_score,
            grade=rubric_eval.grade,
            verdict=verdict,
            executive_summary=summary
        )

    @classmethod
    def evaluate(cls, source_code: str, file_path: str = "synbio_core.py") -> Dict[str, Any]:
        """Dictionary-returning compatibility evaluator for master orchestrator."""
        inst = cls()
        ledger = inst.audit(source_code, file_path=file_path)
        return {
            "passed": ledger.verdict == "PASS",
            "score": ledger.score,
            "grade": ledger.grade,
            "verdict": ledger.verdict,
            "fatal_defects_count": ledger.fatal_defects_count,
            "warnings_count": ledger.warnings_count,
            "defect_ledger": ledger.defect_ledger,
            "executive_summary": ledger.executive_summary
        }
