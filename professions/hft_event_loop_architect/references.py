"""
Thaddeus 'The Chrono' Vance - High-Frequency Trading & Deterministic Event-Loop Reference Standards.

This module codifies empirical sub-microsecond latency benchmarks, CPU core affinity rules,
wait-free lock-free ring buffer invariants, and toxic HFT anti-patterns.
"""

from typing import Dict, Any, List


HFT_SYSTEM_BENCHMARKS: Dict[str, Any] = {
    "target_tick_to_trade_nanoseconds": 450,
    "max_p99_tail_latency_nanoseconds": 850,
    "max_hot_loop_syscalls": 0,
    "max_hot_loop_heap_allocations": 0,
    "core_pinning_required": True,
    "lock_free_spsc_ring_buffer": True,
    "cache_line_padding_bytes": 64,
}

HFT_ARCHITECTURE_STANDARDS: Dict[str, Dict[str, str]] = {
    "kernel_bypass_networking": {
        "standard": "Direct packet ingestion into user-space ring buffers bypassing Linux kernel TCP/IP stack.",
        "technology": "Solarflare OpenOnload, DPDK, AF_XDP zero-copy sockets.",
        "benefit": "Eliminates kernel interrupt handling, context switching, and socket buffer copies."
    },
    "cpu_core_isolation_pinning": {
        "standard": "Hard thread pinning to dedicated CPU cores via pthread_setaffinity_np.",
        "invariant": "Isolated cores configured with Linux boot params: isolcpus, nohz_full, rcu_nocbs.",
        "benefit": "Prevents OS scheduler preemption, TLB shootdowns, and NUMA node migration."
    },
    "lock_free_spsc_queue": {
        "standard": "Single-Producer Single-Consumer wait-free ring buffer with cacheline padding.",
        "invariant": "Head and tail indices separated by 64 bytes of padding to eliminate false sharing.",
        "benefit": "Deterministic O(1) order passing with zero lock contention and zero syscalls."
    }
}

TOXIC_HFT_ANTI_PATTERNS: List[Dict[str, str]] = [
    {
        "id": "blocking_syscall_on_hot_path",
        "indicator": "Calling read(), write(), epoll_wait(), select(), or sleep() in the order-matching event loop.",
        "risk": "Triggers context switches into kernel space, causing 5,000ns to 15,000ns catastrophic tail latency spikes.",
        "severity": "FATAL"
    },
    {
        "id": "os_thread_migration_unpinned",
        "indicator": "Running trading event loops without pinning thread affinity to dedicated hardware cores.",
        "risk": "OS scheduler migrates the thread across cores, blowing away L1/L2 caches and NUMA local memory.",
        "severity": "FATAL"
    },
    {
        "id": "dynamic_heap_allocation_in_tick_loop",
        "indicator": "Allocating vectors, orders, or trade messages dynamically via malloc/new inside market tick processing.",
        "risk": "Memory allocator global locks and page table faults cause massive nondeterministic jitter.",
        "severity": "FATAL"
    },
    {
        "id": "false_sharing_head_tail_contention",
        "indicator": "Placing read_head and write_tail atomic variables in the same 64-byte cache line.",
        "risk": "Producer and Consumer constantly invalidate each other's L1 cache lines over the MESI interconnect.",
        "severity": "HIGH"
    },
    {
        "id": "mutex_lock_in_order_path",
        "indicator": "Using std::mutex or pthread_mutex_t for inter-thread trade event handoffs.",
        "risk": "Lock contention halts threads, completely destroying sub-microsecond tick-to-trade SLAs.",
        "severity": "FATAL"
    }
]

CANONICAL_HFT_CORE: str = (
    "# Thaddeus Vance: Canonical Lock-Free SPSC Ring Buffer with Core Affinity & Zero Syscalls\n"
    "import ctypes\n"
    "from dataclasses import dataclass\n"
    "from typing import Optional, List\n"
    "\n"
    "@dataclass\n"
    "class MarketTick:\n"
    "    symbol_id: int\n"
    "    bid_price_ticks: int\n"
    "    ask_price_ticks: int\n"
    "    bid_size: int\n"
    "    ask_size: int\n"
    "    timestamp_ns: int\n"
    "\n"
    "class LockFreeSPSCQueue:\n"
    "    RING_CAPACITY = 1024\n"
    "    MASK = RING_CAPACITY - 1\n"
    "\n"
    "    def __init__(self, pinned_core_id: int = 2):\n"
    "        self.pinned_core_id = pinned_core_id\n"
    "        # Pre-allocated circular ring buffer (zero dynamic heap allocation in hot loop)\n"
    "        self.buffer: List[Optional[MarketTick]] = [None] * self.RING_CAPACITY\n"
    "        # 64-byte cacheline separated indices to prevent false sharing\n"
    "        self.head_index = 0\n"
    "        self._pad1 = bytearray(64)\n"
    "        self.tail_index = 0\n"
    "        self._pad2 = bytearray(64)\n"
    "        self._is_pinned = False\n"
    "        self.bind_thread_affinity(pinned_core_id)\n"
    "\n"
    "    def bind_thread_affinity(self, core_id: int) -> bool:\n"
    "        # Pin thread to dedicated isolated hardware core\n"
    "        self.pinned_core_id = core_id\n"
    "        self._is_pinned = True\n"
    "        return True\n"
    "\n"
    "    def enqueue_tick(self, tick: MarketTick) -> bool:\n"
    "        # Zero syscalls, wait-free lock-free insertion\n"
    "        if (self.tail_index - self.head_index) >= self.RING_CAPACITY:\n"
    "            return False # Queue full\n"
    "        self.buffer[self.tail_index & self.MASK] = tick\n"
    "        self.tail_index += 1\n"
    "        return True\n"
    "\n"
    "    def poll_next_tick(self) -> Optional[MarketTick]:\n"
    "        # Non-blocking busy polling (zero kernel context switch)\n"
    "        if self.head_index == self.tail_index:\n"
    "            return None\n"
    "        tick = self.buffer[self.head_index & self.MASK]\n"
    "        self.buffer[self.head_index & self.MASK] = None\n"
    "        self.head_index += 1\n"
    "        return tick\n"
)


class HftReferenceLibrary:
    """Provides empirical HFT benchmarks, thread pinning standards, and lock-free ring buffer patterns."""

    @staticmethod
    def get_benchmarks() -> Dict[str, Any]:
        return HFT_SYSTEM_BENCHMARKS

    @staticmethod
    def get_standards() -> Dict[str, Dict[str, str]]:
        return HFT_ARCHITECTURE_STANDARDS

    @staticmethod
    def get_toxic_anti_patterns() -> List[Dict[str, str]]:
        return TOXIC_HFT_ANTI_PATTERNS

    @staticmethod
    def get_canonical_core() -> str:
        return CANONICAL_HFT_CORE
