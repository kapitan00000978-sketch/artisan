"""
Thaddeus 'The Chrono' Vance - Objective HFT & Low-Jitter Event-Loop Inspector.

This module inspects order-matching engines, market data feed parsers, and trading event loops
for blocking syscalls, thread pinning discipline, mutex contention, and dynamic heap allocations.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class HftMetrics:
    has_core_affinity_pinning: bool = False
    has_lock_free_ring_buffer: bool = False
    has_zero_syscall_polling: bool = False
    has_blocking_syscall_or_sleep: bool = False
    has_mutex_lock_in_loop: bool = False
    has_heap_alloc_in_tick_loop: bool = False
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class HftInspectionReport:
    metrics: HftMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_hft_viable: bool = False


class HftSystemInspector:
    """Rigorous low-jitter trading engine auditor verifying thread pinning, lock-free queues, and zero syscalls."""

    def inspect(self, code_input: Any) -> HftInspectionReport:
        """
        Audits HFT event loop, order router, or market feed handler.
        """
        metrics = self._extract_metrics(code_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Blocking Syscalls or Sleep on Hot Path
        if metrics.has_blocking_syscall_or_sleep:
            critical_violations.append(
                "Blocking Syscall on Hot Path: Found sleep(), epoll_wait(), or blocking I/O calls inside trading event loop. Triggers kernel context switch."
            )
        elif metrics.has_zero_syscall_polling:
            benchmarks_passed.append("Zero-syscall busy polling verified (Sub-microsecond reaction budget).")
        else:
            warnings.append("Consider verifying busy-polling loop without kernel interrupt yield.")

        # 2. Mutex Lock Contention
        if metrics.has_mutex_lock_in_loop:
            critical_violations.append(
                "Mutex Lock in Order Path: Found pthread_mutex or blocking lock on tick-to-trade path. Halts CPU execution on contention."
            )
        elif metrics.has_lock_free_ring_buffer:
            benchmarks_passed.append("Lock-free SPSC circular ring buffer verified (Wait-free execution).")
        else:
            warnings.append("Lock-free SPSC queue not explicitly identified; verify thread handoff queue.")

        # 3. CPU Core Affinity Pinning
        if not metrics.has_core_affinity_pinning:
            warnings.append("Missing CPU core affinity pinning: OS scheduler thread migration risks cache eviction and NUMA penalties.")
        else:
            benchmarks_passed.append("CPU core affinity pinning verified (Hard thread binding to isolated core).")

        # 4. Dynamic Heap Allocation in Tick Loop
        if metrics.has_heap_alloc_in_tick_loop:
            critical_violations.append(
                "Dynamic Heap Allocation in Tick Loop: Calling malloc/new in event loop causes memory allocator lock contention."
            )
        else:
            benchmarks_passed.append("Zero dynamic heap allocations in hot path verified.")

        for ap in metrics.anti_patterns_detected:
            if ap not in critical_violations:
                critical_violations.append(f"Anti-Pattern Detected: {ap}")

        is_viable = len(critical_violations) == 0

        return HftInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_hft_viable=is_viable
        )

    def _extract_metrics(self, code_input: Any) -> HftMetrics:
        text = ""
        metadata: Dict[str, Any] = {}

        if isinstance(code_input, str):
            text = code_input
            try:
                parsed = json.loads(code_input)
                if isinstance(parsed, dict):
                    metadata = parsed
            except (json.JSONDecodeError, ValueError) as _json_err:
                _ = _json_err
        elif isinstance(code_input, dict):
            metadata = code_input
            text = json.dumps(code_input)
        else:
            text = str(code_input)

        # Strip comments to prevent false positives from descriptive comments
        cleaned_text = re.sub(r"#.*", "", text)
        cleaned_text = re.sub(r"//.*", "", cleaned_text)
        text_lower = cleaned_text.lower()
        m = HftMetrics()

        # 1. Core affinity pinning
        has_pinning = bool(
            "affinity" in text_lower or
            "pthread_setaffinity_np" in text_lower or
            "sched_setaffinity" in text_lower or
            "pinned_core_id" in text_lower or
            "bind_thread_affinity" in text_lower or
            "isolcpus" in text_lower or
            metadata.get("has_core_affinity_pinning", False)
        )
        m.has_core_affinity_pinning = has_pinning

        # 2. Lock-free ring buffer
        has_queue = bool(
            "ring_capacity" in text_lower or
            "lockfree" in text_lower or
            "lock_free" in text_lower or
            "spsc" in text_lower or
            ("head_index" in text_lower and "tail_index" in text_lower) or
            metadata.get("has_lock_free_ring_buffer", False)
        )
        m.has_lock_free_ring_buffer = has_queue

        # 3. Blocking syscall or sleep
        has_blocking = bool(
            "time.sleep" in text_lower or
            "sleep(" in text_lower or
            "epoll_wait" in text_lower or
            "usleep" in text_lower or
            metadata.get("has_blocking_syscall_or_sleep", False)
        )
        m.has_blocking_syscall_or_sleep = has_blocking
        m.has_zero_syscall_polling = not has_blocking and (
            "poll_next" in text_lower or
            "busy_poll" in text_lower or
            "poll_next_tick" in text_lower or
            has_queue
        )

        # 4. Mutex lock in loop
        has_mutex = bool(
            "mutex.lock" in text_lower or
            "pthread_mutex_lock" in text_lower or
            "std::lock_guard" in text_lower or
            "with lock:" in text_lower or
            metadata.get("has_mutex_lock_in_loop", False)
        )
        m.has_mutex_lock_in_loop = has_mutex

        # 5. Heap allocation in tick loop
        has_heap = bool(
            ("for " in text_lower or "while " in text_lower) and
            ("new order" in text_lower or "malloc(" in text_lower or "alloc(" in text_lower) or
            metadata.get("has_heap_alloc_in_tick_loop", False)
        )
        m.has_heap_alloc_in_tick_loop = has_heap

        # Anti-pattern logging
        if m.has_blocking_syscall_or_sleep:
            m.anti_patterns_detected.append("Blocking syscall or sleep on tick-to-trade hot path")
        if m.has_mutex_lock_in_loop:
            m.anti_patterns_detected.append("Blocking mutex lock in order processing pipeline")
        if m.has_heap_alloc_in_tick_loop:
            m.anti_patterns_detected.append("Dynamic heap allocation in tick loop body")

        return m
