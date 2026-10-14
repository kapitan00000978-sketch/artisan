"""
Unit tests for Dr. Vespera 'The Kinematic' Sterling (Autonomous Robotics & Embodied AI Architect Subsystem).
"""

import pytest
from professions.robotics_embodied_ai_architect.references import (
    RoboticsReferenceLibrary,
    ROBOTICS_CONTROL_BENCHMARKS,
    CANONICAL_ROBOTICS_CORE,
)
from professions.robotics_embodied_ai_architect.inspector import RoboticsSystemInspector
from professions.robotics_embodied_ai_architect.rubric import RoboticsRubric
from professions.robotics_embodied_ai_architect.blind_critic import BlindRoboticsCritic
from professions.robotics_embodied_ai_architect.elevation_engine import RoboticsElevationEngine
from professions.robotics_embodied_ai_architect.master import VesperaSterlingMaster


def test_vespera_references_loading():
    benchmarks = RoboticsReferenceLibrary.get_benchmarks()
    assert benchmarks["target_control_frequency_hz"] == 1000
    assert benchmarks["max_cycle_jitter_microseconds"] == 50
    assert benchmarks["singularity_damping_factor_lambda"] == 0.05

    standards = RoboticsReferenceLibrary.get_standards()
    assert "deterministic_actuation_cycle" in standards
    assert "ekf_sensory_fusion" in standards
    assert "singularity_damped_inverse_kinematics" in standards
    assert "torque_saturation_safety_envelope" in standards

    anti_patterns = RoboticsReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "blocking_sleep_in_control_loop" for ap in anti_patterns)


def test_vespera_inspector_clean_code():
    inspector = RoboticsSystemInspector()
    report = inspector.inspect(CANONICAL_ROBOTICS_CORE)

    assert report.is_robotics_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_bounded_actuation_cycle is True
    assert report.metrics.has_torque_saturation_clamping is True
    assert report.metrics.has_emergency_stop_interlock is True
    assert report.metrics.has_singularity_damping is True
    assert report.metrics.has_ekf_sensor_fusion is True
    assert report.metrics.has_blocking_sleep_in_loop is False
    assert report.metrics.has_uncapped_torque is False


def test_vespera_inspector_flawed_code():
    inspector = RoboticsSystemInspector()
    flawed_code = (
        "def control_loop(raw_torque):\n"
        "    time.sleep(0.01)\n"
        "    return raw_torque\n"
    )
    report = inspector.inspect(flawed_code)

    assert report.is_robotics_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_blocking_sleep_in_loop is True
    assert report.metrics.has_uncapped_torque is True
    assert report.metrics.has_emergency_stop_interlock is False


def test_vespera_rubric_and_veto():
    inspector = RoboticsSystemInspector()
    rubric = RoboticsRubric()

    dangerous_code = (
        "def actuate(joint_id, torque):\n"
        "    time.sleep(0.005)\n"
        "    send_motor_torque(joint_id, torque)\n"
    )
    report = inspector.inspect(dangerous_code)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score <= 45
    assert evaluation.veto_triggered is True
    assert "UNBOUNDED_CONTROL_LOOP_JITTER" in evaluation.veto_reason or "UNCAPPED_MOTOR_TORQUE" in evaluation.veto_reason


def test_vespera_critic_defect_ledger():
    critic = BlindRoboticsCritic()
    flawed_code = (
        "def compute_jacobian(theta):\n"
        "    return numpy.linalg.inv(J)\n"
    )
    ledger = critic.review(flawed_code)

    assert ledger.is_certified is False
    assert ledger.score < 85
    assert any(d.id == "ROB-004" for d in ledger.defects)
    assert any("singularity" in d.description.lower() for d in ledger.defects)


def test_vespera_elevation_engine():
    engine = RoboticsElevationEngine()
    flawed_code = (
        "class RawRoboticsDriver:\n"
        "    def execute_actuation(self, raw_torque):\n"
        "        time.sleep(0.001)\n"
        "        return raw_torque\n"
    )
    elevated_result = engine.elevate(flawed_code)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "time.sleep" not in elevated_result["elevated_code"]
    assert "MAX_TORQUE_NM" in elevated_result["elevated_code"]
    assert "trigger_emergency_stop" in elevated_result["elevated_code"]
    assert "compute_damped_inverse_kinematics" in elevated_result["elevated_code"]


def test_vespera_master_autonomous_cycle():
    master = VesperaSterlingMaster(passing_threshold=85)
    raw_code = (
        "class BasicRobot:\n"
        "    def actuate(self, cmd):\n"
        "        return cmd\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_code)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE ROBOTICS & CONTROL BRIEFING" in result["executive_briefing"]
    assert "ROBOTICS SAFETY CERTIFIED" in result["executive_briefing"]
