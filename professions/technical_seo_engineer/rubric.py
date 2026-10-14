"""
Zane 'The Vector' Sterling - 100-Point Technical SEO & Growth Engineering Rubric.

Evaluates semantic HTML structure, canonical integrity, Core Web Vitals CLS risks,
Schema.org JSON-LD structured data, and social preview protocols.
Passing threshold: 85/100 points.
Veto criteria: Invalid H1 heading count (0 or >1), missing canonical tag, or unsized images causing CLS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.technical_seo_engineer.inspector import SEOInspectionReport, SEOMetrics


@dataclass
class SEORubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class TechnicalSEORubric:
    """Rigorous 100-point weighted evaluation rubric for technical SEO and search indexability."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: SEOInspectionReport) -> SEORubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Heading Hierarchy & Topical Authority (25 pts)
        # ----------------------------------------------------
        p1_score = 0
        if m.h1_count == 0:
            veto_reasons.append("Missing <h1>: Document has no primary semantic title, destroying search topical authority.")
            recommendations.append("Define exactly one descriptive <h1> tag expressing the primary topic and keyword.")
        elif m.h1_count > 1:
            veto_reasons.append(f"Multiple <h1> Headings ({m.h1_count} found): Multiple primary titles fragment search signals.")
            recommendations.append("Demote secondary <h1> tags to <h2> or <h3> to preserve hierarchical integrity.")
        else:
            p1_score += 25

        pillar_scores["heading_hierarchy"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Canonical Integrity & Duplicate Defense (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if not m.has_canonical_link:
            veto_reasons.append(
                "Missing Canonical URL: Document has no <link rel='canonical' href='...'>, risking severe duplicate penalties."
            )
            recommendations.append(
                "Inject a self-referential canonical URL tag: <link rel='canonical' href='https://yourdomain.com/path'>."
            )
        else:
            p2_score += 25

        pillar_scores["canonical_integrity"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: Core Web Vitals CLS Defense (20 pts)
        # ----------------------------------------------------
        p3_score = 0
        if m.images_missing_dimensions > 0:
            veto_reasons.append(
                f"Cumulative Layout Shift (CLS) Hazard: {m.images_missing_dimensions} image(s) lack explicit width and height."
            )
            recommendations.append(
                "Add explicit width and height attributes (or aspect-ratio CSS) to all <img> tags to reserve viewport layout."
            )
        else:
            p3_score += 20

        pillar_scores["cls_layout_stability"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: Schema.org JSON-LD Knowledge Graph (15 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.has_schema_jsonld:
            p4_score += 15
        else:
            p4_score += 4
            recommendations.append(
                "Inject structured Schema.org JSON-LD (e.g. Organization, WebSite, or SoftwareApplication) for Rich Snippet eligibility."
            )

        pillar_scores["schema_knowledge_graph"] = p4_score

        # ----------------------------------------------------
        # Pillar 5: Social Protocols & Metadata Hygiene (15 pts)
        # ----------------------------------------------------
        p5_score = 0
        if m.has_meta_description:
            p5_score += 5
        else:
            recommendations.append("Add a concise meta description between 120 and 160 characters.")

        if m.has_viewport_meta:
            p5_score += 5
        else:
            recommendations.append("Add '<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">'.")

        if m.has_opengraph_tags and m.has_twitter_card:
            p5_score += 5
        elif m.has_opengraph_tags or m.has_twitter_card:
            p5_score += 3
            recommendations.append("Complete social card tags (og:title, og:image, twitter:card='summary_large_image').")
        else:
            recommendations.append("Declare complete OpenGraph and Twitter social card tags.")

        pillar_scores["social_metadata_hygiene"] = p5_score

        total_score = sum(pillar_scores.values())

        # Veto enforcement
        veto_triggered = len(veto_reasons) > 0
        if veto_triggered and total_score >= self.PASSING_THRESHOLD:
            total_score = 65

        is_certified = (total_score >= self.PASSING_THRESHOLD) and not veto_triggered

        return SEORubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
