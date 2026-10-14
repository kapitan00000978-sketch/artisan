"""
Aria Solano - Blind Brand Identity & Visual System Critic.

Evaluates brand systems strictly against emotional color theory,
modular typographic scales, and vector precision standards.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.brand_identity_director.inspector import BrandIdentityInspector, BrandInspectionReport
from professions.brand_identity_director.rubric import BrandIdentityRubric, BrandRubricEvaluation


@dataclass
class BrandDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    visual_impact: str
    actionable_fix: str


@dataclass
class BrandDefectLedger:
    verdict: str  # CERTIFIED_LUMINARY_BRAND or REJECTED_VISUAL_DISSONANCE
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[BrandDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindBrandCritic:
    """Visual identity adversary reviewing brand systems for emotional resonance and aesthetic harmony."""

    def __init__(self):
        self.inspector = BrandIdentityInspector()
        self.rubric = BrandIdentityRubric()

    def review(self, brand_input: Any) -> BrandDefectLedger:
        """
        Runs objective inspection and adversarial rubric scoring, producing a Brand Defect Ledger.
        """
        report: BrandInspectionReport = self.inspector.inspect(brand_input)
        eval_result: BrandRubricEvaluation = self.rubric.evaluate(report)

        defects: List[BrandDefect] = []

        # 1. Critical violations -> FATAL defects
        for i, violation in enumerate(report.critical_violations, start=1):
            if "primary colors" in violation.lower():
                title = "Raw Uncurated Primary Hex Defaults"
                impact = "Interface looks amateurish and dated; destroys user trust and visual gravitas."
                fix = "Adopt a curated 60-30-10 palette using tailored HSL tones (e.g. Electric Indigo #6366F1)."
            elif "typographic anarchy" in violation.lower():
                title = "Typographic Anarchy (3+ Font Families)"
                impact = "Visual noise, uncohesive brand voice, and bloated web font loading payloads."
                fix = "Prune to maximum two paired typefaces (e.g. Outfit for Headings + Inter for Body)."
            elif "viewbox" in violation.lower():
                title = "Malformed Vector SVG (Missing viewBox)"
                impact = "Vector icons render clipped or blurry on responsive viewports and HiDPI screens."
                fix = "Inject viewBox='0 0 24 24' and strip hardcoded absolute pixel widths."
            else:
                title = "Critical Brand Identity Defect"
                impact = "Compromises brand coherence and visual memorability."
                fix = "Align brand tokens to Aria Solano Luminary standards."

            defects.append(
                BrandDefect(
                    defect_id=f"BRAND-FATAL-{i:03d}",
                    severity="FATAL",
                    title=title,
                    description=violation,
                    visual_impact=impact,
                    actionable_fix=fix
                )
            )

        # 2. Veto reasons
        for j, reason in enumerate(eval_result.veto_reasons, start=len(defects) + 1):
            if not any(d.description == reason for d in defects):
                defects.append(
                    BrandDefect(
                        defect_id=f"BRAND-FATAL-{j:03d}",
                        severity="FATAL",
                        title="Brand Integrity Veto",
                        description=reason,
                        visual_impact="Disqualifying visual dissonance.",
                        actionable_fix="Restructure design tokens according to Luminary benchmarks."
                    )
                )

        # 3. Warnings -> HIGH / MEDIUM defects
        for k, warning in enumerate(report.warnings, start=len(defects) + 1):
            sev = "HIGH" if "clear-space" in warning.lower() or "modular" in warning.lower() else "MEDIUM"
            defects.append(
                BrandDefect(
                    defect_id=f"BRAND-WARN-{k:03d}",
                    severity=sev,
                    title="Brand Polish Deficiency",
                    description=warning,
                    visual_impact="Suboptimal hierarchy, crowded logo mark, or iconographic inconsistency.",
                    actionable_fix="Enforce 1x logo clear-space and align typography to a modular scale ratio."
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = "CERTIFIED_LUMINARY_BRAND" if eval_result.is_certified else "REJECTED_VISUAL_DISSONANCE"

        if eval_result.is_certified:
            summary = (
                f"LUMINARY CERTIFIED (Score: {eval_result.total_score}/100). "
                "Harmonious 60-30-10 color balance verified, mathematical modular typography locked, "
                "vector assets normalized, and logo safe-zones respected. The visual identity leaves an indelible mark."
            )
        else:
            summary = (
                f"REJECTED BY THE BRAND DIRECTOR (Score: {eval_result.total_score}/100, Threshold: {eval_result.passing_threshold}). "
                f"Detected {fatal_count} fatal aesthetic flaws and {high_count} brand polish deficiencies. "
                "The visual system lacks soul, hierarchy, and vector precision."
            )

        return BrandDefectLedger(
            verdict=verdict,
            score=eval_result.total_score,
            passing_threshold=eval_result.passing_threshold,
            is_certified=eval_result.is_certified,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
