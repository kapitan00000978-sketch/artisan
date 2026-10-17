"""Adversarial Blind Critic for Mega-Constellation Collision Avoidance.

Embodying the relentless scrutiny of Commander Mira 'The Orbit' Vance.
Audits orbital flight software without bias, enforcing strict miss distance margins,
Hippocratic zero-secondary-conjunction screening, and 5-year post-mission disposal.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from professions.megaconstellation_orbital_collision_avoidance_architect.inspector import (
    OrbitalTrafficCodeInspector,
)
from professions.megaconstellation_orbital_collision_avoidance_architect.rubric import (
    OrbitalTrafficRubricEvaluator,
    OrbitalTrafficEvaluationReport,
)
from professions.megaconstellation_orbital_collision_avoidance_architect.references import (
    OrbitalConjunctionParameters,
    validate_orbital_conjunction_parameters,
)


@dataclass
class BlindCriticVerdict:
    """Rigorous audit verdict from the Orbital Traffic Blind Critic."""
    verdict: str  # "CERTIFIED_WORLD_CLASS" or "REJECTED_DEFECTIVE"
    score: float
    report: OrbitalTrafficEvaluationReport
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


class OrbitalTrafficBlindCritic:
    """Adversarial auditor evaluating orbital software against astrodynamic and code craftsmanship invariants."""

    def __init__(self) -> None:
        self.inspector = OrbitalTrafficCodeInspector()
        self.evaluator = OrbitalTrafficRubricEvaluator()

    def audit(
        self,
        source_code: str,
        params: Optional[OrbitalConjunctionParameters] = None,
    ) -> BlindCriticVerdict:
        """Perform ruthless adversarial review of orbital flight software."""
        findings = self.inspector.inspect_source(source_code)
        metrics: Dict[str, float] = {}

        if params is not None:
            val_res = validate_orbital_conjunction_parameters(params)
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
                f"Commander Mira Vance Approves. Score: {report.total_score:.1f}/100.0. "
                "The code satisfies autonomous collision avoidance margins (>=1km miss, >=250m radial), "
                "zero secondary conjunction creation (Pc_sec <= 1e-6), slot boundary defense, "
                "and clean production implementation."
            )
        else:
            verdict_str = "REJECTED_DEFECTIVE"
            critique = (
                f"Commander Mira Vance Rejection. Score: {report.total_score:.1f}/100.0. "
                "Unacceptable flaws detected: hazardous miss distances, secondary conjunction hazards, "
                "pure two-body propagation, or amateur stubbing. Flight certification denied."
            )

        return BlindCriticVerdict(
            verdict=verdict_str,
            score=report.total_score,
            report=report,
            deductions=deductions,
            critique=critique,
            remediation_plan=remediation_plan,
        )
