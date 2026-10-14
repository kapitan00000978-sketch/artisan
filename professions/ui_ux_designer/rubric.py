"""
Elena Rostova's Weighted UI/UX Design Rubric
Mathematical, uncompromising evaluation of visual hierarchy, ergonomics, and aesthetics.
"""

from typing import Dict, Any, List, Optional


class ElenaDesignRubric:
    """Elena Rostova's 100-point weighted design evaluation rubric."""

    DIMENSIONS: Dict[str, Dict[str, Any]] = {
        "typography_hierarchy": {
            "title": "Typography Scale & Hierarchical Proportion",
            "weight": 0.25,
            "benchmark": "H1/Body scale 2.5x-4.0x with curated modern display font (Inter/Outfit)."
        },
        "contrast_accessibility": {
            "title": "WCAG 2.1 Color Contrast (AA/AAA)",
            "weight": 0.25,
            "benchmark": "Minimum 4.5:1 for body copy; 7.0:1 for AAA certification."
        },
        "spatial_grid_rhythm": {
            "title": "8pt Spatial Grid Consistency",
            "weight": 0.20,
            "benchmark": ">= 75% of paddings, margins, and gaps conforming strictly to 8px intervals."
        },
        "liquid_glass_depth": {
            "title": "Liquid Glass & Atmospheric Elevation",
            "weight": 0.20,
            "benchmark": "Layered frosted glass (backdrop-filter: blur), ambient radial lighting, specular borders."
        },
        "micro_interactions": {
            "title": "Micro-Interactions & Interactive States",
            "weight": 0.10,
            "benchmark": "Fluid cubic-bezier hover states, scale transitions, and tactile feedback."
        }
    }

    def evaluate(self, metrics: Dict[str, Any], benchmark_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculates itemized and composite design score out of 100."""
        target_metrics = benchmark_profile.get("metrics", {}) if benchmark_profile else {}
        min_contrast = target_metrics.get("min_contrast_ratio", 4.5)
        min_grid_pct = target_metrics.get("target_grid_adherence_pct", 75.0)
        scores: Dict[str, Any] = {}

        # 1. Typography Hierarchy (0-10)
        scale = metrics.get("scale_ratio", 1.0)
        fonts = metrics.get("font_families", [])
        has_curated_font = any(f.lower() in ("inter", "outfit", "plus jakarta sans", "sf pro", "helvetica neue") for f in fonts)

        if 2.2 <= scale <= 4.5:
            t_score = 10.0 if has_curated_font else 8.5
        elif (1.8 <= scale < 2.2) or (4.5 < scale <= 5.0):
            t_score = 8.0
        elif 1.4 <= scale < 1.8:
            t_score = 5.5
        else:
            t_score = 3.0

        scores["typography_hierarchy"] = {
            "score": t_score,
            "measured": f"{scale}x scale (H1: {metrics.get('h1_font_size')}px / Body: {metrics.get('body_font_size')}px)",
            "benchmark": "2.2x - 4.5x scale",
            "status": "PASS" if t_score >= 8.0 else "FAIL"
        }

        # 2. Contrast & Accessibility (0-10)
        contrast = metrics.get("contrast_ratio", 1.0)
        if contrast >= 7.0:
            c_score = 10.0
        elif contrast >= 4.5:
            c_score = 8.5
        elif contrast >= 3.0:
            c_score = 5.0
        else:
            c_score = max(1.0, round(contrast * 1.5, 1))

        scores["contrast_accessibility"] = {
            "score": c_score,
            "measured": f"{contrast}:1",
            "benchmark": ">= 4.5:1",
            "status": "PASS" if c_score >= 8.5 else "FAIL"
        }

        # 3. Spatial Grid Rhythm (0-10)
        grid_pct = metrics.get("grid_8pt_adherence_pct", 0.0)
        if grid_pct >= 75.0:
            g_score = 10.0
        elif grid_pct >= 60.0:
            g_score = 8.5
        elif grid_pct >= 40.0:
            g_score = 6.0
        else:
            g_score = max(2.0, round(grid_pct / 10.0, 1))

        scores["spatial_grid_rhythm"] = {
            "score": g_score,
            "measured": f"{grid_pct}% matching 8pt grid",
            "benchmark": ">= 75% adherence",
            "status": "PASS" if g_score >= 8.0 else "FAIL"
        }

        # 4. Liquid Glass & Atmospheric Depth (0-10)
        has_glass = metrics.get("has_liquid_glass", False)
        has_glow = metrics.get("has_ambient_glow", False)
        if has_glass and has_glow:
            d_score = 10.0
        elif has_glass or has_glow:
            d_score = 7.0
        else:
            d_score = 2.5

        scores["liquid_glass_depth"] = {
            "score": d_score,
            "measured": "Layered frosted glass + ambient glow" if (has_glass and has_glow) else ("Partial depth" if (has_glass or has_glow) else "Flat solid opaque CSS"),
            "benchmark": "Layered frosted glass + ambient lighting",
            "status": "PASS" if d_score >= 8.0 else "FAIL"
        }

        # 5. Micro-Interactions (0-10)
        has_anim = metrics.get("has_micro_animations", False)
        m_score = 10.0 if has_anim else 4.0

        scores["micro_interactions"] = {
            "score": m_score,
            "measured": "Smooth transitions / animations present" if has_anim else "Static zero-transition elements",
            "benchmark": "Smooth cubic-bezier transitions on interactive elements",
            "status": "PASS" if m_score >= 8.0 else "FAIL"
        }

        # Weighted calculation
        total_score = round(sum(
            scores[dim]["score"] * self.DIMENSIONS[dim]["weight"]
            for dim in self.DIMENSIONS
        ) * 10, 1)

        return {
            "evaluator": "Elena Rostova (Principal UI/UX Designer)",
            "total_score": total_score,
            "passing_threshold": 85.0,
            "passed": total_score >= 85.0,
            "dimensions": scores
        }
