"""
Thaddeus 'The Chrono' Vance - 100-Point HFT & Low-Jitter Event-Loop Rubric.

Evaluates high-frequency trading event loops, lock-free ring buffers, thread core affinity,
and zero-syscall execution pipelines.
Passing threshold: 85/100 points.
Veto criteria: Blocking syscalls/sleep, mutex locks in order path, or dynamic heap allocations.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.hft_event_loop_architect.inspector import HftInspectionReport, HftMetrics


@dataclass
class HftRubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class HftEventLoopRubric:
    """Rigorous 100-point weighted evaluation rubric for sub-microsecond HFT architecture."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: HftInspectionReport) -> HftRubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Zero-Syscall Busy Polling (30 pts)
        # ----------------------------------------------------
        p1_score = 0
        if m.has_blocking_syscall_or_sleep:
            veto_reasons.append(
                "Blocking Syscall on Hot Path: Found sleep() or blocking kernel calls inside trading event loop."
            )
            recommendations.append(
                "Eliminate sleep() and blocking syscalls. Implement non-blocking busy polling with CPU pause instructions."
            )
        elif m.has_zero_syscall_polling:
            p1_score = 30
        else:
            p1_score = 15
            recommendations.append("Explicitly document non-blocking busy polling loop.")
        pillar_scores["zero_syscall_polling"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Lock-Free Ring Buffer & Mutex Elimination (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if m.has_mutex_lock_in_loop:
            veto_reasons.append(
                "Mutex Lock in Order Path: Blocking mutex locks cause thread descheduling and multi-microsecond tail latency spikes."
            )
            recommendations.append(
                "Replace mutex locks with wait-free Single-Producer Single-Consumer (SPSC) circular ring buffer."
            )
        elif m.has_lock_free_ring_buffer:
            p2_score = 25
        else:
            p2_score = 10
            recommendations.append("Adopt SPSC lock-free circular queue with cacheline padding between head and tail.")
        pillar_scores["lock_free_ring_buffer"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: CPU Core Affinity & NUMA Isolation (25 pts)
        # ----------------------------------------------------
        p3_score = 0
        if m.has_core_affinity_pinning:
            p3_score = 25
        else:
            p3_score = 10
            recommendations.append(
                "Bind trading thread hard to dedicated isolated CPU core (pthread_setaffinity_np / bind_thread_affinity)."
            )
        pillar_scores["core_affinity_isolation"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: Zero Heap Allocation in Hot Loop (20 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.has_heap_alloc_in_tick_loop:
            veto_reasons.append(
                "Dynamic Heap Allocation in Tick Loop: Calling malloc/new in event loop causes memory allocator locks."
            )
            recommendations.append(
                "Pre-allocate static ring buffers and order object pools at startup; zero malloc in event loop."
            )
        else:
            p4_score = 20
        pillar_scores["zero_heap_allocation"] = p4_score

        total_score = sum(pillar_scores.values())
        veto_triggered = len(veto_reasons) > 0

        if veto_triggered:
            total_score = min(total_score, 50)
            is_certified = False
        else:
            is_certified = total_score >= self.PASSING_THRESHOLD

        return HftRubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
