"""
Zane 'The Vector' Sterling - Blind Technical SEO Critic.

Evaluates HTML documents, meta tags, and structured data strictly against
Core Web Vitals stability, single H1 hierarchy, and canonical indexability standards.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.technical_seo_engineer.inspector import SEOSystemInspector, SEOInspectionReport
from professions.technical_seo_engineer.rubric import TechnicalSEORubric, SEORubricEvaluation


@dataclass
class SEODefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    ranking_impact: str
    actionable_fix: str


@dataclass
class SEODefectLedger:
    verdict: str  # CERTIFIED_ORGANIC_SOVEREIGN or REJECTED_INDEXABILITY_FAILURE
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[SEODefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindSEOCritic:
    """Search engine adversary reviewing documents for indexing penalties, layout shifts, and semantic flaws."""

    def __init__(self):
        self.inspector = SEOSystemInspector()
        self.rubric = TechnicalSEORubric()

    def review(self, html_input: Any) -> SEODefectLedger:
        """
        Runs objective inspection and adversarial rubric scoring, producing an SEO Defect Ledger.
        """
        report: SEOInspectionReport = self.inspector.inspect(html_input)
        eval_result: SEORubricEvaluation = self.rubric.evaluate(report)

        defects: List[SEODefect] = []

        # 1. Critical violations -> FATAL defects
        for i, violation in enumerate(report.critical_violations, start=1):
            if "h1" in violation.lower():
                title = "H1 Heading Hierarchy Breakdown"
                impact = "Dilutes primary keyword signals and topical indexing confidence in search engines."
                fix = "Ensure exactly one semantic <h1> element exists per document."
            elif "canonical" in violation.lower():
                title = "Missing Canonical URL Declaration"
                impact = "Exposes page to duplicate content penalties and internal link equity fragmentation."
                fix = "Inject '<link rel=\"canonical\" href=\"...\">' in document <head>."
            elif "layout shift" in violation.lower() or "cls" in violation.lower():
                title = "Core Web Vitals Cumulative Layout Shift (CLS)"
                impact = "Unsized images jump upon rendering, degrading page experience metrics and rankings."
                fix = "Add explicit width and height attributes (or CSS aspect-ratio) to all <img> tags."
            else:
                title = "Critical Technical SEO Violation"
                impact = "Substantially impairs search engine crawling, indexing, or ranking."
                fix = "Refactor HTML document to Zane Sterling Technical SEO standards."

            defects.append(
                SEODefect(
                    defect_id=f"SEO-FATAL-{i:03d}",
                    severity="FATAL",
                    title=title,
                    description=violation,
                    ranking_impact=impact,
                    actionable_fix=fix
                )
            )

        # 2. Veto reasons
        for j, reason in enumerate(eval_result.veto_reasons, start=len(defects) + 1):
            if not any(d.description == reason for d in defects):
                defects.append(
                    SEODefect(
                        defect_id=f"SEO-FATAL-{j:03d}",
                        severity="FATAL",
                        title="Indexability Integrity Veto",
                        description=reason,
                        ranking_impact="Disqualifies document from production deployment under Zane Sterling protocol.",
                        actionable_fix="Resolve the underlying technical SEO violation immediately."
                    )
                )

        # 3. Warnings -> HIGH / MEDIUM defects
        for k, warning in enumerate(report.warnings, start=len(defects) + 1):
            severity = "HIGH" if "schema" in warning.lower() or "alt" in warning.lower() else "MEDIUM"
            if "schema" in warning.lower():
                title = "Missing Schema.org JSON-LD Structured Data"
                impact = "Disqualifies page from Google Rich Snippets and Knowledge Graph cards."
                fix = "Inject '<script type=\"application/ld+json\">' declaring relevant Schema entities."
            elif "alt" in warning.lower():
                title = "Missing Image Alt Attributes"
                impact = "Harms image search indexing and violates web accessibility standards."
                fix = "Add descriptive, keyword-rich alt text to non-decorative images."
            elif "description" in warning.lower():
                title = "Missing Meta Description"
                impact = "Lowers click-through rates (CTR) in search engine result pages (SERPs)."
                fix = "Add '<meta name=\"description\" content=\"...\">' with 120-160 characters."
            else:
                title = "SEO Suboptimality"
                impact = "Suboptimal social sharing previews or mobile display."
                fix = "Complete missing OpenGraph, Twitter, or viewport meta tags."

            defects.append(
                SEODefect(
                    defect_id=f"SEO-WARN-{k:03d}",
                    severity=severity,
                    title=title,
                    description=warning,
                    ranking_impact=impact,
                    actionable_fix=fix
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = (
            "CERTIFIED_ORGANIC_SOVEREIGN"
            if eval_result.is_certified and fatal_count == 0
            else "REJECTED_INDEXABILITY_FAILURE"
        )

        summary = (
            f"Zane Sterling SEO Review: Score {eval_result.total_score}/100. "
            f"Verdict: {verdict}. Fatal defects: {fatal_count}, High defects: {high_count}."
        )

        return SEODefectLedger(
            verdict=verdict,
            score=eval_result.total_score,
            passing_threshold=eval_result.passing_threshold,
            is_certified=eval_result.is_certified and fatal_count == 0,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
