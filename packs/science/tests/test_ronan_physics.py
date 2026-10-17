"""
Unit tests for Ronan Blackwood (Lead Game Systems & Physics Architect Subsystem).
"""

import pytest
from professions.game_physics_architect.references import GameEngineReferenceLibrary
from professions.game_physics_architect.inspector import GamePhysicsInspector
from professions.game_physics_architect.rubric import GamePhysicsRubric
from professions.game_physics_architect.blind_critic import BlindGamePhysicsCritic
from professions.game_physics_architect.elevation_engine import GamePhysicsElevationEngine
from professions.game_physics_architect.master import RonanBlackwoodMaster


def test_ronan_references_loading():
    budgets = GameEngineReferenceLibrary.get_frame_budget_standards()
    assert "target_60fps" in budgets
    assert "target_120fps" in budgets
    assert budgets["target_60fps"]["total_budget_ms"] <= 16.7
    assert budgets["target_120fps"]["total_budget_ms"] <= 8.4

    sim = GameEngineReferenceLibrary.get_simulation_constants()
    assert sim["default_fixed_dt"] == 1.0 / 60.0
    assert sim["max_safe_restitution"] <= 1.0

    anti_patterns = GameEngineReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 5
    assert any(ap["id"] == "variable_dt_physics" for ap in anti_patterns)


def test_ronan_inspector_aaa_engine():
    inspector = GamePhysicsInspector()
    aaa_loop = (
        "const FIXED_DT = 1.0 / 60.0;\n"
        "const MAX_FRAME_TIME = 0.25;\n"
        "let accumulator = 0.0;\n"
        "const particlePool = new ObjectPool(() => ({ x: 0, y: 0 }), 500);\n"
        "const spatialHash = new SpatialHashGrid(64);\n\n"
        "function loop(currentTime) {\n"
        "    let frameTime = Math.min((currentTime - lastTime) / 1000.0, MAX_FRAME_TIME);\n"
        "    accumulator += frameTime;\n"
        "    while (accumulator >= FIXED_DT) {\n"
        "        physicsTick(FIXED_DT);\n"
        "        accumulator -= FIXED_DT;\n"
        "    }\n"
        "    const alpha = accumulator / FIXED_DT;\n"
        "    render(alpha);\n"
        "}\n"
    )
    report = inspector.inspect(aaa_loop)
    assert report.is_simulation_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_fixed_timestep is True
    assert report.metrics.has_variable_dt_leak is False
    assert report.metrics.has_accumulator_clamp is True
    assert report.metrics.has_object_pooling is True
    assert report.metrics.has_broadphase_collision is True


def test_ronan_inspector_flawed_loop():
    inspector = GamePhysicsInspector()
    flawed_loop = (
        "function update(dt) {\n"
        "    pos += vel * dt;\n"
        "    const p = new Particle();\n"
        "    for (let i = 0; i < entities.length; i++) {\n"
        "        for (let j = i + 1; j < entities.length; j++) {\n"
        "            collide(entities[i], entities[j]);\n"
        "        }\n"
        "    }\n"
        "}\n"
    )
    report = inspector.inspect(flawed_loop)
    assert report.is_simulation_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_variable_dt_leak is True
    assert report.metrics.has_heap_allocations_in_loop is True
    assert report.metrics.has_brute_force_all_pairs is True


def test_ronan_rubric_and_veto():
    inspector = GamePhysicsInspector()
    rubric = GamePhysicsRubric()

    stutter_loop = (
        "function tick(dt) {\n"
        "    position += velocity * dt;\n"
        "    new Bullet();\n"
        "}\n"
    )
    report = inspector.inspect(stutter_loop)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) > 0


def test_ronan_critic_defect_ledger():
    critic = BlindGamePhysicsCritic()
    flawed_code = (
        "function update(dt) {\n"
        "    pos += vel * dt;\n"
        "    new Vector();\n"
        "}\n"
    )
    ledger = critic.review(flawed_code)
    assert ledger.verdict == "REJECTED_FRAME_DROP_HAZARD"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 2
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_ronan_elevation_engine():
    engine = GamePhysicsElevationEngine()
    flawed_code = (
        "function update(dt) {\n"
        "    pos += vel * dt;\n"
        "    new Particle();\n"
        "    for (let i = 0; i < entities.length; i++) {\n"
        "        for (let j = i + 1; j < entities.length; j++) {\n"
        "            collide(entities[i], entities[j]);\n"
        "        }\n"
        "    }\n"
        "}\n"
    )
    elevated_result = engine.elevate(flawed_code)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "DETERMINISTIC FIXED-TIMESTEP SIMULATION LOOP" in elevated_result["elevated_engine"]
    assert "ZERO-GC MEMORY MANAGEMENT" in elevated_result["elevated_engine"]
    assert "SpatialHashGrid" in elevated_result["elevated_engine"]


def test_ronan_master_autonomous_cycle():
    master = RonanBlackwoodMaster(passing_threshold=85)
    raw_loop = (
        "function renderLoop(dt) {\n"
        "    pos += vel * dt;\n"
        "    new Particle();\n"
        "}\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_loop)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE GAME SYSTEMS & PHYSICS BRIEFING" in result["executive_briefing"]
    assert "ENGINE CERTIFIED" in result["executive_briefing"]
