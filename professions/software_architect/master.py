"""
🏛️ MARCUS STERLING — SENIOR SOFTWARE ARCHITECT STANDALONE MASTER
Autonomous architectural conscience, AST complexity & modularity inspection, blind outcome critique,
and production-grade refactoring elevation engine.

Usage:
    python professions/software_architect/master.py <target_file> [--benchmark clean_modular_service] [--elevate]
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
    from .references import MarcusArchitectureReferences
    from .inspector import MarcusArchitectureInspector
    from .rubric import MarcusArchitectureRubric
    from .blind_critic import MarcusBlindCritic
    from .elevation_engine import MarcusElevationEngine
except ImportError:
    from references import MarcusArchitectureReferences
    from inspector import MarcusArchitectureInspector
    from rubric import MarcusArchitectureRubric
    from blind_critic import MarcusBlindCritic
    from elevation_engine import MarcusElevationEngine

# Import global ActiveDecisionJournal from studio engine
try:
    from src.studio.active_memory import ActiveDecisionJournal
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.studio.active_memory import ActiveDecisionJournal


class MarcusSterlingMaster:
    """
    Marcus Sterling: The living architectural conscience, structural mind, and systems master.
    Autonomously audits code architecture and refactors systems to clean, resilient standards.
    """

    def __init__(
        self,
        target_file: str,
        benchmark_name: str = "clean_modular_service",
        passing_threshold: float = 85.0,
        max_cycles: int = 3
    ):
        self.target_file = os.path.abspath(target_file)
        self.benchmark_name = benchmark_name
        self.passing_threshold = passing_threshold
        self.max_cycles = max_cycles

        # Components
        self.references = MarcusArchitectureReferences(profile_name=benchmark_name)
        self.inspector = MarcusArchitectureInspector(target_file=self.target_file)
        self.rubric = MarcusArchitectureRubric()
        self.critic = MarcusBlindCritic(passing_score=passing_threshold)
        self.elevation_engine = MarcusElevationEngine()
        self.journal = ActiveDecisionJournal()

    def audit(self) -> Dict[str, Any]:
        """
        Runs an objective, code-blind audit of the target source file.
        Returns metrics, rubric breakdown, and Marcus's verdict.
        """
        metrics = self.inspector.inspect()
        benchmark = self.references.get_benchmarks()
        rubric_eval = self.rubric.evaluate(metrics, benchmark)
        critique = self.critic.critique(rubric_eval, metrics)

        return {
            "evaluator": "Marcus Sterling (Senior Software Architect)",
            "target": self.target_file,
            "benchmark_profile": self.benchmark_name,
            "metrics": metrics,
            "rubric": rubric_eval,
            "critique": critique,
            "score": rubric_eval["total_score"],
            "passed": critique["verdict"] == "CERTIFIED"
        }

    def elevate(self) -> str:
        """Applies Marcus's signature architectural elevation directly to the target file."""
        return self.elevation_engine.elevate(self.target_file)

    def run_autonomous_cycle(self, auto_elevate: bool = True) -> Dict[str, Any]:
        """
        Executes Marcus's full closed-loop architectural craftsmanship cycle:
        1. Measure & Blind Critique
        2. If score < 85 and auto_elevate is True:
           - Consult Active Decision Journal to avoid repeated mistakes
           - Apply surgical refactoring & typing elevation
           - Record decision & score delta in journal
           - Re-audit blindly to verify certificate
        3. Return comprehensive craftsmanship dossier
        """
        cycle_history: List[Dict[str, Any]] = []

        # Initial blind evaluation
        initial_audit = self.audit()
        score_before = initial_audit["score"]
        cycle_history.append({
            "stage": "initial_blind_audit",
            "score": score_before,
            "verdict": initial_audit["critique"]["verdict"],
            "defects_count": initial_audit["critique"]["defects_count"]
        })

        if initial_audit["passed"]:
            return {
                "status": "CERTIFIED_FIRST_PASS",
                "final_score": score_before,
                "passed": True,
                "target": self.target_file,
                "audit": initial_audit,
                "history": cycle_history
            }

        if not auto_elevate:
            return {
                "status": "REJECTED_NEEDS_ELEVATION",
                "final_score": score_before,
                "passed": False,
                "target": self.target_file,
                "audit": initial_audit,
                "history": cycle_history
            }

        # Check Active Decision Journal to verify action is not banned
        action_name = "marcus_structural_refactor_elevation"
        if self.journal.is_action_banned(action_name):
            return {
                "status": "ABORTED_ACTION_BANNED_BY_JOURNAL",
                "final_score": score_before,
                "passed": False,
                "target": self.target_file,
                "audit": initial_audit,
                "history": cycle_history,
                "message": f"Action '{action_name}' is banned in active decision journal due to past regressions."
            }

        # Apply surgical elevation
        defects = [d["flaw"] for d in initial_audit["critique"]["defect_ledger"]]
        self.elevate()

        # Re-audit blindly after elevation
        post_audit = self.audit()
        score_after = post_audit["score"]

        # Record decision in Active Decision Journal
        self.journal.record_decision(
            iteration=1,
            target_file=self.target_file,
            defects_before=defects,
            actions_taken=[action_name],
            score_before=score_before,
            score_after=score_after
        )

        cycle_history.append({
            "stage": "post_elevation_audit",
            "score": score_after,
            "verdict": post_audit["critique"]["verdict"],
            "defects_count": post_audit["critique"]["defects_count"],
            "delta": round(score_after - score_before, 1)
        })

        return {
            "status": "ELEVATED_AND_CERTIFIED" if post_audit["passed"] else "ELEVATED_PARTIAL",
            "final_score": score_after,
            "score_before": score_before,
            "delta": round(score_after - score_before, 1),
            "passed": post_audit["passed"],
            "target": self.target_file,
            "audit": post_audit,
            "history": cycle_history
        }

    def format_console_report(self, result: Dict[str, Any]) -> str:
        """Generates an uncompromising, high-signal architectural report."""
        audit = result.get("audit", {})
        critique = audit.get("critique", {})
        rubric = audit.get("rubric", {})
        dims = rubric.get("dimensions", {})

        lines = [
            "=" * 78,
            "  🏛️ MARCUS STERLING — SENIOR SOFTWARE ARCHITECT REPORT",
            f"     Target: {os.path.basename(self.target_file)} | Benchmark: {self.benchmark_name}",
            "=" * 78,
            f"  Status        : {result.get('status')}",
            f"  Final Score   : {result.get('final_score')}/100 (Threshold: >={self.passing_threshold})",
            f"  Verdict       : {critique.get('verdict')}",
            f"  Summary       : {critique.get('verdict_summary')}",
            "-" * 78,
            "  DIMENSION-BY-DIMENSION BREAKDOWN:"
        ]

        for key, dim in dims.items():
            status_icon = "✅" if dim.get("status") == "PASS" else "❌"
            lines.append(
                f"  {status_icon} {key:<28}: {dim.get('score'):>4}/10 | Measured: {dim.get('measured')} [{dim.get('status')}]"
            )

        if critique.get("defect_ledger"):
            lines.append("-" * 78)
            lines.append(f"  DEFECT LEDGER ({len(critique['defect_ledger'])} item(s)):")
            for i, defect in enumerate(critique["defect_ledger"], 1):
                lines.append(f"   [{i}] [{defect['severity']}] {defect['category']}: {defect['flaw']}")
                lines.append(f"       -> Marcus's Directive: {defect['marcus_directive']}")

        lines.append("=" * 78)
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Marcus Sterling Software Architect Standalone CLI")
    parser.add_argument("target", help="Path to code file (Python/JS/TS) to inspect and elevate")
    parser.add_argument("--benchmark", default="clean_modular_service", choices=["clean_modular_service", "enterprise_resilient_core", "modern_fast_prototype"], help="Benchmark profile")
    parser.add_argument("--elevate", action="store_true", help="Autonomously elevate code to clean architectural standards")
    parser.add_argument("--json", action="store_true", help="Output pure JSON format")

    args = parser.parse_args()

    if not os.path.exists(args.target):
        print(f"Error: Target file '{args.target}' does not exist.", file=sys.stderr)
        sys.exit(1)

    master = MarcusSterlingMaster(target_file=args.target, benchmark_name=args.benchmark)
    result = master.run_autonomous_cycle(auto_elevate=args.elevate)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(master.format_console_report(result))

    if not result.get("passed", False):
        sys.exit(2)


if __name__ == "__main__":
    main()
