import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "sdk")))
from context_selector import SmartMasterSelector

SAMPLE_COUNCIL = {
    "software_architect": {
        "name": "Marcus 'The Vanguard' Sterling",
        "archetype": "Systems Sovereign & Zero-Tech-Debt Purist",
        "motto": "Fail gracefully or do not exist.",
        "criteria": ["Clean architecture", "Zero stubs", "Comprehensive error handling"]
    },
    "cyber_security_auditor": {
        "name": "Gabriel 'The Sentinel' Frost",
        "archetype": "Zero-Trust Inquisitor & Threat Modeling Sovereign",
        "motto": "Assume breach.",
        "criteria": ["No plaintext secrets", "Input sanitization", "Constant-time auth"]
    },
    "principal_designer": {
        "name": "Elena 'The Visionary' Rostova",
        "archetype": "Aesthetic Sovereign & Spatial Ergonomics Master",
        "motto": "Beauty and ergonomics in unison.",
        "criteria": ["WCAG 2.1 AAA contrast", "8pt spatial grid", "Touch targets >=48px"]
    },
    "database_storage_architect": {
        "name": "Cassandra 'The Core' Thorne",
        "archetype": "Data Sovereign & Low-Latency Lead",
        "motto": "Sub-10ms queries, zero N+1 cascades.",
        "criteria": ["Index foreign keys", "Zero N+1 query loops", "Transaction isolation"]
    }
}


def test_selector_keyword_matching_security():
    selector = SmartMasterSelector(SAMPLE_COUNCIL)
    ranked = selector.score_masters("Build a secure FastAPI auth endpoint with bcrypt password hashing")
    top_keys = [r["master_key"] for r in ranked[:2]]
    assert "cyber_security_auditor" in top_keys
    assert "software_architect" in top_keys


def test_selector_file_extension_matching():
    selector = SmartMasterSelector(SAMPLE_COUNCIL)
    # UI styling task with .css and .html
    ranked = selector.score_masters("Update hero banner component styles", files=["styles.css", "index.html"])
    top_keys = [r["master_key"] for r in ranked[:2]]
    assert "principal_designer" in top_keys


def test_selector_database_matching():
    selector = SmartMasterSelector(SAMPLE_COUNCIL)
    ranked = selector.score_masters("Write postgres migration for users table foreign key join", files=["schema.sql"])
    top_keys = [r["master_key"] for r in ranked[:2]]
    assert "database_storage_architect" in top_keys


def test_selector_fallback_on_empty():
    selector = SmartMasterSelector(SAMPLE_COUNCIL)
    selected = selector.select_masters("", files=[], limit=2)
    assert len(selected) == 2
    keys = [s["master_key"] for s in selected]
    assert "software_architect" in keys


def test_selector_dynamic_prompt_generation():
    selector = SmartMasterSelector(SAMPLE_COUNCIL)
    task = "Implement user authentication with bcrypt and JWT"
    lessons = [
        {"category": "auth", "lesson": "Never store plain passwords; always hash with bcrypt."}
    ]
    res = selector.build_dynamic_prompt(task_description=task, lessons=lessons, limit=2)
    assert "prompt" in res
    assert "approx_tokens" in res
    assert res["approx_tokens"] < 1500  # Strict budget ceiling
    prompt_text = res["prompt"]
    assert "4 INVIOLABLE PROTOCOL INVARIANTS" in prompt_text
    assert "ZERO STUBS" in prompt_text
    assert "PAST LESSONS & SCAR TISSUE" in prompt_text
    assert "bcrypt" in prompt_text
