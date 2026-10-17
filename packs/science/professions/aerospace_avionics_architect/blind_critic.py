"""
Commander Cassiopeia 'The Orbital' Sterling - Blind Aerospace Avionics Critic.

Provides an objective, code-blind evaluation of flight software implementations,
generating a strict defect ledger and ruthless mission-critical review.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.aerospace_avionics_architect.inspector import AvionicsSystemInspector, AvionicsInspectionReport
from professions.aerospace_avionics_architect.rubric import AvionicsRubric, AvionicsEvaluation


@dataclass
class AvionicsDefect:
    id: str
    severity: str
    description: str
    actionable_fix: str


@dataclass
class AvionicsDefectLedger:
    score: int
    is_certified: bool
    veto_triggered: bool
    defects: List[AvionicsDefect] = field(default_factory=list)
    summary: str = ""

    @property
    def fatal_defects_count(self) -> int:
        return len([d for d in self.defects if d.severity in ("FATAL", "CRITICAL")])

    @property
    def verdict(self) -> str:
        return "CERTIFIED" if self.is_certified else "REJECTED"


class BlindAvionicsCritic:
    """Objective, unsparing avionics critic auditing flight software against DO-178C Level A standards."""

    def __init__(self):
        self.inspector = AvionicsSystemInspector()
        self.rubric = AvionicsRubric()

    def review(self, code_input: Any) -> AvionicsDefectLedger:
        report: AvionicsInspectionReport = self.inspector.inspect(code_input)
        evaluation: AvionicsEvaluation = self.rubric.evaluate(report)

        defects: List[AvionicsDefect] = []

        # 1. Single Point of Failure
        if report.metrics.has_single_point_of_failure:
            defects.append(
                AvionicsDefect(
                    id="AV-001",
                    severity="FATAL",
                    description="Flight actuation commands driven from a single channel without Triple Modular Redundancy (TMR) voting.",
                    actionable_fix="Pass actuation commands through tmr_majority_vote(ch_a, ch_b, ch_c) with 2-out-of-3 Byzantine quorum."
                )
            )

        # 2. Dynamic Heap Allocation
        if report.metrics.has_dynamic_heap_allocation:
            defects.append(
                AvionicsDefect(
                    id="AV-002",
                    severity="FATAL",
                    description="Dynamic heap memory allocation (malloc/free) detected in flight software, violating DO-178C Level A.",
                    actionable_fix="Pre-allocate all buffers, telemetry structures, and queues as compile-time static memory pools."
                )
            )

        # 3. Missing Autonomous Safe-Mode
        if not report.metrics.has_autonomous_safe_mode:
            defects.append(
                AvionicsDefect(
                    id="AV-003",
                    severity="FATAL",
                    description="Spacecraft software lacks autonomous Safe-Mode fallback, leaving the mission vulnerable to power depletion.",
                    actionable_fix="Implement transition_to_safe_mode() with Sun-pointing attitude hold and payload power-down."
                )
            )

        # 4. Missing Radiation Memory Scrubbing
        if not report.metrics.has_radiation_memory_scrubbing:
            defects.append(
                AvionicsDefect(
                    id="AV-004",
                    severity="HIGH",
                    description="Flight memory lacks active background SEU scrubbing, allowing cosmic ray bit-flips to corrupt state.",
                    actionable_fix="Implement scrub_memory_block() to periodically sweep SRAM/flash and repair single-bit parity errors."
                )
            )

        # 5. Unbounded Sleep in Flight Frame
        if report.metrics.has_unbounded_sleep_in_flight_loop:
            defects.append(
                AvionicsDefect(
                    id="AV-005",
                    severity="HIGH",
                    description="Blocking sleep() inside flight loop violates ARINC 653 cyclic major/minor frame timing deadlines.",
                    actionable_fix="Replace sleep() with deterministic non-blocking monotonic timestamp intervals."
                )
            )

        summary = (
            f"Commander Cassiopeia Sterling Avionics Review: Score {evaluation.total_score}/100. "
            f"{'CERTIFIED for orbital flight deployment.' if evaluation.is_certified else 'REJECTED: Critical flight hazards and single points of failure present.'}"
        )

        return AvionicsDefectLedger(
            score=evaluation.total_score,
            is_certified=evaluation.is_certified,
            veto_triggered=evaluation.veto_triggered,
            defects=defects,
            summary=summary
        )
