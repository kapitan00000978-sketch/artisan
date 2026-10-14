"""
🎮 RONAN BLACKWOOD — LEAD GAME SYSTEMS & PHYSICS ARCHITECT
Autonomous game loop conscience, zero-GC memory inspection, blind outcome critique,
and automated deterministic physics engine elevation.

Usage:
    python professions/game_physics_architect/master.py <engine_file> [--elevate]
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
    from .references import GameEngineReferenceLibrary
    from .inspector import GamePhysicsInspector, GameEngineInspectionReport
    from .rubric import GamePhysicsRubric, GameEngineRubricEvaluation
    from .blind_critic import BlindGamePhysicsCritic, GameEngineDefectLedger
    from .elevation_engine import GamePhysicsElevationEngine
except ImportError:
    from references import GameEngineReferenceLibrary
    from inspector import GamePhysicsInspector, GameEngineInspectionReport
    from rubric import GamePhysicsRubric, GameEngineRubricEvaluation
    from blind_critic import BlindGamePhysicsCritic, GameEngineDefectLedger
    from elevation_engine import GamePhysicsElevationEngine

# Import global ActiveDecisionJournal from studio engine
try:
    from src.studio.active_memory import ActiveDecisionJournal
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.studio.active_memory import ActiveDecisionJournal


class RonanBlackwoodMaster:
    """
    Ronan Blackwood: The living game systems architect, physics engine conscience,
    and determinism purist. Rejects variable-dt physics, eliminates GC stutters,
    and enforces rock-solid 60/120 FPS frame pacing.
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
        self.inspector = GamePhysicsInspector()
        self.rubric = GamePhysicsRubric()
        self.critic = BlindGamePhysicsCritic()
        self.elevation_engine = GamePhysicsElevationEngine()
        self.journal = ActiveDecisionJournal()

    def run_autonomous_cycle(self, input_data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes the closed-loop autonomous game engine audit & elevation lifecycle.
        1. Inspect -> 2. Rubric -> 3. Critic -> 4. Elevate (if < 85) -> 5. Certify & Journal
        """
        data = input_data
        if data is None and self.target_path:
            if os.path.exists(self.target_path):
                with open(self.target_path, "r", encoding="utf-8") as f:
                    data = f.read()
            else:
                raise FileNotFoundError(f"Game engine target file not found: {self.target_path}")

        if data is None:
            # Prototype baseline game loop for testing or demo
            data = (
                "// Flawed Game Loop Prototype\n"
                "function update(dt) {\n"
                "    pos += vel * dt;\n"
                "    const p = new Particle();\n"
                "    for (let i = 0; i < entities.length; i++) {\n"
                "        for (let j = i + 1; j < entities.length; j++) {\n"
                "            checkCollision(entities[i], entities[j]);\n"
                "        }\n"
                "    }\n"
                "}\n"
            )

        # Step 1: Initial Blind Critic Review
        ledger: GameEngineDefectLedger = self.critic.review(data)
        initial_score = ledger.score
        elevated_result: Optional[Dict[str, Any]] = None

        # Step 2: Elevate if failed
        current_data = data
        if not ledger.is_certified:
            elevated_result = self.elevation_engine.elevate(current_data, max_iterations=self.max_cycles)
            current_data = elevated_result["elevated_engine"]
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
            "elevated_engine": current_data,
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
                target_file=self.target_path if self.target_path else "game_loop.js",
                defects_before=[f"Fatal defects: {fatal_defects}"],
                actions_taken=["ronan_deterministic_physics_elevation"],
                score_before=float(initial_score),
                score_after=float(final_score)
            )
        except Exception as _journal_err:
            sys.stderr.write(f"Note: Decision journal record skipped: {_journal_err}\n")

    def _generate_briefing(self, engine_data: Any, ledger: GameEngineDefectLedger) -> str:
        report = self.inspector.inspect(engine_data)
        m = report.metrics

        status_icon = "🎮 [ENGINE CERTIFIED]" if ledger.is_certified else "⚠️ [REJECTED FRAME DROP HAZARD]"

        briefing = [
            f"# {status_icon} EXECUTIVE GAME SYSTEMS & PHYSICS BRIEFING",
            f"**Auditor:** Ronan 'The Engine' Blackwood (Lead Game Systems & Physics Architect)",
            f"**Final Score:** {ledger.score}/100 (Threshold: {ledger.passing_threshold})",
            f"**Verdict:** {ledger.verdict}",
            "",
            "## ⏱️ I. Frame Budget & Simulation Rigor Matrix",
            f"- **Simulation Timestep:** {'DETERMINISTIC FIXED ACCUMULATOR' if m.has_fixed_timestep and not m.has_variable_dt_leak else 'VARIABLE DT (HAZARD - TUNNELING)'}",
            f"- **Spiral-of-Death Safety:** {'CLAMP CONFIGURED (<= 0.25s)' if m.has_accumulator_clamp else 'UNPROTECTED'}",
            f"- **Hot-Loop Memory Management:** {'ZERO-GC OBJECT POOLING' if m.has_object_pooling and not m.has_heap_allocations_in_loop else 'HEAP ALLOCATIONS DETECTED (GC STALL RISK)'}",
            f"- **Collision Broadphase:** {'SPATIAL PARTITIONING ACTIVE' if m.has_broadphase_collision else 'O(N^2) ALL-PAIRS BOTTLENECK'}",
            f"- **Energy Conservation (Restitution):** {f'STABLE ({m.max_restitution:.2f})' if m.max_restitution < 1.0 else 'VIOLATED (>= 1.0 EXPLOSION)'}",
            f"- **Visual State Interpolation:** {'ALPHA BLENDING ENABLED' if m.has_alpha_interpolation else 'RAW TICKS (HIGH-HZ JITTER)'}",
            "",
            "## 🛑 II. Defect & Remediation Ledger",
        ]

        if not ledger.defects:
            briefing.append("✅ Zero simulation defects identified. Game loop satisfies AAA 60/120 FPS performance standards.")
        else:
            for d in ledger.defects:
                briefing.append(f"- **[{d.severity}] {d.title}:** {d.description}")
                briefing.append(f"  *Engine Impact:* {d.engine_impact}")
                briefing.append(f"  *Actionable Fix:* {d.actionable_fix}")

        briefing.extend([
            "",
            "## 🎮 III. Ronan Blackwood's Simulation Directive",
            ledger.critic_verdict_summary,
            ""
        ])

        return "\n".join(briefing)


def main():
    parser = argparse.ArgumentParser(
        description="Ronan Blackwood: Lead Game Systems & Physics Standalone Auditor"
    )
    parser.add_argument("target", nargs="?", default=None, help="Path to game source or loop script")
    parser.add_argument("--elevate", action="store_true", help="Automatically elevate flawed game loops")
    parser.add_argument("--threshold", type=int, default=85, help="Minimum passing score")

    args = parser.parse_args()

    master = RonanBlackwoodMaster(target_path=args.target, passing_threshold=args.threshold)
    result = master.run_autonomous_cycle()

    print(result["executive_briefing"])

    if not result["is_certified"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
