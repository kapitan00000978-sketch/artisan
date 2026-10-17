"""Code-blind adversarial critic for Subsea Autonomous Robotics & Deep-Sea Navigation.

Maintained by Commander Orion 'The Deep' Sterling.
Delivers an unsparing audit of structural implosion safety factors,
acoustic navigation calibration, and subsea fail-safe architectures.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
from .inspector import DeepSeaInspector, DeepSeaInspectionResult
from .rubric import DeepSeaRubric, DeepSeaRubricEvaluation


@dataclass
class DeepSeaDefectLedger:
    """Actionable defect ledger emitted by the blind critic."""
    target_file: str
    fatal_defects_count: int
    warnings_count: int
    defect_ledger: List[Dict[str, Any]] = field(default_factory=list)
    score: float = 0.0
    grade: str = "F"
    verdict: str = "REJECT"
    executive_summary: str = ""


class DeepSeaBlindCritic:
    """Adversarial evaluator with zero tolerance for subsea implosion risks."""

    def __init__(self) -> None:
        self.inspector = DeepSeaInspector()

    def audit(self, source_code: str, file_path: str = "subsea_core.py") -> DeepSeaDefectLedger:
        """Ruthlessly audit source code and build actionable defect ledger."""
        inspection = self.inspector.inspect_source(source_code, file_path=file_path)
        rubric_eval = DeepSeaRubric.evaluate(inspection)

        defects: List[Dict[str, Any]] = []

        # Analyze syntax
        if not inspection.syntax_valid:
            defects.append({
                "type": "SYNTAX_FATAL",
                "description": "Code fails Python AST parsing; cannot be deployed to subsea vehicle",
                "fatal": True,
                "remediation": "Correct syntax errors immediately"
            })

        # Analyze missing core capabilities
        if not inspection.capabilities.get("has_hydrostatic_calc"):
            defects.append({
                "type": "MISSING_HYDROSTATIC_CALC",
                "description": "Missing hydrostatic pressure calculation function (P = rho * g * h)",
                "fatal": False,
                "remediation": "Implement compute_hydrostatic_pressure using density=1030 kg/m^3 and standard gravity"
            })

        if not inspection.capabilities.get("has_sound_speed_model"):
            defects.append({
                "type": "MISSING_SOUND_SPEED_MODEL",
                "description": "Missing empirical sound velocity profile (Mackenzie/Del Grosso) calibration",
                "fatal": False,
                "remediation": "Implement calculate_sound_velocity with 9-term empirical acoustic formula"
            })

        if not inspection.capabilities.get("has_hull_safety_check"):
            defects.append({
                "type": "MISSING_HULL_SAFETY_VERIFICATION",
                "description": "Missing structural crush safety factor verification against hull collapse rating",
                "fatal": True,
                "remediation": "Implement verify_hull_safety enforcing SF >= 1.50"
            })

        if not inspection.capabilities.get("has_telemetry_eval"):
            defects.append({
                "type": "MISSING_TELEMETRY_EVAL",
                "description": "Missing real-time subsea telemetry safety evaluation executive",
                "fatal": False,
                "remediation": "Implement evaluate_telemetry_safety checking acoustic drift, compensation, and insulation"
            })

        if not inspection.capabilities.get("has_passive_jettison"):
            defects.append({
                "type": "MISSING_PASSIVE_JETTISON",
                "description": "Missing passive burn-wire / emergency drop-weight ballast release fail-safe",
                "fatal": True,
                "remediation": "Implement trigger_passive_jettison guaranteeing fail-safe positive buoyancy ascent"
            })

        # Analyze domain violations & vetoes
        for v in inspection.violations:
            is_fatal = any(k in v for k in ["Substandard hull collapse", "Depth rating", "Lazy stub", "Empty pass"])
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
            f"Commander Orion Sterling Audit: Score {rubric_eval.total_score:.1f}/100 [{rubric_eval.grade}]. "
            f"Fatal defects: {fatal_count}, Warnings: {warnings_count}. Verdict: {verdict}."
        )

        return DeepSeaDefectLedger(
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
    def evaluate(cls, source_code: str, file_path: str = "subsea_core.py") -> Dict[str, Any]:
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
