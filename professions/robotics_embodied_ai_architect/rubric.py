"""
Dr. Vespera 'The Kinematic' Sterling - 100-Point Weighted Robotics Rubric.

Evaluates robotics control implementations against hard real-time determinism,
torque saturation clamping, emergency stop interlocks, and singularity-damped kinematics.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.robotics_embodied_ai_architect.inspector import RoboticsInspectionReport, RoboticsMetrics


@dataclass
class RoboticsDimensionScore:
    name: str
    weight: int
    score: int
    status: str
    reasons: List[str] = field(default_factory=list)


@dataclass
class RoboticsEvaluation:
    total_score: int
    is_certified: bool
    dimensions: List[RoboticsDimensionScore]
    veto_triggered: bool
    veto_reason: str = ""
    veto_reasons: List[str] = field(default_factory=list)


class RoboticsRubric:
    """100-point weighted domain rubric enforcing Vespera Sterling robotics control standards."""

    PASSING_THRESHOLD: int = 85

    def evaluate(self, report: RoboticsInspectionReport) -> RoboticsEvaluation:
        m: RoboticsMetrics = report.metrics
        dimensions: List[RoboticsDimensionScore] = []
        veto_triggered = False
        veto_reasons: List[str] = []

        # 1. Hard Real-Time Determinism (25 pts)
        d1_score = 0
        d1_reasons = []
        if m.has_blocking_sleep_in_loop:
            d1_score = 0
            d1_reasons.append("VETO: Blocking sleep or delay detected inside actuation loop.")
            veto_triggered = True
            veto_reasons.append("UNBOUNDED_CONTROL_LOOP_JITTER: Blocking delay destroys real-time determinism.")
        elif m.has_bounded_actuation_cycle:
            d1_score = 25
            d1_reasons.append("Deterministic monotonic clock timing verified without blocking delays.")
        else:
            d1_score = 15
            d1_reasons.append("Actuation cycle timing should use explicit monotonic clock intervals.")
        dimensions.append(RoboticsDimensionScore(
            name="Hard Real-Time Determinism",
            weight=25,
            score=d1_score,
            status="PASSED" if d1_score >= 20 else "FAILED",
            reasons=d1_reasons
        ))

        # 2. Safety Torque Saturation Clamping (25 pts)
        d2_score = 0
        d2_reasons = []
        if m.has_uncapped_torque:
            d2_score = 0
            d2_reasons.append("VETO: Uncapped motor torque commands detected without saturation clamp.")
            veto_triggered = True
            veto_reasons.append("UNCAPPED_MOTOR_TORQUE: Unbounded torque risks mechanical gear and motor destruction.")
        elif m.has_torque_saturation_clamping:
            d2_score = 25
            d2_reasons.append("Hard torque saturation limits (max_torque clamping) enforced.")
        else:
            d2_score = 10
            d2_reasons.append("Torque bounds should be explicitly clamped to rated motor limits.")
        dimensions.append(RoboticsDimensionScore(
            name="Torque Saturation Clamping",
            weight=25,
            score=d2_score,
            status="PASSED" if d2_score >= 20 else "FAILED",
            reasons=d2_reasons
        ))

        # 3. Emergency Stop Interlock (20 pts)
        d3_score = 0
        d3_reasons = []
        if not m.has_emergency_stop_interlock:
            d3_score = 0
            d3_reasons.append("VETO: Missing emergency stop (E-Stop) safety interlock.")
            veto_triggered = True
            veto_reasons.append("MISSING_EMERGENCY_STOP: Physical robots must have immediate fail-safe E-Stop capability.")
        else:
            d3_score = 20
            d3_reasons.append("Emergency stop safety interlock verified with zero-torque safe state.")
        dimensions.append(RoboticsDimensionScore(
            name="Emergency Stop Interlock",
            weight=20,
            score=d3_score,
            status="PASSED" if d3_score >= 15 else "FAILED",
            reasons=d3_reasons
        ))

        # 4. Singularity-Damped Kinematics (15 pts)
        d4_score = 0
        d4_reasons = []
        if m.has_undamped_inversion:
            d4_score = 0
            d4_reasons.append("Undamped raw Jacobian matrix inversion detected.")
        elif m.has_singularity_damping:
            d4_score = 15
            d4_reasons.append("Singularity-damped kinematics (Damped Least Squares / regularizer) active.")
        else:
            d4_score = 10
            d4_reasons.append("Kinematic inversion should incorporate singularity damping factor.")
        dimensions.append(RoboticsDimensionScore(
            name="Singularity-Damped Kinematics",
            weight=15,
            score=d4_score,
            status="PASSED" if d4_score >= 12 else "FAILED",
            reasons=d4_reasons
        ))

        # 5. Sensory Fusion & Covariance Tracking (15 pts)
        d5_score = 0
        d5_reasons = []
        if m.has_ekf_sensor_fusion:
            d5_score = 15
            d5_reasons.append("EKF sensory fusion with covariance tracking verified.")
        else:
            d5_score = 8
            d5_reasons.append("State estimation should fuse sensory inputs with explicit error covariance.")
        dimensions.append(RoboticsDimensionScore(
            name="Sensory Fusion & Covariance",
            weight=15,
            score=d5_score,
            status="PASSED" if d5_score >= 12 else "FAILED",
            reasons=d5_reasons
        ))

        total_score = sum(d.score for d in dimensions)
        if veto_triggered:
            total_score = min(total_score, 45)

        is_certified = (total_score >= self.PASSING_THRESHOLD) and not veto_triggered
        veto_reason = " | ".join(veto_reasons) if veto_reasons else ""

        return RoboticsEvaluation(
            total_score=total_score,
            is_certified=is_certified,
            dimensions=dimensions,
            veto_triggered=veto_triggered,
            veto_reason=veto_reason,
            veto_reasons=veto_reasons
        )
