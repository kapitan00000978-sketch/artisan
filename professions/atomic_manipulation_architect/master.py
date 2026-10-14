#!/usr/bin/env python3
"""
Master Controller: Dr. Valentina 'The Sub-Atomic' Sterling
Principal Scanning Probe Microscopy & Atomic Manipulation Architect
Closed-loop dual-agent reflection engine for atomic-scale nanotechnology and quantum manipulation.
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

from .inspector import AtomicManipulationInspector
from .rubric import AtomicManipulationRubric
from .blind_critic import AtomicManipulationBlindCritic
from .elevation_engine import AtomicManipulationElevationEngine


class DrValentinaSterling:
    """
    Principal Scanning Probe Microscopy & Atomic Manipulation Architect.
    Enforces exponential quantum tunneling barrier calibration, qPlus tuning fork mechanics,
    piezoelectric hysteresis/creep suppression, cryogenic thermal drift stability,
    and single-atom placement accuracy.
    """

    NAME = "Dr. Valentina 'The Sub-Atomic' Sterling"
    ARCHETYPE = "Sub-Atomic Sovereign & Quantum Manipulation Conscience"
    MOTTO = (
        "At the atomic scale, matter ceases to be a continuous bulk—it resolves into individual atomic cores surrounded by clouds of electron probability. "
        "A scanning tunneling microscope without ultra-high vacuum chamber pressure, sub-Kelvin vibrational isolation, "
        "qPlus tuning fork force sensors, closed-loop capacitive drift compensation, and picometer tip trajectory control "
        "is not an instrument of nanotechnology—it is a blind needle plowing through atomic lattices. "
        "We manipulate individual atoms one by one with quantum mechanical precision."
    )

    def __init__(self, min_passing_score: int = 95, max_iterations: int = 3):
        self.min_passing_score = min_passing_score
        self.max_iterations = max_iterations
        self.inspector = AtomicManipulationInspector()
        self.critic = AtomicManipulationBlindCritic()
        self.elevation_engine = AtomicManipulationElevationEngine()
        self.journal = ActiveDecisionJournal() if ActiveDecisionJournal else None

    def execute_closed_loop(self, source_code: str, target_file: str = "atomic_manipulation_core.py") -> Dict[str, Any]:
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
