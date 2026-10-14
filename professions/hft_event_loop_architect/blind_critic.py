"""
Thaddeus 'The Chrono' Vance - Blind HFT & Low-Jitter Event-Loop Critic.

Evaluates high-frequency trading event loops strictly against blocking syscalls,
mutex contention, thread migration, and dynamic heap allocations.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.hft_event_loop_architect.inspector import HftSystemInspector, HftInspectionReport
from professions.hft_event_loop_architect.rubric import HftEventLoopRubric, HftRubricEvaluation


@dataclass
class HftDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    latency_risk: str
    actionable_fix: str


@dataclass
class HftDefectLedger:
    verdict: str  # CERTIFIED_DETERMINISTIC_SUB_MICROSECOND or REJECTED_JITTER_LATENCY_HELL
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[HftDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindHftCritic:
    """HFT adversary auditing order paths for tail latency spikes, context switches, and cache thrashing."""

    def __init__(self):
        self.inspector = HftSystemInspector()
        self.rubric = HftEventLoopRubric()

    def review(self, code_input: Any) -> HftDefectLedger:
        """
        Runs objective inspection and adversarial rubric scoring, producing an HFT Defect Ledger.
        """
        report: HftInspectionReport = self.inspector.inspect(code_input)
        evaluation: HftRubricEvaluation = self.rubric.evaluate(report)

        defects: List[HftDefect] = []

        # Map critical violations to FATAL / HIGH defects
        for i, violation in enumerate(report.critical_violations, 1):
            if "Blocking Syscall" in violation:
                defects.append(
                    HftDefect(
                        defect_id=f"HFT-FATAL-00{i}",
                        severity="FATAL",
                        title="Blocking Syscall in Hot Trading Loop",
                        description=violation,
                        latency_risk="Context switches into kernel space incur 10,000ns+ tail latency penalties.",
                        actionable_fix="Replace sleep/blocking syscalls with non-blocking busy polling and CPU pause hints."
                    )
                )
            elif "Mutex Lock" in violation:
                defects.append(
                    HftDefect(
                        defect_id=f"HFT-FATAL-00{i}",
                        severity="FATAL",
                        title="Blocking Mutex Lock on Order Path",
                        description=violation,
                        latency_risk="Thread suspension under lock contention ruins sub-microsecond tick-to-trade SLA.",
                        actionable_fix="Adopt wait-free Single-Producer Single-Consumer (SPSC) circular ring buffer."
                    )
                )
            elif "Dynamic Heap" in violation:
                defects.append(
                    HftDefect(
                        defect_id=f"HFT-FATAL-00{i}",
                        severity="FATAL",
                        title="Dynamic Heap Allocation in Tick Loop",
                        description=violation,
                        latency_risk="Memory allocator lock contention and minor page faults inject unpredictable latency jitter.",
                        actionable_fix="Pre-allocate fixed-size circular ring buffer and object pools outside event loop."
                    )
                )
            else:
                defects.append(
                    HftDefect(
                        defect_id=f"HFT-HIGH-00{i}",
                        severity="HIGH",
                        title="HFT Low-Jitter Violation",
                        description=violation,
                        latency_risk="Severe risk of tail latency degradation.",
                        actionable_fix="Remediate against Thaddeus Vance low-jitter event-loop standards."
                    )
                )

        # Map warnings
        for j, warning in enumerate(report.warnings, 1):
            severity = "HIGH" if "affinity" in warning.lower() else "MEDIUM"
            defects.append(
                HftDefect(
                    defect_id=f"HFT-WARN-00{j}",
                    severity=severity,
                    title="HFT Architecture Warning",
                    description=warning,
                    latency_risk="Risk of thread migration, cache thrashing, or NUMA remote access.",
                    actionable_fix="Bind thread affinity to isolated CPU core via bind_thread_affinity()."
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = (
            "CERTIFIED_DETERMINISTIC_SUB_MICROSECOND"
            if evaluation.is_certified and fatal_count == 0
            else "REJECTED_JITTER_LATENCY_HELL"
        )

        summary = (
            f"Thaddeus Vance HFT Review: Score {evaluation.total_score}/100. "
            f"Verdict: {verdict}. Fatal defects: {fatal_count}, High defects: {high_count}."
        )

        return HftDefectLedger(
            verdict=verdict,
            score=evaluation.total_score,
            passing_threshold=evaluation.passing_threshold,
            is_certified=evaluation.is_certified and fatal_count == 0,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
