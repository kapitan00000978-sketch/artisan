"""
Lucas Cruz - Blind Mobile Systems & Kinetic Ergonomics Critic.

Evaluates mobile code strictly against main-thread fluidity (120Hz),
memory retain cycle hygiene, and offline-first durability.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.mobile_systems_architect.inspector import MobileSystemsInspector, MobileInspectionReport
from professions.mobile_systems_architect.rubric import MobileSystemsRubric, MobileRubricEvaluation


@dataclass
class MobileDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    device_impact: str
    actionable_fix: str


@dataclass
class MobileDefectLedger:
    verdict: str  # CERTIFIED_KINETIC_120HZ or REJECTED_STUTTER_HAZARD
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[MobileDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindMobileCritic:
    """Mobile adversary reviewing code strictly for device fluidness, memory safety, and battery health."""

    def __init__(self):
        self.inspector = MobileSystemsInspector()
        self.rubric = MobileSystemsRubric()

    def review(self, mobile_input: Any) -> MobileDefectLedger:
        """
        Runs objective inspection and adversarial rubric scoring, producing a Mobile Defect Ledger.
        """
        report: MobileInspectionReport = self.inspector.inspect(mobile_input)
        eval_result: MobileRubricEvaluation = self.rubric.evaluate(report)

        defects: List[MobileDefect] = []

        # 1. Critical violations -> FATAL defects
        for i, violation in enumerate(report.critical_violations, start=1):
            if "main-thread" in violation.lower():
                title = "Main-Thread Blocking I/O Stall"
                impact = "UI freezes, touch gestures stutter, and OS terminates process with 0x8badf00d watchdog kill."
                fix = "Offload synchronous I/O to background queue: DispatchQueue.global() or Dispatchers.IO."
            elif "retain cycle" in violation.lower():
                title = "Escaping Closure Retain Cycle"
                impact = "ViewControllers and image buffers are retained in memory; triggers OS Low-Memory jetsam termination."
                fix = "Capture self weakly via [weak self] and unwrap with guard let self = self else { return }."
            elif "offline" in violation.lower():
                title = "Unmitigated Offline Failure"
                impact = "App crashes or shows empty blank screen when connectivity drops in transit/subway."
                fix = "Implement local persistence cache (SQLite, Room, or CoreData) with offline error fallback."
            else:
                title = "Critical Mobile Architecture Flaw"
                impact = "Severely degrades device fluidity, battery, or stability."
                fix = "Re-architect component according to Lucas Cruz kinetic benchmarks."

            defects.append(
                MobileDefect(
                    defect_id=f"MOBILE-FATAL-{i:03d}",
                    severity="FATAL",
                    title=title,
                    description=violation,
                    device_impact=impact,
                    actionable_fix=fix
                )
            )

        # 2. Veto reasons
        for j, reason in enumerate(eval_result.veto_reasons, start=len(defects) + 1):
            if not any(d.description == reason for d in defects):
                defects.append(
                    MobileDefect(
                        defect_id=f"MOBILE-FATAL-{j:03d}",
                        severity="FATAL",
                        title="Mobile Quality Veto",
                        description=reason,
                        device_impact="Violates Tier-1 mobile user experience criteria.",
                        actionable_fix="Refactor threading and memory architecture."
                    )
                )

        # 3. Warnings -> HIGH / MEDIUM defects
        for k, warning in enumerate(report.warnings, start=len(defects) + 1):
            sev = "HIGH" if "battery" in warning.lower() or "touch target" in warning.lower() else "MEDIUM"
            defects.append(
                MobileDefect(
                    defect_id=f"MOBILE-WARN-{k:03d}",
                    severity=sev,
                    title="Mobile Performance Deficiency",
                    description=warning,
                    device_impact="Battery drainage, thermal throttling, or scroll jank.",
                    actionable_fix="Batch network calls, enlarge touch targets to >= 48dp, and add list item keys."
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = "CERTIFIED_KINETIC_120HZ" if eval_result.is_certified else "REJECTED_STUTTER_HAZARD"

        if eval_result.is_certified:
            summary = (
                f"KINETIC CERTIFIED (Score: {eval_result.total_score}/100). "
                "Main-thread hygiene verified, zero retain cycles detected, "
                "offline persistence active, and 48dp ergonomic touch targets preserved. Locked 120Hz fluidity guaranteed."
            )
        else:
            summary = (
                f"REJECTED BY THE MOBILE ARCHITECT (Score: {eval_result.total_score}/100, Threshold: {eval_result.passing_threshold}). "
                f"Detected {fatal_count} fatal threading/memory flaws and {high_count} operational warnings. "
                "The app will stutter, leak memory, or crash when offline."
            )

        return MobileDefectLedger(
            verdict=verdict,
            score=eval_result.total_score,
            passing_threshold=eval_result.passing_threshold,
            is_certified=eval_result.is_certified,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
