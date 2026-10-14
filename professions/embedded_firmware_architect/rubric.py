"""
Morpheus 'The Kernel' Vance - 100-Point Weighted Embedded Firmware Rubric.

Evaluates C/C++ bare-metal firmware implementations against zero-malloc static allocation,
hardware watchdog supervision, deferred ISR execution, and volatile MMIO discipline.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.embedded_firmware_architect.inspector import FirmwareInspectionReport, FirmwareMetrics


@dataclass
class FirmwareDimensionScore:
    name: str
    weight: int
    score: int
    status: str
    reasons: List[str] = field(default_factory=list)


@dataclass
class FirmwareEvaluation:
    total_score: int
    is_certified: bool
    dimensions: List[FirmwareDimensionScore]
    veto_triggered: bool
    veto_reason: str = ""
    veto_reasons: List[str] = field(default_factory=list)


class FirmwareRubric:
    """100-point weighted domain rubric enforcing Morpheus Vance bare-metal firmware standards."""

    PASSING_THRESHOLD: int = 85

    def evaluate(self, report: FirmwareInspectionReport) -> FirmwareEvaluation:
        m: FirmwareMetrics = report.metrics
        dimensions: List[FirmwareDimensionScore] = []
        veto_triggered = False
        veto_reasons: List[str] = []

        # 1. Zero-Heap Static Allocation (25 pts)
        d1_score = 0
        d1_reasons = []
        if m.has_dynamic_heap_allocation_risk:
            d1_score = 0
            d1_reasons.append("VETO: Dynamic heap allocation (malloc/free/new) detected in embedded firmware.")
            veto_triggered = True
            veto_reasons.append("DYNAMIC_HEAP_ALLOCATION: Malloc on bare-metal systems causes fatal heap fragmentation.")
        elif m.has_zero_heap_allocation:
            d1_score = 25
            d1_reasons.append("100% static allocation verified; zero dynamic heap fragmentation risk.")
        else:
            d1_score = 15
            d1_reasons.append("Ensure all memory buffers are statically allocated at compile time.")
        dimensions.append(FirmwareDimensionScore(
            name="Zero-Heap Static Allocation",
            weight=25,
            score=d1_score,
            status="PASSED" if d1_score >= 20 else "FAILED",
            reasons=d1_reasons
        ))

        # 2. Hardware Watchdog Supervision (25 pts)
        d2_score = 0
        d2_reasons = []
        if not m.has_hardware_watchdog:
            d2_score = 0
            d2_reasons.append("VETO: Missing hardware watchdog timer (WDT/IWDG) initialization.")
            veto_triggered = True
            veto_reasons.append("MISSING_HARDWARE_WATCHDOG: Unsupervised firmware risks unrecoverable deadlock.")
        else:
            d2_score = 25
            d2_reasons.append("Hardware watchdog supervisor initialized and refreshed on cadence.")
        dimensions.append(FirmwareDimensionScore(
            name="Watchdog Supervision",
            weight=25,
            score=d2_score,
            status="PASSED" if d2_score >= 20 else "FAILED",
            reasons=d2_reasons
        ))

        # 3. ISR Execution Discipline (20 pts)
        d3_score = 0
        d3_reasons = []
        if m.has_blocking_delay_in_isr:
            d3_score = 0
            d3_reasons.append("VETO: Blocking delay or sleep detected inside interrupt handler.")
            veto_triggered = True
            veto_reasons.append("BLOCKING_DELAY_IN_ISR: Interrupt handlers must never block or sleep.")
        else:
            d3_score = 20
            d3_reasons.append("Interrupt service routines conform to non-blocking sub-5µs deferred budget.")
        dimensions.append(FirmwareDimensionScore(
            name="ISR Latency Discipline",
            weight=20,
            score=d3_score,
            status="PASSED" if d3_score >= 15 else "FAILED",
            reasons=d3_reasons
        ))

        # 4. Volatile MMIO Qualification & Barriers (15 pts)
        d4_score = 0
        d4_reasons = []
        if m.has_volatile_mmio_registers:
            d4_score = 15
            d4_reasons.append("Peripheral registers qualified as volatile with memory barriers.")
        else:
            d4_score = 8
            d4_reasons.append("Ensure hardware peripheral registers use volatile qualification.")
        dimensions.append(FirmwareDimensionScore(
            name="Volatile MMIO & Barriers",
            weight=15,
            score=d4_score,
            status="PASSED" if d4_score >= 12 else "FAILED",
            reasons=d4_reasons
        ))

        # 5. DMA Cache Coherency (15 pts)
        d5_score = 0
        d5_reasons = []
        if m.has_dma_cache_coherency:
            d5_score = 15
            d5_reasons.append("DMA cache coherency maintenance (clean/invalidate/DMB) verified.")
        else:
            d5_score = 10
            d5_reasons.append("Consider verifying cache maintenance operations surrounding DMA transfers.")
        dimensions.append(FirmwareDimensionScore(
            name="DMA Cache Coherency",
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

        return FirmwareEvaluation(
            total_score=total_score,
            is_certified=is_certified,
            dimensions=dimensions,
            veto_triggered=veto_triggered,
            veto_reason=veto_reason,
            veto_reasons=veto_reasons
        )
