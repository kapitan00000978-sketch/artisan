"""
Dr. Vespera 'The Kinematic' Sterling - Blind Robotics Critic.

Provides an objective, code-blind evaluation of robotic control implementations,
generating a strict defect ledger and ruthless engineering review.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.robotics_embodied_ai_architect.inspector import RoboticsSystemInspector, RoboticsInspectionReport
from professions.robotics_embodied_ai_architect.rubric import RoboticsRubric, RoboticsEvaluation


@dataclass
class RoboticsDefect:
    id: str
    severity: str
    description: str
    actionable_fix: str


@dataclass
class RoboticsDefectLedger:
    score: int
    is_certified: bool
    veto_triggered: bool
    defects: List[RoboticsDefect] = field(default_factory=list)
    summary: str = ""

    @property
    def fatal_defects_count(self) -> int:
        return len([d for d in self.defects if d.severity in ("FATAL", "CRITICAL")])

    @property
    def verdict(self) -> str:
        return "CERTIFIED" if self.is_certified else "REJECTED"


class BlindRoboticsCritic:
    """Objective, unsparing robotics critic auditing control loops against physical safety standards."""

    def __init__(self):
        self.inspector = RoboticsSystemInspector()
        self.rubric = RoboticsRubric()

    def review(self, code_input: Any) -> RoboticsDefectLedger:
        report: RoboticsInspectionReport = self.inspector.inspect(code_input)
        evaluation: RoboticsEvaluation = self.rubric.evaluate(report)

        defects: List[RoboticsDefect] = []

        # 1. Blocking sleep
        if report.metrics.has_blocking_sleep_in_loop:
            defects.append(
                RoboticsDefect(
                    id="ROB-001",
                    severity="CRITICAL",
                    description="Blocking sleep() call found on inner actuation path, destroying hard real-time loop determinism.",
                    actionable_fix="Replace blocking sleep with non-blocking monotonic clock cycle tracking (time.monotonic_ns)."
                )
            )

        # 2. Uncapped motor torque
        if report.metrics.has_uncapped_torque:
            defects.append(
                RoboticsDefect(
                    id="ROB-002",
                    severity="FATAL",
                    description="Unbounded motor torque commands sent without saturation clamping.",
                    actionable_fix="Enforce torque saturation clamping: safe_torque = max(-MAX_TORQUE_NM, min(MAX_TORQUE_NM, raw_torque))."
                )
            )

        # 3. Missing emergency stop
        if not report.metrics.has_emergency_stop_interlock:
            defects.append(
                RoboticsDefect(
                    id="ROB-003",
                    severity="FATAL",
                    description="Robotic system lacks emergency stop (E-Stop) or fail-safe zero-torque interlock.",
                    actionable_fix="Implement trigger_emergency_stop() interlock returning 0.0 torque immediately when active."
                )
            )

        # 4. Undamped kinematic inversion
        if report.metrics.has_undamped_inversion:
            defects.append(
                RoboticsDefect(
                    id="ROB-004",
                    severity="HIGH",
                    description="Kinematic Jacobian inverted without singularity damping, causing velocity explosion near singularities.",
                    actionable_fix="Implement Damped Least Squares (Levenberg-Marquardt): jacobian / (jacobian**2 + damping**2)."
                )
            )

        # 5. Missing EKF sensory fusion
        if not report.metrics.has_ekf_sensor_fusion:
            defects.append(
                RoboticsDefect(
                    id="ROB-005",
                    severity="MEDIUM",
                    description="State estimation relies on open-loop integration without Kalman filter covariance tracking.",
                    actionable_fix="Implement update_sensor_fusion_ekf() fusing IMU accelerations with encoder positions."
                )
            )

        summary = (
            f"Dr. Vespera Sterling Robotics Review: Score {evaluation.total_score}/100. "
            f"{'CERTIFIED for physical deployment.' if evaluation.is_certified else 'REJECTED: Kinetic hazards and real-time violations present.'}"
        )

        return RoboticsDefectLedger(
            score=evaluation.total_score,
            is_certified=evaluation.is_certified,
            veto_triggered=evaluation.veto_triggered,
            defects=defects,
            summary=summary
        )
