"""
Commander Cassiopeia 'The Orbital' Sterling - 100-Point Weighted Aerospace Avionics Rubric.

Evaluates flight software implementations against Triple Modular Redundancy (TMR),
autonomous safe-mode contingency, radiation SEU scrubbing, and DO-178C static memory discipline.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.aerospace_avionics_architect.inspector import AvionicsInspectionReport, AvionicsMetrics


@dataclass
class AvionicsDimensionScore:
    name: str
    weight: int
    score: int
    status: str
    reasons: List[str] = field(default_factory=list)


@dataclass
class AvionicsEvaluation:
    total_score: int
    is_certified: bool
    dimensions: List[AvionicsDimensionScore]
    veto_triggered: bool
    veto_reason: str = ""
    veto_reasons: List[str] = field(default_factory=list)


class AvionicsRubric:
    """100-point weighted domain rubric enforcing Cassiopeia Sterling aerospace avionics standards."""

    PASSING_THRESHOLD: int = 85

    def evaluate(self, report: AvionicsInspectionReport) -> AvionicsEvaluation:
        m: AvionicsMetrics = report.metrics
        dimensions: List[AvionicsDimensionScore] = []
        veto_triggered = False
        veto_reasons: List[str] = []

        # 1. Triple Modular Redundancy (TMR) (25 pts)
        d1_score = 0
        d1_reasons = []
        if m.has_single_point_of_failure:
            d1_score = 0
            d1_reasons.append("VETO: Single point of failure (SPOF) detected in critical flight control path.")
            veto_triggered = True
            veto_reasons.append("SINGLE_POINT_OF_FAILURE: Critical flight actuation must be voted across triply redundant channels.")
        elif m.has_tmr_majority_voting:
            d1_score = 25
            d1_reasons.append("Triple Modular Redundancy (2-out-of-3 Byzantine majority voting) verified.")
        else:
            d1_score = 15
            d1_reasons.append("Critical commands should implement triply redundant majority voting.")
        dimensions.append(AvionicsDimensionScore(
            name="Triple Modular Redundancy",
            weight=25,
            score=d1_score,
            status="PASSED" if d1_score >= 20 else "FAILED",
            reasons=d1_reasons
        ))

        # 2. Autonomous Safe-Mode Contingency (25 pts)
        d2_score = 0
        d2_reasons = []
        if not m.has_autonomous_safe_mode:
            d2_score = 0
            d2_reasons.append("VETO: Missing autonomous safe-mode fallback state machine.")
            veto_triggered = True
            veto_reasons.append("MISSING_AUTONOMOUS_SAFE_MODE: Spacecraft must autonomously enter safe-hold upon anomaly.")
        else:
            d2_score = 25
            d2_reasons.append("Autonomous Safe-Mode contingency and power bus monitoring verified.")
        dimensions.append(AvionicsDimensionScore(
            name="Autonomous Safe-Mode",
            weight=25,
            score=d2_score,
            status="PASSED" if d2_score >= 20 else "FAILED",
            reasons=d2_reasons
        ))

        # 3. Radiation SEU Memory Scrubbing (20 pts)
        d3_score = 0
        d3_reasons = []
        if m.has_radiation_memory_scrubbing:
            d3_score = 20
            d3_reasons.append("Radiation SEU soft error scrubbing with EDAC verified.")
        else:
            d3_score = 10
            d3_reasons.append("Consider verifying periodic background EDAC memory scrubbing.")
        dimensions.append(AvionicsDimensionScore(
            name="Radiation Memory Scrubbing",
            weight=20,
            score=d3_score,
            status="PASSED" if d3_score >= 15 else "FAILED",
            reasons=d3_reasons
        ))

        # 4. ARINC 653 Time & Space Partitioning (15 pts)
        d4_score = 0
        d4_reasons = []
        if m.has_unbounded_sleep_in_flight_loop:
            d4_score = 0
            d4_reasons.append("VETO: Unbounded sleep in flight loop violates deterministic partition deadlines.")
            veto_triggered = True
            veto_reasons.append("UNBOUNDED_EXECUTION_DELAY: Flight loop must not contain blocking sleep calls.")
        elif m.has_deterministic_time_framing:
            d4_score = 15
            d4_reasons.append("Deterministic major frame timing verified.")
        else:
            d4_score = 10
            d4_reasons.append("Major flight frame execution should use monotonic time tracking.")
        dimensions.append(AvionicsDimensionScore(
            name="ARINC 653 Partitioning",
            weight=15,
            score=d4_score,
            status="PASSED" if d4_score >= 12 else "FAILED",
            reasons=d4_reasons
        ))

        # 5. DO-178C Level A Zero-Heap Discipline (15 pts)
        d5_score = 0
        d5_reasons = []
        if m.has_dynamic_heap_allocation:
            d5_score = 0
            d5_reasons.append("VETO: Dynamic heap allocation detected in DO-178C Level A flight software.")
            veto_triggered = True
            veto_reasons.append("DYNAMIC_HEAP_ALLOCATION: Malloc/free prohibited in critical flight software.")
        else:
            d5_score = 15
            d5_reasons.append("100% static allocation verified; zero dynamic memory fragmentation.")
        dimensions.append(AvionicsDimensionScore(
            name="DO-178C Memory Discipline",
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

        return AvionicsEvaluation(
            total_score=total_score,
            is_certified=is_certified,
            dimensions=dimensions,
            veto_triggered=veto_triggered,
            veto_reason=veto_reason,
            veto_reasons=veto_reasons
        )
