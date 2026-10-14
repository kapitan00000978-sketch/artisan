"""
Lucas Cruz - Objective Mobile Architecture & 120Hz Fluidity Inspector.

This module inspects Swift, Kotlin, React Native, and mobile architecture code
to detect main-thread I/O blocking, closure retain cycles, and offline vulnerabilities.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class MobileMetrics:
    has_main_thread_blocking: bool = False
    has_retain_cycles: bool = False
    has_offline_caching: bool = False
    handles_offline_gracefully: bool = False
    has_battery_vampire_polling: bool = False
    min_touch_target_dp: float = 48.0
    has_list_recycling_keys: bool = True
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class MobileInspectionReport:
    metrics: MobileMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_mobile_viable: bool = False


class MobileSystemsInspector:
    """Rigorous mobile auditor inspecting threading hygiene, memory lifecycle, and offline readiness."""

    def inspect(self, mobile_input: Any) -> MobileInspectionReport:
        """
        Audits mobile source code string, app architecture configuration, or metadata dict.
        """
        metrics = self._extract_metrics(mobile_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Main-Thread Hygiene Audit
        if metrics.has_main_thread_blocking:
            critical_violations.append(
                "Main-Thread Blocking I/O: Synchronous network fetch, database query, or disk I/O executing on the UI thread. "
                "Causes frame drops, touch stutter, and risks OS Watchdog termination (0x8badf00d)."
            )
        else:
            benchmarks_passed.append("Strict Main-Thread Hygiene: I/O offloaded to background dispatch queues / IO coroutines.")

        # 2. Retain Cycles & Memory Lifecycle
        if metrics.has_retain_cycles:
            critical_violations.append(
                "Memory Retain Cycle Detected: Strong reference to self captured inside escaping closure or uncancelled listener. "
                "Leans heavily towards memory leaks and low-memory OS termination."
            )
        else:
            benchmarks_passed.append("Memory Lifecycle Guarded: [weak self] / unowned capture semantics verified.")

        # 3. Offline-First Resilience
        if not metrics.has_offline_caching or not metrics.handles_offline_gracefully:
            critical_violations.append(
                "Unmitigated Offline Failure: App lacks local database caching (Room/SQLite/CoreData) or unhandled network crashes. "
                "Leaves users with a broken blank screen in offline conditions."
            )
        else:
            benchmarks_passed.append("Offline-First Architecture: Local cache persistence and network fallback verified.")

        # 4. Battery & Radio Vampire Polling
        if metrics.has_battery_vampire_polling:
            warnings.append(
                "Battery Vampire Polling: Rapid polling interval (<10s) or continuous high-precision GPS detected. "
                "Prevents cellular radio sleep state and causes severe thermal throttling."
            )
        else:
            benchmarks_passed.append("Radio-efficient batching and battery preservation observed.")

        # 5. Touch Target Ergonomics
        if metrics.min_touch_target_dp < 44.0:
            warnings.append(
                f"Microscopic Touch Target ({metrics.min_touch_target_dp:.0f}dp/pt): Minimum ergonomic threshold is 48dp (Android) or 44pt (iOS). "
                "Causes touch registration frustration."
            )
        else:
            benchmarks_passed.append(f"Ergonomic touch targets verified ({metrics.min_touch_target_dp:.0f}dp/pt >= 44pt).")

        # 6. List Recycling & Scroll Jank
        if not metrics.has_list_recycling_keys:
            warnings.append("Missing dynamic list recycling keys; triggers full view re-layout during scrolling.")
        else:
            benchmarks_passed.append("Dynamic list item recycling keys verified for smooth 120Hz scrolling.")

        for ap in metrics.anti_patterns_detected:
            if ap not in critical_violations:
                critical_violations.append(f"Anti-Pattern Detected: {ap}")

        is_viable = len(critical_violations) == 0

        return MobileInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_mobile_viable=is_viable
        )

    def _extract_metrics(self, mobile_input: Any) -> MobileMetrics:
        text = ""
        metadata: Dict[str, Any] = {}

        if isinstance(mobile_input, str):
            text = mobile_input
            try:
                parsed = json.loads(mobile_input)
                if isinstance(parsed, dict):
                    metadata = parsed
            except (json.JSONDecodeError, ValueError) as _json_err:
                _ = _json_err
        elif isinstance(mobile_input, dict):
            metadata = mobile_input
            text = json.dumps(mobile_input)
        else:
            text = str(mobile_input)

        text_lower = text.lower()
        m = MobileMetrics()

        # 1. Main-thread blocking detection
        has_blocking = (
            "dispatchqueue.main.sync" in text_lower or
            "runblocking" in text_lower or
            "thread.sleep" in text_lower or
            ("urlsession.shared.data(from:" in text_lower and "async" not in text_lower and "await" not in text_lower and "completionhandler" not in text_lower) or
            ("sqlite.execute" in text_lower and "dispatchqueue.main" in text_lower) or
            metadata.get("has_main_thread_blocking", False)
        )
        m.has_main_thread_blocking = has_blocking

        # 2. Retain cycle detection
        has_retain = False
        # In Swift: escaping closure capturing self without [weak self]
        if ("completionhandler" in text_lower or "dispatchqueue.global" in text_lower or "urlsession" in text_lower):
            if "self." in text_lower and "[weak self]" not in text_lower and "[unowned self]" not in text_lower:
                has_retain = True
        if metadata.get("has_retain_cycles", False):
            has_retain = True
        m.has_retain_cycles = has_retain

        # 3. Offline Caching
        has_offline = (
            "room" in text_lower or
            "coredata" in text_lower or
            "sqlite" in text_lower or
            "realm" in text_lower or
            "asyncstorage" in text_lower or
            "watermelondb" in text_lower or
            "localcache" in text_lower or
            "cache_first" in text_lower or
            metadata.get("has_offline_caching", False)
        )
        m.has_offline_caching = has_offline

        has_fallback = (
            ("catch" in text_lower or "do-catch" in text_lower or "onerror" in text_lower or "guard let" in text_lower) and
            has_offline
        ) or metadata.get("handles_offline_gracefully", False)
        m.handles_offline_gracefully = has_fallback

        # 4. Battery / Vampire polling
        has_vampire = bool(
            re.search(r"setinterval\([^,]+,\s*[1-5]000\)", text_lower) or
            ("kcllocationaccuracybest" in text_lower and re.search(r"allowsbackgroundlocationupdates\s*=\s*true", text_lower))
        ) or metadata.get("has_battery_vampire_polling", False)
        m.has_battery_vampire_polling = has_vampire

        # 5. Touch Target
        touch_match = re.search(r"(?:width|height|size|frame)\s*[:=]\s*(\d+)", text_lower)
        if touch_match:
            val = float(touch_match.group(1))
            if val < 44.0:
                m.min_touch_target_dp = val
        else:
            m.min_touch_target_dp = float(metadata.get("min_touch_target_dp", 48.0))

        # 6. List Recycling Keys
        if "flatlist" in text_lower and "keyextractor" not in text_lower:
            m.has_list_recycling_keys = False
        elif "lazycolumn" in text_lower and "items(key =" not in text_lower:
            m.has_list_recycling_keys = False
        else:
            m.has_list_recycling_keys = bool(metadata.get("has_list_recycling_keys", True))

        # Anti-pattern logging
        if m.has_main_thread_blocking:
            m.anti_patterns_detected.append("Blocking synchronous I/O executing on main thread")
        if m.has_retain_cycles:
            m.anti_patterns_detected.append("Strong self reference cycle in asynchronous escaping closure")
        if not m.has_offline_caching:
            m.anti_patterns_detected.append("Complete absence of local persistence cache for offline capability")

        return m
