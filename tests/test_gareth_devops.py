"""
Unit & Integration Tests for Gareth Drake (DevOps & Cloud SRE Architect Subsystem)
"""

import os
import shutil
import tempfile
import pytest

from professions.devops_sre_architect.references import GarethDevOpsReferences
from professions.devops_sre_architect.inspector import GarethDevOpsInspector
from professions.devops_sre_architect.rubric import GarethDevOpsRubric
from professions.devops_sre_architect.blind_critic import GarethBlindCritic
from professions.devops_sre_architect.elevation_engine import GarethElevationEngine
from professions.devops_sre_architect.master import GarethDrakeMaster


@pytest.fixture
def temp_workspace():
    """Creates a temporary workspace for isolated testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_gareth_references_loading():
    refs = GarethDevOpsReferences()
    assert "production_kubernetes_resilient" in refs.get_available_profiles()
    assert "cloud_native_docker_hardened" in refs.get_available_profiles()
    assert "idempotent_ci_cd_pipeline" in refs.get_available_profiles()

    profile = refs.get_benchmarks()
    assert profile["metrics"]["forbid_root_user"] is True
    assert profile["metrics"]["forbid_unpinned_latest_tag"] is True


def test_gareth_inspector_hardened_dockerfile(temp_workspace):
    dockerfile = os.path.join(temp_workspace, "Dockerfile")
    with open(dockerfile, "w", encoding="utf-8") as f:
        f.write("""FROM node:20-alpine
WORKDIR /app
COPY . .
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8080/healthz || exit 1
USER 10001:10001
CMD ["node", "server.js"]
""")

    inspector = GarethDevOpsInspector(dockerfile)
    metrics = inspector.inspect()

    assert metrics["file_type"] == "dockerfile"
    assert metrics["has_non_root_user"] is True
    assert metrics["has_unpinned_latest_tag"] is False
    assert metrics["has_healthcheck"] is True
    assert len(metrics["flaws_detected"]) == 0


def test_gareth_inspector_flawed_dockerfile(temp_workspace):
    dockerfile = os.path.join(temp_workspace, "Dockerfile")
    with open(dockerfile, "w", encoding="utf-8") as f:
        f.write("""FROM node:latest
WORKDIR /app
COPY . .
CMD ["node", "server.js"]
""")

    inspector = GarethDevOpsInspector(dockerfile)
    metrics = inspector.inspect()

    assert metrics["has_non_root_user"] is False
    assert metrics["has_unpinned_latest_tag"] is True
    assert metrics["has_healthcheck"] is False
    assert len(metrics["flaws_detected"]) >= 3


def test_gareth_rubric_and_critic_rejection():
    rubric = GarethDevOpsRubric()
    critic = GarethBlindCritic(passing_score=85.0)

    poor_metrics = {
        "has_non_root_user": False,
        "has_unpinned_latest_tag": True,
        "has_healthcheck": False,
        "has_resource_limits": False,
        "has_graceful_shutdown": False,
        "has_script_error_trap": False
    }

    eval_result = rubric.evaluate(poor_metrics)
    assert eval_result["passed"] is False
    assert eval_result["total_score"] < 40.0

    critique = critic.critique(eval_result, poor_metrics)
    assert critique["verdict"] == "REJECTED"
    assert critique["defects_count"] >= 4
    assert any(d["category"] == "CONTAINER_SECURITY" for d in critique["defect_ledger"])
    assert any(d["category"] == "OBSERVABILITY_PROBES" for d in critique["defect_ledger"])


def test_gareth_elevation_engine_dockerfile(temp_workspace):
    dockerfile = os.path.join(temp_workspace, "Dockerfile")
    with open(dockerfile, "w", encoding="utf-8") as f:
        f.write("""FROM node:latest
WORKDIR /app
COPY . .
CMD ["node", "server.js"]
""")

    engine = GarethElevationEngine()
    elevated = engine.elevate(dockerfile)

    assert "FROM node:stable" in elevated or "FROM node:20-alpine" in elevated
    assert "USER 10001:10001" in elevated
    assert "HEALTHCHECK" in elevated


def test_gareth_elevation_engine_yaml(temp_workspace):
    yaml_file = os.path.join(temp_workspace, "deploy.yaml")
    with open(yaml_file, "w", encoding="utf-8") as f:
        f.write("""apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
""")

    engine = GarethElevationEngine()
    elevated = engine.elevate(yaml_file)

    assert "resources:" in elevated
    assert "limits:" in elevated
    assert "livenessProbe:" in elevated
    assert "runAsNonRoot: true" in elevated


def test_gareth_master_autonomous_cycle(temp_workspace):
    dockerfile = os.path.join(temp_workspace, "Dockerfile")
    with open(dockerfile, "w", encoding="utf-8") as f:
        f.write("""FROM node:latest
WORKDIR /app
COPY . .
CMD ["node", "server.js"]
""")

    master = GarethDrakeMaster(target_file=dockerfile, passing_threshold=85.0)

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
    assert "GARETH DRAKE" in report
    assert "CERTIFIED" in report
