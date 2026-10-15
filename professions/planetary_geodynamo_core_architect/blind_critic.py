"""Adversarial Blind Critic for Planetary Geodynamo Core Simulations.

Embodying the relentless scrutiny of Dr. Lyra 'The Core' Sterling.
Audits code without preconceptions, producing strict verdicts and actionable remediation plans.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from professions.planetary_geodynamo_core_architect.inspector import GeodynamoCodeInspector
from professions.planetary_geodynamo_core_architect.rubric import GeodynamoRubricEvaluator, GeodynamoEvaluationReport
from professions.planetary_geodynamo_core_architect.references import (
    GeodynamoCoreParameters,
    validate_geodynamo_parameters,
)


@dataclass
class BlindCriticVerdict:
    """Rigorous audit verdict from the Blind Critic."""
    verdict: str  # "CERTIFIED_WORLD_CLASS" or "REJECTED_DEFECTIVE"
    score: float
    report: GeodynamoEvaluationReport
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


class PlanetaryGeodynamoBlindCritic:
    """Adversarial auditor evaluating geodynamo source against physical and code craftsmanship invariants."""

    def __init__(self) -> None:
        self.inspector = GeodynamoCodeInspector()
        self.evaluator = GeodynamoRubricEvaluator()

    def audit(
        self,
        source_code: str,
        params: Optional[GeodynamoCoreParameters] = None,
    ) -> BlindCriticVerdict:
        """Perform ruthless adversarial review of geodynamo source code."""
        findings = self.inspector.inspect_source(source_code)
        metrics: Dict[str, float] = {}

        if params is not None:
            val_res = validate_geodynamo_parameters(params)
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
                f"Dr. Lyra Sterling Approves. Score: {report.total_score:.1f}/100.0. "
                "The code satisfies magnetostrophic MAC balance, super-critical Magnetic Reynolds induction, "
                "proper CMB/ICB driving, and clean production implementation."
            )
        else:
            verdict_str = "REJECTED_DEFECTIVE"
            critique = (
                f"Dr. Lyra Sterling Rejection. Score: {report.total_score:.1f}/100.0. "
                "Unacceptable flaws detected: sub-critical induction, neglected Lorentz balance, "
                "or amateurish stubbing. Work cannot be certified for planetary core geophysics."
            )

        return BlindCriticVerdict(
            verdict=verdict_str,
            score=report.total_score,
            report=report,
            deductions=deductions,
            critique=critique,
            remediation_plan=remediation_plan,
        )
