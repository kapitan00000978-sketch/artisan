"""Evaluation Rubric for Nuclear Reactor Physics & Criticality Safety.

Author: Dr. Magnus 'The Core' Sterling
Status: Production 100-Point Weighted Rubric with Veto Accumulation
"""

from typing import Any, Dict, List, Tuple


class NuclearCriticalityRubric:
    """100-point weighted evaluation rubric for reactor kinetics and criticality safety."""

    PASSING_THRESHOLD: int = 85

    @classmethod
    def evaluate(cls, metrics: Dict[str, Any]) -> Tuple[int, Dict[str, int], bool, str]:
        """Evaluate code metrics against nuclear safety and criticality benchmarks.

        Returns:
            Tuple[int, Dict[str, int], bool, str]: (total_score, breakdown, passed, veto_reason)
        """
        breakdown: Dict[str, int] = {
            "neutron_kinetics_delayed": 0,
            "criticality_margin_dollars": 0,
            "passive_doppler_feedback": 0,
            "thermal_dnbr_safety": 0,
            "scram_stuck_rod_redundancy": 0,
        }
        veto_reasons: List[str] = []

        # Global Syntax Veto
        if not metrics.get("ast_valid", False):
            veto_reasons.append(f"SyntaxError: {metrics.get('syntax_error', 'Invalid Python AST')}")

        # Lazy Stubs Veto
        if metrics.get("has_lazy_stubs", False):
            veto_reasons.append("CraftsmanshipDefect: Found lazy placeholders or TODO/FIXME stubs")

        # 1. Neutron Kinetics & Delayed Precursors (20 pts)
        kinetics_score = 0
        if metrics.get("has_prke_kinetics", False):
            kinetics_score += 20
        else:
            veto_reasons.append("KineticsDeficit: Missing point reactor kinetics or delayed precursor groups")
        breakdown["neutron_kinetics_delayed"] = kinetics_score

        # 2. Criticality Margin in Dollars (20 pts)
        react_score = 0
        if metrics.get("has_reactivity_dollars", False):
            react_score += 20
        if metrics.get("has_prompt_critical_hazard", False):
            veto_reasons.append("PromptCriticalHazard: Reactivity exceeds $1.00 prompt critical threshold")
        breakdown["criticality_margin_dollars"] = react_score

        # 3. Passive Doppler Feedback (20 pts)
        doppler_score = 0
        if metrics.get("has_doppler_feedback", False):
            doppler_score += 20
        if metrics.get("has_positive_doppler_hazard", False):
            veto_reasons.append("ChernobylHazard: Positive fuel Doppler temperature coefficient detected")
        elif not metrics.get("has_doppler_feedback", False):
            veto_reasons.append("PassiveSafetyDeficit: Missing negative fuel Doppler temperature feedback")
        breakdown["passive_doppler_feedback"] = doppler_score

        # 4. Thermal DNBR Safety Margin (20 pts)
        dnbr_score = 0
        if metrics.get("has_dnbr_safety", False):
            dnbr_score += 20
        else:
            veto_reasons.append("ThermalMarginDeficit: Missing Departure from Nucleate Boiling Ratio (DNBR >= 1.30)")
        breakdown["thermal_dnbr_safety"] = dnbr_score

        # 5. SCRAM & Stuck Rod Redundancy (20 pts)
        scram_score = 0
        if metrics.get("has_scram_control", False):
            scram_score += 20
        breakdown["scram_stuck_rod_redundancy"] = scram_score

        total_score = sum(breakdown.values())
        veto_reason = " | ".join(veto_reasons) if veto_reasons else ""
        passed = (total_score >= cls.PASSING_THRESHOLD) and (len(veto_reasons) == 0)

        return total_score, breakdown, passed, veto_reason
