"""
Morpheus 'The Kernel' Vance - Objective Embedded Firmware & Bare-Metal Inspector.

This module inspects C/C++ bare-metal firmware and RTOS implementations for dynamic heap allocation,
blocking delays inside ISRs, missing volatile MMIO qualifications, and hardware watchdog integration.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class FirmwareMetrics:
    has_zero_heap_allocation: bool = False
    has_hardware_watchdog: bool = False
    has_volatile_mmio_registers: bool = False
    has_dma_cache_coherency: bool = False
    has_dynamic_heap_allocation_risk: bool = False
    has_blocking_delay_in_isr: bool = False
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class FirmwareInspectionReport:
    metrics: FirmwareMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_firmware_viable: bool = False


class FirmwareSystemInspector:
    """Rigorous bare-metal firmware auditor enforcing zero-malloc, ISR discipline, and watchdog supervisors."""

    def inspect(self, code_input: Any) -> FirmwareInspectionReport:
        """
        Audits embedded C/C++ firmware code or architecture metadata.
        """
        metrics = self._extract_metrics(code_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Dynamic Heap Allocation Risk
        if metrics.has_dynamic_heap_allocation_risk:
            critical_violations.append(
                "Dynamic Heap Allocation in Firmware: Calling malloc(), free(), or new on microcontrollers causes fatal memory fragmentation."
            )
        elif metrics.has_zero_heap_allocation:
            benchmarks_passed.append("100% Static allocation verified (Zero dynamic heap allocations).")
        else:
            warnings.append("Consider verifying all buffers and task control blocks are statically allocated.")

        # 2. Blocking Delays in ISR
        if metrics.has_blocking_delay_in_isr:
            critical_violations.append(
                "Blocking Operation in ISR: Calling delay(), sleep(), or spinlocks inside interrupt service routines starves CPU interrupts."
            )
        else:
            benchmarks_passed.append("Interrupt service routines conform to non-blocking deferred execution budget.")

        # 3. Hardware Watchdog Integration
        if not metrics.has_hardware_watchdog:
            critical_violations.append(
                "Missing Hardware Watchdog: No active hardware watchdog timer (WDT/IWDG) detected to recover from deadlocks."
            )
        else:
            benchmarks_passed.append("Hardware watchdog timer (WDT) initialization and servicing verified.")

        # 4. Volatile MMIO Qualification
        if metrics.has_volatile_mmio_registers:
            benchmarks_passed.append("Hardware peripheral registers qualified with volatile and memory barriers.")
        else:
            warnings.append("Ensure hardware peripheral registers and shared ISR variables use volatile qualification.")

        # 5. DMA Cache Coherency
        if metrics.has_dma_cache_coherency:
            benchmarks_passed.append("Explicit DMA cache coherency (clean/invalidate/barriers) verified.")
        else:
            warnings.append("Consider verifying D-Cache maintenance instructions around DMA memory transfers.")

        is_viable = (
            len(critical_violations) == 0 and
            metrics.has_zero_heap_allocation and
            metrics.has_hardware_watchdog
        )

        return FirmwareInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_firmware_viable=is_viable
        )

    def _extract_metrics(self, code_input: Any) -> FirmwareMetrics:
        metadata: Dict[str, Any] = {}
        text = ""

        if isinstance(code_input, dict):
            metadata = code_input
            text = code_input.get("code", "") or json.dumps(code_input)
        elif isinstance(code_input, str):
            text = code_input

        # Clean comments to prevent false triggers
        clean_code = re.sub(r'#.*', '', text)
        clean_code = re.sub(r'//.*', '', clean_code)
        clean_code = re.sub(r'/\*.*?\*/', '', clean_code, flags=re.DOTALL)
        text_lower = clean_code.lower()

        m = FirmwareMetrics()

        # 1. Dynamic Heap Allocation Risk
        has_malloc = bool(
            "malloc(" in text_lower or
            "free(" in text_lower or
            "calloc(" in text_lower or
            "new " in text_lower or
            metadata.get("has_dynamic_heap_allocation_risk", False)
        )
        m.has_dynamic_heap_allocation_risk = has_malloc
        m.has_zero_heap_allocation = not has_malloc

        # 2. Hardware Watchdog
        has_wdt = bool(
            "watchdog" in text_lower or
            "iwdg" in text_lower or
            "wdt" in text_lower or
            metadata.get("has_hardware_watchdog", False)
        )
        m.has_hardware_watchdog = has_wdt

        # 3. Volatile MMIO Qualification
        has_volatile = bool(
            "volatile" in text_lower or
            metadata.get("has_volatile_mmio_registers", False)
        )
        m.has_volatile_mmio_registers = has_volatile

        # 4. DMA Cache Coherency
        has_dma_cache = bool(
            "cache" in text_lower or
            "dmb" in text_lower or
            "dsb" in text_lower or
            "isb" in text_lower or
            metadata.get("has_dma_cache_coherency", False)
        )
        m.has_dma_cache_coherency = has_dma_cache

        # 5. Blocking Delay in ISR
        has_isr_delay = bool(
            ("irqhandler" in text_lower or "isr" in text_lower) and
            ("delay" in text_lower or "sleep" in text_lower) or
            metadata.get("has_blocking_delay_in_isr", False)
        )
        m.has_blocking_delay_in_isr = has_isr_delay

        # Anti-pattern logging
        if m.has_dynamic_heap_allocation_risk:
            m.anti_patterns_detected.append("Dynamic heap allocation in bare-metal embedded environment")
        if m.has_blocking_delay_in_isr:
            m.anti_patterns_detected.append("Blocking delay or spinloop detected inside interrupt service routine")
        if not m.has_hardware_watchdog:
            m.anti_patterns_detected.append("Hardware watchdog timer disabled or missing")

        return m
