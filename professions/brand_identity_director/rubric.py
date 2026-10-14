"""
Aria Solano - 100-Point Brand Identity & Visual System Rubric.

Evaluates brand guidelines, color palettes, typography systems, and vector assets.
Passing threshold: 85/100 points.
Veto criteria: Raw primary defaults, typographic anarchy (3+ fonts), or malformed SVGs.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.brand_identity_director.inspector import BrandInspectionReport, BrandMetrics


@dataclass
class BrandRubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class BrandIdentityRubric:
    """Rigorous 100-point weighted evaluation rubric for global brand systems."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: BrandInspectionReport) -> BrandRubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Color Theory & 60-30-10 Balance (25 pts)
        # ----------------------------------------------------
        p1_score = 0
        if m.has_raw_primary_colors:
            veto_reasons.append("Raw primary hex codes detected (#0000FF, #FF0000); destroys visual authority.")
            recommendations.append("Replace raw hex primaries with a tailored 9-shade HSL semantic palette.")
        else:
            p1_score += 15

        if m.has_60_30_10_balance:
            p1_score += 10
        else:
            p1_score += 3
            recommendations.append("Structure color tokens into 60% dominant base, 30% structural secondary, and 10% accent.")

        pillar_scores["color_theory_and_balance"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Mathematical Typography Hierarchy (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if m.font_families_count >= 3:
            veto_reasons.append(f"Typographic Anarchy: {m.font_families_count} font families create cognitive friction.")
            recommendations.append("Reduce font families to maximum 2 complementary typefaces (e.g. Outfit + Inter).")
        else:
            p2_score += 15

        if m.has_modular_type_scale:
            p2_score += 10
        else:
            p2_score += 4
            recommendations.append("Align heading and body sizes to a mathematical modular scale ratio (1.250 or 1.333).")

        pillar_scores["typography_hierarchy"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: Vector Precision & Asset Integrity (20 pts)
        # ----------------------------------------------------
        p3_score = 0
        if not m.has_svg_viewbox:
            veto_reasons.append("Vector SVG missing viewBox attribute; causes unresponsive distortion on high-DPI viewports.")
            recommendations.append("Declare viewBox='0 0 24 24' and strip hardcoded absolute width/height dimensions.")
        else:
            p3_score += 20

        pillar_scores["vector_precision"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: Logo Sovereignty & Clear-Space (15 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.has_logo_clear_space:
            p4_score += 15
        else:
            p4_score += 5
            recommendations.append("Define explicit logo clear-space boundary equal to 1x the mark height/width.")

        pillar_scores["logo_sovereignty"] = p4_score

        # ----------------------------------------------------
        # Pillar 5: Iconographic & Brand Voice Cohesion (15 pts)
        # ----------------------------------------------------
        p5_score = 0
        if m.has_unified_icon_stroke:
            p5_score += 8
        else:
            recommendations.append("Unify icon stroke-width to standard 2.0px with round linecaps across all glyphs.")

        if m.brand_archetype != "undefined":
            p5_score += 7
        else:
            p5_score += 3
            recommendations.append("Define core Brand Archetype (Sovereign, Magician, Sage, Rebel) to anchor voice and visual tone.")

        pillar_scores["brand_voice_cohesion"] = p5_score

        total_score = sum(pillar_scores.values())

        # Veto enforcement
        veto_triggered = len(veto_reasons) > 0
        if veto_triggered and total_score >= self.PASSING_THRESHOLD:
            total_score = 70

        is_certified = (total_score >= self.PASSING_THRESHOLD) and not veto_triggered

        return BrandRubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
