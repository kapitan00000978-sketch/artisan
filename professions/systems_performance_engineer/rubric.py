"""
Valerie 'The Edge' Cross - 100-Point Systems & Low-Level Performance Rubric.

Evaluates C++/Rust systems code, zero-allocation hot paths, 64-byte cache line alignment,
and SIMD branchless vectorization.
Passing threshold: 85/100 points.
Veto criteria: Heap allocations in hot loop bodies, or unaligned false sharing hazards.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.systems_performance_engineer.inspector import SystemsInspectionReport, SystemsMetrics


@dataclass
class SystemsRubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class SystemsPerformanceRubric:
    """Rigorous 100-point weighted evaluation rubric for low-level systems performance and mechanical sympathy."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: SystemsInspectionReport) -> SystemsRubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Zero-Allocation Hot Path Discipline (30 pts)
        # ----------------------------------------------------
        p1_score = 0
        if m.has_heap_alloc_in_loop:
            veto_reasons.append(
                "Heap Allocation in Hot Loop: Calling malloc, new, or Box::new inside inner loops causes memory allocator locks."
            )
            recommendations.append(
                "Pre-allocate memory buffers upfront using stack arrays, monolithic memory arenas, or ring buffers."
            )
        elif m.has_zero_allocation_hot_loop:
            p1_score += 30
        else:
            p1_score += 10
            recommendations.append("Ensure hot processing loops execute without any dynamic heap allocations.")

        pillar_scores["zero_allocation_hot_path"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: 64-Byte Cache Line Alignment (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if m.has_false_sharing_vulnerability:
            veto_reasons.append(
                "False Sharing Hazard: Mutable atomic variables across threads share the same 64-byte CPU cache line."
            )
            recommendations.append(
                "Align thread-shared structs to 64 bytes using alignas(64) or #[repr(align(64))] and insert padding."
            )
        elif m.has_cache_line_alignment:
            p2_score += 25
        else:
            p2_score += 10
            recommendations.append(
                "Declare explicit alignas(64) alignment on core structs to respect hardware cache line boundaries."
            )

        pillar_scores["cache_line_alignment"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: Zero-Copy Slices & Memory Views (20 pts)
        # ----------------------------------------------------
        p3_score = 0
        if m.has_zero_copy_slices:
            p3_score += 20
        else:
            p3_score += 8
            recommendations.append(
                "Pass non-owning slices (std::span, std::string_view, &[u8]) to avoid deep memcpy buffer duplication."
            )

        pillar_scores["zero_copy_slices"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: SIMD Vectorization & Branchless Math (15 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.has_simd_or_branchless_optimization:
            p4_score += 15
        else:
            p4_score += 6
            recommendations.append(
                "Add SIMD vectorization directives (#pragma omp simd) or branchless arithmetic to assist the compiler."
            )

        pillar_scores["simd_and_branchless"] = p4_score

        # ----------------------------------------------------
        # Pillar 5: Deterministic Resource Lifecycles (10 pts)
        # ----------------------------------------------------
        p5_score = 10
        pillar_scores["deterministic_lifecycles"] = p5_score

        total_score = sum(pillar_scores.values())

        # Veto enforcement
        veto_triggered = len(veto_reasons) > 0
        if veto_triggered and total_score >= self.PASSING_THRESHOLD:
            total_score = 65

        is_certified = (total_score >= self.PASSING_THRESHOLD) and not veto_triggered

        return SystemsRubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
