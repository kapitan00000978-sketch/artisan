#!/usr/bin/env python3
"""
Master Controller: Dr. Aurelius 'The Orbital' Sterling
Principal Astrodynamics & Interplanetary Trajectory Architect
Closed-loop dual-agent reflection engine for mission-critical orbital software.
"""

import sys
import os
from typing import Dict, Any, Optional

# Add workspace root for journal and shared infrastructure
workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

try:
    from scripts.active_decision_journal import ActiveDecisionJournal
except ImportError:
    ActiveDecisionJournal = None

from .inspector import AstrodynamicsInspector
from .rubric import AstrodynamicsRubric
from .blind_critic import AstrodynamicsBlindCritic
from .elevation_engine import AstrodynamicsElevationEngine


class DrAureliusSterling:
    """
    Principal Astrodynamics & Interplanetary Trajectory Architect.
    Enforces patched conics, Tisserand parameter invariance, Jacobi constant
    stationkeeping, and solar radiation pressure compensation.
    """

    NAME = "Dr. Aurelius 'The Orbital' Sterling"
    ARCHETYPE = "Celestial Mechanics Sovereign & Trajectory Determinism Conscience"
    MOTTO = (
        "In deep space, gravity does not forgive a milligram of propellant deficit or a microradian of vector error. "
        "An interplanetary trajectory without patched conics, Tisserand parameter conservation, halo orbit "
        "stationkeeping, and solar radiation pressure compensation turns a billion-dollar probe into dead space derelict. "
        "We navigate the solar system with celestial mathematical certainty."
    )

    def __init__(self, min_passing_score: int = 95, max_iterations: int = 3):
        self.min_passing_score = min_passing_score
        self.max_iterations = max_iterations
        self.inspector = AstrodynamicsInspector()
        self.critic = AstrodynamicsBlindCritic()
        self.elevation_engine = AstrodynamicsElevationEngine()
        self.journal = ActiveDecisionJournal() if ActiveDecisionJournal else None

    def execute_closed_loop(self, source_code: str, target_file: str = "trajectory_executive.py") -> Dict[str, Any]:
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
