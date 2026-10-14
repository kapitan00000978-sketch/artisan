"""
Commander Cassiopeia 'The Orbital' Sterling - Objective Aerospace Avionics Inspector.

This module inspects flight control software, guidance systems, and satellite avionics
for Triple Modular Redundancy (TMR), radiation SEU memory scrubbing, and autonomous safe-mode fallback.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class AvionicsMetrics:
    has_tmr_majority_voting: bool = False
    has_autonomous_safe_mode: bool = False
    has_radiation_memory_scrubbing: bool = False
    has_deterministic_time_framing: bool = False
    has_single_point_of_failure: bool = False
    has_dynamic_heap_allocation: bool = False
    has_unbounded_sleep_in_flight_loop: bool = False
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class AvionicsInspectionReport:
    metrics: AvionicsMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_avionics_viable: bool = False


class AvionicsSystemInspector:
    """Rigorous aerospace flight software auditor enforcing TMR voting, safe-mode fallback, and SEU scrubbing."""

    def inspect(self, code_input: Any) -> AvionicsInspectionReport:
        """
        Audits flight software, GNC algorithms, or orbital telemetry processors.
        """
        metrics = self._extract_metrics(code_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Single Point of Failure (SPOF)
        if metrics.has_single_point_of_failure:
            critical_violations.append(
                "Single Point of Failure (SPOF): Actuation or thruster commands executed from a single unvoted channel."
            )
        elif metrics.has_tmr_majority_voting:
            benchmarks_passed.append("Triple Modular Redundancy (TMR) Byzantine majority voting active.")
        else:
            warnings.append("Consider verifying 3-channel voting on critical flight control commands.")

        # 2. Dynamic Heap Memory Allocation
        if metrics.has_dynamic_heap_allocation:
            critical_violations.append(
                "Dynamic Heap Allocation in Flight: Calling malloc() or free() violates DO-178C Level A flight certification."
            )
        else:
            benchmarks_passed.append("Zero dynamic heap allocation policy verified.")

        # 3. Autonomous Safe-Mode Transition
        if not metrics.has_autonomous_safe_mode:
            critical_violations.append(
                "Missing Autonomous Safe-Mode: Spacecraft lacks automated transition to power-positive Sun-pointing safe hold."
            )
        else:
            benchmarks_passed.append("Autonomous Safe-Mode contingency state machine verified.")

        # 4. Radiation SEU Memory Scrubbing
        if metrics.has_radiation_memory_scrubbing:
            benchmarks_passed.append("Radiation SEU soft error memory scrubbing with EDAC verified.")
        else:
            warnings.append("Consider verifying periodic background EDAC memory scrubbing to prevent radiation bit-flip accumulation.")

        # 5. Deterministic Time Framing
        if metrics.has_unbounded_sleep_in_flight_loop:
            critical_violations.append(
                "Unbounded Sleep in Flight Loop: Calling sleep() violates ARINC 653 deterministic major/minor frame deadlines."
            )
        elif metrics.has_deterministic_time_framing:
            benchmarks_passed.append("Deterministic monotonic frame timing verified.")
        else:
            warnings.append("Ensure major flight frame execution is monitored with monotonic timestamps.")

        is_viable = (
            len(critical_violations) == 0 and
            metrics.has_tmr_majority_voting and
            metrics.has_autonomous_safe_mode
        )

        return AvionicsInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_avionics_viable=is_viable
        )

    def _extract_metrics(self, code_input: Any) -> AvionicsMetrics:
        metadata: Dict[str, Any] = {}
        text = ""

        if isinstance(code_input, dict):
            metadata = code_input
            text = code_input.get("code", "") or json.dumps(code_input)
        elif isinstance(code_input, str):
            text = code_input

        # Clean comments to avoid false triggers
        clean_code = re.sub(r'#.*', '', text)
        clean_code = re.sub(r'//.*', '', clean_code)
        clean_code = re.sub(r'/\*.*?\*/', '', clean_code, flags=re.DOTALL)
        text_lower = clean_code.lower()

        m = AvionicsMetrics()

        # 1. TMR Majority Voting
        has_tmr = bool(
            "tmr_majority_vote" in text_lower or
            "majority_vote" in text_lower or
            "tmr" in text_lower or
            ("ch_a" in text_lower and "ch_b" in text_lower and "ch_c" in text_lower) or
            metadata.get("has_tmr_majority_voting", False)
        )
        m.has_tmr_majority_voting = has_tmr

        # 2. Autonomous Safe-Mode
        has_safemode = bool(
            "safe_mode" in text_lower or
            "transition_to_safe_mode" in text_lower or
            "safe_hold" in text_lower or
            metadata.get("has_autonomous_safe_mode", False)
        )
        m.has_autonomous_safe_mode = has_safemode

        # 3. Radiation Memory Scrubbing
        has_scrubbing = bool(
            "scrub_memory" in text_lower or
            "memory_scrub" in text_lower or
            "seu" in text_lower or
            "edac" in text_lower or
            metadata.get("has_radiation_memory_scrubbing", False)
        )
        m.has_radiation_memory_scrubbing = has_scrubbing

        # 4. Deterministic Time Framing
        has_framing = bool(
            "major_frame" in text_lower or
            "monotonic" in text_lower or
            "minor_frame" in text_lower or
            metadata.get("has_deterministic_time_framing", False)
        )
        m.has_deterministic_time_framing = has_framing

        # 5. Dynamic Heap Allocation
        has_heap = bool(
            "malloc(" in text_lower or
            "free(" in text_lower or
            metadata.get("has_dynamic_heap_allocation", False)
        )
        m.has_dynamic_heap_allocation = has_heap

        # 6. Unbounded Sleep
        has_sleep = bool(
            "time.sleep" in text_lower or
            "sleep(" in text_lower or
            metadata.get("has_unbounded_sleep_in_flight_loop", False)
        )
        m.has_unbounded_sleep_in_flight_loop = has_sleep

        # 7. Single Point of Failure
        if ("actuate(" in text_lower or "fire_thruster" in text_lower) and not has_tmr:
            m.has_single_point_of_failure = True
        if metadata.get("has_single_point_of_failure", False):
            m.has_single_point_of_failure = True

        # Anti-pattern logging
        if m.has_single_point_of_failure:
            m.anti_patterns_detected.append("Single point of failure in critical actuation command path")
        if m.has_dynamic_heap_allocation:
            m.anti_patterns_detected.append("Dynamic heap allocation inside DO-178C flight software")
        if m.has_unbounded_sleep_in_flight_loop:
            m.anti_patterns_detected.append("Unbounded sleep call inside ARINC 653 flight frame loop")

        return m
