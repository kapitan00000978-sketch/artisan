"""Pulsed Power Terawatt Z-Pinch Plasma Confinement 100-Point Evaluation Rubric.

Embodying the quantitative evaluation standards of Dr. Thaddeus 'The Pulse' Vance.
A strict passing score requires >= 95.0 / 100.0 points.
"""

from dataclasses import dataclass, field
from typing import Dict, List


PASSING_SCORE_THRESHOLD = 95.0


@dataclass
class CriterionResult:
    """Detailed score report for an individual rubric dimension."""
    dimension_name: str
    max_points: float
    points_awarded: float
    findings: List[str] = field(default_factory=list)


@dataclass
class PulsedPowerEvaluationReport:
    """Holistic rubric assessment for pulsed power Z-pinch plasma code."""
    total_score: float
    is_passing: bool
    criteria: Dict[str, CriterionResult] = field(default_factory=dict)
    summary: str = ""


class PulsedPowerRubricEvaluator:
    """Evaluates pulsed power source code against Dr. Thaddeus Vance's four pillars."""

    def evaluate(self, findings: List[Dict[str, str]], metrics: Dict[str, float]) -> PulsedPowerEvaluationReport:
        """Calculate score based on findings and quantitative metrics."""
        # 1. Fast Terawatt Drive Delivery (30 pts)
        c1_findings: List[str] = []
        c1_points = 30.0

        for f in findings:
            ftype = f.get("type", "")
            if ftype == "SUB_CRITICAL_DISCHARGE_CURRENT":
                c1_points -= 20.0
                c1_findings.append("Critical: Peak current below 20.0 MA driver threshold.")
            elif ftype == "SLOW_CURRENT_RISE_TIME":
                c1_points -= 20.0
                c1_findings.append("Critical: Current rise time > 100.0 ns; MRT disruption unavoidable.")
            elif ftype == "SUB_TERAWATT_POWER":
                c1_points -= 10.0
                c1_findings.append("High: Peak electrical power < 80.0 TW.")

        c1_points = max(0.0, c1_points)

        # 2. Magnetized Liner Inertial Fusion Triad (25 pts)
        c2_findings: List[str] = []
        c2_points = 25.0

        for f in findings:
            ftype = f.get("type", "")
            if ftype == "UNMAGNETIZED_PINCH_MODE":
                c2_points -= 25.0
                c2_findings.append("Critical: Unmagnetized pinch model without MagLIF stabilization.")
            elif ftype == "INSUFFICIENT_PRESEED_BFIELD":
                c2_points -= 15.0
                c2_findings.append("High: Pre-seeded axial B-field < 10.0 T.")
            elif ftype == "INSUFFICIENT_LASER_PREHEAT":
                c2_points -= 10.0
                c2_findings.append("High: Laser pre-heat energy < 2.0 kJ.")
            elif ftype == "SUB_MEGABAR_PRESSURE":
                c2_points -= 10.0
                c2_findings.append("High: Magnetic drive pressure < 10.0 Mbar.")

        c2_points = max(0.0, c2_points)

        # 3. Dynamic Stability & Switch Synchronization (25 pts)
        c3_findings: List[str] = []
        c3_points = 25.0

        for f in findings:
            ftype = f.get("type", "")
            if ftype == "EXCESSIVE_SWITCH_JITTER":
                c3_points -= 15.0
                c3_findings.append("High: Switch trigger jitter > 2.0 ns; pulse desynchronization.")
            elif ftype == "EXCESSIVE_MRT_GROWTH":
                c3_points -= 15.0
                c3_findings.append("High: MRT amplitude ratio > 15.0%; liner wall breakup.")

        c3_points = max(0.0, c3_points)

        # 4. Code Craftsmanship & Production Hardening (20 pts)
        c4_findings: List[str] = []
        c4_points = 20.0

        for f in findings:
            ftype = f.get("type", "")
            if ftype in ("LAZY_STUB", "EMPTY_FUNCTION_STUB"):
                c4_points -= 10.0
                c4_findings.append(f"Critical: Unfinished placeholder or empty stub: {f.get('message')}")
            elif ftype in ("BARE_EXCEPT", "SILENT_PASS_EXCEPT", "EMPTY_CATCH_BLOCK"):
                c4_points -= 10.0
                c4_findings.append(f"Critical: Silent error suppression or bare except: {f.get('message')}")
            elif ftype == "PYTHON_SYNTAX_ERROR":
                c4_points -= 20.0
                c4_findings.append(f"Critical: Syntax error: {f.get('message')}")

        c4_points = max(0.0, c4_points)

        total_score = c1_points + c2_points + c3_points + c4_points
        is_passing = total_score >= PASSING_SCORE_THRESHOLD

        criteria = {
            "fast_terawatt_drive": CriterionResult(
                dimension_name="Fast Terawatt Drive Delivery",
                max_points=30.0,
                points_awarded=c1_points,
                findings=c1_findings,
            ),
            "maglif_triad": CriterionResult(
                dimension_name="Magnetized Liner Inertial Fusion Triad",
                max_points=25.0,
                points_awarded=c2_points,
                findings=c2_findings,
            ),
            "stability_and_synchronization": CriterionResult(
                dimension_name="Dynamic Stability & Switch Synchronization",
                max_points=25.0,
                points_awarded=c3_points,
                findings=c3_findings,
            ),
            "code_craftsmanship": CriterionResult(
                dimension_name="Code Craftsmanship & Production Hardening",
                max_points=20.0,
                points_awarded=c4_points,
                findings=c4_findings,
            ),
        }

        if is_passing:
            summary = (
                f"PASSED ({total_score:.1f}/100.0). Code adheres to Dr. Thaddeus Vance's "
                "rigorous pulsed power and Z-pinch plasma confinement invariants."
            )
        else:
            summary = (
                f"REJECTED ({total_score:.1f}/100.0). Score is below the 95.0 threshold. "
                "Immediate self-remediation required."
            )

        return PulsedPowerEvaluationReport(
            total_score=total_score,
            is_passing=is_passing,
            criteria=criteria,
            summary=summary,
        )
