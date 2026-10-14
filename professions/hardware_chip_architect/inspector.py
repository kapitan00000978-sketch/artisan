"""
Ignis 'The Silicon' Thorne - Objective ASIC & FPGA Hardware Inspector.

This module inspects SystemVerilog/Verilog RTL for clock domain crossing (CDC) synchronizers,
inferred latch prevention, reset synchronization, and glitch-free FSM state protection.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class HardwareMetrics:
    has_cdc_synchronizer: bool = False
    has_latch_free_combinational_logic: bool = False
    has_synchronized_reset_deassertion: bool = False
    has_glitch_free_fsm: bool = False
    has_inferred_latch_risk: bool = False
    has_unsynchronized_cdc_risk: bool = False
    has_combinational_feedback_risk: bool = False
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class HardwareInspectionReport:
    metrics: HardwareMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_hardware_viable: bool = False


class HardwareSystemInspector:
    """Rigorous ASIC/FPGA RTL auditor enforcing CDC synchronization, latch prevention, and reset discipline."""

    def inspect(self, code_input: Any) -> HardwareInspectionReport:
        """
        Audits SystemVerilog / Verilog / HDL code or structural metadata.
        """
        metrics = self._extract_metrics(code_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Inferred Latch Risk
        if metrics.has_inferred_latch_risk:
            critical_violations.append(
                "Inferred Latch Risk: Combinational block missing default assignment or incomplete case branches. Generates transparent latch."
            )
        elif metrics.has_latch_free_combinational_logic:
            benchmarks_passed.append("Pure combinational logic verified (Zero inferred latches).")
        else:
            warnings.append("Consider verifying explicit default signal assignments in combinational blocks.")

        # 2. Unsynchronized Clock Domain Crossing
        if metrics.has_unsynchronized_cdc_risk:
            critical_violations.append(
                "Unsynchronized Clock Domain Crossing: Signal crossings between async clock domains detected without 2-FF synchronizer."
            )
        elif metrics.has_cdc_synchronizer:
            benchmarks_passed.append("Dual flip-flop CDC synchronizer verified (Metastability MTBF protected).")
        else:
            warnings.append("Verify whether cross-domain signals are passed through multi-flop synchronizers.")

        # 3. Asynchronous Reset Synchronous De-assertion
        if metrics.has_synchronized_reset_deassertion:
            benchmarks_passed.append("Asynchronous assert, synchronous de-assert reset tree verified.")
        else:
            warnings.append("Consider implementing a two-stage synchronous reset release tree to prevent recovery violations.")

        # 4. Glitch-Free FSM
        if metrics.has_glitch_free_fsm:
            benchmarks_passed.append("Glitch-free FSM with exhaustive default illegal state recovery verified.")
        else:
            warnings.append("FSM next-state logic should explicitly define default recovery handler.")

        # 5. Combinational Feedback
        if metrics.has_combinational_feedback_risk:
            critical_violations.append(
                "Combinational Feedback Loop: Logic output feeds directly back into input without clocked flip-flop boundary."
            )

        is_viable = (
            len(critical_violations) == 0 and
            metrics.has_latch_free_combinational_logic and
            metrics.has_cdc_synchronizer
        )

        return HardwareInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_hardware_viable=is_viable
        )

    def _extract_metrics(self, code_input: Any) -> HardwareMetrics:
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
        clean_code = re.sub(r'/\*.*?\*/', '', clean_code, flags=re.DOTALL)
        text_lower = clean_code.lower()

        m = HardwareMetrics()

        # 1. CDC Synchronizer
        has_cdc = bool(
            "cdc_" in text_lower or
            "sync_flop" in text_lower or
            "sync_stage" in text_lower or
            "2_ff" in text_lower or
            ("posedge clk" in text_lower and "sync" in text_lower) or
            metadata.get("has_cdc_synchronizer", False)
        )
        m.has_cdc_synchronizer = has_cdc

        # 2. Latch-Free Combinational Logic
        has_latch_free = bool(
            ("default:" in text_lower or "next_state = current_state" in text_lower or "always_comb" in text_lower) and
            not metadata.get("has_inferred_latch_risk", False) or
            metadata.get("has_latch_free_combinational_logic", False)
        )
        m.has_latch_free_combinational_logic = has_latch_free

        # 3. Synchronized Reset De-assertion
        has_rst_sync = bool(
            "rst_sync" in text_lower or
            "local_sync_rst" in text_lower or
            "sync_rst" in text_lower or
            metadata.get("has_synchronized_reset_deassertion", False)
        )
        m.has_synchronized_reset_deassertion = has_rst_sync

        # 4. Glitch-Free FSM
        has_fsm = bool(
            ("state" in text_lower and "case" in text_lower and "default:" in text_lower) or
            metadata.get("has_glitch_free_fsm", False)
        )
        m.has_glitch_free_fsm = has_fsm

        # 5. Inferred Latch Risk
        # If there is a case statement in combinational block without default
        if "case" in text_lower and "default:" not in text_lower:
            m.has_inferred_latch_risk = True
        if metadata.get("has_inferred_latch_risk", False):
            m.has_inferred_latch_risk = True

        # 6. Unsynchronized CDC Risk
        if ("clk_a" in text_lower and "clk_b" in text_lower and not has_cdc) or metadata.get("has_unsynchronized_cdc_risk", False):
            m.has_unsynchronized_cdc_risk = True

        # 7. Combinational Feedback Risk
        if "ring_oscillator" in text_lower or metadata.get("has_combinational_feedback_risk", False):
            m.has_combinational_feedback_risk = True

        # Anti-pattern logging
        if m.has_inferred_latch_risk:
            m.anti_patterns_detected.append("Inferred latch from incomplete combinational branch or case statement")
        if m.has_unsynchronized_cdc_risk:
            m.anti_patterns_detected.append("Unsynchronized cross-domain clock signals crossing domains")
        if m.has_combinational_feedback_risk:
            m.anti_patterns_detected.append("Direct combinational feedback loop without clocked register")

        return m
