"""Geodynamo Core Fluid Dynamics and Magnetic Generation 100-Point Evaluation Rubric.

Embodying the quantitative evaluation standards of Dr. Lyra 'The Core' Sterling.
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
class GeodynamoEvaluationReport:
    """Holistic rubric assessment for planetary geodynamo core code."""
    total_score: float
    is_passing: bool
    criteria: Dict[str, CriterionResult] = field(default_factory=dict)
    summary: str = ""


class GeodynamoRubricEvaluator:
    """Evaluates planetary geodynamo code against Dr. Lyra Sterling's four pillars."""

    def evaluate(self, findings: List[Dict[str, str]], metrics: Dict[str, float]) -> GeodynamoEvaluationReport:
        """Calculate score based on findings and quantitative metrics."""
        # 1. Magnetostrophic MAC Balance & Dynamo Induction (30 pts)
        c1_findings: List[str] = []
        c1_points = 30.0

        for f in findings:
            ftype = f.get("type", "")
            if ftype == "NON_MAGNETOSTROPHIC_DYNAMICS":
                c1_points -= 30.0
                c1_findings.append("Critical: Pure hydrodynamic model ignoring magnetic Lorentz forces.")
            elif ftype == "SUB_CRITICAL_MAGNETIC_REYNOLDS":
                c1_points -= 20.0
                c1_findings.append("Critical: Magnetic Reynolds number below induction threshold (Rm < 50.0).")
            elif ftype == "EXCESSIVE_ROSSBY_NUMBER":
                c1_points -= 10.0
                c1_findings.append("High: Rossby number breaches planetary rotation limit (Ro > 1.0e-6).")
            elif ftype == "EXCESSIVE_EKMAN_NUMBER":
                c1_points -= 10.0
                c1_findings.append("High: Ekman number exceeds molecular viscous limit (Ek > 1.0e-14).")
            elif ftype == "ELSASSER_NUMBER_DIVERGENCE":
                c1_points -= 10.0
                c1_findings.append("High: Elsasser number outside MAC balance envelope [0.10, 10.0].")

        c1_points = max(0.0, c1_points)

        # 2. Thermal & Compositional Core Driving (25 pts)
        c2_findings: List[str] = []
        c2_points = 25.0

        for f in findings:
            ftype = f.get("type", "")
            if ftype == "SUB_ADIABATIC_CMB_FLUX":
                c2_points -= 15.0
                c2_findings.append("High: CMB heat flux below super-adiabatic threshold (Q_CMB < 10.0 TW).")
            elif ftype == "INSUFFICIENT_ICB_BUOYANCY":
                c2_points -= 10.0
                c2_findings.append("High: ICB light-element compositional buoyancy flux insufficient.")

        c2_points = max(0.0, c2_points)

        # 3. Geomagnetic Dipole Observable Envelope (25 pts)
        c3_findings: List[str] = []
        c3_points = 25.0

        for f in findings:
            ftype = f.get("type", "")
            if ftype == "WEAK_SURFACE_DIPOLE_FRACTION":
                c3_points -= 15.0
                c3_findings.append("High: Surface dipole energy fraction < 80.0%.")
            elif ftype == "EXCESSIVE_DIPOLE_TILT":
                c3_points -= 10.0
                c3_findings.append("Medium: Dipole tilt exceeds 15.0 degrees offset from spin axis.")

        c3_points = max(0.0, c3_points)

        # 4. Code Craftsmanship & Zero-Defect Standards (20 pts)
        c4_findings: List[str] = []
        c4_points = 20.0

        for f in findings:
            ftype = f.get("type", "")
            if ftype in ("LAZY_STUB", "EMPTY_FUNCTION_STUB"):
                c4_points -= 10.0
                c4_findings.append(f"Critical: Unfinished placeholder or empty stub detected: {f.get('message')}")
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
            "mac_balance_and_induction": CriterionResult(
                dimension_name="Magnetostrophic MAC Balance & Dynamo Induction",
                max_points=30.0,
                points_awarded=c1_points,
                findings=c1_findings,
            ),
            "core_thermal_compositional_driving": CriterionResult(
                dimension_name="Thermal & Compositional Core Driving",
                max_points=25.0,
                points_awarded=c2_points,
                findings=c2_findings,
            ),
            "geomagnetic_dipole_observables": CriterionResult(
                dimension_name="Geomagnetic Dipole Observable Envelope",
                max_points=25.0,
                points_awarded=c3_points,
                findings=c3_findings,
            ),
            "code_craftsmanship": CriterionResult(
                dimension_name="Code Craftsmanship & Zero-Defect Standards",
                max_points=20.0,
                points_awarded=c4_points,
                findings=c4_findings,
            ),
        }

        if is_passing:
            summary = (
                f"PASSED ({total_score:.1f}/100.0). Code adheres to Dr. Lyra Sterling's "
                "rigorous magnetostrophic geodynamo invariants."
            )
        else:
            summary = (
                f"REJECTED ({total_score:.1f}/100.0). Score is below the 95.0 threshold. "
                "Immediate self-remediation required."
            )

        return GeodynamoEvaluationReport(
            total_score=total_score,
            is_passing=is_passing,
            criteria=criteria,
            summary=summary,
        )
