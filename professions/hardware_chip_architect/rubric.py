"""
Ignis 'The Silicon' Thorne - 100-Point Weighted Hardware Architecture Rubric.

Evaluates ASIC/FPGA RTL implementations against inferred latch elimination,
dual-flop CDC synchronization, synchronized reset de-assertion, and glitch-free FSM safety.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.hardware_chip_architect.inspector import HardwareInspectionReport, HardwareMetrics


@dataclass
class HardwareDimensionScore:
    name: str
    weight: int
    score: int
    status: str
    reasons: List[str] = field(default_factory=list)


@dataclass
class HardwareEvaluation:
    total_score: int
    is_certified: bool
    dimensions: List[HardwareDimensionScore]
    veto_triggered: bool
    veto_reason: str = ""
    veto_reasons: List[str] = field(default_factory=list)


class HardwareRubric:
    """100-point weighted domain rubric enforcing Ignis Thorne silicon hardware standards."""

    PASSING_THRESHOLD: int = 85

    def evaluate(self, report: HardwareInspectionReport) -> HardwareEvaluation:
        m: HardwareMetrics = report.metrics
        dimensions: List[HardwareDimensionScore] = []
        veto_triggered = False
        veto_reasons: List[str] = []

        # 1. Latch-Free Combinational Logic (25 pts)
        d1_score = 0
        d1_reasons = []
        if m.has_inferred_latch_risk:
            d1_score = 0
            d1_reasons.append("VETO: Inferred transparent latch detected from incomplete conditional branches.")
            veto_triggered = True
            veto_reasons.append("INFERRED_TRANSPARENT_LATCH: Inferred latches cause timing races and ATPG failure.")
        elif m.has_latch_free_combinational_logic:
            d1_score = 25
            d1_reasons.append("Pure combinational logic verified without inferred level-sensitive latches.")
        else:
            d1_score = 15
            d1_reasons.append("Combinational blocks should provide explicit default assignments.")
        dimensions.append(HardwareDimensionScore(
            name="Latch-Free Combinational Logic",
            weight=25,
            score=d1_score,
            status="PASSED" if d1_score >= 20 else "FAILED",
            reasons=d1_reasons
        ))

        # 2. Clock Domain Crossing (CDC) Synchronization (25 pts)
        d2_score = 0
        d2_reasons = []
        if m.has_unsynchronized_cdc_risk:
            d2_score = 0
            d2_reasons.append("VETO: Unsynchronized clock domain crossing detected without multi-flop synchronizer.")
            veto_triggered = True
            veto_reasons.append("UNSYNCHRONIZED_CLOCK_CROSSING: Unsynchronized CDC causes catastrophic metastability.")
        elif m.has_cdc_synchronizer:
            d2_score = 25
            d2_reasons.append("Multi-flop CDC synchronizer protects cross-domain signals against metastability.")
        else:
            d2_score = 10
            d2_reasons.append("Signals crossing clock boundaries must be synchronized via multi-flop stages.")
        dimensions.append(HardwareDimensionScore(
            name="CDC Synchronization",
            weight=25,
            score=d2_score,
            status="PASSED" if d2_score >= 20 else "FAILED",
            reasons=d2_reasons
        ))

        # 3. Synchronized Reset De-assertion Discipline (20 pts)
        d3_score = 0
        d3_reasons = []
        if m.has_synchronized_reset_deassertion:
            d3_score = 20
            d3_reasons.append("Asynchronous assert, synchronous de-assert reset tree verified.")
        else:
            d3_score = 10
            d3_reasons.append("Reset signals should use two-stage synchronous de-assertion to prevent recovery timing faults.")
        dimensions.append(HardwareDimensionScore(
            name="Reset Discipline",
            weight=20,
            score=d3_score,
            status="PASSED" if d3_score >= 15 else "FAILED",
            reasons=d3_reasons
        ))

        # 4. Glitch-Free FSM Safety (15 pts)
        d4_score = 0
        d4_reasons = []
        if m.has_glitch_free_fsm:
            d4_score = 15
            d4_reasons.append("Glitch-free FSM with exhaustive default illegal state recovery verified.")
        else:
            d4_score = 8
            d4_reasons.append("FSM next-state logic should trap unused states with a default handler.")
        dimensions.append(HardwareDimensionScore(
            name="Glitch-Free FSM Safety",
            weight=15,
            score=d4_score,
            status="PASSED" if d4_score >= 12 else "FAILED",
            reasons=d4_reasons
        ))

        # 5. Timing Closure & Feedback Loop Defense (15 pts)
        d5_score = 0
        d5_reasons = []
        if m.has_combinational_feedback_risk:
            d5_score = 0
            d5_reasons.append("VETO: Unclocked combinational feedback ring loop detected.")
            veto_triggered = True
            veto_reasons.append("COMBINATIONAL_FEEDBACK_LOOP: Combinational loop causes ring oscillation.")
        else:
            d5_score = 15
            d5_reasons.append("Zero unclocked combinational feedback loops; synchronous boundaries preserved.")
        dimensions.append(HardwareDimensionScore(
            name="Timing & Feedback Defense",
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

        return HardwareEvaluation(
            total_score=total_score,
            is_certified=is_certified,
            dimensions=dimensions,
            veto_triggered=veto_triggered,
            veto_reason=veto_reason,
            veto_reasons=veto_reasons
        )
