#!/usr/bin/env python3
"""
Master Controller: Commander Zachary 'The Sub-Zero' Sterling
Principal Cryogenic Superconducting & Dilution Refrigerator Systems Architect
Closed-loop dual-agent reflection engine for millikelvin quantum hardware.
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

from .inspector import CryogenicInspector
from .rubric import CryogenicRubric
from .blind_critic import CryogenicBlindCritic
from .elevation_engine import CryogenicElevationEngine


class CommanderZacharySterling:
    """
    Principal Cryogenic Superconducting & Dilution Refrigerator Systems Architect.
    Enforces dilution cooling power thermodynamics, Kapitza boundary resistance modeling,
    superconducting critical current safety envelopes, and sub-10 millikelvin base stability.
    """

    NAME = "Commander Zachary 'The Sub-Zero' Sterling"
    ARCHETYPE = "Millikelvin Sovereign & Thermal Boundary Conscience"
    MOTTO = (
        "Heat is the mortal enemy of quantum states and superconducting currents. "
        "At room temperature, thermal phonon vibrations destroy macroscopic quantum superposition. "
        "But a dilution refrigerator or superconducting cryostat without Kapitza thermal boundary resistance modeling, "
        "3He/4He phase separation cooling power calculations, active pulse-tube vibration damping, and "
        "sub-10 millikelvin temperature stability is a thermal breakdown waiting to happen. "
        "We preserve absolute zero with thermodynamic rigor."
    )

    def __init__(self, min_passing_score: int = 95, max_iterations: int = 3):
        self.min_passing_score = min_passing_score
        self.max_iterations = max_iterations
        self.inspector = CryogenicInspector()
        self.critic = CryogenicBlindCritic()
        self.elevation_engine = CryogenicElevationEngine()
        self.journal = ActiveDecisionJournal() if ActiveDecisionJournal else None

    def execute_closed_loop(self, source_code: str, target_file: str = "dilution_cryostat.py") -> Dict[str, Any]:
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
