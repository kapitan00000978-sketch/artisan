"""
Unit & Integration Tests for Gabriel Frost (Principal Cybersecurity Auditor Subsystem)
"""

import os
import shutil
import tempfile
import pytest

from professions.cybersecurity_auditor.references import GabrielSecurityReferences
from professions.cybersecurity_auditor.inspector import GabrielSecurityInspector
from professions.cybersecurity_auditor.rubric import GabrielSecurityRubric
from professions.cybersecurity_auditor.blind_critic import GabrielBlindCritic
from professions.cybersecurity_auditor.elevation_engine import GabrielElevationEngine
from professions.cybersecurity_auditor.master import GabrielFrostMaster


@pytest.fixture
def temp_workspace():
    """Creates a temporary workspace for isolated testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_gabriel_references_loading():
    refs = GabrielSecurityReferences()
    assert "owasp_top_10_production" in refs.get_available_profiles()
    assert "fintech_zero_trust_strict" in refs.get_available_profiles()
    assert "api_perimeter_hardened" in refs.get_available_profiles()

    profile = refs.get_benchmarks()
    assert profile["metrics"]["max_allowed_hardcoded_secrets"] == 0
    assert profile["metrics"]["requires_safe_link_isolation"] is True


def test_gabriel_inspector_clean_code(temp_workspace):
    py_file = os.path.join(temp_workspace, "secure_api.py")
    with open(py_file, "w", encoding="utf-8") as f:
        f.write("""import os

api_key = os.environ.get("STRIPE_API_KEY", "")
def query_user(user_id: int):
    # Parameterized query safe from SQLi
    return ("SELECT * FROM users WHERE id = %s", (user_id,))
""")

    inspector = GabrielSecurityInspector(py_file)
    metrics = inspector.inspect()

    assert metrics["total_vulnerabilities"] == 0
    assert metrics["has_critical_blocker"] is False
    assert len(metrics["secret_leaks"]) == 0
    assert len(metrics["injections_found"]) == 0


def test_gabriel_inspector_vulnerable_code(temp_workspace):
    py_file = os.path.join(temp_workspace, "vulnerable.py")
    with open(py_file, "w", encoding="utf-8") as f:
        f.write("""api_key = "sk_live_secret1234567890abcdef"
def run_command(cmd):
    import subprocess
    subprocess.run(cmd, shell=True)
def load_data(f):
    import yaml
    return yaml.load(f)
""")

    inspector = GabrielSecurityInspector(py_file)
    metrics = inspector.inspect()

    assert metrics["total_vulnerabilities"] >= 3
    assert metrics["has_critical_blocker"] is True
    assert len(metrics["secret_leaks"]) >= 1
    assert any("shell=True" in item["pattern_desc"] for item in metrics["injections_found"])
    assert len(metrics["deserialization_flaws"]) >= 1


def test_gabriel_rubric_and_critic_rejection():
    rubric = GabrielSecurityRubric()
    critic = GabrielBlindCritic(passing_score=85.0)

    poor_metrics = {
        "secret_leaks": [{"pattern_desc": "Hardcoded credential", "occurrences": 1}],
        "injections_found": [{"pattern_desc": "SQL Injection in query", "occurrences": 1}],
        "deserialization_flaws": [{"pattern_desc": "pickle.loads() RCE risk", "occurrences": 1}],
        "transport_flaws": [{"pattern_desc": "verify=False", "occurrences": 1}],
        "total_vulnerabilities": 4,
        "has_critical_blocker": True
    }

    eval_result = rubric.evaluate(poor_metrics)
    assert eval_result["passed"] is False
    assert eval_result["total_score"] < 40.0

    critique = critic.critique(eval_result, poor_metrics)
    assert critique["verdict"] == "REJECTED"
    assert critique["defects_count"] >= 4
    assert any(d["category"] == "CREDENTIAL_EXPOSURE" for d in critique["defect_ledger"])
    assert any(d["category"] == "INJECTION_ATTACK_SURFACE" for d in critique["defect_ledger"])


def test_gabriel_elevation_engine(temp_workspace):
    py_file = os.path.join(temp_workspace, "app.py")
    with open(py_file, "w", encoding="utf-8") as f:
        f.write("""api_key = "sk_live_123456789012345"
def fetch_data():
    import requests
    return requests.get("https://api.example.com", verify=False)
def run_cmd(cmd):
    import subprocess
    return subprocess.run(cmd, shell=True)
""")

    engine = GabrielElevationEngine()
    elevated = engine.elevate(py_file)

    assert 'os.environ.get("API_KEY"' in elevated
    assert "verify=True" in elevated
    assert "shell=False" in elevated


def test_gabriel_master_autonomous_cycle(temp_workspace):
    py_file = os.path.join(temp_workspace, "unsafe_service.py")
    with open(py_file, "w", encoding="utf-8") as f:
        f.write("""secret_key = "production_super_secret_token_12345"
def execute_task(task):
    import subprocess
    subprocess.call(task, shell=True)
""")

    master = GabrielFrostMaster(target_file=py_file, passing_threshold=85.0)

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
    assert "GABRIEL FROST" in report
    assert "CERTIFIED" in report
