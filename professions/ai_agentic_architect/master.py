"""
🧠 NAOMI 'THE NEURAL' CHEN — PRINCIPAL AI AGENTIC SYSTEMS & LLM ARCHITECT
Autonomous cognitive conscience, agent state machine inspection, blind execution critique,
and deterministic schema-enforced agent elevation engine.

Usage:
    python professions/ai_agentic_architect/master.py <agent_file> [--elevate]
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
    from .references import AgenticReferenceLibrary
    from .inspector import AgenticSystemInspector, AgenticInspectionReport
    from .rubric import AgenticArchitectureRubric, AgenticRubricEvaluation
    from .blind_critic import BlindAgenticCritic, AgenticDefectLedger
    from .elevation_engine import AgenticElevationEngine
except ImportError:
    from references import AgenticReferenceLibrary
    from inspector import AgenticSystemInspector, AgenticInspectionReport
    from rubric import AgenticArchitectureRubric, AgenticRubricEvaluation
    from blind_critic import BlindAgenticCritic, AgenticDefectLedger
    from elevation_engine import AgenticElevationEngine

# Import global ActiveDecisionJournal from studio engine
try:
    from src.studio.active_memory import ActiveDecisionJournal
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.studio.active_memory import ActiveDecisionJournal


class NaomiChenMaster:
    """
    Naomi Chen: The living AI agentic systems sovereign, state machine inquisitor,
    and cognitive conscience. Eliminates runaway while loops, enforces prompt injection shields,
    and mandates deterministic structured schema returns.
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
        self.inspector = AgenticSystemInspector()
        self.rubric = AgenticArchitectureRubric()
        self.critic = BlindAgenticCritic()
        self.elevation_engine = AgenticElevationEngine()
        self.journal = ActiveDecisionJournal()

    def run_autonomous_cycle(self, input_data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes the closed-loop autonomous AI agent audit & elevation lifecycle.
        1. Inspect -> 2. Rubric -> 3. Critic -> 4. Elevate (if < 85) -> 5. Certify & Journal
        """
        data = input_data
        if data is None and self.target_path:
            if os.path.exists(self.target_path):
                with open(self.target_path, "r", encoding="utf-8") as f:
                    data = f.read()
            else:
                raise FileNotFoundError(f"Agent target file not found: {self.target_path}")

        if data is None:
            # Baseline prototype flawed agent loop for testing or demo
            data = (
                "# Flawed Agent Loop\n"
                "def run_agent(user_input: str):\n"
                "    prompt = f'System: You are an agent. Solve: {user_input}'\n"
                "    while True:\n"
                "        response = llm(prompt)\n"
                "        if 'DONE' in response:\n"
                "            break\n"
            )

        # Step 1: Initial Blind Critic Review
        ledger: AgenticDefectLedger = self.critic.review(data)
        initial_score = ledger.score
        elevated_result: Optional[Dict[str, Any]] = None

        # Step 2: Elevate if failed
        current_data = data
        if not ledger.is_certified:
            elevated_result = self.elevation_engine.elevate(current_data, max_iterations=self.max_cycles)
            current_data = elevated_result["elevated_agent"]
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
            "elevated_agent": current_data,
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
                target_file=self.target_path if self.target_path else "agent_workflow.py",
                defects_before=[f"Fatal defects: {fatal_defects}"],
                actions_taken=["naomi_agentic_deterministic_elevation"],
                score_before=float(initial_score),
                score_after=float(final_score)
            )
        except Exception as _journal_err:
            sys.stderr.write(f"Note: Decision journal record skipped: {_journal_err}\n")

    def _generate_briefing(self, agent_data: Any, ledger: AgenticDefectLedger) -> str:
        report = self.inspector.inspect(agent_data)
        m = report.metrics

        status_icon = "🧠 [DETERMINISTIC AGENT CERTIFIED]" if ledger.is_certified else "⚠️ [REJECTED STOCHASTIC CHAOS]"

        briefing = [
            f"# {status_icon} EXECUTIVE AI AGENTIC ARCHITECTURE BRIEFING",
            f"**Auditor:** Naomi 'The Neural' Chen (Principal AI Agentic Systems & LLM Architect)",
            f"**Final Score:** {ledger.score}/100 (Threshold: {ledger.passing_threshold})",
            f"**Verdict:** {ledger.verdict}",
            "",
            "## 1. Agent Health & Safety Metrics",
            f"- **Circuit Breaker Ceiling:** {'PASS (max_iterations bounded)' if m.has_max_iteration_circuit_breaker else 'FAIL (Unbounded Loop)'}",
            f"- **Prompt Injection Shield:** {'PASS (Delimiters Enforced)' if m.has_prompt_injection_delimiter else 'FAIL (Raw Concatenation)'}",
            f"- **Structured Schema Enforcement:** {'PASS (Deterministic Schema)' if m.has_structured_output_schema else 'FAIL (Unstructured String Parsing)'}",
            f"- **Tool Execution Sandbox:** {'PASS (Validated Whitelist)' if m.has_tool_execution_sandbox else 'WARN (Unchecked Execution)'}",
            "",
            "## 2. Defects Ledger & Architectural Interventions",
        ]

        if ledger.defects:
            for d in ledger.defects:
                briefing.append(f"### [{d.severity}] {d.title} ({d.defect_id})")
                briefing.append(f"- **Description:** {d.description}")
                briefing.append(f"- **Agentic Impact:** {d.agentic_impact}")
                briefing.append(f"- **Actionable Fix:** {d.actionable_fix}")
                briefing.append("")
        else:
            briefing.append("Zero runaway loop or prompt injection defects detected. Mathematical agentic determinism achieved.")

        return "\n".join(briefing)


def main():
    parser = argparse.ArgumentParser(
        description="Naomi Chen: Autonomous AI Agentic Systems & LLM Architecture Master"
    )
    parser.add_argument("target", nargs="?", help="Path to AI agent Python/TS code or prompt configuration")
    parser.add_argument("--elevate", action="store_true", help="Automatically elevate flawed agent workflows")
    parser.add_argument("--threshold", type=int, default=85, help="Passing score threshold (default: 85)")
    args = parser.parse_args()

    master = NaomiChenMaster(target_path=args.target, passing_threshold=args.threshold)
    results = master.run_autonomous_cycle()

    print(results["executive_briefing"])

    if args.elevate and "elevated_agent" in results:
        print("\n--- ELEVATED DETERMINISTIC AGENT ---")
        print(results["elevated_agent"])

    sys.exit(0 if results["is_certified"] else 1)


if __name__ == "__main__":
    main()
