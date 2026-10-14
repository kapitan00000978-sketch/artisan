"""
Lucas Cruz - 100-Point Mobile Systems & 120Hz Fluidity Rubric.

Evaluates mobile architecture, main-thread hygiene, and memory lifecycle against Tier-1 standards.
Passing threshold: 85/100 points.
Veto criteria: Main-thread blocking I/O, escaping closure retain cycles, or unhandled offline crashes.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.mobile_systems_architect.inspector import MobileInspectionReport, MobileMetrics


@dataclass
class MobileRubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class MobileSystemsRubric:
    """Rigorous 100-point weighted evaluation rubric for native and cross-platform mobile systems."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: MobileInspectionReport) -> MobileRubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Main Thread Hygiene & 120Hz Pacing (25 pts)
        # ----------------------------------------------------
        p1_score = 0
        if m.has_main_thread_blocking:
            veto_reasons.append("Main-thread blocking I/O: UI thread stalled by synchronous disk/network execution.")
            recommendations.append("Dispatch blocking I/O to background queue: DispatchQueue.global(qos: .userInitiated) or Dispatchers.IO.")
        else:
            p1_score += 25

        pillar_scores["main_thread_hygiene"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Memory Lifecycle & Retain Cycle Defense (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if m.has_retain_cycles:
            veto_reasons.append("Retain Cycle Detected: Strong self capture in escaping asynchronous closure causes severe memory leaks.")
            recommendations.append("Capture self weakly using [weak self] with guard let self = self else { return } unwrap.")
        else:
            p2_score += 25

        pillar_scores["memory_and_retain_cycles"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: Offline-First Resilience (20 pts)
        # ----------------------------------------------------
        p3_score = 0
        if not m.has_offline_caching:
            veto_reasons.append("Absence of offline caching: App cannot function or display data without active network connection.")
            recommendations.append("Implement local persistence layer (SQLite, Room, or CoreData) with cache-first reading.")
        else:
            p3_score += 12

        if m.handles_offline_gracefully:
            p3_score += 8
        else:
            recommendations.append("Add graceful error boundary with offline banner and cached fallback view.")

        pillar_scores["offline_first_resilience"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: Battery & Radio Preservation (15 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.has_battery_vampire_polling:
            p4_score += 4
            recommendations.append("Eliminate rapid polling; replace with push notifications or batch requests to >= 60-second intervals.")
        else:
            p4_score += 15

        pillar_scores["battery_and_radio"] = p4_score

        # ----------------------------------------------------
        # Pillar 5: Touch Ergonomics & Scroll Fluidity (15 pts)
        # ----------------------------------------------------
        p5_score = 0
        if m.min_touch_target_dp >= 44.0:
            p5_score += 8
        else:
            p5_score += 3
            recommendations.append(f"Expand touch target from {m.min_touch_target_dp:.0f}dp to minimum 48dp (Android) or 44pt (iOS).")

        if m.has_list_recycling_keys:
            p5_score += 7
        else:
            p5_score += 2
            recommendations.append("Add unique keys / recycling identifiers to dynamic list items to eliminate scroll jank.")

        pillar_scores["ergonomics_and_fluidity"] = p5_score

        total_score = sum(pillar_scores.values())

        # Veto enforcement
        veto_triggered = len(veto_reasons) > 0
        if veto_triggered and total_score >= self.PASSING_THRESHOLD:
            total_score = 72

        is_certified = (total_score >= self.PASSING_THRESHOLD) and not veto_triggered

        return MobileRubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
