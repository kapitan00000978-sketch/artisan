#!/usr/bin/env python3
"""
Master Controller: Commander Rowan 'The Fusion-Drive' Sterling
Principal Direct Fusion Rocket & Magnetoplasmadynamic Propulsion Architect
Closed-loop dual-agent reflection engine for thermonuclear star engines, magnetic nozzles, and MPD thrusters.
"""

import sys
import os
from typing import Dict, Any, Optional

# Add workspace root for journal and shared infrastructure
workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

try:
    from src.studio.active_memory import ActiveDecisionJournal
except ImportError:
    ActiveDecisionJournal = None

from .inspector import FusionRocketInspector
from .rubric import FusionRocketRubric
from .blind_critic import FusionRocketBlindCritic
from .elevation_engine import FusionRocketElevationEngine


class CommanderRowanSterling:
    """
    Principal Direct Fusion Rocket & Magnetoplasmadynamic Propulsion Architect.
    Enforces ultra-high specific impulse, magnetic nozzle Alfven Mach detachment,
    HTS magnet secondary neutron shielding, beam divergence limits, and thrust power conversion.
    """

    NAME = "Commander Rowan 'The Fusion-Drive' Sterling"
    ARCHETYPE = "Thermonuclear Exhaust Sovereign & Magnetic Nozzle Conscience"
    MOTTO = (
        "Chemical rockets are firecrackers chained to fuel tanks—90% of their mass is propellant, their exhaust velocities are capped at four kilometers per second, "
        "and human voyages across the solar system drag on for years. Direct Fusion Drive and magnetoplasmadynamic thrusters tap the nuclear binding energy of hydrogen isotopes. "
        "A fusion propulsion engine without magnetic nozzle Alfven detachment modeling, ten-thousand-second specific impulse verification, "
        "superconducting coil neutron shield thermal limits, and sub-twelve-degree beam divergence is not an interplanetary star engine—it is an explosive flying tokamak. "
        "We propel humanity to the outer planets with exhaust velocities measured in thousands of kilometers per second."
    )

    def __init__(self, min_passing_score: int = 95, max_iterations: int = 3):
        self.min_passing_score = min_passing_score
        self.max_iterations = max_iterations
        self.inspector = FusionRocketInspector()
        self.critic = FusionRocketBlindCritic()
        self.elevation_engine = FusionRocketElevationEngine()
        self.journal = ActiveDecisionJournal() if ActiveDecisionJournal else None

    def execute_closed_loop(self, source_code: str, target_file: str = "fusion_engine_core.py") -> Dict[str, Any]:
        """
        Executes autonomous dual-agent reflection loop:
        Draft -> Blind Critic Audit -> Elevation Engine -> Verification.
        """
        current_code = source_code
        total_actions = []

        for iteration in range(1, self.max_iterations + 1):
            audit = self.critic.audit(current_code)
            score_before = audit["score"]
            flaws = audit["critique_notes"]

            if audit["score"] >= self.min_passing_score:
                return {
                    "status": "CERTIFIED",
                    "iterations": iteration,
                    "final_score": audit["score"],
                    "master": self.NAME,
                    "motto": self.MOTTO,
                    "elevated_code": current_code,
                    "actions_applied": total_actions,
                    "flaws_detected": len(flaws)
                }

            # Elevation required
            elevated_code, actions = self.elevation_engine.elevate(current_code)
            total_actions.extend(actions)

            # Re-audit
            post_audit = self.critic.audit(elevated_code)
            score_after = post_audit["score"]

            if self.journal:
                self.journal.record_decision(
                    iteration,
                    target_file,
                    flaws,
                    actions,
                    score_before,
                    score_after
                )

            current_code = elevated_code

            if post_audit["score"] >= self.min_passing_score:
                return {
                    "status": "CERTIFIED",
                    "iterations": iteration,
                    "final_score": post_audit["score"],
                    "master": self.NAME,
                    "motto": self.MOTTO,
                    "elevated_code": current_code,
                    "actions_applied": total_actions,
                    "flaws_detected": len(flaws)
                }

        # Fallback if max iterations reached
        final_audit = self.critic.audit(current_code)
        return {
            "status": "PROVISIONAL" if final_audit["score"] >= 80 else "REJECTED",
            "iterations": self.max_iterations,
            "final_score": final_audit["score"],
            "master": self.NAME,
            "motto": self.MOTTO,
            "elevated_code": current_code,
            "actions_applied": total_actions,
            "flaws_detected": final_audit["flaw_count"]
        }
