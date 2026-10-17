"""Code-blind adversarial critic for Hypersonic Aerothermodynamics & Scramjet Propulsion.

Maintained by Dr. Zephyr 'The Hypersonic' Sterling.
Delivers an unsparing audit of scramjet unstart margins,
real-gas aerothermal models, and thermal protection boundaries.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
from .inspector import HypersonicInspector, HypersonicInspectionResult
from .rubric import HypersonicRubric, HypersonicRubricEvaluation


@dataclass
class HypersonicDefectLedger:
    """Actionable defect ledger emitted by the blind critic."""
    target_file: str
    fatal_defects_count: int
    warnings_count: int
    defect_ledger: List[Dict[str, Any]] = field(default_factory=list)
    score: float = 0.0
    grade: str = "F"
    verdict: str = "REJECT"
    executive_summary: str = ""


class HypersonicBlindCritic:
    """Adversarial evaluator with zero tolerance for scramjet unstart or aerothermal burn-through."""

    def __init__(self) -> None:
        self.inspector = HypersonicInspector()

    def audit(self, source_code: str, file_path: str = "hypersonic_core.py") -> HypersonicDefectLedger:
        """Ruthlessly audit source code and build actionable defect ledger."""
        inspection = self.inspector.inspect_source(source_code, file_path=file_path)
        rubric_eval = HypersonicRubric.evaluate(inspection)

        defects: List[Dict[str, Any]] = []

        if not inspection.syntax_valid:
            defects.append({
                "type": "SYNTAX_FATAL",
                "description": "Code fails Python AST parsing; cannot be deployed to hypersonic flight control",
                "fatal": True,
                "remediation": "Correct syntax errors immediately"
            })

        if not inspection.capabilities.get("has_aerothermal_heating"):
            defects.append({
                "type": "MISSING_AEROTHERMAL_HEATING",
                "description": "Missing Sutton-Graves stagnation heat flux calculation formula",
                "fatal": False,
                "remediation": "Implement calculate_stagnation_aerothermal_heating with Sutton-Graves constant"
            })

        if not inspection.capabilities.get("has_real_gas_model"):
            defects.append({
                "type": "MISSING_REAL_GAS_MODEL",
                "description": "Missing high-temperature real-gas molecular dissociation damping",
                "fatal": False,
                "remediation": "Implement evaluate_real_gas_shock_temperature accounting for O2/N2 dissociation above 2000K"
            })

        if not inspection.capabilities.get("has_isolator_stability"):
            defects.append({
                "type": "MISSING_ISOLATOR_STABILITY",
                "description": "Missing scramjet isolator shock train stability margin evaluation",
                "fatal": True,
                "remediation": "Implement evaluate_scramjet_isolator_stability enforcing margin >= 1.25"
            })

        if not inspection.capabilities.get("has_telemetry_eval"):
            defects.append({
                "type": "MISSING_TELEMETRY_EVAL",
                "description": "Missing real-time hypersonic flight telemetry safety auditor",
                "fatal": False,
                "remediation": "Implement evaluate_telemetry_safety verifying Mach, TPS SF, and unstart margin"
            })

        if not inspection.capabilities.get("has_unstart_mitigation"):
            defects.append({
                "type": "MISSING_UNSTART_MITIGATION",
                "description": "Missing active unstart mitigation via fuel throttling and bleed doors",
                "fatal": True,
                "remediation": "Implement trigger_unstart_mitigation with sub-5ms response"
            })

        for v in inspection.violations:
            is_fatal = any(k in v for k in ["Substandard scramjet isolator", "Substandard Thermal Protection", "Lazy stub", "Empty pass"])
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
            f"Dr. Zephyr Sterling Audit: Score {rubric_eval.total_score:.1f}/100 [{rubric_eval.grade}]. "
            f"Fatal defects: {fatal_count}, Warnings: {warnings_count}. Verdict: {verdict}."
        )

        return HypersonicDefectLedger(
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
    def evaluate(cls, source_code: str, file_path: str = "hypersonic_core.py") -> Dict[str, Any]:
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
