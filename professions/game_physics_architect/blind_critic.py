"""
Ronan Blackwood - Blind Game Systems & Physics Critic.

Evaluates game loops, physics integration, and memory discipline strictly
against deterministic simulation and zero-GC frame budget standards.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.game_physics_architect.inspector import GamePhysicsInspector, GameEngineInspectionReport
from professions.game_physics_architect.rubric import GamePhysicsRubric, GameEngineRubricEvaluation


@dataclass
class PhysicsDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    engine_impact: str
    actionable_fix: str


@dataclass
class GameEngineDefectLedger:
    verdict: str  # CERTIFIED_ENGINE_CANON or REJECTED_FRAME_DROP_HAZARD
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[PhysicsDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindGamePhysicsCritic:
    """Simulation adversary reviewing game engines strictly for frame pacing and mathematical determinism."""

    def __init__(self):
        self.inspector = GamePhysicsInspector()
        self.rubric = GamePhysicsRubric()

    def review(self, engine_input: Any) -> GameEngineDefectLedger:
        """
        Runs objective inspection and adversarial rubric scoring, producing an Engine Defect Ledger.
        """
        report: GameEngineInspectionReport = self.inspector.inspect(engine_input)
        eval_result: GameEngineRubricEvaluation = self.rubric.evaluate(report)

        defects: List[PhysicsDefect] = []

        # 1. Critical violations -> FATAL defects
        for i, violation in enumerate(report.critical_violations, start=1):
            if "variable-timestep" in violation.lower():
                title = "Variable-Timestep Physics Integration"
                impact = "Tunneling through solid colliders, frame-rate dependent jump physics, non-deterministic bugs."
                fix = "Decouple physics into fixed accumulator loop: while (accumulator >= FIXED_DT)."
            elif "hot-loop" in violation.lower() or "heap allocation" in violation.lower():
                title = "Per-Frame Heap Allocation (GC Stall Hazard)"
                impact = "Triggers periodic browser/runtime Garbage Collection spikes of 50-100ms, breaking 60fps."
                fix = "Pre-allocate all entities, temporary vectors, and particle instances inside an Object Pool."
            elif "o(n^2)" in violation.lower() or "all-pairs" in violation.lower():
                title = "O(N^2) All-Pairs Collision Bottleneck"
                impact = "CPU execution time explodes quadratically as entities scale; catastrophic FPS drops."
                fix = "Implement Spatial Hash Grid or Quadtree broadphase spatial partitioning."
            elif "energy conservation" in violation.lower():
                title = "Restitution Energy Amplification"
                impact = "Over-unity restitution (>= 1.0) creates compounding velocity instability; simulation explodes."
                fix = "Clamp restitution coefficient to <= 0.98."
            else:
                title = "Critical Simulation Architecture Flaw"
                impact = "Breaks deterministic physics simulation or violates 16.6ms frame budget."
                fix = "Re-architect game loop according to Ronan Blackwood benchmarks."

            defects.append(
                PhysicsDefect(
                    defect_id=f"ENGINE-FATAL-{i:03d}",
                    severity="FATAL",
                    title=title,
                    description=violation,
                    engine_impact=impact,
                    actionable_fix=fix
                )
            )

        # 2. Veto reasons
        for j, reason in enumerate(eval_result.veto_reasons, start=len(defects) + 1):
            if not any(d.description == reason for d in defects):
                defects.append(
                    PhysicsDefect(
                        defect_id=f"ENGINE-FATAL-{j:03d}",
                        severity="FATAL",
                        title="Simulation Veto Criterion",
                        description=reason,
                        engine_impact="Disqualifying game engine performance defect.",
                        actionable_fix="Refactor game loop and memory architecture."
                    )
                )

        # 3. Warnings -> HIGH / MEDIUM defects
        for k, warning in enumerate(report.warnings, start=len(defects) + 1):
            sev = "HIGH" if "spiral" in warning.lower() or "random" in warning.lower() else "MEDIUM"
            defects.append(
                PhysicsDefect(
                    defect_id=f"ENGINE-WARN-{k:03d}",
                    severity=sev,
                    title="Engine Fluidity Warning",
                    description=warning,
                    engine_impact="Visual micro-jitter or vulnerability to CPU freeze under heavy load.",
                    actionable_fix="Clamp frame delta and apply visual alpha state interpolation."
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = "CERTIFIED_ENGINE_CANON" if eval_result.is_certified else "REJECTED_FRAME_DROP_HAZARD"

        if eval_result.is_certified:
            summary = (
                f"ENGINE CERTIFIED (Score: {eval_result.total_score}/100). "
                "Fixed timestep accumulator verified, zero-GC memory pooling active, "
                "spatial partitioning operational, and alpha visual interpolation configured. Solid 60/120 FPS guaranteed."
            )
        else:
            summary = (
                f"REJECTED BY THE ENGINE ARCHITECT (Score: {eval_result.total_score}/100, Threshold: {eval_result.passing_threshold}). "
                f"Detected {fatal_count} fatal frame-stutter flaws and {high_count} simulation vulnerabilities. "
                "The game loop will stutter, drop frames under load, or tunnel through collision geometry."
            )

        return GameEngineDefectLedger(
            verdict=verdict,
            score=eval_result.total_score,
            passing_threshold=eval_result.passing_threshold,
            is_certified=eval_result.is_certified,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
