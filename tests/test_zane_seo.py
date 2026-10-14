"""
Unit tests for Zane Sterling (Technical SEO & Growth Engineering Subsystem).
"""

import pytest
from professions.technical_seo_engineer.references import (
    SEOReferenceLibrary,
    CANONICAL_SEO_HEAD_CORE,
)
from professions.technical_seo_engineer.inspector import SEOSystemInspector
from professions.technical_seo_engineer.rubric import TechnicalSEORubric
from professions.technical_seo_engineer.blind_critic import BlindSEOCritic
from professions.technical_seo_engineer.elevation_engine import TechnicalSEOElevationEngine
from professions.technical_seo_engineer.master import ZaneSterlingMaster


def test_zane_references_loading():
    vitals = SEOReferenceLibrary.get_core_web_vitals()
    assert vitals["max_lcp_seconds"] == 1.2
    assert vitals["max_cls_score"] == 0.000
    assert vitals["max_inp_ms"] == 100.0

    entities = SEOReferenceLibrary.get_schema_entities()
    assert "organization" in entities
    assert "website" in entities
    assert "software_application" in entities
    assert entities["organization"]["@type"] == "Organization"

    anti_patterns = SEOReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "missing_canonical_link" for ap in anti_patterns)


def test_zane_inspector_clean_html():
    inspector = SEOSystemInspector()
    report = inspector.inspect(CANONICAL_SEO_HEAD_CORE)

    assert report.is_seo_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.h1_count == 1
    assert report.metrics.has_canonical_link is True
    assert report.metrics.images_missing_dimensions == 0
    assert report.metrics.has_meta_description is True
    assert report.metrics.has_viewport_meta is True
    assert report.metrics.has_schema_jsonld is True


def test_zane_inspector_flawed_html():
    inspector = SEOSystemInspector()
    flawed_html = (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head><title>Flawed Page</title></head>\n"
        "<body>\n"
        "    <h1>First Title</h1>\n"
        "    <h1>Conflicting Title</h1>\n"
        '    <img src="pic.jpg">\n'
        "</body>\n"
        "</html>\n"
    )
    report = inspector.inspect(flawed_html)

    assert report.is_seo_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.h1_count == 2
    assert report.metrics.has_canonical_link is False
    assert report.metrics.images_missing_dimensions >= 1


def test_zane_rubric_and_veto():
    inspector = SEOSystemInspector()
    rubric = TechnicalSEORubric()

    bad_html = (
        "<!DOCTYPE html>\n"
        "<html><body>\n"
        "    <h1>Title A</h1>\n"
        "    <h1>Title B</h1>\n"
        "</body></html>\n"
    )
    report = inspector.inspect(bad_html)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) >= 2


def test_zane_critic_defect_ledger():
    critic = BlindSEOCritic()
    flawed_html = (
        "<!DOCTYPE html>\n"
        "<html><body>\n"
        '    <img src="hero.png">\n'
        "</body></html>\n"
    )
    ledger = critic.review(flawed_html)

    assert ledger.verdict == "REJECTED_INDEXABILITY_FAILURE"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 2
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_zane_elevation_engine():
    engine = TechnicalSEOElevationEngine()
    flawed_html = (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head><title>Unoptimized Site</title></head>\n"
        "<body>\n"
        "    <h1>Primary Title</h1>\n"
        "    <h1>Second Title</h1>\n"
        '    <img src="logo.png">\n'
        "</body>\n"
        "</html>\n"
    )
    elevated_result = engine.elevate(flawed_html)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "canonical" in elevated_result["elevated_html"]
    assert 'width="1200"' in elevated_result["elevated_html"]
    assert "schema.org" in elevated_result["elevated_html"]
    assert elevated_result["metrics"].h1_count == 1


def test_zane_master_autonomous_cycle():
    master = ZaneSterlingMaster(passing_threshold=85)
    raw_html = (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head><title>Sample</title></head>\n"
        "<body>\n"
        "    <h1>First Heading</h1>\n"
        "    <h1>Second Heading</h1>\n"
        '    <img src="shot.jpg">\n'
        "</body>\n"
        "</html>\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_html)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE TECHNICAL SEO BRIEFING" in result["executive_briefing"]
    assert "ORGANIC SOVEREIGN CERTIFIED" in result["executive_briefing"]
