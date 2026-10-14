"""
Step 4 — Weighted Empirical Rubrics (Rubrika)
Turns subjective opinion into mathematical judgment.
Every criterion has a numeric 0-10 score, an empirical formula, and a specific weight.
"""

from typing import Dict, Any, List


class RubricEngine:
    """
    Evaluates raw objective measurements against weighted empirical rubrics.
    Produces deterministic, justifiable scores instead of vague feelings.
    """

    RUBRIC_SPEC: Dict[str, Dict[str, Any]] = {
        "contrast_accessibility": {
            "title": "Color Contrast & Accessibility (WCAG 2.1)",
            "weight": 0.25,
            "description": "Text to background contrast ratio (Target >= 4.5:1 for AA, >= 7:1 for AAA)."
        },
        "typography_hierarchy": {
            "title": "Typography Scale & Proportion",
            "weight": 0.25,
            "description": "Visual weight ratio between H1 and Body copy (Target: 2.5x to 4.0x)."
        },
        "spatial_grid_harmony": {
            "title": "8pt Spatial Grid Consistency",
            "weight": 0.20,
            "description": "Percentage of layout margins, paddings, and heights adhering to 8px increments."
        },
        "content_readability": {
            "title": "Copy Clarity & Readability Ease",
            "weight": 0.15,
            "description": "Flesch-Kincaid Reading Ease (Target: 55 to 75 for optimal engagement)."
        },
        "visual_depth_modernity": {
            "title": "Aesthetic Depth & Modern Layering",
            "weight": 0.15,
            "description": "Presence of frosted glass elevation, ambient glow, and high-fidelity depth."
        }
    }

    def evaluate(self, measurements: Dict[str, Any], reference_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates scores (0.0 to 10.0) for each rubric dimension and computes weighted composite score (0 to 100).
        """
        line_items: Dict[str, Any] = {}

        # 1. Contrast Score
        contrast = measurements.get("contrast_ratio", 1.0)
        if contrast >= 7.0:
            c_score = 10.0
        elif contrast >= 4.5:
            c_score = 8.0
        elif contrast >= 3.0:
            c_score = 5.0
        else:
            c_score = max(1.0, round(contrast * 1.5, 1))

        line_items["contrast_accessibility"] = {
            "score": c_score,
            "measured": f"{contrast}:1",
            "benchmark": ">= 4.5:1",
            "status": "PASS" if c_score >= 8.0 else "FAIL"
        }

        # 2. Typography Hierarchy Score
        scale_ratio = measurements.get("typography_scale_ratio", 1.0)
        if 2.5 <= scale_ratio <= 4.5:
            t_score = 10.0
        elif 2.0 <= scale_ratio < 2.5 or 4.5 < scale_ratio <= 5.5:
            t_score = 8.0
        elif 1.5 <= scale_ratio < 2.0:
            t_score = 5.0
        else:
            t_score = 3.0

        line_items["typography_hierarchy"] = {
            "score": t_score,
            "measured": f"{scale_ratio}x scale ratio (H1: {measurements.get('h1_font_size_px')}px / Body: {measurements.get('body_font_size_px')}px)",
            "benchmark": "2.5x - 4.0x scale",
            "status": "PASS" if t_score >= 8.0 else "FAIL"
        }

        # 3. Spatial Grid Consistency
        grid_pct = measurements.get("grid_8pt_adherence_pct", 0.0)
        if grid_pct >= 80.0:
            g_score = 10.0
        elif grid_pct >= 60.0:
            g_score = 7.5
        elif grid_pct >= 40.0:
            g_score = 5.0
        else:
            g_score = max(2.0, round(grid_pct / 10.0, 1))

        line_items["spatial_grid_harmony"] = {
            "score": g_score,
            "measured": f"{grid_pct}% matching 8pt grid",
            "benchmark": ">= 75% adherence",
            "status": "PASS" if g_score >= 7.5 else "FAIL"
        }

        # 4. Readability Score
        readability = measurements.get("flesch_readability", 50.0)
        target_readability = reference_profile.get("flesch_reading_ease_target", 65.0)
        diff = abs(readability - target_readability)
        if diff <= 10.0:
            r_score = 10.0
        elif diff <= 20.0:
            r_score = 7.5
        elif diff <= 35.0:
            r_score = 5.0
        else:
            r_score = 3.0

        line_items["content_readability"] = {
            "score": r_score,
            "measured": f"{readability} Flesch ease",
            "benchmark": f"Target: ~{target_readability}",
            "status": "PASS" if r_score >= 7.5 else "FAIL"
        }

        # 5. Visual Depth & Modernity
        has_glass = measurements.get("has_glassmorphism", False)
        v_score = 10.0 if has_glass else 3.5

        line_items["visual_depth_modernity"] = {
            "score": v_score,
            "measured": "Layered frosted glass + elevation detected" if has_glass else "Flat CSS, zero layered glassmorphism",
            "benchmark": "Modern layered frosted glass & depth",
            "status": "PASS" if v_score >= 8.0 else "FAIL"
        }

        # Compute total weighted score (0 to 100)
        weighted_sum = sum(
            line_items[k]["score"] * self.RUBRIC_SPEC[k]["weight"]
            for k in self.RUBRIC_SPEC
        )
        total_score = round(weighted_sum * 10, 1)

        return {
            "total_score": total_score,
            "passed": total_score >= 80.0,
            "dimensions": line_items,
            "rubric_spec": self.RUBRIC_SPEC
        }
