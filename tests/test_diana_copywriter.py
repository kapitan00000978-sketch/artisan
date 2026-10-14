"""
Unit & Integration Tests for Diana Drake (Direct-Response Copywriter Subsystem)
"""

import os
import shutil
import tempfile
import pytest

from professions.conversion_copywriter.references import DianaCopywritingReferences
from professions.conversion_copywriter.inspector import (
    DianaCopywritingInspector,
    count_syllables
)
from professions.conversion_copywriter.rubric import DianaCopywritingRubric
from professions.conversion_copywriter.blind_critic import DianaBlindCritic
from professions.conversion_copywriter.elevation_engine import DianaElevationEngine
from professions.conversion_copywriter.master import DianaDrakeMaster


@pytest.fixture
def temp_workspace():
    """Creates a temporary workspace for isolated testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_diana_references_loading():
    refs = DianaCopywritingReferences()
    assert "saas_high_converting_landing" in refs.get_available_profiles()
    assert "direct_response_sales_letter" in refs.get_available_profiles()
    assert "microcopy_product_onboarding" in refs.get_available_profiles()

    profile = refs.get_benchmarks()
    assert profile["metrics"]["min_flesch_reading_ease"] >= 60.0
    assert profile["metrics"]["max_allowed_ai_cliches"] == 0


def test_diana_syllable_counter():
    assert count_syllables("the") == 1
    assert count_syllables("easy") >= 1
    assert count_syllables("conversion") >= 2
    assert count_syllables("architecture") >= 3


def test_diana_inspector_clean_copy(temp_workspace):
    html_file = os.path.join(temp_workspace, "clean_copy.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head><title>Clean Landing</title></head>
<body>
<h1>Ship Production Systems Faster Without Outages</h1>
<p>You can deploy your stack in seconds. Your team saves ten hours every week. You get automated safety.</p>
<button>Launch Experience</button>
</body>
</html>""")

    inspector = DianaCopywritingInspector(html_file)
    metrics = inspector.inspect()

    assert metrics["has_weak_h1"] is False
    assert len(metrics["ai_cliches_found"]) == 0
    assert len(metrics["passive_ctas_found"]) == 0
    assert metrics["you_count"] >= 3
    assert metrics["you_to_we_ratio"] >= 1.5
    assert metrics["flesch_reading_ease"] >= 60.0


def test_diana_inspector_flawed_copy(temp_workspace):
    html_file = os.path.join(temp_workspace, "flawed_copy.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head><title>Bland Site</title></head>
<body>
<h1>Welcome to Our Website</h1>
<p>In today's fast-paced world, we provide cutting-edge solutions to seamlessly revolutionize your business. We are the best team.</p>
<button>Click here</button>
</body>
</html>""")

    inspector = DianaCopywritingInspector(html_file)
    metrics = inspector.inspect()

    assert metrics["has_weak_h1"] is True
    assert len(metrics["ai_cliches_found"]) >= 2
    assert "click here" in metrics["passive_ctas_found"]
    assert metrics["we_count"] >= 2


def test_diana_rubric_and_critic_rejection():
    rubric = DianaCopywritingRubric()
    critic = DianaBlindCritic(passing_score=85.0)

    poor_metrics = {
        "flesch_reading_ease": 35.0,
        "avg_words_per_sentence": 32.0,
        "h1_text": "Welcome",
        "has_weak_h1": True,
        "ai_cliches_found": ["welcome to", "revolutionize"],
        "passive_ctas_found": ["click here"],
        "you_to_we_ratio": 0.2,
        "you_count": 1,
        "we_count": 5
    }

    eval_result = rubric.evaluate(poor_metrics)
    assert eval_result["passed"] is False
    assert eval_result["total_score"] < 40.0

    critique = critic.critique(eval_result, poor_metrics)
    assert critique["verdict"] == "REJECTED"
    assert critique["defects_count"] >= 4
    assert any(d["category"] == "HEADLINE_HOOK" for d in critique["defect_ledger"])
    assert any(d["category"] == "CLICHE_POLLUTION" for d in critique["defect_ledger"])


def test_diana_elevation_engine(temp_workspace):
    html_file = os.path.join(temp_workspace, "page.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
<h1>Welcome to App</h1>
<p>In today's fast-paced world, we provide automated testing. Click here to learn more.</p>
<button>Click here</button>
<a class="btn">Learn more</a>
</body>
</html>""")

    engine = DianaElevationEngine()
    elevated = engine.elevate(html_file)

    assert "Ship Production Code" in elevated
    assert "In today's" not in elevated
    assert "You get automated testing" in elevated
    assert ">Launch Experience<" in elevated
    assert ">Explore Architecture<" in elevated


def test_diana_master_autonomous_cycle(temp_workspace):
    html_file = os.path.join(temp_workspace, "bland_landing.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head><title>Bland Landing</title></head>
<body>
<h1>Welcome to System</h1>
<p>We provide tools for teams. We offer fast backups. You get peace of mind.</p>
<button>Click here</button>
</body>
</html>""")

    master = DianaDrakeMaster(target_file=html_file, passing_threshold=85.0)

    # Initial audit should fail due to weak H1 and passive CTA
    initial_audit = master.audit()
    assert initial_audit["passed"] is False

    # Run closed-loop autonomous cycle with auto_elevate=True
    cycle_result = master.run_autonomous_cycle(auto_elevate=True)

    assert cycle_result["passed"] is True
    assert cycle_result["final_score"] >= 85.0
    assert cycle_result["delta"] > 0
    assert "ELEVATED_AND_CERTIFIED" in cycle_result["status"]

    report = master.format_console_report(cycle_result)
    assert "DIANA DRAKE" in report
    assert "CERTIFIED" in report
