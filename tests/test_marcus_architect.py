"""
Unit & Integration Tests for Marcus Sterling (Senior Software Architect Subsystem)
"""

import os
import shutil
import tempfile
import pytest

from professions.software_architect.references import MarcusArchitectureReferences
from professions.software_architect.inspector import MarcusArchitectureInspector
from professions.software_architect.rubric import MarcusArchitectureRubric
from professions.software_architect.blind_critic import MarcusBlindCritic
from professions.software_architect.elevation_engine import MarcusElevationEngine
from professions.software_architect.master import MarcusSterlingMaster


@pytest.fixture
def temp_workspace():
    """Creates a temporary workspace for isolated testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_marcus_references_loading():
    refs = MarcusArchitectureReferences()
    assert "clean_modular_service" in refs.get_available_profiles()
    assert "enterprise_resilient_core" in refs.get_available_profiles()
    assert "modern_fast_prototype" in refs.get_available_profiles()

    profile = refs.get_benchmarks()
    assert profile["metrics"]["max_cyclomatic_complexity"] <= 8
    assert profile["metrics"]["max_allowed_empty_catches"] == 0
    assert profile["metrics"]["max_allowed_stubs_or_todos"] == 0


def test_marcus_inspector_clean_python(temp_workspace):
    py_file = os.path.join(temp_workspace, "clean_service.py")
    with open(py_file, "w", encoding="utf-8") as f:
        f.write("""from typing import Optional, Dict, Any

def calculate_tax(amount: float, rate: float = 0.15) -> float:
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return round(amount * rate, 2)
""")

    inspector = MarcusArchitectureInspector(py_file)
    metrics = inspector.inspect()

    assert metrics["file_type"] == "python"
    assert metrics["functions_count"] == 1
    assert metrics["max_cyclomatic_complexity"] == 2
    assert metrics["silent_exception_swallows"] == 0
    assert metrics["todo_placeholder_count"] == 0
    assert metrics["type_annotation_pct"] == 100.0


def test_marcus_inspector_flawed_python(temp_workspace):
    py_file = os.path.join(temp_workspace, "flawed_code.py")
    with open(py_file, "w", encoding="utf-8") as f:
        f.write("""def bad_process(x):
    # TODO: implement real logic
    try:
        if x > 10 and x < 20 or x == 30:
            for i in range(x):
                if i % 2 == 0:
                    pass
    except:
        pass
""")

    inspector = MarcusArchitectureInspector(py_file)
    metrics = inspector.inspect()

    assert metrics["silent_exception_swallows"] >= 1
    assert metrics["todo_placeholder_count"] >= 1
    assert metrics["max_cyclomatic_complexity"] >= 4
    assert metrics["type_annotation_pct"] == 0.0


def test_marcus_rubric_and_critic_rejection():
    rubric = MarcusArchitectureRubric()
    critic = MarcusBlindCritic(passing_score=85.0)

    poor_metrics = {
        "max_cyclomatic_complexity": 18,
        "avg_cyclomatic_complexity": 12.0,
        "max_function_lines": 85,
        "god_functions_count": 2,
        "silent_exception_swallows": 3,
        "todo_placeholder_count": 4,
        "type_annotation_pct": 20.0
    }

    eval_result = rubric.evaluate(poor_metrics)
    assert eval_result["passed"] is False
    assert eval_result["total_score"] < 40.0

    critique = critic.critique(eval_result, poor_metrics)
    assert critique["verdict"] == "REJECTED"
    assert critique["defects_count"] >= 4
    assert any(d["category"] == "COMPLEXITY" for d in critique["defect_ledger"])
    assert any(d["category"] == "ERROR_DISCIPLINE" for d in critique["defect_ledger"])


def test_marcus_elevation_engine(temp_workspace):
    py_file = os.path.join(temp_workspace, "raw.py")
    with open(py_file, "w", encoding="utf-8") as f:
        f.write("""def process_data(data):
    # TODO: optimize query
    try:
        return data
    except Exception:
        pass
""")

    engine = MarcusElevationEngine()
    elevated = engine.elevate(py_file)

    assert "from typing import" in elevated
    assert "-> Any:" in elevated
    assert "except Exception as _err:" in elevated
    assert "Resolved per Marcus Sterling" in elevated


def test_marcus_master_autonomous_cycle(temp_workspace):
    py_file = os.path.join(temp_workspace, "sloppy_module.py")
    with open(py_file, "w", encoding="utf-8") as f:
        f.write("""def handle_request(req):
    # TODO: fix this later
    try:
        val = req.get('key')
        return val
    except:
        pass
""")

    master = MarcusSterlingMaster(target_file=py_file, passing_threshold=85.0)

    # Initial audit should fail
    initial_audit = master.audit()
    assert initial_audit["passed"] is False

    # Run closed-loop autonomous cycle with auto_elevate=True
    cycle_result = master.run_autonomous_cycle(auto_elevate=True)

    assert cycle_result["passed"] is True
    assert cycle_result["final_score"] >= 85.0
    assert cycle_result["delta"] > 0
    assert "ELEVATED_AND_CERTIFIED" in cycle_result["status"]

    report = master.format_console_report(cycle_result)
    assert "MARCUS STERLING" in report
    assert "CERTIFIED" in report
