"""
Unit tests for Aria Solano (Global Brand Director & Visual Identity Subsystem).
"""

import pytest
from professions.brand_identity_director.references import BrandReferenceLibrary
from professions.brand_identity_director.inspector import BrandIdentityInspector
from professions.brand_identity_director.rubric import BrandIdentityRubric
from professions.brand_identity_director.blind_critic import BlindBrandCritic
from professions.brand_identity_director.elevation_engine import BrandIdentityElevationEngine
from professions.brand_identity_director.master import AriaSolanoMaster


def test_aria_references_loading():
    color_b = BrandReferenceLibrary.get_color_benchmarks()
    assert color_b["dominant_canvas_pct"] == 60.0
    assert color_b["secondary_structure_pct"] == 30.0
    assert color_b["accent_energy_pct"] == 10.0

    type_scales = BrandReferenceLibrary.get_typography_scales()
    assert "major_third" in type_scales
    assert "perfect_fourth" in type_scales
    assert type_scales["major_third"]["ratio"] == 1.250

    anti_patterns = BrandReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "raw_primary_defaults" for ap in anti_patterns)


def test_aria_inspector_luminary_brand():
    inspector = BrandIdentityInspector()
    luminary_tokens = (
        ":root {\n"
        "    /* 60-30-10 Color Architecture */\n"
        "    --color-canvas-dominant: #0F172A;\n"
        "    --color-surface-secondary: #1E293B;\n"
        "    --color-accent-kinetic: #6366F1;\n"
        "    /* Modular Scale Typography (1.250) */\n"
        "    --font-heading: 'Outfit', sans-serif;\n"
        "    --font-body: 'Inter', sans-serif;\n"
        "}\n"
        "h1 { font-family: var(--font-heading); }\n"
        "p { font-family: var(--font-body); }\n"
        ".brand-logo { margin: 2rem; padding: 1.5rem; clear_space: 1x; }\n"
        '<svg viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2z"/></svg>\n'
    )
    report = inspector.inspect(luminary_tokens)
    assert report.is_brand_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_raw_primary_colors is False
    assert report.metrics.has_60_30_10_balance is True
    assert report.metrics.font_families_count <= 2
    assert report.metrics.has_svg_viewbox is True


def test_aria_inspector_flawed_brand():
    inspector = BrandIdentityInspector()
    flawed_brand = (
        ":root {\n"
        "    --color-primary: #0000ff;\n"
        "    --color-danger: #ff0000;\n"
        "    font-family: 'Comic Sans';\n"
        "}\n"
        "h1 { font-family: 'Roboto'; }\n"
        "h2 { font-family: 'Times New Roman'; }\n"
        '<svg width="50" height="50"><rect width="50" height="50"/></svg>\n'
    )
    report = inspector.inspect(flawed_brand)
    assert report.is_brand_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_raw_primary_colors is True
    assert report.metrics.font_families_count >= 3
    assert report.metrics.has_svg_viewbox is False


def test_aria_rubric_and_veto():
    inspector = BrandIdentityInspector()
    rubric = BrandIdentityRubric()

    bad_brand = (
        ":root { color: #0000ff; }\n"
        "h1 { font-family: 'Impact'; }\n"
        "h2 { font-family: 'Papyrus'; }\n"
        "p { font-family: 'Arial'; }\n"
    )
    report = inspector.inspect(bad_brand)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) > 0


def test_aria_critic_defect_ledger():
    critic = BlindBrandCritic()
    flawed_brand = (
        ":root { --bg: #ff0000; }\n"
        "h1 { font-family: 'Impact'; }\n"
        "h2 { font-family: 'Papyrus'; }\n"
        "h3 { font-family: 'Courier'; }\n"
    )
    ledger = critic.review(flawed_brand)
    assert ledger.verdict == "REJECTED_VISUAL_DISSONANCE"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 2
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_aria_elevation_engine():
    engine = BrandIdentityElevationEngine()
    flawed_input = (
        ":root {\n"
        "    --primary: #0000ff;\n"
        "    font-family: 'Comic Sans';\n"
        "}\n"
        "h1 { font-family: 'Roboto'; }\n"
        "p { font-family: 'Arial'; }\n"
        '<svg width="60" height="60"><circle cx="30" cy="30" r="20"/></svg>\n'
    )
    elevated_result = engine.elevate(flawed_input)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "60-30-10 SEMANTIC COLOR TOKENS" in elevated_result["elevated_brand"]
    assert "MODULAR TYPOGRAPHY" in elevated_result["elevated_brand"]
    assert "viewBox=" in elevated_result["elevated_brand"]
    assert "LOGO CLEAR-SPACE" in elevated_result["elevated_brand"]


def test_aria_master_autonomous_cycle():
    master = AriaSolanoMaster(passing_threshold=85)
    raw_brand = (
        ":root { --brand: #ff0000; }\n"
        "h1 { font-family: 'Times'; }\n"
        "h2 { font-family: 'Courier'; }\n"
        "p { font-family: 'Arial'; }\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_brand)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE BRAND IDENTITY BRIEFING" in result["executive_briefing"]
    assert "LUMINARY CERTIFIED" in result["executive_briefing"]
