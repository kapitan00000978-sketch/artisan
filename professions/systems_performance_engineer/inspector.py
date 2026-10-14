"""
Valerie 'The Edge' Cross - Objective Systems & Low-Level Performance Inspector.

This module inspects C++, Rust, and C systems code to detect heap allocations in hot loops,
false sharing across cache lines, redundant memcpy operations, and unvectorized scalar math.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class SystemsMetrics:
    has_cache_line_alignment: bool = False
    has_zero_allocation_hot_loop: bool = False
    has_heap_alloc_in_loop: bool = False
    has_zero_copy_slices: bool = False
    has_simd_or_branchless_optimization: bool = False
    has_false_sharing_vulnerability: bool = False
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class SystemsInspectionReport:
    metrics: SystemsMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_systems_viable: bool = False


class SystemsPerformanceInspector:
    """Rigorous low-level performance auditor evaluating mechanical sympathy and hardware efficiency."""

    def inspect(self, code_input: Any) -> SystemsInspectionReport:
        """
        Audits C++, Rust, or systems performance source code or performance profile dict.
        """
        metrics = self._extract_metrics(code_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Zero-Allocation Hot Path Discipline
        if metrics.has_heap_alloc_in_loop:
            critical_violations.append(
                "Heap Allocation in Hot Loop: Calling dynamic allocator (malloc/new/Box::new) inside loop body. "
                "Causes thread lock contention, cache misses, and multi-microsecond tail latency spikes."
            )
        elif metrics.has_zero_allocation_hot_loop:
            benchmarks_passed.append("Zero-allocation hot loop verified (Pre-allocated stack/arena buffers).")

        # 2. Cache Line Alignment (64-Byte Discipline)
        if metrics.has_false_sharing_vulnerability:
            critical_violations.append(
                "False Sharing Hazard: Adjacent thread-shared atomic variables lack 64-byte alignment/padding. "
                "Triggers severe cache-line thrashing across CPU cores on multicore architectures."
            )
        elif metrics.has_cache_line_alignment:
            benchmarks_passed.append("64-byte cache line alignment verified (alignas(64) / #[repr(align(64))]).")
        else:
            warnings.append("No explicit 64-byte cache line alignment specified for thread-shared structs.")

        # 3. Zero-Copy Slice Passing
        if not metrics.has_zero_copy_slices:
            warnings.append("Consider passing zero-copy slices (std::span, std::string_view, &[u8]) instead of owning containers.")
        else:
            benchmarks_passed.append("Zero-copy slice reference passing verified.")

        # 4. SIMD & Vectorization
        if metrics.has_simd_or_branchless_optimization:
            benchmarks_passed.append("SIMD vectorization hints or branchless arithmetic verified.")

        for ap in metrics.anti_patterns_detected:
            if ap not in critical_violations:
                critical_violations.append(f"Anti-Pattern Detected: {ap}")

        is_viable = len(critical_violations) == 0

        return SystemsInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_systems_viable=is_viable
        )

    def _extract_metrics(self, code_input: Any) -> SystemsMetrics:
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

        text_lower = text.lower()
        m = SystemsMetrics()

        # 1. Cache line alignment
        has_align = bool(
            "alignas(64)" in text_lower or
            "repr(align(64))" in text_lower or
            "cache_line" in text_lower or
            metadata.get("has_cache_line_alignment", False)
        )
        m.has_cache_line_alignment = has_align

        # 2. Heap allocation in loop
        has_loop_alloc = bool(
            re.search(r"(?:for|while)\s*\([^)]*\)\s*\{[^}]*(?:new\s+\w+|malloc\(|Box::new|Vec::new)", text) or
            (("for " in text_lower or "while " in text_lower or "while(" in text_lower) and ("malloc(" in text_lower or "new " in text_lower or "box::new" in text_lower or "vec::new" in text_lower)) or
            metadata.get("has_heap_alloc_in_loop", False)
        )
        m.has_heap_alloc_in_loop = has_loop_alloc
        m.has_zero_allocation_hot_loop = not has_loop_alloc and ("for " in text_lower or "while " in text_lower or "process_batch" in text_lower)

        # 3. False sharing detection
        has_false_sharing = bool(
            ("atomic" in text_lower and not has_align) or
            metadata.get("has_false_sharing_vulnerability", False)
        )
        m.has_false_sharing_vulnerability = has_false_sharing

        # 4. Zero copy slices
        has_slices = bool(
            "std::span" in text_lower or
            "std::string_view" in text_lower or
            "&[u8]" in text_lower or
            "&str" in text_lower or
            "const " in text_lower and "&" in text_lower or
            metadata.get("has_zero_copy_slices", False)
        )
        m.has_zero_copy_slices = has_slices

        # 5. SIMD / Branchless
        has_simd = bool(
            "#pragma omp simd" in text_lower or
            "simd" in text_lower or
            "_mm256" in text_lower or
            "branchless" in text_lower or
            metadata.get("has_simd_or_branchless_optimization", False)
        )
        m.has_simd_or_branchless_optimization = has_simd

        # Anti-pattern logging
        if m.has_heap_alloc_in_loop:
            m.anti_patterns_detected.append("Dynamic heap allocation in inner loop body")
        if m.has_false_sharing_vulnerability:
            m.anti_patterns_detected.append("False sharing cache-line hazard across threads")

        return m
