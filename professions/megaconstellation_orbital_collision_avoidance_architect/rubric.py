"""Mega-Constellation Autonomous Orbital Traffic & Collision Avoidance 100-Point Evaluation Rubric.

Embodying the quantitative evaluation standards of Commander Mira 'The Orbit' Vance.
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
class OrbitalTrafficEvaluationReport:
    """Holistic rubric assessment for mega-constellation collision avoidance software."""
    total_score: float
    is_passing: bool
    criteria: Dict[str, CriterionResult] = field(default_factory=dict)
    summary: str = ""


class OrbitalTrafficRubricEvaluator:
    """Evaluates orbital flight dynamics source against Commander Mira Vance's four pillars."""

    def evaluate(self, findings: List[Dict[str, str]], metrics: Dict[str, float]) -> OrbitalTrafficEvaluationReport:
        """Calculate score based on findings and quantitative metrics."""
        # 1. Autonomous Conjunction & Miss Margin Defense (30 pts)
        c1_findings: List[str] = []
        c1_points = 30.0

        for f in findings:
            ftype = f.get("type", "")
            if ftype == "INSUFFICIENT_MISS_DISTANCE":
                c1_points -= 20.0
                c1_findings.append("Critical: 3D miss distance < 1000.0 m safety buffer.")
            elif ftype == "INSUFFICIENT_RADIAL_SEPARATION":
                c1_points -= 15.0
                c1_findings.append("High: Radial separation < 250.0 m margin.")
            elif ftype == "ACTIONABLE_CONJUNCTION_RISK":
                # High risk conjunction noted
                c1_findings.append("Notice: Actionable conjunction risk (Pc >= 1.0e-4).")

        c1_points = max(0.0, c1_points)

        # 2. Hippocratic Screening & Covariance Realism (25 pts)
        c2_findings: List[str] = []
        c2_points = 25.0

        for f in findings:
            ftype = f.get("type", "")
            if ftype == "SECONDARY_CONJUNCTION_HAZARD":
                c2_points -= 25.0
                c2_findings.append("Critical: Avoidance burn introduces secondary conjunction Pc_sec > 1.0e-6.")
            elif ftype == "SIMPLIFIED_ORBITAL_PROPAGATION":
                c2_points -= 15.0
                c2_findings.append("High: Pure two-body Kepler propagation ignoring J2 geopotential and drag.")
            elif ftype == "EXCESSIVE_COVARIANCE_UNCERTAINTY":
                c2_points -= 10.0
                c2_findings.append("High: Ephemeris positional covariance uncertainty > 50.0 m.")

        c2_points = max(0.0, c2_points)

        # 3. Constellation Slot-Keeping & Post-Mission Disposal (25 pts)
        c3_findings: List[str] = []
        c3_points = 25.0

        for f in findings:
            ftype = f.get("type", "")
            if ftype == "ORBITAL_SLOT_DEVIATION":
                c3_points -= 15.0
                c3_findings.append("High: Orbital altitude offset exceeds +/- 50.0 m corridor.")
            elif ftype == "DEORBIT_TIMELINE_VIOLATION":
                c3_points -= 15.0
                c3_findings.append("High: Post-mission disposal lifetime exceeds 5.0-year ceiling.")
            elif ftype == "EXCESSIVE_CASUALTY_RISK":
                c3_points -= 10.0
                c3_findings.append("High: Atmospheric re-entry casualty risk > 1.0e-4.")

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
            "conjunction_miss_margins": CriterionResult(
                dimension_name="Autonomous Conjunction & Miss Margin Defense",
                max_points=30.0,
                points_awarded=c1_points,
                findings=c1_findings,
            ),
            "hippocratic_screening": CriterionResult(
                dimension_name="Hippocratic Screening & Covariance Realism",
                max_points=25.0,
                points_awarded=c2_points,
                findings=c2_findings,
            ),
            "slot_keeping_and_disposal": CriterionResult(
                dimension_name="Constellation Slot-Keeping & Post-Mission Disposal",
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
                f"PASSED ({total_score:.1f}/100.0). Code adheres to Commander Mira Vance's "
                "rigorous mega-constellation collision avoidance and orbital flight dynamics invariants."
            )
        else:
            summary = (
                f"REJECTED ({total_score:.1f}/100.0). Score is below the 95.0 threshold. "
                "Immediate self-remediation required."
            )

        return OrbitalTrafficEvaluationReport(
            total_score=total_score,
            is_passing=is_passing,
            criteria=criteria,
            summary=summary,
        )
