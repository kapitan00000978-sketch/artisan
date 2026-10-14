"""
Morpheus 'The Kernel' Vance - Blind Embedded Firmware Critic.

Provides an objective, code-blind evaluation of C/C++ bare-metal firmware implementations,
generating a strict defect ledger and ruthless embedded review.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.embedded_firmware_architect.inspector import FirmwareSystemInspector, FirmwareInspectionReport
from professions.embedded_firmware_architect.rubric import FirmwareRubric, FirmwareEvaluation


@dataclass
class FirmwareDefect:
    id: str
    severity: str
    description: str
    actionable_fix: str


@dataclass
class FirmwareDefectLedger:
    score: int
    is_certified: bool
    veto_triggered: bool
    defects: List[FirmwareDefect] = field(default_factory=list)
    summary: str = ""

    @property
    def fatal_defects_count(self) -> int:
        return len([d for d in self.defects if d.severity in ("FATAL", "CRITICAL")])

    @property
    def verdict(self) -> str:
        return "CERTIFIED" if self.is_certified else "REJECTED"


class BlindFirmwareCritic:
    """Objective, unsparing firmware critic auditing embedded code against bare-metal safety standards."""

    def __init__(self):
        self.inspector = FirmwareSystemInspector()
        self.rubric = FirmwareRubric()

    def review(self, code_input: Any) -> FirmwareDefectLedger:
        report: FirmwareInspectionReport = self.inspector.inspect(code_input)
        evaluation: FirmwareEvaluation = self.rubric.evaluate(report)

        defects: List[FirmwareDefect] = []

        # 1. Dynamic Heap Allocation
        if report.metrics.has_dynamic_heap_allocation_risk:
            defects.append(
                FirmwareDefect(
                    id="FW-001",
                    severity="FATAL",
                    description="Dynamic heap allocation (malloc/free) detected, risking irreversible heap fragmentation lockups.",
                    actionable_fix="Replace dynamic memory allocations with static arrays, ring buffers, or fixed-size memory pools."
                )
            )

        # 2. Blocking Delay in ISR
        if report.metrics.has_blocking_delay_in_isr:
            defects.append(
                FirmwareDefect(
                    id="FW-002",
                    severity="FATAL",
                    description="Blocking delay or spinloop detected inside an interrupt service routine, causing interrupt starvation.",
                    actionable_fix="Remove blocking calls from ISR; defer processing to worker tasks using direct-to-task event flags."
                )
            )

        # 3. Missing Hardware Watchdog
        if not report.metrics.has_hardware_watchdog:
            defects.append(
                FirmwareDefect(
                    id="FW-003",
                    severity="FATAL",
                    description="Firmware lacks independent hardware watchdog timer (WDT/IWDG) initialization and supervisor refresh.",
                    actionable_fix="Initialize hardware watchdog (bsp_watchdog_init) and refresh periodically from main loop or health task."
                )
            )

        # 4. Missing Volatile MMIO Qualification
        if not report.metrics.has_volatile_mmio_registers:
            defects.append(
                FirmwareDefect(
                    id="FW-004",
                    severity="MEDIUM",
                    description="Hardware peripheral registers accessed without volatile qualification, risking compiler dead-code elimination.",
                    actionable_fix="Qualify all hardware memory-mapped register pointers with volatile uint32_t*."
                )
            )

        # 5. Missing DMA Cache Coherency
        if not report.metrics.has_dma_cache_coherency:
            defects.append(
                FirmwareDefect(
                    id="FW-005",
                    severity="MEDIUM",
                    description="DMA memory buffers lack explicit D-Cache clean and invalidate instructions, risking stale data reads.",
                    actionable_fix="Insert cache invalidate (__asm__ volatile(\"dsb 0xF\")) instructions around DMA buffer accesses."
                )
            )

        summary = (
            f"Morpheus Vance Firmware Review: Score {evaluation.total_score}/100. "
            f"{'CERTIFIED for bare-metal production deployment.' if evaluation.is_certified else 'REJECTED: Embedded reliability and heap fragmentation risks present.'}"
        )

        return FirmwareDefectLedger(
            score=evaluation.total_score,
            is_certified=evaluation.is_certified,
            veto_triggered=evaluation.veto_triggered,
            defects=defects,
            summary=summary
        )
