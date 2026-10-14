#!/usr/bin/env python3
"""
Master Controller: Dr. Helena 'The Synapse' Vance
Principal Neural Interface & Biomechatronic BCI Architect
Closed-loop dual-agent reflection engine for intracortical implants, neurostimulation, and BCI decoders.
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

from .inspector import NeuralInterfaceInspector
from .rubric import NeuralInterfaceRubric
from .blind_critic import NeuralInterfaceBlindCritic
from .elevation_engine import NeuralInterfaceElevationEngine


class DrHelenaVance:
    """
    Principal Neural Interface & Biomechatronic BCI Architect.
    Enforces Shannon charge injection safety bounds, Pennes tissue thermal limits,
    active biphasic charge balancing, sub-10ms closed-loop decoding latency,
    and microelectrode interface impedance integrity.
    """

    NAME = "Dr. Helena 'The Synapse' Vance"
    ARCHETYPE = "Neuro-Electrochemical Sovereign & Biomechatronic Conscience"
    MOTTO = (
        "The human brain is a non-linear electrochemical network composed of eighty-six billion neurons firing microvolt action potentials through fragile biological tissue. "
        "A neural implant without Shannon charge injection safety bounds, active biphasic charge balancing, "
        "sub-Kelvin tissue heating dissipation modeling, real-time spike sorting latency guarantees, "
        "and foreign body glial encapsulation impedance monitoring is not an interface of medicine—it is an invasive electro-toxic hazard. "
        "We bridge human consciousness and silicon biomechatronics with picocoulomb precision and zero neurological trauma."
    )

    def __init__(self, min_passing_score: int = 95, max_iterations: int = 3):
        self.min_passing_score = min_passing_score
        self.max_iterations = max_iterations
        self.inspector = NeuralInterfaceInspector()
        self.critic = NeuralInterfaceBlindCritic()
        self.elevation_engine = NeuralInterfaceElevationEngine()
        self.journal = ActiveDecisionJournal() if ActiveDecisionJournal else None

    def execute_closed_loop(self, source_code: str, target_file: str = "neural_bci_core.py") -> Dict[str, Any]:
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
