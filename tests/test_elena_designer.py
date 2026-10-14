"""
Unit & Integration Tests for Elena Rostova (Principal UI/UX Designer Subsystem)
"""

import os
import shutil
import tempfile
import pytest

from professions.ui_ux_designer.references import ElenaDesignReferences
from professions.ui_ux_designer.inspector import (
    ElenaDesignInspector,
    calculate_contrast_ratio,
    calculate_relative_luminance,
    parse_color
)
from professions.ui_ux_designer.rubric import ElenaDesignRubric
from professions.ui_ux_designer.blind_critic import ElenaBlindCritic
from professions.ui_ux_designer.elevation_engine import ElenaElevationEngine
from professions.ui_ux_designer.master import ElenaRostovaMaster


@pytest.fixture
def temp_workspace():
    """Creates a temporary workspace for isolated testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_references_loading():
    refs = ElenaDesignReferences()
    assert "linear_dark_luxe" in refs.get_available_profiles()
    assert "apple_spatial_glass" in refs.get_available_profiles()
    assert "stripe_fluid_ambient" in refs.get_available_profiles()

    profile = refs.get_benchmarks()
    assert profile["metrics"]["min_contrast_ratio"] >= 4.5
    assert profile["metrics"]["grid_unit_px"] == 8


def test_contrast_math():
    white = (255, 255, 255)
    black = (0, 0, 0)
    assert calculate_contrast_ratio(white, black) == 21.0
    assert calculate_contrast_ratio(white, white) == 1.0

    parsed_hex = parse_color("#ffffff")
    assert parsed_hex == (255, 255, 255)

    parsed_rgb = parse_color("rgb(10, 20, 30)")
    assert parsed_rgb == (10, 20, 30)


def test_inspector_static_analysis(temp_workspace):
    html_file = os.path.join(temp_workspace, "raw_mockup.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
<style>
body { font-size: 16px; background: #ffffff; color: #000000; padding: 16px; margin: 24px; }
h1 { font-size: 48px; font-family: 'Outfit'; }
</style>
</head>
<body>
<h1>Hello World</h1>
<p>Some body copy</p>
</body>
</html>""")

    inspector = ElenaDesignInspector(html_file)
    metrics = inspector.inspect()
    assert metrics["h1_font_size"] == 48.0
    assert metrics["body_font_size"] == 16.0
    assert metrics["scale_ratio"] == 3.0
    assert metrics["grid_8pt_adherence_pct"] > 0
    assert "Outfit" in metrics["font_families"]


def test_rubric_and_blind_critic_rejection():
    rubric = ElenaDesignRubric()
    critic = ElenaBlindCritic(passing_score=85.0)

    # Poor metrics: low contrast, no glass, flat
    poor_metrics = {
        "h1_font_size": 18.0,
        "body_font_size": 16.0,
        "scale_ratio": 1.12,
        "font_families": ["Times New Roman"],
        "contrast_ratio": 2.1,
        "grid_8pt_adherence_pct": 20.0,
        "has_liquid_glass": False,
        "has_ambient_glow": False,
        "has_micro_animations": False
    }

    eval_result = rubric.evaluate(poor_metrics)
    assert eval_result["passed"] is False
    assert eval_result["total_score"] < 50.0

    critique = critic.critique(eval_result, poor_metrics)
    assert critique["verdict"] == "REJECTED"
    assert critique["defects_count"] >= 3
    assert any(d["category"] == "TYPOGRAPHY" for d in critique["defect_ledger"])
    assert any(d["category"] == "ACCESSIBILITY" for d in critique["defect_ledger"])


def test_elevation_engine_transformation(temp_workspace):
    html_file = os.path.join(temp_workspace, "page.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html><html><head><title>Test</title></head><body><h1>Welcome</h1><button>Click here</button></body></html>")

    engine = ElenaElevationEngine()
    elevated_content = engine.elevate(html_file)

    assert "elena-design-system-elevation" in elevated_content
    assert "backdrop-filter: blur" in elevated_content
    assert "fonts.googleapis.com" in elevated_content
    assert "Experience" in elevated_content
    assert "Launch Experience" in elevated_content


def test_elena_master_autonomous_cycle(temp_workspace):
    html_file = os.path.join(temp_workspace, "unpolished.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
<title>Unpolished</title>
<style>
body { font-size: 14px; background: #ffffff; color: #555555; }
h1 { font-size: 20px; }
</style>
</head>
<body>
<h1>Welcome to My Store</h1>
<p>Buy products now</p>
<button>Click here</button>
</body>
</html>""")

    master = ElenaRostovaMaster(target_html=html_file, passing_threshold=85.0)

    # Initial audit should fail
    initial_audit = master.audit()
    assert initial_audit["passed"] is False

    # Run autonomous cycle with auto_elevate=True
    cycle_result = master.run_autonomous_cycle(auto_elevate=True)

    assert cycle_result["passed"] is True
    assert cycle_result["final_score"] >= 85.0
    assert cycle_result["delta"] > 0
    assert "ELEVATED_AND_CERTIFIED" in cycle_result["status"]

    report = master.format_console_report(cycle_result)
    assert "ELENA ROSTOVA" in report
    assert "CERTIFIED" in report
