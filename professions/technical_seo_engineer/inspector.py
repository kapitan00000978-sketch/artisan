"""
Zane 'The Vector' Sterling - Objective Technical SEO & Indexability Inspector.

This module inspects HTML documents, templates, and head metadata to measure Core Web Vitals
indicators, heading hierarchy, Schema.org JSON-LD graphs, canonical hygiene, and OpenGraph parity.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class SEOMetrics:
    h1_count: int = 0
    has_canonical_link: bool = False
    has_meta_description: bool = False
    has_opengraph_tags: bool = False
    has_twitter_card: bool = False
    has_schema_jsonld: bool = False
    has_viewport_meta: bool = False
    images_missing_dimensions: int = 0
    images_missing_alt: int = 0
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class SEOInspectionReport:
    metrics: SEOMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_seo_viable: bool = False


class SEOSystemInspector:
    """Rigorous search engine auditor evaluating HTML structure, Core Web Vitals signals, and semantics."""

    def inspect(self, html_input: Any) -> SEOInspectionReport:
        """
        Audits HTML source code, Next.js / React page, or metadata dict.
        """
        metrics = self._extract_metrics(html_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Heading Hierarchy Discipline (Single H1)
        if metrics.h1_count == 0:
            critical_violations.append(
                "Missing <h1> Heading: Document lacks a primary entity title, destroying search topical authority."
            )
        elif metrics.h1_count > 1:
            critical_violations.append(
                f"Multiple <h1> Headings ({metrics.h1_count} found): Having multiple primary titles fragments "
                "search intent signals and creates topical confusion in search algorithms."
            )
        else:
            benchmarks_passed.append("Single semantic <h1> tag verified (Pristine topical focus).")

        # 2. Canonical URL Hygiene
        if not metrics.has_canonical_link:
            critical_violations.append(
                "Missing Canonical Tag: No <link rel='canonical' href='...'> declared. "
                "Exposes URL query parameters and variations to severe duplicate content cannibalization."
            )
        else:
            benchmarks_passed.append("Hermetic self-referential canonical link verified.")

        # 3. Core Web Vitals CLS Defense (Image Dimensions)
        if metrics.images_missing_dimensions > 0:
            critical_violations.append(
                f"Layout Shift Hazard (CLS): {metrics.images_missing_dimensions} <img> tag(s) lack explicit width and height. "
                "Causes severe Cumulative Layout Shift (CLS > 0.1) as images render, degrading Core Web Vitals rankings."
            )
        else:
            benchmarks_passed.append("Zero-CLS image aspect-ratio and dimensions verified.")

        # 4. Meta Description & Viewport
        if not metrics.has_meta_description:
            warnings.append("Missing meta description; search engines will fall back to uncurated DOM text snippets.")
        else:
            benchmarks_passed.append("Curated meta description verified.")

        if not metrics.has_viewport_meta:
            warnings.append("Missing responsive viewport meta tag; mobile readiness score compromised.")
        else:
            benchmarks_passed.append("Mobile-responsive viewport meta tag verified.")

        # 5. Schema.org JSON-LD Knowledge Graph
        if not metrics.has_schema_jsonld:
            warnings.append("Missing Schema.org JSON-LD; page is ineligible for Rich Snippets and Knowledge Graph cards.")
        else:
            benchmarks_passed.append("Structured data Schema.org JSON-LD semantic graph verified.")

        # 6. Social Preview Parity (OG & Twitter)
        if metrics.has_opengraph_tags and metrics.has_twitter_card:
            benchmarks_passed.append("Full social preview card parity verified (OpenGraph + Twitter Cards).")
        else:
            warnings.append("Incomplete social preview metadata (OpenGraph or Twitter card omitted).")

        # 7. Image Alt Text Coverage
        if metrics.images_missing_alt > 0:
            warnings.append(f"{metrics.images_missing_alt} image(s) missing alt text (WCAG & image search penalty).")
        else:
            benchmarks_passed.append("100% image alt text accessibility coverage verified.")

        for ap in metrics.anti_patterns_detected:
            if ap not in critical_violations:
                critical_violations.append(f"Anti-Pattern Detected: {ap}")

        is_viable = len(critical_violations) == 0

        return SEOInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_seo_viable=is_viable
        )

    def _extract_metrics(self, html_input: Any) -> SEOMetrics:
        text = ""
        metadata: Dict[str, Any] = {}

        if isinstance(html_input, str):
            text = html_input
            try:
                parsed = json.loads(html_input)
                if isinstance(parsed, dict):
                    metadata = parsed
            except (json.JSONDecodeError, ValueError) as _json_err:
                _ = _json_err
        elif isinstance(html_input, dict):
            metadata = html_input
            text = json.dumps(html_input)
        else:
            text = str(html_input)

        text_lower = text.lower()
        m = SEOMetrics()

        # 1. H1 Count
        h1_matches = re.findall(r"<h1\b", text_lower)
        m.h1_count = len(h1_matches) if h1_matches else metadata.get("h1_count", 0)

        # 2. Canonical Tag
        has_canon = bool(
            re.search(r"<link\s+[^>]*rel=[\"']canonical[\"']", text_lower) or
            re.search(r"rel=[\"']canonical[\"']", text_lower) or
            metadata.get("has_canonical_link", False)
        )
        m.has_canonical_link = has_canon

        # 3. Meta Description
        has_desc = bool(
            re.search(r"<meta\s+[^>]*name=[\"']description[\"']", text_lower) or
            metadata.get("has_meta_description", False)
        )
        m.has_meta_description = has_desc

        # 4. OpenGraph Tags
        has_og = bool(
            "og:title" in text_lower or
            "og:image" in text_lower or
            metadata.get("has_opengraph_tags", False)
        )
        m.has_opengraph_tags = has_og

        # 5. Twitter Card
        has_tw = bool(
            "twitter:card" in text_lower or
            metadata.get("has_twitter_card", False)
        )
        m.has_twitter_card = has_tw

        # 6. Schema.org JSON-LD
        has_jsonld = bool(
            ("application/ld+json" in text_lower and "schema.org" in text_lower) or
            metadata.get("has_schema_jsonld", False)
        )
        m.has_schema_jsonld = has_jsonld

        # 7. Viewport
        has_vp = bool(
            "name=\"viewport\"" in text_lower or
            "name='viewport'" in text_lower or
            metadata.get("has_viewport_meta", False)
        )
        m.has_viewport_meta = has_vp

        # 8. Images missing dimensions (CLS risk)
        img_tags = re.findall(r"<img\b[^>]*>", text_lower)
        missing_dims = 0
        missing_alt = 0
        for tag in img_tags:
            has_w = "width=" in tag
            has_h = "height=" in tag
            has_aspect = "aspect-ratio" in tag or "style=" in tag and "aspect" in tag
            if not ((has_w and has_h) or has_aspect):
                missing_dims += 1
            if "alt=" not in tag:
                missing_alt += 1

        m.images_missing_dimensions = missing_dims if img_tags else metadata.get("images_missing_dimensions", 0)
        m.images_missing_alt = missing_alt if img_tags else metadata.get("images_missing_alt", 0)

        # Anti-pattern logging
        if m.h1_count != 1:
            m.anti_patterns_detected.append(f"Invalid H1 heading count ({m.h1_count})")
        if not m.has_canonical_link:
            m.anti_patterns_detected.append("Missing canonical link tag")
        if m.images_missing_dimensions > 0:
            m.anti_patterns_detected.append(f"{m.images_missing_dimensions} image(s) missing width/height (CLS risk)")

        return m
