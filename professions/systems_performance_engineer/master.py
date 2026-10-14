"""
⚙️ VALERIE 'THE EDGE' CROSS — PRINCIPAL SYSTEMS & LOW-LEVEL PERFORMANCE ARCHITECT
Autonomous hardware conscience, cache alignment inspection, blind latency critique,
and zero-allocation SIMD systems elevation engine.

Usage:
    python professions/systems_performance_engineer/master.py <code_file> [--elevate]
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
    from .references import SystemsReferenceLibrary
    from .inspector import SystemsPerformanceInspector, SystemsInspectionReport
    from .rubric import SystemsPerformanceRubric, SystemsRubricEvaluation
    from .blind_critic import BlindSystemsCritic, SystemsDefectLedger
    from .elevation_engine import SystemsElevationEngine
except ImportError:
    from references import SystemsReferenceLibrary
    from inspector import SystemsPerformanceInspector, SystemsInspectionReport
    from rubric import SystemsPerformanceRubric, SystemsRubricEvaluation
    from blind_critic import BlindSystemsCritic, SystemsDefectLedger
    from elevation_engine import SystemsElevationEngine

# Import global ActiveDecisionJournal from studio engine
try:
    from src.studio.active_memory import ActiveDecisionJournal
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.studio.active_memory import ActiveDecisionJournal


class ValerieCrossMaster:
    """
    Valerie Cross: The living systems performance sovereign, mechanical sympathy inquisitor,
    and hardware conscience. Eliminates heap allocations in hot paths, enforces 64-byte
    cache line alignment, and sculpts sub-microsecond SIMD pipelines.
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
        self.inspector = SystemsPerformanceInspector()
        self.rubric = SystemsPerformanceRubric()
        self.critic = BlindSystemsCritic()
        self.elevation_engine = SystemsElevationEngine()
        self.journal = ActiveDecisionJournal()

    def run_autonomous_cycle(self, input_data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes the closed-loop autonomous systems performance audit & elevation lifecycle.
        1. Inspect -> 2. Rubric -> 3. Critic -> 4. Elevate (if < 85) -> 5. Certify & Journal
        """
        data = input_data
        if data is None and self.target_path:
            if os.path.exists(self.target_path):
                with open(self.target_path, "r", encoding="utf-8") as f:
                    data = f.read()
            else:
                raise FileNotFoundError(f"Systems target file not found: {self.target_path}")

        if data is None:
            # Baseline prototype flawed systems code for testing or demo
            data = (
                "// Flawed Systems Pipeline\n"
                "struct ThreadState { std::atomic<int> counter; };\n"
                "void process_data(std::vector<int> data) {\n"
                "    for (int i = 0; i < data.size(); ++i) {\n"
                "        int* buffer = new int[64];\n"
                "        delete[] buffer;\n"
                "    }\n"
                "}\n"
            )

        # Step 1: Initial Blind Critic Review
        ledger: SystemsDefectLedger = self.critic.review(data)
        initial_score = ledger.score
        elevated_result: Optional[Dict[str, Any]] = None

        # Step 2: Elevate if failed
        current_data = data
        if not ledger.is_certified:
            elevated_result = self.elevation_engine.elevate(current_data, max_iterations=self.max_cycles)
            current_data = elevated_result["elevated_code"]
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
            "elevated_code": current_data,
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
                target_file=self.target_path if self.target_path else "pipeline.cpp",
                defects_before=[f"Fatal defects: {fatal_defects}"],
                actions_taken=["valerie_systems_performance_elevation"],
                score_before=float(initial_score),
                score_after=float(final_score)
            )
        except Exception as _journal_err:
            sys.stderr.write(f"Note: Decision journal record skipped: {_journal_err}\n")

    def _generate_briefing(self, code_data: Any, ledger: SystemsDefectLedger) -> str:
        report = self.inspector.inspect(code_data)
        m = report.metrics

        status_icon = "⚙️ [MECHANICAL SYMPATHY CERTIFIED]" if ledger.is_certified else "⚠️ [REJECTED SILICON STRANGULATION]"

        briefing = [
            f"# {status_icon} EXECUTIVE LOW-LEVEL SYSTEMS BRIEFING",
            f"**Auditor:** Valerie 'The Edge' Cross (Principal Systems & Low-Level Performance Architect)",
            f"**Final Score:** {ledger.score}/100 (Threshold: {ledger.passing_threshold})",
            f"**Verdict:** {ledger.verdict}",
            "",
            "## 1. Hardware Metrics & Silicon Discipline",
            f"- **Zero-Allocation Hot Loop:** {'PASS (Pre-allocated Memory)' if m.has_zero_allocation_hot_loop else 'FAIL (Dynamic Heap Allocation)'}",
            f"- **64-Byte Cache Alignment:** {'PASS (alignas(64) Enforced)' if m.has_cache_line_alignment else 'WARN (Potential Cache Misses)'}",
            f"- **False Sharing Immunity:** {'FAIL (Thread Contention Risk)' if m.has_false_sharing_vulnerability else 'PASS (Zero False Sharing)'}",
            f"- **Zero-Copy Memory Views:** {'PASS (Slices / std::span)' if m.has_zero_copy_slices else 'WARN (Pass-by-value / Memcpy)'}",
            f"- **SIMD Vectorization:** {'ACTIVE (#pragma omp simd)' if m.has_simd_or_branchless_optimization else 'SCALAR EXECUTION'}",
            "",
            "## 2. Defects Ledger & Architectural Interventions",
        ]

        if ledger.defects:
            for d in ledger.defects:
                briefing.append(f"### [{d.severity}] {d.title} ({d.defect_id})")
                briefing.append(f"- **Description:** {d.description}")
                briefing.append(f"- **Hardware Impact:** {d.hardware_impact}")
                briefing.append(f"- **Actionable Fix:** {d.actionable_fix}")
                briefing.append("")
        else:
            briefing.append("Zero hardware or cache line defects detected. Flawless mechanical sympathy and tail latency discipline achieved.")

        return "\n".join(briefing)


def main():
    parser = argparse.ArgumentParser(
        description="Valerie Cross: Autonomous Systems & Low-Level Performance Master"
    )
    parser.add_argument("target", nargs="?", help="Path to C++/Rust/C source file or profile")
    parser.add_argument("--elevate", action="store_true", help="Automatically elevate flawed systems code")
    parser.add_argument("--threshold", type=int, default=85, help="Passing score threshold (default: 85)")
    args = parser.parse_args()

    master = ValerieCrossMaster(target_path=args.target, passing_threshold=args.threshold)
    results = master.run_autonomous_cycle()

    print(results["executive_briefing"])

    if args.elevate and "elevated_code" in results:
        print("\n--- ELEVATED HIGH-PERFORMANCE CODE ---")
        print(results["elevated_code"])

    sys.exit(0 if results["is_certified"] else 1)


if __name__ == "__main__":
    main()
