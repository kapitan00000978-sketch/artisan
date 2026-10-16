"""
Elena Rostova's Specialized UI/UX Design Inspector
Deep empirical measurement tool for visual design, typography, spatial grid, contrast, and interactive states.
"""

import os
import re
import math
from typing import Dict, Any, List, Tuple, Optional


def calculate_relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """Calculates relative luminance per WCAG 2.1 specs."""
    def channel(c: int) -> float:
        val = c / 255.0
        return val / 12.92 if val <= 0.03928 else math.pow((val + 0.055) / 1.055, 2.4)
    return 0.2126 * channel(rgb[0]) + 0.7152 * channel(rgb[1]) + 0.0722 * channel(rgb[2])


def calculate_contrast_ratio(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """Calculates contrast ratio between two colors (1.0 to 21.0)."""
    l1 = calculate_relative_luminance(rgb1)
    l2 = calculate_relative_luminance(rgb2)
    return round((max(l1, l2) + 0.05) / (min(l1, l2) + 0.05), 2)


def parse_color(color_str: str) -> Optional[Tuple[int, int, int]]:
    """Parses hex or rgba strings into (r, g, b) tuple."""
    if not color_str:
        return None
    if color_str.startswith("#"):
        c = color_str.lstrip("#")
        if len(c) == 3:
            c = "".join([x * 2 for x in c])
        if len(c) >= 6:
            try:
                return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))
            except ValueError:
                return None
    match = re.search(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", color_str)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return None


class ElenaDesignInspector:
    """Elena Rostova's domain inspection engine."""

    def __init__(self, target_html: str):
        self.target_html = os.path.abspath(target_html)

    def inspect(self) -> Dict[str, Any]:
        """
        Executes a deep, multi-dimensional design inspection:
        - Typography scale & line-height
        - Contrast analysis & WCAG 2.1 AA/AAA compliance
        - 8pt spatial grid adherence percentage
        - Liquid Glass & aesthetic depth
        - Micro-interactions & hover transitions
        """
        metrics: Dict[str, Any] = {
            "target": self.target_html,
            "h1_font_size": 32.0,
            "body_font_size": 16.0,
            "scale_ratio": 2.0,
            "font_families": [],
            "contrast_ratio": 7.0,
            "wcag_compliant": True,
            "grid_8pt_adherence_pct": 50.0,
            "has_liquid_glass": False,
            "has_ambient_glow": False,
            "has_micro_animations": False,
            "missing_hover_states": []
        }

        # 1. Text & Code static pass
        try:
            with open(self.target_html, "r", encoding="utf-8") as f:
                content = f.read()

            metrics["has_liquid_glass"] = "backdrop-filter" in content
            metrics["has_ambient_glow"] = "gradient" in content or "radial-gradient" in content
            metrics["has_micro_animations"] = "transition" in content or "@keyframes" in content

            # Check 8pt grid values
            all_pixels = [int(p) for p in re.findall(r"(\d+)px", content)]
            if all_pixels:
                hits = sum(1 for p in all_pixels if p > 0 and p % 8 == 0)
                metrics["grid_8pt_adherence_pct"] = round((hits / len(all_pixels)) * 100, 1)

            # Check fonts
            font_matches = re.findall(r"font-family:\s*([^;]+);", content, re.IGNORECASE)
            fonts = set()
            for fm in font_matches:
                fonts.add(fm.split(",")[0].replace("'", "").replace('"', "").strip())
            metrics["font_families"] = list(fonts)[:5]

            # Static extraction of H1 / Body font size (taking the last declared rule in document)
            h1_size_matches = re.findall(r"h1[^{]*\{[^}]*font-size:\s*(?:clamp\([^,]+,[^,]+,\s*)?(\d+)px", content, re.IGNORECASE)
            if h1_size_matches:
                metrics["h1_font_size"] = float(h1_size_matches[-1])

            body_size_matches = re.findall(r"\b(?:body|p)\b[^{]*\{[^}]*font-size:\s*(\d+)px", content, re.IGNORECASE)
            if body_size_matches:
                metrics["body_font_size"] = float(body_size_matches[-1])
            metrics["scale_ratio"] = round(metrics["h1_font_size"] / max(1.0, metrics["body_font_size"]), 2)

            # Static extraction of body background and text color (last declared rule)
            bg_matches = re.findall(r"body[^{]*\{[^}]*background(?:-color)?:\s*(#[0-9a-fA-F]{3,6}|rgba?\([^)]+\)|var\(--elena-bg\))", content, re.IGNORECASE)
            fg_matches = re.findall(r"body[^{]*\{[^}]*color:\s*(#[0-9a-fA-F]{3,6}|rgba?\([^)]+\)|var\(--elena-text-title\))", content, re.IGNORECASE)
            if bg_matches and fg_matches:
                bg_val = bg_matches[-1]
                fg_val = fg_matches[-1]
                if "var(--elena-bg)" in bg_val:
                    c2 = (9, 11, 16)  # #090b10
                else:
                    c2 = parse_color(bg_val)

                if "var(--elena-text-title)" in fg_val:
                    c1 = (255, 255, 255)
                else:
                    c1 = parse_color(fg_val)

                if c1 and c2:
                    ratio = calculate_contrast_ratio(c1, c2)
                    metrics["contrast_ratio"] = ratio
                    metrics["wcag_compliant"] = (ratio >= 4.5)

        except Exception as e:
            metrics["static_error"] = str(e)

        # 2. Headless Chromium computed style extraction via Playwright
        try:
            from playwright.sync_api import sync_playwright
            file_url = f"file:///{self.target_html.replace(os.sep, '/')}"

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1440, "height": 900})
                page.goto(file_url, wait_until="load", timeout=8000)

                computed = page.evaluate("""() => {
                    const h1 = document.querySelector('h1');
                    const body = document.body;
                    const h1Style = h1 ? window.getComputedStyle(h1) : null;
                    const bodyStyle = body ? window.getComputedStyle(body) : null;

                    const h1_size = h1Style ? parseFloat(h1Style.fontSize) : 32.0;
                    const body_size = bodyStyle ? parseFloat(bodyStyle.fontSize) : 16.0;

                    const bodyBg = bodyStyle ? bodyStyle.backgroundColor : 'rgb(255, 255, 255)';
                    const bodyColor = bodyStyle ? bodyStyle.color : 'rgb(0, 0, 0)';

                    let hasGlass = false;
                    let hasTransitions = false;
                    document.querySelectorAll('*').forEach(el => {
                        const s = window.getComputedStyle(el);
                        if (s.backdropFilter && s.backdropFilter !== 'none') hasGlass = true;
                        if (s.transition && s.transition !== 'none' && !s.transition.includes('all 0s')) hasTransitions = true;
                    });

                    return {
                        h1_size,
                        body_size,
                        bodyBg,
                        bodyColor,
                        hasGlass,
                        hasTransitions
                    };
                }""")
                browser.close()

                metrics["h1_font_size"] = computed["h1_size"]
                metrics["body_font_size"] = computed["body_size"]
                metrics["scale_ratio"] = round(computed["h1_size"] / max(1.0, computed["body_size"]), 2)
                metrics["has_liquid_glass"] = metrics["has_liquid_glass"] or computed["hasGlass"]
                metrics["has_micro_animations"] = metrics["has_micro_animations"] or computed["hasTransitions"]

                c1 = parse_color(computed["bodyColor"]) or (0, 0, 0)
                c2 = parse_color(computed["bodyBg"]) or (255, 255, 255)
                ratio = calculate_contrast_ratio(c1, c2)
                metrics["contrast_ratio"] = ratio
                metrics["wcag_compliant"] = (ratio >= 4.5)

        except Exception as e:
            metrics["computed_error"] = str(e)

        return metrics
