"""
Lucas Cruz - Mobile Systems & 120Hz Fluidity Reference Standards.

This module codifies empirical mobile performance benchmarks, main-thread hygiene rules,
touch target ergonomics, and offline-first architectural patterns.
"""

from typing import Dict, Any, List


MOBILE_FRAME_STANDARDS: Dict[str, Dict[str, float]] = {
    "120hz_promotion": {
        "frame_budget_ms": 8.333,
        "max_input_latency_ms": 16.0,
        "max_draw_dispatch_ms": 3.0
    },
    "60hz_standard": {
        "frame_budget_ms": 16.666,
        "max_input_latency_ms": 32.0,
        "max_draw_dispatch_ms": 6.0
    }
}

ERGONOMIC_BENCHMARKS: Dict[str, Any] = {
    "ios_min_touch_target_pt": 44.0,
    "android_min_touch_target_dp": 48.0,
    "max_cold_start_time_seconds": 1.2,
    "max_idle_ram_mb": 80.0,
    "max_background_time_seconds": 30.0,
    "cellular_radio_batch_interval_seconds": 60.0
}

TOXIC_MOBILE_ANTI_PATTERNS: List[Dict[str, str]] = [
    {
        "id": "main_thread_blocking_io",
        "indicator": "Executing network requests, SQLite queries, or disk reads on UI / Main Dispatch thread.",
        "risk": "Freezes UI, causes frame drops, and triggers OS Watchdog kill (0x8badf00d).",
        "severity": "FATAL"
    },
    {
        "id": "retain_cycle_strong_self",
        "indicator": "Capturing self strongly inside escaping asynchronous closures or completion handlers.",
        "risk": "Prevents deallocation of ViewControllers and large bitmap caches; triggers OS memory kill.",
        "severity": "FATAL"
    },
    {
        "id": "unhandled_offline_crash",
        "indicator": "Throwing unhandled network exceptions when device has no connectivity without local cache fallback.",
        "risk": "Leaves user staring at a blank screen or crashing when network is lost.",
        "severity": "FATAL"
    },
    {
        "id": "vampire_gps_polling",
        "indicator": "Continuously requesting high-accuracy GPS (kCLLocationAccuracyBest) without distance filtering.",
        "risk": "Heats up phone, drains 20%+ battery per hour, and degrades user device health.",
        "severity": "HIGH"
    },
    {
        "id": "microscopic_touch_target",
        "indicator": "Interactive button or tap target with dimensions < 44pt (iOS) or < 48dp (Android).",
        "risk": "Causes touch registration misses, tap frustration, and accessibility guideline failure.",
        "severity": "HIGH"
    },
    {
        "id": "unkeyed_dynamic_list",
        "indicator": "Rendering dynamic lists without stable unique item keys or cell recycling IDs.",
        "risk": "Forces layout recalculation on every scroll tick; devastating scroll jank and stutter.",
        "severity": "MEDIUM"
    }
]

CANONICAL_SWIFT_SAFE_DISPATCH: str = (
    "// Lucas Cruz: Zero-Stutter Background Offloading & Weak Self Discipline\n"
    "DispatchQueue.global(qos: .userInitiated).async { [weak self] in\n"
    "    let result = self?.performHeavyProcessing()\n"
    "    DispatchQueue.main.async { [weak self] in\n"
    "        guard let self = self else { return }\n"
    "        self.updateUI(with: result)\n"
    "    }\n"
    "}\n"
)


class MobileReferenceLibrary:
    """Provides empirical mobile benchmarks, thread hygiene rules, and anti-patterns."""

    @staticmethod
    def get_frame_standards() -> Dict[str, Dict[str, float]]:
        return MOBILE_FRAME_STANDARDS

    @staticmethod
    def get_ergonomic_benchmarks() -> Dict[str, Any]:
        return ERGONOMIC_BENCHMARKS

    @staticmethod
    def get_toxic_anti_patterns() -> List[Dict[str, str]]:
        return TOXIC_MOBILE_ANTI_PATTERNS

    @staticmethod
    def get_canonical_swift_dispatch() -> str:
        return CANONICAL_SWIFT_SAFE_DISPATCH
