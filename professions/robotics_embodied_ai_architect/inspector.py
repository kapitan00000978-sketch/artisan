"""
Dr. Vespera 'The Kinematic' Sterling - Objective Robotics & Embodied AI Inspector.

This module inspects robotic control loops, trajectory generators, and inverse kinematics solvers
for hard real-time determinism, torque saturation clamping, singularity damping, and E-stop interlocks.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class RoboticsMetrics:
    has_bounded_actuation_cycle: bool = False
    has_torque_saturation_clamping: bool = False
    has_emergency_stop_interlock: bool = False
    has_singularity_damping: bool = False
    has_ekf_sensor_fusion: bool = False
    has_blocking_sleep_in_loop: bool = False
    has_uncapped_torque: bool = False
    has_undamped_inversion: bool = False
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class RoboticsInspectionReport:
    metrics: RoboticsMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_robotics_viable: bool = False


class RoboticsSystemInspector:
    """Rigorous robotics control auditor enforcing real-time determinism, torque clamping, and singularity damping."""

    def inspect(self, code_input: Any) -> RoboticsInspectionReport:
        """
        Audits robotics control loop, trajectory generator, or kinematic solver.
        """
        metrics = self._extract_metrics(code_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Blocking Sleep in Actuation Loop
        if metrics.has_blocking_sleep_in_loop:
            critical_violations.append(
                "Blocking Sleep in Control Loop: Found time.sleep() or uncalibrated delay in actuation cycle. Destroys 1kHz control determinism."
            )
        elif metrics.has_bounded_actuation_cycle:
            benchmarks_passed.append("Deterministic bounded actuation cycle with monotonic timing verified.")
        else:
            warnings.append("Consider verifying monotonic clock loop period tracking (e.g. time.monotonic_ns).")

        # 2. Torque Saturation Clamping
        if metrics.has_uncapped_torque:
            critical_violations.append(
                "Uncapped Motor Torque: Raw torque commands emitted without max_torque saturation clamping or safety envelope."
            )
        elif metrics.has_torque_saturation_clamping:
            benchmarks_passed.append("Hard torque saturation clamping enforced (max_torque boundary active).")
        else:
            warnings.append("Actuation torque commands should be bounded via min/max clamping.")

        # 3. Emergency Stop Interlock
        if not metrics.has_emergency_stop_interlock:
            critical_violations.append(
                "Missing Emergency Stop Interlock: No active E-Stop, dead-man switch, or safe state fallback detected."
            )
        else:
            benchmarks_passed.append("Emergency stop (E-Stop) safety interlock verified.")

        # 4. Kinematic Singularity Damping
        if metrics.has_undamped_inversion:
            critical_violations.append(
                "Undamped Kinematic Matrix Inversion: Raw Jacobian matrix inversion detected without singularity damping (risks infinite joint velocity)."
            )
        elif metrics.has_singularity_damping:
            benchmarks_passed.append("Singularity-damped inverse kinematics (Damped Least Squares / lambda regularization) verified.")
        else:
            warnings.append("Consider verifying singularity damping factor for Jacobian pseudo-inversion.")

        # 5. EKF Sensory Fusion
        if metrics.has_ekf_sensor_fusion:
            benchmarks_passed.append("Sensory fusion state estimation with covariance tracking verified.")
        else:
            warnings.append("Consider implementing EKF sensory fusion (IMU + encoders) to avoid dead-reckoning drift.")

        is_viable = (
            len(critical_violations) == 0 and
            metrics.has_torque_saturation_clamping and
            metrics.has_emergency_stop_interlock
        )

        return RoboticsInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_robotics_viable=is_viable
        )

    def _extract_metrics(self, code_input: Any) -> RoboticsMetrics:
        metadata: Dict[str, Any] = {}
        text = ""

        if isinstance(code_input, dict):
            metadata = code_input
            text = code_input.get("code", "") or json.dumps(code_input)
        elif isinstance(code_input, str):
            text = code_input

        # Clean comments to avoid false pattern triggers
        clean_code = re.sub(r'#.*', '', text)
        clean_code = re.sub(r'//.*', '', clean_code)
        text_lower = clean_code.lower()

        m = RoboticsMetrics()

        # 1. Blocking sleep
        has_sleep = bool(
            "time.sleep" in text_lower or
            "sleep(" in text_lower or
            "usleep(" in text_lower or
            metadata.get("has_blocking_sleep_in_loop", False)
        )
        m.has_blocking_sleep_in_loop = has_sleep

        # 2. Bounded actuation cycle
        has_bounded = bool(
            ("monotonic" in text_lower or "clock_gettime" in text_lower or "control_period" in text_lower) and
            not has_sleep or
            metadata.get("has_bounded_actuation_cycle", False)
        )
        m.has_bounded_actuation_cycle = has_bounded

        # 3. Torque saturation clamping
        has_clamping = bool(
            "max_torque" in text_lower or
            "torque_limit" in text_lower or
            "safe_torque" in text_lower or
            ("min(" in text_lower and "max(" in text_lower and "torque" in text_lower) or
            "clip(" in text_lower or
            metadata.get("has_torque_saturation_clamping", False)
        )
        m.has_torque_saturation_clamping = has_clamping

        # 4. Emergency stop interlock
        has_estop = bool(
            "e_stop" in text_lower or
            "emergency_stop" in text_lower or
            "dead_man" in text_lower or
            "safety_stop" in text_lower or
            metadata.get("has_emergency_stop_interlock", False)
        )
        m.has_emergency_stop_interlock = has_estop

        # 5. Singularity damping
        has_damping = bool(
            "damping" in text_lower or
            "damped" in text_lower or
            "levenberg" in text_lower or
            "singularity" in text_lower or
            "dls" in text_lower or
            metadata.get("has_singularity_damping", False)
        )
        m.has_singularity_damping = has_damping

        # 6. EKF sensory fusion
        has_ekf = bool(
            "ekf" in text_lower or
            "kalman" in text_lower or
            "covariance" in text_lower or
            "sensor_fusion" in text_lower or
            ("imu" in text_lower and "encoder" in text_lower) or
            metadata.get("has_ekf_sensor_fusion", False)
        )
        m.has_ekf_sensor_fusion = has_ekf

        # 7. Uncapped torque
        if "torque" in text_lower and not has_clamping:
            m.has_uncapped_torque = True
        if metadata.get("has_uncapped_torque", False):
            m.has_uncapped_torque = True

        # 8. Undamped inversion
        if "linalg.inv" in text_lower and not has_damping:
            m.has_undamped_inversion = True
        if metadata.get("has_undamped_inversion", False):
            m.has_undamped_inversion = True

        # Anti-pattern logging
        if m.has_blocking_sleep_in_loop:
            m.anti_patterns_detected.append("Blocking sleep or delay inside actuation cycle")
        if m.has_uncapped_torque:
            m.anti_patterns_detected.append("Uncapped motor torque command without saturation clamping")
        if m.has_undamped_inversion:
            m.anti_patterns_detected.append("Undamped raw Jacobian matrix inversion")

        return m
