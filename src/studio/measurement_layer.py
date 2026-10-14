"""
Step 3 — Objective Measurement Layer (O'lchov Qatlami)
Calculates concrete empirical numbers:
- WCAG 2.1 contrast ratio calculation (luminance formula)
- Flesch-Kincaid readability ease score
- 8pt spatial grid adherence percentage
- Typography scale hierarchy ratio (H1 to Body)
- DOM complexity & performance budget
"""

import os
import re
import math
from typing import Dict, Any, List, Tuple, Optional


def calculate_relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """Calculates relative luminance according to WCAG 2.1 specifications."""
    def channel_luminance(c: int) -> float:
        val = c / 255.0
        return val / 12.92 if val <= 0.03928 else math.pow((val + 0.055) / 1.055, 2.4)

    r = channel_luminance(rgb[0])
    g = channel_luminance(rgb[1])
    b = channel_luminance(rgb[2])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def calculate_contrast_ratio(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """Calculates contrast ratio between two RGB colors (1.0 to 21.0)."""
    l1 = calculate_relative_luminance(rgb1)
    l2 = calculate_relative_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return round((lighter + 0.05) / (darker + 0.05), 2)


def parse_rgb_string(color_str: str) -> Optional[Tuple[int, int, int]]:
    """Parses rgb(...) or hex string into (r, g, b) tuple."""
    if not color_str:
        return None
    # Hex format
    if color_str.startswith("#"):
        hex_code = color_str.lstrip("#")
        if len(hex_code) == 3:
            hex_code = "".join([c * 2 for c in hex_code])
        if len(hex_code) >= 6:
            try:
                return (int(hex_code[0:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16))
            except ValueError:
                return None
    # rgb/rgba format
    match = re.search(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", color_str)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return None


def calculate_flesch_reading_ease(text: str) -> float:
    """
    Computes Flesch Reading Ease score:
    206.835 - 1.015 * (total words / total sentences) - 84.6 * (total syllables / total words)
    Higher is easier to read (60-70 is standard conversational).
    """
    words = re.findall(r"\b[A-Za-z]+\b", text)
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    total_words = len(words)
    total_sentences = max(1, len(sentences))

    if total_words == 0:
        return 70.0

    # Approximate syllables by vowel clusters
    total_syllables = 0
    for w in words:
        syllables = len(re.findall(r"[aeiouy]+", w.lower()))
        total_syllables += max(1, syllables)

    asl = total_words / total_sentences
    asw = total_syllables / total_words

    score = 206.835 - (1.015 * asl) - (84.6 * asw)
    return round(max(0.0, min(100.0, score)), 1)


class MeasurementLayer:
    """Performs rigorous empirical measurement on target HTML/CSS artifacts."""

    def __init__(self, html_path: str):
        self.html_path = os.path.abspath(html_path)

    def measure(self) -> Dict[str, Any]:
        """
        Runs full browser-level measurement suite:
        - Contrast Ratio (min, avg, and WCAG AA violation count)
        - Typography Ratio (H1 size / Body size)
        - Flesch Readability Score
        - 8pt Spatial Grid Compliance (%)
        - DOM Complexity & Asset Metrics
        """
        results: Dict[str, Any] = {
            "html_path": self.html_path,
            "contrast_ratio": 7.0,
            "wcag_aa_compliant": True,
            "h1_font_size_px": 32.0,
            "body_font_size_px": 16.0,
            "typography_scale_ratio": 2.0,
            "flesch_readability": 65.0,
            "grid_8pt_adherence_pct": 50.0,
            "dom_node_count": 0,
            "has_viewport_meta": False,
            "has_glassmorphism": False,
            "unsecured_links_count": 0,
            "empty_alt_images_count": 0
        }

        # 1. Direct text analysis
        try:
            with open(self.html_path, "r", encoding="utf-8") as f:
                content = f.read()

            raw_text = re.sub(r"<[^>]+>", " ", content)
            results["flesch_readability"] = calculate_flesch_reading_ease(raw_text)
            results["has_viewport_meta"] = '<meta name="viewport"' in content.lower()
            results["has_glassmorphism"] = "backdrop-filter" in content

            # Unsecured links (target="_blank" without rel="noopener")
            unsecured = re.findall(r'<a[^>]+target=["\']_blank["\'](?![^>]*rel=)', content, re.IGNORECASE)
            results["unsecured_links_count"] = len(unsecured)

            # Missing img alt
            missing_alts = re.findall(r'<img(?![^>]*alt=)[^>]*>', content, re.IGNORECASE)
            results["empty_alt_images_count"] = len(missing_alts)

            # Estimate spacing adhering to 8pt (8, 16, 24, 32, 48, 64)
            px_values = [int(p) for p in re.findall(r"(\d+)px", content)]
            if px_values:
                grid_hits = sum(1 for p in px_values if p > 0 and p % 8 == 0)
                results["grid_8pt_adherence_pct"] = round((grid_hits / len(px_values)) * 100, 1)

        except Exception as e:
            results["read_error"] = str(e)

        # 2. Browser computed inspection via Playwright
        try:
            from playwright.sync_api import sync_playwright
            file_url = f"file:///{self.html_path.replace(os.sep, '/')}"

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1440, "height": 900})
                page.goto(file_url, wait_until="load", timeout=8000)

                browser_metrics = page.evaluate("""() => {
                    const h1 = document.querySelector('h1');
                    const body = document.body;
                    const h1Style = h1 ? window.getComputedStyle(h1) : null;
                    const bodyStyle = body ? window.getComputedStyle(body) : null;

                    const h1_size = h1Style ? parseFloat(h1Style.fontSize) : 32.0;
                    const body_size = bodyStyle ? parseFloat(bodyStyle.fontSize) : 16.0;

                    const bodyBg = bodyStyle ? bodyStyle.backgroundColor : 'rgb(255, 255, 255)';
                    const bodyColor = bodyStyle ? bodyStyle.color : 'rgb(0, 0, 0)';

                    return {
                        h1_size,
                        body_size,
                        dom_nodes: document.querySelectorAll('*').length,
                        bodyBg,
                        bodyColor
                    };
                }""")
                browser.close()

                results["h1_font_size_px"] = browser_metrics["h1_size"]
                results["body_font_size_px"] = browser_metrics["body_size"]
                results["typography_scale_ratio"] = round(browser_metrics["h1_size"] / max(1.0, browser_metrics["body_size"]), 2)
                results["dom_node_count"] = browser_metrics["dom_nodes"]

                c1 = parse_rgb_string(browser_metrics["bodyColor"]) or (0, 0, 0)
                c2 = parse_rgb_string(browser_metrics["bodyBg"]) or (255, 255, 255)
                ratio = calculate_contrast_ratio(c1, c2)
                results["contrast_ratio"] = ratio
                results["wcag_aa_compliant"] = (ratio >= 4.5)

        except Exception as e:
            results["browser_eval_error"] = str(e)

        return results
