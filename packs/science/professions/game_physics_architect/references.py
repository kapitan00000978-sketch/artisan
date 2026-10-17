"""
Ronan Blackwood - Game Systems & Physics Engine Reference Standards.

This module codifies empirical physics simulation standards, frame budget limits,
deterministic accumulator loop templates, and zero-allocation memory benchmarks.
"""

from typing import Dict, Any, List


FRAME_BUDGET_STANDARDS: Dict[str, Dict[str, float]] = {
    "target_60fps": {
        "total_budget_ms": 16.666,
        "max_physics_budget_ms": 4.5,
        "max_collision_budget_ms": 3.0,
        "max_gameplay_logic_ms": 3.0,
        "max_render_dispatch_ms": 6.0
    },
    "target_120fps": {
        "total_budget_ms": 8.333,
        "max_physics_budget_ms": 2.2,
        "max_collision_budget_ms": 1.5,
        "max_gameplay_logic_ms": 1.5,
        "max_render_dispatch_ms": 3.0
    }
}

SIMULATION_CONSTANTS: Dict[str, Any] = {
    "default_fixed_dt": 1.0 / 60.0,
    "high_precision_fixed_dt": 1.0 / 120.0,
    "max_accumulator_clamp_seconds": 0.25,  # Prevents spiral of death
    "broadphase_entity_threshold": 25,     # Broadphase mandatory if dynamic entities > 25
    "max_safe_restitution": 0.98,          # Restitution >= 1.0 violates energy conservation
    "recommended_pool_sizes": {
        "particles": 1000,
        "projectiles": 200,
        "audio_voices": 32
    }
}

TOXIC_GAME_ENGINE_ANTI_PATTERNS: List[Dict[str, str]] = [
    {
        "id": "variable_dt_physics",
        "indicator": "Position integrated directly using variable frame delta (pos += vel * dt) without fixed accumulator.",
        "risk": "Tunneling through obstacles, non-deterministic physics, frame-rate dependent jump trajectories.",
        "severity": "FATAL"
    },
    {
        "id": "heap_alloc_in_hot_loop",
        "indicator": "Instantiating objects (new Vector, new Particle, {}, []) inside update() or render() loops.",
        "risk": "Triggers periodic Garbage Collection spikes, leading to devastating 50-100ms micro-stutters.",
        "severity": "FATAL"
    },
    {
        "id": "brute_force_all_pairs_collision",
        "indicator": "Testing collisions with nested loops for (i=0; i<N; i++) for (j=i+1; j<N; j++) without broadphase.",
        "risk": "O(N^2) complexity causes CPU bottleneck and catastrophic frame drops as entity count scales.",
        "severity": "FATAL"
    },
    {
        "id": "missing_accumulator_clamp",
        "indicator": "Accumulating frame delta without a maximum clamp (e.g., dt > 0.25s).",
        "risk": "'Spiral of death' freeze: A slow frame generates a large delta, triggering hundreds of sub-steps that stall the CPU permanently.",
        "severity": "HIGH"
    },
    {
        "id": "unseeded_simulation_randomness",
        "indicator": "Calling unseeded Math.random() inside physics, AI, or procedural simulation updates.",
        "risk": "Multiplayer desynchronization, inability to replay physics bugs, non-deterministic state divergence.",
        "severity": "HIGH"
    },
    {
        "id": "missing_alpha_interpolation",
        "indicator": "Rendering directly at raw physics positions without interpolating between previous and current state.",
        "risk": "Visual jitter and temporal aliasing on high-refresh-rate displays (120Hz/144Hz/240Hz).",
        "severity": "MEDIUM"
    }
]

CANONICAL_FIXED_STEP_LOOP: str = (
    "// Ronan Blackwood: Deterministic Fixed Timestep Game Loop with Alpha Interpolation\n"
    "const FIXED_DT = 1.0 / 60.0;\n"
    "const MAX_FRAME_TIME = 0.25;\n"
    "let accumulator = 0.0;\n"
    "let lastTime = performance.now();\n\n"
    "function mainLoop(currentTime) {\n"
    "    let frameTime = (currentTime - lastTime) / 1000.0;\n"
    "    lastTime = currentTime;\n"
    "    if (frameTime > MAX_FRAME_TIME) frameTime = MAX_FRAME_TIME; // Clamp to avoid spiral of death\n"
    "    accumulator += frameTime;\n\n"
    "    while (accumulator >= FIXED_DT) {\n"
    "        savePreviousPhysicsState();\n"
    "        updateFixedPhysics(FIXED_DT);\n"
    "        accumulator -= FIXED_DT;\n"
    "    }\n\n"
    "    const alpha = accumulator / FIXED_DT;\n"
    "    render(alpha); // Smooth visual state interpolation\n"
    "    requestAnimationFrame(mainLoop);\n"
    "}\n"
)


class GameEngineReferenceLibrary:
    """Provides empirical game engine benchmarks and deterministic loop specifications."""

    @staticmethod
    def get_frame_budget_standards() -> Dict[str, Dict[str, float]]:
        return FRAME_BUDGET_STANDARDS

    @staticmethod
    def get_simulation_constants() -> Dict[str, Any]:
        return SIMULATION_CONSTANTS

    @staticmethod
    def get_toxic_anti_patterns() -> List[Dict[str, str]]:
        return TOXIC_GAME_ENGINE_ANTI_PATTERNS

    @staticmethod
    def get_canonical_fixed_step_loop() -> str:
        return CANONICAL_FIXED_STEP_LOOP
