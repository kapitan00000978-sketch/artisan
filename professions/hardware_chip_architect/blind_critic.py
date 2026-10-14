"""
Ignis 'The Silicon' Thorne - Blind Hardware Critic.

Provides an objective, code-blind evaluation of ASIC/FPGA RTL implementations,
generating a strict defect ledger and ruthless hardware review.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.hardware_chip_architect.inspector import HardwareSystemInspector, HardwareInspectionReport
from professions.hardware_chip_architect.rubric import HardwareRubric, HardwareEvaluation


@dataclass
class HardwareDefect:
    id: str
    severity: str
    description: str
    actionable_fix: str


@dataclass
class HardwareDefectLedger:
    score: int
    is_certified: bool
    veto_triggered: bool
    defects: List[HardwareDefect] = field(default_factory=list)
    summary: str = ""

    @property
    def fatal_defects_count(self) -> int:
        return len([d for d in self.defects if d.severity in ("FATAL", "CRITICAL")])

    @property
    def verdict(self) -> str:
        return "CERTIFIED" if self.is_certified else "REJECTED"


class BlindHardwareCritic:
    """Objective, unsparing hardware critic auditing RTL against silicon synthesis standards."""

    def __init__(self):
        self.inspector = HardwareSystemInspector()
        self.rubric = HardwareRubric()

    def review(self, code_input: Any) -> HardwareDefectLedger:
        report: HardwareInspectionReport = self.inspector.inspect(code_input)
        evaluation: HardwareEvaluation = self.rubric.evaluate(report)

        defects: List[HardwareDefect] = []

        # 1. Inferred Latch Risk
        if report.metrics.has_inferred_latch_risk:
            defects.append(
                HardwareDefect(
                    id="HW-001",
                    severity="FATAL",
                    description="Inferred transparent latch detected from missing case default or incomplete conditional assignment.",
                    actionable_fix="Add default assignment at block start (next_state = current_state) or provide explicit default: branch."
                )
            )

        # 2. Unsynchronized CDC Risk
        if report.metrics.has_unsynchronized_cdc_risk:
            defects.append(
                HardwareDefect(
                    id="HW-002",
                    severity="FATAL",
                    description="Signal crosses asynchronous clock domains without 2-FF or 3-FF synchronizer stages.",
                    actionable_fix="Pass async signal through dual-stage flip-flop synchronizer (cdc_meta_flop <= in; cdc_sync_flop <= cdc_meta_flop)."
                )
            )

        # 3. Combinational Feedback Loop
        if report.metrics.has_combinational_feedback_risk:
            defects.append(
                HardwareDefect(
                    id="HW-003",
                    severity="FATAL",
                    description="Unclocked combinational feedback loop detected, creating uncontrolled ring oscillator.",
                    actionable_fix="Break combinational loop with a clocked register boundary (always @(posedge clk))."
                )
            )

        # 4. Missing Reset Synchronizer
        if not report.metrics.has_synchronized_reset_deassertion:
            defects.append(
                HardwareDefect(
                    id="HW-004",
                    severity="MEDIUM",
                    description="Reset de-assertion is unclocked, risking recovery/removal timing violations across registers.",
                    actionable_fix="Implement a 2-stage synchronous reset release tree: rst_sync_stage1 <= 1'b1; rst_sync_stage2 <= rst_sync_stage1."
                )
            )

        # 5. Missing FSM Illegal State Trap
        if not report.metrics.has_glitch_free_fsm:
            defects.append(
                HardwareDefect(
                    id="HW-005",
                    severity="MEDIUM",
                    description="FSM state decode lacks explicit default recovery branch to trap single event upset (SEU) corruptions.",
                    actionable_fix="Add default: next_state = STATE_IDLE; inside FSM case statement."
                )
            )

        summary = (
            f"Ignis Thorne Hardware Review: Score {evaluation.total_score}/100. "
            f"{'CERTIFIED for silicon synthesis and tape-out.' if evaluation.is_certified else 'REJECTED: Silicon timing defects and metastability risks present.'}"
        )

        return HardwareDefectLedger(
            score=evaluation.total_score,
            is_certified=evaluation.is_certified,
            veto_triggered=evaluation.veto_triggered,
            defects=defects,
            summary=summary
        )
