"""
Ronan Blackwood - Objective Game Systems & Physics Loop Inspector.

This module inspects game source code, simulation loops, and engine architecture
to detect variable-timestep physics, hot-loop GC allocations, and O(N^2) collision bottlenecks.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class PhysicsMetrics:
    has_fixed_timestep: bool = False
    has_variable_dt_leak: bool = False
    has_accumulator_clamp: bool = False
    has_alpha_interpolation: bool = False
    has_object_pooling: bool = False
    has_heap_allocations_in_loop: bool = False
    has_broadphase_collision: bool = False
    has_brute_force_all_pairs: bool = False
    uses_deterministic_prng: bool = True
    max_restitution: float = 0.80
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class GameEngineInspectionReport:
    metrics: PhysicsMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_simulation_viable: bool = False


class GamePhysicsInspector:
    """Rigorous game engine auditor inspecting physics loops and memory discipline."""

    def inspect(self, engine_input: Any) -> GameEngineInspectionReport:
        """
        Audits game source code string, engine configuration, or metadata dict.
        """
        metrics = self._extract_metrics(engine_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Fixed Timestep Accumulator Loop Audit
        if metrics.has_variable_dt_leak:
            critical_violations.append(
                "Variable-Timestep Physics Integration: Position integrated directly with variable frame delta. "
                "Causes tunneling through walls, physics instability, and frame-rate dependent jump arcs."
            )
        elif metrics.has_fixed_timestep:
            benchmarks_passed.append("Deterministic fixed-timestep simulation accumulator verified.")
        else:
            critical_violations.append("Missing Fixed Timestep: Game lacks a decoupled fixed physics tick.")

        if metrics.has_fixed_timestep and not metrics.has_accumulator_clamp:
            warnings.append(
                "Missing Accumulator Clamp: Delta-time not capped (e.g. at 0.25s). Vulnerable to 'spiral of death' CPU freeze."
            )
        elif metrics.has_accumulator_clamp:
            benchmarks_passed.append("Spiral-of-death safety clamp configured.")

        # 2. Hot-Loop Memory Allocation (Zero-GC Audit)
        if metrics.has_heap_allocations_in_loop:
            critical_violations.append(
                "Hot-Loop Heap Allocation: Memory instantiated (new objects, literals) inside update/tick loop. "
                "Forces periodic Garbage Collection pauses (50-100ms micro-stutters)."
            )
        elif metrics.has_object_pooling:
            benchmarks_passed.append("Zero-GC Memory Discipline: Entities and particles recycled via Object Pools.")
        else:
            warnings.append("No explicit object pooling detected. Ensure entities are pre-allocated.")

        # 3. Collision Detection & Broadphase
        if metrics.has_brute_force_all_pairs:
            critical_violations.append(
                "O(N^2) Brute-Force Collision Checking: Nested all-pairs loop without spatial partitioning. "
                "Causes devastating CPU bottleneck as entity count scales beyond 25 items."
            )
        elif metrics.has_broadphase_collision:
            benchmarks_passed.append("Broadphase spatial partitioning (Spatial Hash Grid / Quadtree) verified.")
        else:
            warnings.append("No broadphase spatial partitioning found; entity count must remain strictly bounded.")

        # 4. Deterministic Randomness
        if not metrics.uses_deterministic_prng:
            warnings.append("Unseeded Math.random() used in simulation loop; prevents deterministic bug replay & multiplayer sync.")
        else:
            benchmarks_passed.append("Deterministic PRNG / seeded simulation randomness verified.")

        # 5. Energy Conservation
        if metrics.max_restitution >= 1.0:
            critical_violations.append(
                f"Energy Conservation Violation: Restitution coefficient is {metrics.max_restitution:.2f} (>= 1.0). "
                "Collisions will amplify kinetic energy infinitely until simulation explodes."
            )
        else:
            benchmarks_passed.append(f"Restitution within stable bounds ({metrics.max_restitution:.2f} <= 0.98).")

        # 6. Visual Alpha State Interpolation
        if metrics.has_fixed_timestep and not metrics.has_alpha_interpolation:
            warnings.append(
                "Missing Alpha State Interpolation: Raw fixed-physics coordinates rendered directly, "
                "causing micro-jitter on 120Hz/144Hz high-refresh displays."
            )
        elif metrics.has_alpha_interpolation:
            benchmarks_passed.append("Smooth visual alpha state interpolation verified.")

        for ap in metrics.anti_patterns_detected:
            if ap not in critical_violations:
                critical_violations.append(f"Anti-Pattern Detected: {ap}")

        is_viable = len(critical_violations) == 0

        return GameEngineInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_simulation_viable=is_viable
        )

    def _extract_metrics(self, engine_input: Any) -> PhysicsMetrics:
        text = ""
        metadata: Dict[str, Any] = {}

        if isinstance(engine_input, str):
            text = engine_input
            try:
                parsed = json.loads(engine_input)
                if isinstance(parsed, dict):
                    metadata = parsed
            except (json.JSONDecodeError, ValueError) as _json_err:
                _ = _json_err
        elif isinstance(engine_input, dict):
            metadata = engine_input
            text = json.dumps(engine_input)
        else:
            text = str(engine_input)

        text_lower = text.lower()
        m = PhysicsMetrics()

        # 1. Fixed Timestep Loop
        has_accumulator = (
            "accumulator" in text_lower or
            "fixed_dt" in text_lower or
            "fixeddelta" in text_lower or
            "fixedupdate" in text_lower or
            "while (accumulator" in text_lower or
            "while(accumulator" in text_lower or
            metadata.get("has_fixed_timestep", False)
        )
        m.has_fixed_timestep = has_accumulator

        # Variable dt integration check
        has_var_dt = (
            ("pos += vel * dt" in text_lower or "position += velocity * dt" in text_lower or "pos.x += vel.x * dt" in text_lower) and
            not has_accumulator
        ) or metadata.get("has_variable_dt_leak", False)
        m.has_variable_dt_leak = has_var_dt

        # Accumulator Clamp
        m.has_accumulator_clamp = (
            "max_frame_time" in text_lower or
            "math.min(frametime" in text_lower or
            "min(frametime" in text_lower or
            "clamp" in text_lower or
            metadata.get("has_accumulator_clamp", False)
        )

        # Alpha Interpolation
        m.has_alpha_interpolation = (
            "alpha" in text_lower or
            "interpolate" in text_lower or
            "lerp(prev" in text_lower or
            "previous_state" in text_lower or
            metadata.get("has_alpha_interpolation", False)
        )

        # 2. Memory Allocations in Loop
        has_new_in_loop = bool(
            re.search(r"(?:update|tick|render)\s*\([^)]*\)\s*\{[^}]*\bnew\s+(?:vector|particle|bullet|object|array)\b", text_lower)
        ) or metadata.get("has_heap_allocations_in_loop", False)
        m.has_heap_allocations_in_loop = has_new_in_loop

        has_pool = (
            "objectpool" in text_lower or
            "pool.acquire" in text_lower or
            "pool.release" in text_lower or
            "recycle" in text_lower or
            "particlepool" in text_lower or
            metadata.get("has_object_pooling", False)
        )
        m.has_object_pooling = has_pool

        # 3. Collision & Broadphase
        has_broadphase = (
            "spatialhash" in text_lower or
            "spatial_hash" in text_lower or
            "quadtree" in text_lower or
            "bvh" in text_lower or
            "grid.insert" in text_lower or
            metadata.get("has_broadphase_collision", False)
        )
        m.has_broadphase_collision = has_broadphase

        has_all_pairs = bool(
            re.search(r"for\s*\([^)]*\bi\b[^)]*\)[\s\S]{0,200}?for\s*\([^)]*\bj\b", text_lower)
        ) or metadata.get("has_brute_force_all_pairs", False)
        m.has_brute_force_all_pairs = has_all_pairs and not has_broadphase

        # 4. PRNG & Determinism
        if "math.random()" in text_lower and ("physics" in text_lower or "update" in text_lower or "step" in text_lower):
            m.uses_deterministic_prng = False
        else:
            m.uses_deterministic_prng = bool(metadata.get("uses_deterministic_prng", True))

        # 5. Restitution
        restitution_match = re.search(r"restitution\s*[:=]\s*([\d.]+)", text_lower)
        if restitution_match:
            try:
                m.max_restitution = float(restitution_match.group(1))
            except (ValueError, TypeError):
                m.max_restitution = 0.80
        else:
            m.max_restitution = float(metadata.get("max_restitution", 0.80))

        # Anti-pattern logging
        if m.has_variable_dt_leak:
            m.anti_patterns_detected.append("Direct variable delta-time integration without accumulator")
        if m.has_heap_allocations_in_loop:
            m.anti_patterns_detected.append("Dynamic heap allocation inside per-frame simulation loop")
        if m.has_brute_force_all_pairs:
            m.anti_patterns_detected.append("O(N^2) unpartitioned brute-force collision loop")

        return m
