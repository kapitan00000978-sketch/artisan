"""
Step 5 — Blind Independent Critic (Mustaqil Tanqidchi)
The Critic NEVER looks at the author's internal code or implementation excuses.
It evaluates ONLY the resulting artifact: rendered metrics, visual outputs, and rubrics.
Produces an objective, structured defect ledger.
"""

from typing import Dict, Any, List


class BlindCritic:
    """
    Independent Critic that judges strictly by outcomes and quantitative rubrics.
    Does not rationalize or excuse defects based on implementation complexity.
    """

    def __init__(self, rubric_threshold: float = 80.0):
        self.rubric_threshold = rubric_threshold

    def audit(self, rubric_result: Dict[str, Any], measurements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits evaluation outcomes blindly and compiles a structured defect ledger.
        """
        total_score = rubric_result["total_score"]
        dimensions = rubric_result["dimensions"]
        defect_ledger: List[Dict[str, Any]] = []

        # 1. Audit contrast
        contrast_data = dimensions.get("contrast_accessibility", {})
        if contrast_data.get("status") == "FAIL":
            defect_ledger.append({
                "dimension": "contrast_accessibility",
                "severity": "CRITICAL",
                "issue": f"Text contrast ratio is {contrast_data.get('measured')}, failing WCAG AA threshold of {contrast_data.get('benchmark')}.",
                "fix_directive": "Darken background or brighten foreground text to achieve at least 4.5:1 contrast."
            })

        # 2. Audit typography scale
        typo_data = dimensions.get("typography_hierarchy", {})
        if typo_data.get("status") == "FAIL":
            defect_ledger.append({
                "dimension": "typography_hierarchy",
                "severity": "MAJOR",
                "issue": f"Hero heading lacks visual dominance: {typo_data.get('measured')} (Expected {typo_data.get('benchmark')}).",
                "fix_directive": "Scale H1 font size to at least 2.5x the body copy size (e.g., 48px-64px for 16px body)."
            })

        # 3. Audit spatial grid
        grid_data = dimensions.get("spatial_grid_harmony", {})
        if grid_data.get("status") == "FAIL":
            defect_ledger.append({
                "dimension": "spatial_grid_harmony",
                "severity": "MINOR",
                "issue": f"Layout spacing is erratic ({grid_data.get('measured')}). Violates systematic 8pt rhythm.",
                "fix_directive": "Standardize all margins, paddings, and container gaps to multiples of 8px (8, 16, 24, 32, 48, 64px)."
            })

        # 4. Audit visual depth
        depth_data = dimensions.get("visual_depth_modernity", {})
        if depth_data.get("status") == "FAIL":
            defect_ledger.append({
                "dimension": "visual_depth_modernity",
                "severity": "MAJOR",
                "issue": "Aesthetic depth is flat and reminiscent of entry-level mockups.",
                "fix_directive": "Implement layered frosted glass elevation (backdrop-filter: blur), subtle ambient glow, and specular borders."
            })

        # 5. Security & Link Hygiene
        if measurements.get("unsecured_links_count", 0) > 0:
            defect_ledger.append({
                "dimension": "security_hygiene",
                "severity": "CRITICAL",
                "issue": f"Found {measurements['unsecured_links_count']} link(s) with target='_blank' lacking rel='noopener noreferrer'.",
                "fix_directive": "Add rel='noopener noreferrer' to prevent reverse tabnabbing attacks."
            })

        # 6. Mobile Responsiveness
        if not measurements.get("has_viewport_meta", False):
            defect_ledger.append({
                "dimension": "mobile_responsiveness",
                "severity": "BLOCKER",
                "issue": "Missing <meta name='viewport'> tag. Page renders broken on mobile devices.",
                "fix_directive": "Insert standard <meta name='viewport' content='width=device-width, initial-scale=1.0'> tag."
            })

        passed = (total_score >= self.rubric_threshold) and (len([d for d in defect_ledger if d["severity"] in ("CRITICAL", "BLOCKER")]) == 0)

        verdict = "CERTIFIED_WORLD_CLASS" if passed else "REJECTED_REMEDIATION_REQUIRED"

        return {
            "verdict": verdict,
            "passed": passed,
            "total_score": total_score,
            "threshold": self.rubric_threshold,
            "defects_count": len(defect_ledger),
            "defect_ledger": defect_ledger
        }
