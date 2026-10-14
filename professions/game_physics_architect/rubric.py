"""
Ronan Blackwood - 100-Point Game Systems & Physics Engine Rubric.

Evaluates game loops, physics integration, and memory discipline against AAA engine standards.
Passing threshold: 85/100 points.
Veto criteria: Variable delta-time physics, hot-loop GC allocations, or energy amplification (restitution >= 1.0).
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.game_physics_architect.inspector import GameEngineInspectionReport, PhysicsMetrics


@dataclass
class GameEngineRubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class GamePhysicsRubric:
    """Rigorous 100-point weighted evaluation rubric for game systems and physics engines."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: GameEngineInspectionReport) -> GameEngineRubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Deterministic Simulation Loop (25 pts)
        # ----------------------------------------------------
        p1_score = 0
        if m.has_variable_dt_leak:
            veto_reasons.append("Variable delta-time integration detected: Physics simulation depends on variable render frame rate.")
            recommendations.append("Decouple physics into fixed-timestep accumulator loop: while (accumulator >= FIXED_DT).")
        elif m.has_fixed_timestep:
            p1_score += 15
        else:
            veto_reasons.append("Missing fixed timestep accumulator: Simulation lacks deterministic time stepping.")
            recommendations.append("Implement canonical fixed-timestep accumulator game loop.")

        if m.has_accumulator_clamp:
            p1_score += 5
        else:
            recommendations.append("Clamp frame time delta (e.g. max 0.25s) to prevent 'spiral of death' CPU freeze.")

        if m.has_fixed_timestep and not m.has_variable_dt_leak:
            p1_score += 5

        pillar_scores["deterministic_simulation_loop"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Memory & Zero-GC Discipline (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if m.has_heap_allocations_in_loop:
            veto_reasons.append("Hot-Loop Garbage Collection hazard: Dynamic objects instantiated inside update() or render().")
            recommendations.append("Pre-allocate vectors, particles, and temporary structs; mutate in-place.")
        else:
            p2_score += 15

        if m.has_object_pooling:
            p2_score += 10
        else:
            p2_score += 3
            recommendations.append("Implement pre-allocated Object Pool for dynamic entities (projectiles, particles, VFX).")

        pillar_scores["memory_and_zero_gc"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: Collision Detection & Broadphase (20 pts)
        # ----------------------------------------------------
        p3_score = 0
        if m.has_brute_force_all_pairs:
            veto_reasons.append("O(N^2) unpartitioned all-pairs collision loop causes severe CPU choking.")
            recommendations.append("Implement Spatial Hash Grid or Quadtree broadphase pruning.")
        elif m.has_broadphase_collision:
            p3_score += 15
        else:
            p3_score += 6
            recommendations.append("Add spatial hash grid to keep collision checks sub-millisecond.")

        p3_score += 5  # Narrowphase solver credit

        pillar_scores["collision_and_broadphase"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: Numerical Stability & Energy Conservation (15 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.max_restitution >= 1.0:
            veto_reasons.append(f"Restitution {m.max_restitution:.2f} >= 1.0 violates conservation of energy (infinite explosion).")
            recommendations.append("Clamp coefficient of restitution to <= 0.98 to guarantee numerical stability.")
        else:
            p4_score += 10

        p4_score += 5  # Symplectic integration credit

        pillar_scores["numerical_stability_and_energy"] = p4_score

        # ----------------------------------------------------
        # Pillar 5: State Interpolation & Visual Fluidity (15 pts)
        # ----------------------------------------------------
        p5_score = 0
        if m.has_alpha_interpolation:
            p5_score += 10
        else:
            p5_score += 3
            recommendations.append("Interpolate between previous and current physics state with alpha ratio for 120Hz/144Hz monitors.")

        if m.uses_deterministic_prng:
            p5_score += 5
        else:
            recommendations.append("Replace unseeded Math.random() with deterministic XorShift32 / LCG for reproducible state.")

        pillar_scores["state_interpolation_and_fluidity"] = p5_score

        total_score = sum(pillar_scores.values())

        # Veto enforcement
        veto_triggered = len(veto_reasons) > 0
        if veto_triggered and total_score >= self.PASSING_THRESHOLD:
            total_score = 71

        is_certified = (total_score >= self.PASSING_THRESHOLD) and not veto_triggered

        return GameEngineRubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
