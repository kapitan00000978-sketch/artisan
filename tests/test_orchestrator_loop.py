import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.studio.reference_collector import ReferenceCollector
from src.studio.measurement_layer import MeasurementLayer, calculate_contrast_ratio
from src.studio.rubric_engine import RubricEngine
from src.studio.blind_critic import BlindCritic
from src.studio.remediator_loop import RemediatorAgent
from src.studio.active_memory import ActiveDecisionJournal
from src.studio.orchestrator import StudioOrchestrator


def test_reference_collector_profile():
    collector = ReferenceCollector("saas_landing")
    profile = collector.get_benchmark_profile()
    assert profile["h1_font_size_px"] == 56.0
    assert profile["min_contrast_ratio"] == 4.5
    assert profile["glassmorphism_rate"] > 0.8


def test_measurement_layer_contrast_and_flesch(tmp_path):
    test_html = tmp_path / "measure_test.html"
    test_html.write_text("<!DOCTYPE html><html><body><h1 style='color: #000000; background: #ffffff;'>Hello World</h1></body></html>", encoding="utf-8")
    
    measure = MeasurementLayer(str(test_html))
    results = measure.measure()
    assert results["flesch_readability"] > 0
    assert "contrast_ratio" in results


def test_rubric_engine_scoring():
    rubric = RubricEngine()
    profile = {"flesch_reading_ease_target": 65.0}
    
    # Failing measurements
    bad_meas = {
        "contrast_ratio": 2.0,
        "typography_scale_ratio": 1.1,
        "grid_8pt_adherence_pct": 20.0,
        "flesch_readability": 15.0,
        "has_glassmorphism": False
    }
    bad_eval = rubric.evaluate(bad_meas, profile)
    assert bad_eval["total_score"] < 50.0
    assert bad_eval["passed"] is False

    # Elite measurements
    good_meas = {
        "contrast_ratio": 9.5,
        "typography_scale_ratio": 3.0,
        "grid_8pt_adherence_pct": 90.0,
        "flesch_readability": 65.0,
        "has_glassmorphism": True
    }
    good_eval = rubric.evaluate(good_meas, profile)
    assert good_eval["total_score"] >= 80.0
    assert good_eval["passed"] is True


def test_blind_critic_audit():
    critic = BlindCritic(rubric_threshold=80.0)
    rubric_res = {
        "total_score": 45.0,
        "dimensions": {
            "contrast_accessibility": {"status": "FAIL", "measured": "2.0:1", "benchmark": ">= 4.5:1"},
            "typography_hierarchy": {"status": "FAIL", "measured": "1.2x", "benchmark": "2.5x-4.0x"}
        }
    }
    meas = {"unsecured_links_count": 1, "has_viewport_meta": False}
    audit = critic.audit(rubric_res, meas)
    assert audit["passed"] is False
    assert audit["verdict"] == "REJECTED_REMEDIATION_REQUIRED"
    assert len(audit["defect_ledger"]) >= 4


def test_full_orchestrator_closed_loop(tmp_path):
    draft_html = tmp_path / "orchestrator_test.html"
    draft_html.write_text("<!DOCTYPE html><html><head><title>Test</title></head><body><h1>Draft</h1><a href='http://x.com' target='_blank'>Link</a></body></html>", encoding="utf-8")
    
    journal_file = str(tmp_path / "test_journal.json")
    orchestrator = StudioOrchestrator(
        str(draft_html),
        passing_threshold=75.0,
        max_iterations=3
    )
    orchestrator.journal = ActiveDecisionJournal(journal_path=journal_file)
    result = orchestrator.run(auto_remediate=True)

    assert result["status"] == "CERTIFIED"
    assert result["final_score"] >= 75.0
    assert os.path.exists(journal_file)
