"""
Unit & Integration Tests for Kaelen Vane (Principal 3D & Spatial CGI Artist Subsystem)
"""

import os
import shutil
import tempfile
import pytest

from professions.spatial_3d_artist.references import Kaelen3DReferences
from professions.spatial_3d_artist.inspector import Kaelen3DInspector
from professions.spatial_3d_artist.rubric import Kaelen3DRubric
from professions.spatial_3d_artist.blind_critic import KaelenBlindCritic
from professions.spatial_3d_artist.elevation_engine import KaelenElevationEngine
from professions.spatial_3d_artist.master import KaelenVaneMaster


@pytest.fixture
def temp_workspace():
    """Creates a temporary workspace for isolated testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_kaelen_references_loading():
    refs = Kaelen3DReferences()
    assert "webgl_realtime_optimized" in refs.get_available_profiles()
    assert "unreal_cinematic_pbr" in refs.get_available_profiles()
    assert "apple_spatial_vision" in refs.get_available_profiles()

    profile = refs.get_benchmarks()
    assert profile["metrics"]["max_poly_count"] > 0
    assert profile["metrics"]["requires_pbr_shading"] is True
    assert profile["metrics"]["requires_three_point_lighting"] is True


def test_kaelen_inspector_threejs(temp_workspace):
    html_file = os.path.join(temp_workspace, "scene.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head><title>3D Scene</title></head>
<body>
<script>
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    const light = new THREE.PointLight(0xffffff, 1);
    scene.add(light);
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
</script>
</body>
</html>""")

    inspector = Kaelen3DInspector(html_file)
    metrics = inspector.inspect()

    assert metrics["file_type"] == "threejs_webgl"
    assert metrics["has_flat_unlit_materials"] is True
    assert metrics["has_pbr_materials"] is False
    assert metrics["light_count"] == 1
    assert metrics["has_three_point_lighting"] is False
    assert metrics["has_aces_tone_mapping"] is False


def test_kaelen_inspector_obj_geometry(temp_workspace):
    obj_file = os.path.join(temp_workspace, "cube.obj")
    with open(obj_file, "w", encoding="utf-8") as f:
        f.write("""v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 1.0 1.0 0.0
v 0.0 1.0 0.0
vn 0.0 0.0 1.0
f 1//1 2//1 3//1
f 1//1 3//1 4//1
""")

    inspector = Kaelen3DInspector(obj_file)
    metrics = inspector.inspect()

    assert metrics["file_type"] == "obj_geometry"
    assert metrics["estimated_poly_count"] == 2
    assert metrics["has_normals"] is True
    assert metrics["manifold_topology"] is True


def test_kaelen_rubric_and_critic_rejection():
    rubric = Kaelen3DRubric()
    critic = KaelenBlindCritic(passing_score=85.0)

    poor_metrics = {
        "has_pbr_materials": False,
        "has_flat_unlit_materials": True,
        "light_count": 1,
        "has_three_point_lighting": False,
        "has_shadow_maps": False,
        "has_soft_shadows": False,
        "has_aces_tone_mapping": False,
        "has_srgb_encoding": False,
        "has_orbit_controls": False,
        "has_camera_damping": False,
        "estimated_poly_count": 2500,
        "manifold_topology": True
    }

    eval_result = rubric.evaluate(poor_metrics)
    assert eval_result["passed"] is False
    assert eval_result["total_score"] < 50.0

    critique = critic.critique(eval_result, poor_metrics)
    assert critique["verdict"] == "REJECTED"
    assert critique["defects_count"] >= 3
    assert any(d["category"] == "PBR_SHADING" for d in critique["defect_ledger"])
    assert any(d["category"] == "LIGHTING_AND_SHADOWS" for d in critique["defect_ledger"])


def test_kaelen_elevation_engine(temp_workspace):
    html_file = os.path.join(temp_workspace, "scene.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head><title>3D Scene</title></head>
<body>
<script>
    const scene = new THREE.Scene();
    const renderer = new THREE.WebGLRenderer();
    const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
</script>
</body>
</html>""")

    engine = KaelenElevationEngine()
    elevated = engine.elevate(html_file)

    assert "MeshStandardMaterial" in elevated
    assert "ACESFilmicToneMapping" in elevated
    assert "setupKaelenStudioLighting" in elevated
    assert "DirectionalLight" in elevated


def test_kaelen_master_autonomous_cycle(temp_workspace):
    html_file = os.path.join(temp_workspace, "amateur_3d.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head><title>Amateur 3D</title></head>
<body>
<script>
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    const light = new THREE.PointLight(0xffffff, 1);
    scene.add(light);
    const material = new THREE.MeshBasicMaterial({ color: 0x0000ff });
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), material);
    scene.add(mesh);
</script>
</body>
</html>""")

    master = KaelenVaneMaster(target_file=html_file, passing_threshold=85.0)

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
    assert "KAELEN VANE" in report
    assert "CERTIFIED" in report
