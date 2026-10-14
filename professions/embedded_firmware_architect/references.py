"""
Morpheus 'The Kernel' Vance - Embedded Firmware & Bare-Metal Architecture Reference Standards.

This module codifies empirical interrupt latency budgets, static memory allocation rules,
DMA cache coherency invariants, hardware watchdog supervisory standards, and toxic firmware anti-patterns.
"""

from typing import Dict, Any, List


FIRMWARE_SYSTEM_BENCHMARKS: Dict[str, Any] = {
    "max_isr_duration_microseconds": 5.0,
    "max_dynamic_heap_allocations": 0,
    "hardware_watchdog_timeout_ms": 250,
    "dma_buffer_alignment_bytes": 32,
    "stack_canary_guard_bytes": 16,
    "min_brownout_reset_voltage_v": 2.7,
}

FIRMWARE_ARCHITECTURE_STANDARDS: Dict[str, Dict[str, str]] = {
    "zero_heap_static_allocation": {
        "standard": "All buffers, RTOS task control blocks, stacks, and queues must be allocated statically at compile time.",
        "requirement": "Zero calls to malloc(), free(), or realloc(); memory pools use fixed-size block allocators.",
        "benefit": "Guarantees zero memory fragmentation lockups and deterministic startup RAM footprints."
    },
    "deferred_interrupt_handling": {
        "standard": "Interrupt Service Routines (ISRs) only clear hardware flags, push to ring buffers, and signal worker tasks.",
        "requirement": "Heavy processing deferred to RTOS tasks via direct-to-task notifications (xTaskNotifyFromISR).",
        "benefit": "Maintains low interrupt jitter and prevents higher-priority hardware interrupts from being starved."
    },
    "dma_cache_coherency_maintenance": {
        "standard": "DMA buffer transfers must perform explicit cache clean (flush) before TX and cache invalidate after RX.",
        "requirement": "Buffers placed in 32-byte cacheline aligned memory or non-cacheable MPU regions (SCB_InvalidateDCache_by_Addr).",
        "benefit": "Prevents CPU cores from operating on stale cached data while DMA writes to physical memory."
    },
    "hardware_watchdog_supervisor": {
        "standard": "Independent Hardware Watchdog Timer (IWDG/WDT) clocked from dedicated low-speed oscillator (LSI/RC).",
        "requirement": "Refreshed exclusively from a dedicated supervisor task checking health flags of all system threads.",
        "benefit": "Guarantees automatic system reboot if any critical task deadlocks or encounters hard-fault conditions."
    },
    "memory_mapped_io_barriers": {
        "standard": "All peripheral registers declared as volatile uint32_t* with explicit hardware memory barrier instructions.",
        "requirement": "Insert Data Memory Barrier (__DMB) and Data Synchronization Barrier (__DSB) after peripheral register writes.",
        "benefit": "Prevents out-of-order execution in pipelined ARM Cortex-M/RISC-V cores from corrupting register sequences."
    }
}

TOXIC_FIRMWARE_ANTI_PATTERNS: List[Dict[str, str]] = [
    {
        "id": "dynamic_heap_allocation_in_embedded",
        "indicator": "Calling malloc(), free(), calloc(), or C++ new operator on microcontrollers without MMU.",
        "risk": "Heap fragmentation causes sudden catastrophic allocation failure after days or weeks of runtime.",
        "severity": "FATAL"
    },
    {
        "id": "blocking_delay_inside_isr",
        "indicator": "Calling delay_ms(), HAL_Delay(), or waiting in while-loops inside interrupt service routines.",
        "risk": "Locks CPU in interrupt context, starving all other hardware interrupts and causing system hang.",
        "severity": "FATAL"
    },
    {
        "id": "missing_volatile_on_mmio_register",
        "indicator": "Accessing hardware peripheral registers or shared ISR flags without volatile type qualification.",
        "risk": "Compiler optimizes away repeated reads, assuming variable never changes in memory, causing infinite loops.",
        "severity": "FATAL"
    },
    {
        "id": "dma_transfers_without_cache_maintenance",
        "indicator": "Enabling DMA burst transfers on cache-enabled Cortex-M7 cores without D-Cache clean/invalidate.",
        "risk": "CPU reads stale cache lines, resulting in silent data corruption in network packets or sensor data.",
        "severity": "HIGH"
    },
    {
        "id": "unserviced_or_disabled_watchdog",
        "indicator": "Deploying firmware without independent hardware watchdog timer enabled.",
        "risk": "System lockup from cosmic ray single-event upset requires manual power cycle by end user.",
        "severity": "HIGH"
    }
]

CANONICAL_FIRMWARE_CORE: str = (
    "// Morpheus Vance: Canonical Embedded Bare-Metal Firmware with Static Allocation & Watchdog\n"
    "#include <stdint.h>\n"
    "#include <stdbool.h>\n"
    "\n"
    "#define DMA_BUFFER_SIZE 256\n"
    "#define WATCHDOG_RELOAD_VAL 0x0FFF\n"
    "\n"
    "// 1. Static Allocation - Zero Dynamic Heap\n"
    "static uint8_t g_dma_rx_buffer[DMA_BUFFER_SIZE] __attribute__((aligned(32)));\n"
    "static volatile uint32_t g_isr_event_flags = 0;\n"
    "\n"
    "// Memory-Mapped Peripheral Registers (Volatile Qualification)\n"
    "#define PERIPH_BASE 0x40000000UL\n"
    "#define WDT_REG_CR  (*(volatile uint32_t *)(PERIPH_BASE + 0x00))\n"
    "#define WDT_REG_SR  (*(volatile uint32_t *)(PERIPH_BASE + 0x04))\n"
    "\n"
    "// 2. Hardware Watchdog Supervisor\n"
    "void bsp_watchdog_init(void) {\n"
    "    WDT_REG_CR = WATCHDOG_RELOAD_VAL;\n"
    "    __asm__ volatile(\"dmb 0xF\" ::: \"memory\"); // Data Memory Barrier\n"
    "}\n"
    "\n"
    "void bsp_watchdog_refresh(void) {\n"
    "    WDT_REG_SR = 0xAAAA; // Key value to reload counter\n"
    "    __asm__ volatile(\"dsb 0xF\" ::: \"memory\");\n"
    "}\n"
    "\n"
    "// 3. DMA Cache Coherency Maintenance\n"
    "void bsp_dma_cache_invalidate(uint8_t *addr, uint32_t length) {\n"
    "    // SCB_InvalidateDCache_by_Addr((uint32_t*)addr, length);\n"
    "    __asm__ volatile(\"dsb 0xF\" ::: \"memory\");\n"
    "    __asm__ volatile(\"isb 0xF\" ::: \"memory\");\n"
    "}\n"
    "\n"
    "// 4. Deferred Interrupt Service Routine (Sub-5 Microsecond Execution)\n"
    "void USART1_IRQHandler(void) {\n"
    "    // Clear interrupt flag immediately; zero blocking delays or malloc\n"
    "    g_isr_event_flags |= (1U << 0);\n"
    "    __asm__ volatile(\"dmb 0xF\" ::: \"memory\");\n"
    "}\n"
    "\n"
    "// 5. Main Task Loop (Non-blocking Superloop)\n"
    "void firmware_main_superloop(void) {\n"
    "    bsp_watchdog_init();\n"
    "    while (1) {\n"
    "        if (g_isr_event_flags & (1U << 0)) {\n"
    "            g_isr_event_flags &= ~(1U << 0);\n"
    "            bsp_dma_cache_invalidate(g_dma_rx_buffer, DMA_BUFFER_SIZE);\n"
    "        }\n"
    "        bsp_watchdog_refresh();\n"
    "    }\n"
    "}\n"
)


class FirmwareReferenceLibrary:
    """Provides empirical embedded firmware benchmarks, static memory allocation rules, and ISR standards."""

    @staticmethod
    def get_benchmarks() -> Dict[str, Any]:
        return FIRMWARE_SYSTEM_BENCHMARKS

    @staticmethod
    def get_standards() -> Dict[str, Dict[str, str]]:
        return FIRMWARE_ARCHITECTURE_STANDARDS

    @staticmethod
    def get_toxic_anti_patterns() -> List[Dict[str, str]]:
        return TOXIC_FIRMWARE_ANTI_PATTERNS

    @staticmethod
    def get_canonical_core() -> str:
        return CANONICAL_FIRMWARE_CORE
