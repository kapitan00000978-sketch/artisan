"""Code-blind adversarial critic for Particle Accelerators & Relativistic Beam Dynamics.

Maintained by Dr. Julian 'The Accelerator' Vance.
Delivers an unsparing audit of betatron tune resonances,
superconducting cavity quench interlocks, and machine protection systems.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
from .inspector import AcceleratorInspector, AcceleratorInspectionResult
from .rubric import AcceleratorRubric, AcceleratorRubricEvaluation


@dataclass
class AcceleratorDefectLedger:
    """Actionable defect ledger emitted by the blind critic."""
    target_file: str
    fatal_defects_count: int
    warnings_count: int
    defect_ledger: List[Dict[str, Any]] = field(default_factory=list)
    score: float = 0.0
    grade: str = "F"
    verdict: str = "REJECT"
    executive_summary: str = ""


class AcceleratorBlindCritic:
    """Adversarial evaluator with zero tolerance for beam resonance or cavity quench damage."""

    def __init__(self) -> None:
        self.inspector = AcceleratorInspector()

    def audit(self, source_code: str, file_path: str = "accelerator_core.py") -> AcceleratorDefectLedger:
        """Ruthlessly audit source code and build actionable defect ledger."""
        inspection = self.inspector.inspect_source(source_code, file_path=file_path)
        rubric_eval = AcceleratorRubric.evaluate(inspection)

        defects: List[Dict[str, Any]] = []

        if not inspection.syntax_valid:
            defects.append({
                "type": "SYNTAX_FATAL",
                "description": "Code fails Python AST parsing; cannot be deployed to accelerator machine control",
                "fatal": True,
                "remediation": "Correct syntax errors immediately"
            })

        if not inspection.capabilities.get("has_relativistic_kinematics"):
            defects.append({
                "type": "MISSING_RELATIVISTIC_KINEMATICS",
                "description": "Missing relativistic Lorentz factor and magnetic rigidity calculations",
                "fatal": False,
                "remediation": "Implement compute_relativistic_lorentz_state calculating gamma, beta, and rigidity"
            })

        if not inspection.capabilities.get("has_tune_resonance_guard"):
            defects.append({
                "type": "MISSING_TUNE_RESONANCE_GUARD",
                "description": "Missing betatron tune resonance stopband avoidance verification",
                "fatal": True,
                "remediation": "Implement evaluate_betatron_tune_resonances enforcing margin >= 0.05"
            })

        if not inspection.capabilities.get("has_cavity_quench_check"):
            defects.append({
                "type": "MISSING_CAVITY_QUENCH_CHECK",
                "description": "Missing superconducting RF cavity temperature and quench interlock checks",
                "fatal": True,
                "remediation": "Implement cavity quench monitoring verifying T <= 2.0K and trip <= 10us"
            })

        if not inspection.capabilities.get("has_telemetry_eval"):
            defects.append({
                "type": "MISSING_TELEMETRY_EVAL",
                "description": "Missing real-time beam telemetry safety evaluation executive",
                "fatal": False,
                "remediation": "Implement evaluate_telemetry_safety auditing beam loss, vacuum, and tunes"
            })

        if not inspection.capabilities.get("has_kicker_dump_abort"):
            defects.append({
                "type": "MISSING_KICKER_DUMP_ABORT",
                "description": "Missing fast kicker machine protection beam extraction dump",
                "fatal": True,
                "remediation": "Implement trigger_machine_protection_dump with sub-3us response"
            })

        for v in inspection.violations:
            is_fatal = any(k in v for k in ["Substandard betatron tune", "Superconducting RF cavity", "Lazy stub", "Empty pass"])
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
            f"Dr. Julian Vance Audit: Score {rubric_eval.total_score:.1f}/100 [{rubric_eval.grade}]. "
            f"Fatal defects: {fatal_count}, Warnings: {warnings_count}. Verdict: {verdict}."
        )

        return AcceleratorDefectLedger(
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
    def evaluate(cls, source_code: str, file_path: str = "accelerator_core.py") -> Dict[str, Any]:
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
