"""Adversarial Blind Critic for Pulsed Power and Z-Pinch Plasma Simulations.

Embodying the relentless scrutiny of Dr. Thaddeus 'The Pulse' Vance.
Audits source code without bias, enforcing sub-100ns rise times,
multi-mega-ampere peak currents, and strict switch synchronization.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from professions.pulsed_power_terawatt_plasma_architect.inspector import PulsedPowerCodeInspector
from professions.pulsed_power_terawatt_plasma_architect.rubric import (
    PulsedPowerRubricEvaluator,
    PulsedPowerEvaluationReport,
)
from professions.pulsed_power_terawatt_plasma_architect.references import (
    PulsedPowerParameters,
    validate_pulsed_power_parameters,
)


@dataclass
class BlindCriticVerdict:
    """Rigorous audit verdict from the Pulsed Power Blind Critic."""
    verdict: str  # "CERTIFIED_WORLD_CLASS" or "REJECTED_DEFECTIVE"
    score: float
    report: PulsedPowerEvaluationReport
    deductions: List[Dict[str, Any]] = field(default_factory=list)
    critique: str = ""
    remediation_plan: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.verdict == "CERTIFIED_WORLD_CLASS"

    def __getitem__(self, item: str) -> Any:
        if item == "passed":
            return self.passed
        if item == "flaw_count":
            return len(self.deductions)
        if item == "flaws":
            return self.deductions
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(item)


class PulsedPowerBlindCritic:
    """Adversarial auditor evaluating pulsed power source against physical and code craftsmanship invariants."""

    def __init__(self) -> None:
        self.inspector = PulsedPowerCodeInspector()
        self.evaluator = PulsedPowerRubricEvaluator()

    def audit(
        self,
        source_code: str,
        params: Optional[PulsedPowerParameters] = None,
    ) -> BlindCriticVerdict:
        """Perform ruthless adversarial review of pulsed power source code."""
        findings = self.inspector.inspect_source(source_code)
        metrics: Dict[str, float] = {}

        if params is not None:
            val_res = validate_pulsed_power_parameters(params)
            metrics = val_res.metrics
            for viol in val_res.violations:
                findings.append({
                    "type": "PARAMETRIC_VIOLATION",
                    "line": 0,
                    "message": viol,
                    "severity": "CRITICAL",
                })

        report = self.evaluator.evaluate(findings, metrics)

        deductions: List[Dict[str, Any]] = []
        remediation_plan: List[str] = []

        for dim_key, crit in report.criteria.items():
            if crit.points_awarded < crit.max_points:
                loss = crit.max_points - crit.points_awarded
                deductions.append({
                    "dimension": crit.dimension_name,
                    "points_lost": loss,
                    "findings": crit.findings,
                })
                for find in crit.findings:
                    remediation_plan.append(f"Remediate [{crit.dimension_name}]: {find}")

        if report.is_passing:
            verdict_str = "CERTIFIED_WORLD_CLASS"
            critique = (
                f"Dr. Thaddeus Vance Approves. Score: {report.total_score:.1f}/100.0. "
                "The code satisfies mega-ampere current delivery, sub-100ns rise times, "
                "proper MagLIF pre-heating and flux compression, and zero-defect implementation."
            )
        else:
            verdict_str = "REJECTED_DEFECTIVE"
            critique = (
                f"Dr. Thaddeus Vance Rejection. Score: {report.total_score:.1f}/100.0. "
                "Unacceptable flaws detected: slow rise time, excessive switch jitter, "
                "unmagnetized pinch assumptions, or amateur stubbing. Cannot be certified."
            )

        return BlindCriticVerdict(
            verdict=verdict_str,
            score=report.total_score,
            report=report,
            deductions=deductions,
            critique=critique,
            remediation_plan=remediation_plan,
        )
