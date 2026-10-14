"""
Valerie 'The Edge' Cross - Blind Systems & Low-Level Performance Critic.

Evaluates C++, Rust, and C systems code strictly against zero-allocation hot paths,
64-byte cache line alignment, and SIMD hardware efficiency.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.systems_performance_engineer.inspector import SystemsPerformanceInspector, SystemsInspectionReport
from professions.systems_performance_engineer.rubric import SystemsPerformanceRubric, SystemsRubricEvaluation


@dataclass
class SystemsDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    hardware_impact: str
    actionable_fix: str


@dataclass
class SystemsDefectLedger:
    verdict: str  # CERTIFIED_MECHANICAL_SYMPATHY or REJECTED_SILICON_STRANGULATION
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[SystemsDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindSystemsCritic:
    """Systems adversary reviewing hot paths for heap stalls, cache invalidations, and pipeline stalls."""

    def __init__(self):
        self.inspector = SystemsPerformanceInspector()
        self.rubric = SystemsPerformanceRubric()

    def review(self, code_input: Any) -> SystemsDefectLedger:
        """
        Runs objective inspection and adversarial rubric scoring, producing a Systems Defect Ledger.
        """
        report: SystemsInspectionReport = self.inspector.inspect(code_input)
        eval_result: SystemsRubricEvaluation = self.rubric.evaluate(report)

        defects: List[SystemsDefect] = []

        # 1. Critical violations -> FATAL defects
        for i, violation in enumerate(report.critical_violations, start=1):
            if "heap" in violation.lower() or "malloc" in violation.lower() or "alloc" in violation.lower():
                title = "Dynamic Heap Allocation in Hot Loop Body"
                impact = "Invokes kernel/allocator lock contention, inducing multi-microsecond tail latency jitter."
                fix = "Pre-allocate memory arena or stack buffers outside the loop; eliminate all dynamic allocations."
            elif "false sharing" in violation.lower() or "cache" in violation.lower():
                title = "False Sharing CPU Cache Thrashing"
                impact = "Adjacent cores constantly invalidate L1/L2 cache lines across the interconnect bus."
                fix = "Align thread state structs to 64 bytes using alignas(64) and add padding."
            else:
                title = "Critical Low-Level Hardware Violation"
                impact = "Substantially degrades hardware throughput and tail latency."
                fix = "Refactor code to Valerie Cross mechanical sympathy standards."

            defects.append(
                SystemsDefect(
                    defect_id=f"SYS-FATAL-{i:03d}",
                    severity="FATAL",
                    title=title,
                    description=violation,
                    hardware_impact=impact,
                    actionable_fix=fix
                )
            )

        # 2. Veto reasons
        for j, reason in enumerate(eval_result.veto_reasons, start=len(defects) + 1):
            if not any(d.description == reason for d in defects):
                defects.append(
                    SystemsDefect(
                        defect_id=f"SYS-FATAL-{j:03d}",
                        severity="FATAL",
                        title="Hardware Performance Veto",
                        description=reason,
                        hardware_impact="Disqualifies code from production deployment under Valerie Cross protocol.",
                        actionable_fix="Remediate the underlying low-level anti-pattern immediately."
                    )
                )

        # 3. Warnings -> HIGH / MEDIUM defects
        for k, warning in enumerate(report.warnings, start=len(defects) + 1):
            severity = "HIGH" if "alignment" in warning.lower() else "MEDIUM"
            title = "Unspecified Cache Line Alignment" if "alignment" in warning.lower() else "Redundant Data Copies"
            impact = "May cross cache boundaries, incurring extra memory cycles." if "alignment" in warning.lower() else "Unnecessary memcpy overhead."
            fix = "Explicitly annotate alignas(64)." if "alignment" in warning.lower() else "Pass zero-copy views (std::span or slices)."

            defects.append(
                SystemsDefect(
                    defect_id=f"SYS-WARN-{k:03d}",
                    severity=severity,
                    title=title,
                    description=warning,
                    hardware_impact=impact,
                    actionable_fix=fix
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = (
            "CERTIFIED_MECHANICAL_SYMPATHY"
            if eval_result.is_certified and fatal_count == 0
            else "REJECTED_SILICON_STRANGULATION"
        )

        summary = (
            f"Valerie Cross Systems Review: Score {eval_result.total_score}/100. "
            f"Verdict: {verdict}. Fatal defects: {fatal_count}, High defects: {high_count}."
        )

        return SystemsDefectLedger(
            verdict=verdict,
            score=eval_result.total_score,
            passing_threshold=eval_result.passing_threshold,
            is_certified=eval_result.is_certified and fatal_count == 0,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
