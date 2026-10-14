"""
Aria Solano - Brand Identity & Visual System Reference Standards.

This module codifies empirical visual design standards, the 60-30-10 color balance,
mathematical modular typography scales, and vector precision benchmarks.
"""

from typing import Dict, Any, List


COLOR_DISTRIBUTION_BENCHMARKS: Dict[str, Any] = {
    "dominant_canvas_pct": 60.0,      # Background, neutral surface, canvas
    "secondary_structure_pct": 30.0,  # Cards, navigation, typography, borders
    "accent_energy_pct": 10.0,        # Key CTA, focal icons, brand highlights
    "min_wcag_contrast_normal": 4.5,
    "min_wcag_contrast_large": 3.0,
    "curated_accent_hues": {
        "electric_indigo": "#6366F1",
        "kinetic_amber": "#F59E0B",
        "cyber_emerald": "#10B981",
        "sovereign_rose": "#F43F5E",
        "celestial_cyan": "#06B6D4"
    }
}

MODULAR_TYPOGRAPHY_SCALES: Dict[str, Dict[str, Any]] = {
    "major_third": {
        "ratio": 1.250,
        "use_case": "Standard SaaS, modern enterprise applications",
        "scale": {
            "caption": "0.80rem",
            "body": "1.00rem",
            "h4": "1.25rem",
            "h3": "1.563rem",
            "h2": "1.953rem",
            "h1": "2.441rem",
            "display": "3.052rem"
        }
    },
    "perfect_fourth": {
        "ratio": 1.333,
        "use_case": "Marketing landing pages, editorial storytelling",
        "scale": {
            "caption": "0.75rem",
            "body": "1.00rem",
            "h4": "1.333rem",
            "h3": "1.777rem",
            "h2": "2.369rem",
            "h1": "3.157rem",
            "display": "4.209rem"
        }
    },
    "golden_ratio": {
        "ratio": 1.618,
        "use_case": "Luxury, dramatic brand showcases, posters",
        "scale": {
            "caption": "0.618rem",
            "body": "1.00rem",
            "h4": "1.618rem",
            "h3": "2.618rem",
            "h2": "4.236rem",
            "h1": "6.854rem",
            "display": "11.089rem"
        }
    }
}

VECTOR_PRECISION_STANDARDS: Dict[str, Any] = {
    "standard_icon_viewbox": "0 0 24 24",
    "standard_stroke_width": 2.0,
    "stroke_linecap": "round",
    "stroke_linejoin": "round",
    "min_logo_clear_space_multiplier": 1.0  # 1x mark dimension margin
}

TOXIC_BRAND_ANTI_PATTERNS: List[Dict[str, str]] = [
    {
        "id": "raw_primary_defaults",
        "indicator": "Using uncurated harsh hex colors (#0000FF, #FF0000, #00FF00) without design system tonal scaling.",
        "risk": "Visual amateurism; causes eye fatigue and undermines user trust in product credibility.",
        "severity": "FATAL"
    },
    {
        "id": "violating_60_30_10",
        "indicator": "Using accent color as background across > 30% of viewport surface.",
        "risk": "Destroys visual hierarchy and blinds the user to actual Call-To-Action focal points.",
        "severity": "FATAL"
    },
    {
        "id": "typographic_anarchy",
        "indicator": "Using 3 or more unrelated font families within the same brand interface.",
        "risk": "Visual dissonance, brand identity schizophrenia, and inflated web font payload size.",
        "severity": "FATAL"
    },
    {
        "id": "malformed_vector_svg",
        "indicator": "SVG icons or logos missing viewBox attribute or containing raster bitmap payloads.",
        "risk": "Assets blur and scale defectively on Retina/HiDPI screens; unresponsive UI distortion.",
        "severity": "HIGH"
    },
    {
        "id": "logo_clear_space_crowding",
        "indicator": "Placing navigation elements, headers, or buttons within 1x mark height of the logo.",
        "risk": "Suffocates the brand mark and destroys visual gravitas.",
        "severity": "HIGH"
    }
]


class BrandReferenceLibrary:
    """Provides empirical visual design benchmarks, typography scales, and brand standards."""

    @staticmethod
    def get_color_benchmarks() -> Dict[str, Any]:
        return COLOR_DISTRIBUTION_BENCHMARKS

    @staticmethod
    def get_typography_scales() -> Dict[str, Dict[str, Any]]:
        return MODULAR_TYPOGRAPHY_SCALES

    @staticmethod
    def get_vector_standards() -> Dict[str, Any]:
        return VECTOR_PRECISION_STANDARDS

    @staticmethod
    def get_toxic_anti_patterns() -> List[Dict[str, str]]:
        return TOXIC_BRAND_ANTI_PATTERNS
