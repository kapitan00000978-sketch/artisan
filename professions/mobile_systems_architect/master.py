"""
📱 LUCAS CRUZ — PRINCIPAL MOBILE SYSTEMS ARCHITECT
Autonomous 120Hz fluidity conscience, main-thread hygiene inspection, blind outcome critique,
and automated offline-first mobile architecture elevation engine.

Usage:
    python professions/mobile_systems_architect/master.py <mobile_file> [--elevate]
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, List, Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception as _enc_err:
        sys.stderr.write(f"Note: UTF-8 stdout reconfiguration skipped: {_enc_err}\n")

try:
    from .references import MobileReferenceLibrary
    from .inspector import MobileSystemsInspector, MobileInspectionReport
    from .rubric import MobileSystemsRubric, MobileRubricEvaluation
    from .blind_critic import BlindMobileCritic, MobileDefectLedger
    from .elevation_engine import MobileSystemsElevationEngine
except ImportError:
    from references import MobileReferenceLibrary
    from inspector import MobileSystemsInspector, MobileInspectionReport
    from rubric import MobileSystemsRubric, MobileRubricEvaluation
    from blind_critic import BlindMobileCritic, MobileDefectLedger
    from elevation_engine import MobileSystemsElevationEngine

# Import global ActiveDecisionJournal from studio engine
try:
    from src.studio.active_memory import ActiveDecisionJournal
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.studio.active_memory import ActiveDecisionJournal


class LucasCruzMaster:
    """
    Lucas Cruz: The living mobile systems architect, 120Hz fluidity conscience,
    and kinetic ergonomics purist. Eliminates main-thread blocking, eradicates retain cycles,
    and enforces rock-solid offline-first mobile performance.
    """

    def __init__(
        self,
        target_path: Optional[str] = None,
        passing_threshold: int = 85,
        max_cycles: int = 3
    ):
        self.target_path = os.path.abspath(target_path) if target_path else None
        self.passing_threshold = passing_threshold
        self.max_cycles = max_cycles
        self.inspector = MobileSystemsInspector()
        self.rubric = MobileSystemsRubric()
        self.critic = BlindMobileCritic()
        self.elevation_engine = MobileSystemsElevationEngine()
        self.journal = ActiveDecisionJournal()

    def run_autonomous_cycle(self, input_data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes the closed-loop autonomous mobile audit & elevation lifecycle.
        1. Inspect -> 2. Rubric -> 3. Critic -> 4. Elevate (if < 85) -> 5. Certify & Journal
        """
        data = input_data
        if data is None and self.target_path:
            if os.path.exists(self.target_path):
                with open(self.target_path, "r", encoding="utf-8") as f:
                    data = f.read()
            else:
                raise FileNotFoundError(f"Mobile target file not found: {self.target_path}")

        if data is None:
            # Baseline prototype mobile component for testing or demo
            data = (
                "// Flawed Mobile Feed View Component\n"
                "class FeedViewController: UIViewController {\n"
                "    func loadData() {\n"
                "        DispatchQueue.main.sync {\n"
                "            let data = NetworkClient.fetchSync()\n"
                "            self.render(data)\n"
                "        }\n"
                "    }\n"
                "}\n"
            )

        # Step 1: Initial Blind Critic Review
        ledger: MobileDefectLedger = self.critic.review(data)
        initial_score = ledger.score
        elevated_result: Optional[Dict[str, Any]] = None

        # Step 2: Elevate if failed
        current_data = data
        if not ledger.is_certified:
            elevated_result = self.elevation_engine.elevate(current_data, max_iterations=self.max_cycles)
            current_data = elevated_result["elevated_mobile"]
            ledger = elevated_result["final_ledger"]

        # Step 3: Record in Journal
        self._record_journal_entry(
            initial_score=initial_score,
            final_score=ledger.score,
            is_certified=ledger.is_certified,
            fatal_defects=ledger.fatal_defects_count,
            verdict=ledger.verdict
        )

        # Step 4: Generate Executive Briefing
        briefing = self._generate_briefing(current_data, ledger)

        return {
            "is_certified": ledger.is_certified,
            "initial_score": initial_score,
            "final_score": ledger.score,
            "verdict": ledger.verdict,
            "fatal_defects_count": ledger.fatal_defects_count,
            "defects": ledger.defects,
            "elevated_mobile": current_data,
            "executive_briefing": briefing,
            "summary": ledger.critic_verdict_summary
        }

    def _record_journal_entry(
        self,
        initial_score: int,
        final_score: int,
        is_certified: bool,
        fatal_defects: int,
        verdict: str
    ) -> None:
        try:
            self.journal.record_decision(
                iteration=1,
                target_file=self.target_path if self.target_path else "FeedViewController.swift",
                defects_before=[f"Fatal defects: {fatal_defects}"],
                actions_taken=["lucas_120hz_mobile_fluidity_elevation"],
                score_before=float(initial_score),
                score_after=float(final_score)
            )
        except Exception as _journal_err:
            sys.stderr.write(f"Note: Decision journal record skipped: {_journal_err}\n")

    def _generate_briefing(self, mobile_data: Any, ledger: MobileDefectLedger) -> str:
        report = self.inspector.inspect(mobile_data)
        m = report.metrics

        status_icon = "📱 [KINETIC CERTIFIED]" if ledger.is_certified else "⚠️ [REJECTED STUTTER HAZARD]"

        briefing = [
            f"# {status_icon} EXECUTIVE MOBILE SYSTEMS BRIEFING",
            f"**Auditor:** Lucas 'The Kinetic' Cruz (Principal Mobile Systems Architect)",
            f"**Final Score:** {ledger.score}/100 (Threshold: {ledger.passing_threshold})",
            f"**Verdict:** {ledger.verdict}",
            "",
            "## ⚡ I. 120Hz Fluidity & System Health Matrix",
            f"- **Main-Thread I/O Hygiene:** {'HERMETIC (Background Dispatch)' if not m.has_main_thread_blocking else 'BLOCKING (UI Thread Stall Hazard)'}",
            f"- **Memory Retain Cycles:** {'ZERO RETAIN CYCLES ([weak self])' if not m.has_retain_cycles else 'RETAIN CYCLE DETECTED (Leak Risk)'}",
            f"- **Offline-First Persistence:** {'SQLITE / ROOM CACHE ACTIVE' if m.has_offline_caching else 'MISSING (White-Screen Failure)'}",
            f"- **Touch Target Ergonomics:** {f'OPTIMAL ({m.min_touch_target_dp:.0f}dp >= 44pt)' if m.min_touch_target_dp >= 44.0 else f'DEFICIENT ({m.min_touch_target_dp:.0f}dp < 44pt)'}",
            f"- **Battery & Radio Preservation:** {'EFFICIENT BATCHING' if not m.has_battery_vampire_polling else 'VAMPIRE POLLING DETECTED'}",
            "",
            "## 🛑 II. Defect & Remediation Ledger",
        ]

        if not ledger.defects:
            briefing.append("✅ Zero mobile defects identified. Architecture satisfies Tier-1 120Hz ProMotion standards.")
        else:
            for d in ledger.defects:
                briefing.append(f"- **[{d.severity}] {d.title}:** {d.description}")
                briefing.append(f"  *Device Impact:* {d.device_impact}")
                briefing.append(f"  *Actionable Fix:* {d.actionable_fix}")

        briefing.extend([
            "",
            "## 📱 III. Lucas Cruz's Kinetic Directive",
            ledger.critic_verdict_summary,
            ""
        ])

        return "\n".join(briefing)


def main():
    parser = argparse.ArgumentParser(
        description="Lucas Cruz: Principal Mobile Systems Standalone Auditor"
    )
    parser.add_argument("target", nargs="?", default=None, help="Path to mobile source code or component")
    parser.add_argument("--elevate", action="store_true", help="Automatically elevate flawed mobile code")
    parser.add_argument("--threshold", type=int, default=85, help="Minimum passing score")

    args = parser.parse_args()

    master = LucasCruzMaster(target_path=args.target, passing_threshold=args.threshold)
    result = master.run_autonomous_cycle()

    print(result["executive_briefing"])

    if not result["is_certified"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
