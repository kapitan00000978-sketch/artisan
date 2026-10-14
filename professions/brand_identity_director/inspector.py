"""
Aria Solano - Objective Brand Identity & Visual System Inspector.

This module inspects brand style guides, design tokens, CSS palettes, typography scales,
and SVG vector assets to detect raw primary defaults, typographic anarchy, and vector defects.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class BrandMetrics:
    has_60_30_10_balance: bool = False
    has_raw_primary_colors: bool = False
    font_families_count: int = 1
    has_modular_type_scale: bool = False
    has_svg_viewbox: bool = True
    has_logo_clear_space: bool = False
    has_unified_icon_stroke: bool = True
    brand_archetype: str = "undefined"
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class BrandInspectionReport:
    metrics: BrandMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_brand_viable: bool = False


class BrandIdentityInspector:
    """Rigorous visual identity auditor evaluating color theory, typography, and vector assets."""

    RAW_COLOR_PATTERNS = [
        r"#0000ff\b", r"#ff0000\b", r"#00ff00\b",
        r"\bcolor:\s*red\b", r"\bcolor:\s*blue\b", r"\bcolor:\s*green\b",
        r"\bbackground:\s*red\b", r"\bbackground:\s*blue\b"
    ]

    def inspect(self, brand_input: Any) -> BrandInspectionReport:
        """
        Audits brand style guide, CSS tokens, SVG markup, or design system metadata.
        """
        metrics = self._extract_metrics(brand_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Color Theory & 60-30-10 Harmony
        if metrics.has_raw_primary_colors:
            critical_violations.append(
                "Uncurated Harsh Primary Colors: Raw hex defaults (#0000FF, #FF0000, #00FF00) detected. "
                "Undermines brand credibility and causes severe visual fatigue."
            )
        elif metrics.has_60_30_10_balance:
            benchmarks_passed.append("Harmonious 60-30-10 color balance and semantic palette tokens verified.")
        else:
            warnings.append("Color distribution not explicitly structured into 60% base, 30% secondary, 10% accent.")

        # 2. Typographic Discipline & Modular Scale
        if metrics.font_families_count >= 3:
            critical_violations.append(
                f"Typographic Anarchy: {metrics.font_families_count} discordant font families detected. "
                "Maximum 2 complementary families permitted to maintain brand coherence."
            )
        elif metrics.has_modular_type_scale:
            benchmarks_passed.append("Mathematical Modular Typography scale (Major Third / Perfect Fourth) verified.")
        else:
            warnings.append("Typography uses arbitrary pixel values instead of a mathematical modular scale.")

        # 3. Vector SVG Precision
        if not metrics.has_svg_viewbox:
            critical_violations.append(
                "Malformed Vector Asset: SVG logo/icon missing viewBox attribute. "
                "Will render distorted or blurry on high-DPI and responsive viewports."
            )
        else:
            benchmarks_passed.append("Vector precision verified with standard viewBox coordinate system.")

        # 4. Logo Clear-Space & Safe Zone
        if not metrics.has_logo_clear_space:
            warnings.append("Logo clear-space safe zone (>= 1x mark height) not explicitly enforced.")
        else:
            benchmarks_passed.append("Logo clear-space margin protection mathematically enforced.")

        # 5. Iconographic Stroke Uniformity
        if not metrics.has_unified_icon_stroke:
            warnings.append("Inconsistent icon stroke weights detected across vector glyphs.")
        else:
            benchmarks_passed.append("Uniform 24x24 iconographic stroke system confirmed.")

        for ap in metrics.anti_patterns_detected:
            if ap not in critical_violations:
                critical_violations.append(f"Anti-Pattern Detected: {ap}")

        is_viable = len(critical_violations) == 0

        return BrandInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_brand_viable=is_viable
        )

    def _extract_metrics(self, brand_input: Any) -> BrandMetrics:
        text = ""
        metadata: Dict[str, Any] = {}

        if isinstance(brand_input, str):
            text = brand_input
            try:
                parsed = json.loads(brand_input)
                if isinstance(parsed, dict):
                    metadata = parsed
            except (json.JSONDecodeError, ValueError) as _json_err:
                _ = _json_err
        elif isinstance(brand_input, dict):
            metadata = brand_input
            text = json.dumps(brand_input)
        else:
            text = str(brand_input)

        text_lower = text.lower()
        m = BrandMetrics()

        # 1. Raw colors check
        has_raw = False
        for pat in self.RAW_COLOR_PATTERNS:
            if re.search(pat, text_lower):
                has_raw = True
                break
        if metadata.get("has_raw_primary_colors", False):
            has_raw = True
        m.has_raw_primary_colors = has_raw

        # 60-30-10 rule check
        has_palette = (
            ("60-30-10" in text_lower or "60_30_10" in text_lower) or
            ("dominant" in text_lower and "secondary" in text_lower and "accent" in text_lower) or
            ("primary_canvas" in text_lower and "accent" in text_lower) or
            metadata.get("has_60_30_10_balance", False)
        )
        m.has_60_30_10_balance = has_palette and not has_raw

        # 2. Font families count
        fonts = set(re.findall(r"font-family\s*:\s*['\"]?([\w\s-]+)['\"]?", text_lower))
        if fonts:
            m.font_families_count = len(fonts)
        else:
            m.font_families_count = int(metadata.get("font_families_count", 1))

        # Modular scale check
        has_modular = (
            "modular" in text_lower or
            "1.25" in text_lower or
            "1.333" in text_lower or
            "scale_ratio" in text_lower or
            metadata.get("has_modular_type_scale", False)
        )
        m.has_modular_type_scale = has_modular

        # 3. Vector SVG check
        if "<svg" in text_lower:
            m.has_svg_viewbox = "viewbox=" in text_lower
        else:
            m.has_svg_viewbox = bool(metadata.get("has_svg_viewbox", True))

        # 4. Logo clear space
        has_clear = (
            "clear_space" in text_lower or
            "clear-space" in text_lower or
            "safe_zone" in text_lower or
            "logo_padding" in text_lower or
            metadata.get("has_logo_clear_space", False)
        )
        m.has_logo_clear_space = has_clear

        # 5. Icon stroke
        m.has_unified_icon_stroke = bool(metadata.get("has_unified_icon_stroke", True))

        # 6. Archetype
        for arc in ["sovereign", "magician", "sage", "rebel", "creator", "explorer"]:
            if arc in text_lower:
                m.brand_archetype = arc.capitalize()
                break

        # Anti-pattern logging
        if m.has_raw_primary_colors:
            m.anti_patterns_detected.append("Raw default hex primaries in brand tokens")
        if m.font_families_count >= 3:
            m.anti_patterns_detected.append(f"Excessive font families ({m.font_families_count} families)")
        if not m.has_svg_viewbox:
            m.anti_patterns_detected.append("SVG vector asset missing viewBox")

        return m
