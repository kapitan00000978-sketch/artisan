#!/usr/bin/env python3
"""
Master Controller: Dr. Gideon 'The Refraction' Sterling
Principal Optical Metamaterials & Transformation Optics Architect
Closed-loop dual-agent reflection engine for negative-index media, superlenses, and transformation optics.
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

from .inspector import OpticalMetamaterialInspector
from .rubric import OpticalMetamaterialRubric
from .blind_critic import OpticalMetamaterialBlindCritic
from .elevation_engine import OpticalMetamaterialElevationEngine


class DrGideonSterling:
    """
    Principal Optical Metamaterials & Transformation Optics Architect.
    Enforces negative-index double-negative electrodynamics, Veselago superlens evanescent wave amplification,
    Pendry transformation cloaking tensors, split-ring resonator coupling, and optical figure of merit (FOM).
    """

    NAME = "Dr. Gideon 'The Refraction' Sterling"
    ARCHETYPE = "Negative-Index Sovereign & Transformation Optics Conscience"
    MOTTO = (
        "In natural materials, atoms constrain electromagnetism to positive permittivity and permeability—light refracts forward, "
        "lenses obey the Abbe diffraction limit, and objects cast unavoidable shadows. "
        "In artificially structured metamaterials, sub-wavelength split-ring resonators and hyperbolic nanolaminates rewrite Maxwell's equations. "
        "Refraction turns backward with a negative index, evanescent waves amplify to resolve sub-nanometer features, "
        "and transformation optics bends light around objects like water around a smooth stone. "
        "We sculpt the refractive metric of space-time itself."
    )

    def __init__(self, min_passing_score: int = 95, max_iterations: int = 3):
        self.min_passing_score = min_passing_score
        self.max_iterations = max_iterations
        self.inspector = OpticalMetamaterialInspector()
        self.critic = OpticalMetamaterialBlindCritic()
        self.elevation_engine = OpticalMetamaterialElevationEngine()
        self.journal = ActiveDecisionJournal() if ActiveDecisionJournal else None

    def execute_closed_loop(self, source_code: str, target_file: str = "metamaterial_core.py") -> Dict[str, Any]:
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
