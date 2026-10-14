"""Code-Blind Evaluator for Nuclear Reactor Physics & Criticality Safety.

Author: Dr. Magnus 'The Core' Sterling
Status: Production Adversarial Critic
"""

from typing import Any, Dict, List
from professions.nuclear_criticality_architect.inspector import NuclearCriticalityInspector
from professions.nuclear_criticality_architect.rubric import NuclearCriticalityRubric


class NuclearCriticalityBlindCritic:
    """Impartial code-blind critic identifying prompt criticality hazards and thermal runaway risks."""

    @classmethod
    def evaluate(cls, code: str) -> Dict[str, Any]:
        """Perform unbiased audit of nuclear physics code and produce actionable defect ledger."""
        metrics = NuclearCriticalityInspector.inspect(code)
        score, breakdown, passed, veto_reason = NuclearCriticalityRubric.evaluate(metrics)

        defect_ledger: List[Dict[str, str]] = []

        if not metrics.get("ast_valid", False):
            defect_ledger.append({
                "rule": "AST_SYNTAX_VALIDITY",
                "severity": "FATAL",
                "description": f"Code contains invalid Python syntax: {metrics.get('syntax_error')}",
                "remediation": "Correct syntax to produce valid AST.",
            })

        if metrics.get("has_lazy_stubs", False):
            defect_ledger.append({
                "rule": "ZERO_LAZY_STUBS",
                "severity": "FATAL",
                "description": "Found placeholder stubs or TODO/FIXME markers.",
                "remediation": "Implement production logic end-to-end with zero placeholders.",
            })

        if metrics.get("has_prompt_critical_hazard", False):
            defect_ledger.append({
                "rule": "PROMPT_CRITICALITY_PREVENTION",
                "severity": "FATAL",
                "description": "Detected uncontrolled reactivity exceeding $1.00 prompt criticality threshold.",
                "remediation": "Enforce reactivity limits strictly below delayed neutron fraction ($ <= 0.80$).",
            })

        if metrics.get("has_positive_doppler_hazard", False):
            defect_ledger.append({
                "rule": "NEGATIVE_DOPPLER_FEEDBACK",
                "severity": "FATAL",
                "description": "Detected positive fuel Doppler temperature coefficient (Chernobyl-type runaway).",
                "remediation": "Enforce strictly negative fuel Doppler coefficient (alpha_f <= -1.5 pcm/K).",
            })

        if not metrics.get("has_prke_kinetics", False):
            defect_ledger.append({
                "rule": "DELAYED_NEUTRON_PRKE",
                "severity": "FATAL",
                "description": "Missing 6-group delayed neutron precursor Point Reactor Kinetics equations.",
                "remediation": "Implement PointReactorKineticsSolver with 6 standard delayed precursor groups.",
            })

        if not metrics.get("has_dnbr_safety", False):
            defect_ledger.append({
                "rule": "THERMAL_DNBR_MARGIN",
                "severity": "CRITICAL",
                "description": "Missing Departure from Nucleate Boiling Ratio (DNBR >= 1.30) thermal margin checks.",
                "remediation": "Implement verify_thermal_dnbr comparing local heat flux against critical heat flux.",
            })

        if not metrics.get("has_scram_control", False):
            defect_ledger.append({
                "rule": "SCRAM_EMERGENCY_SHUTDOWN",
                "severity": "CRITICAL",
                "description": "Missing fast gravity SCRAM insertion (<= 2.5s) or N-1 stuck rod analysis.",
                "remediation": "Implement verify_scram_shutdown enforcing <= 2.5s gravity drop.",
            })

        fatal_defects_count = sum(1 for d in defect_ledger if d["severity"] == "FATAL")
        verdict = "APPROVED" if (passed and fatal_defects_count == 0) else "REJECTED"

        return {
            "score": score,
            "breakdown": breakdown,
            "passed": passed,
            "veto_reason": veto_reason,
            "defect_ledger": defect_ledger,
            "fatal_defects_count": fatal_defects_count,
            "verdict": verdict,
        }
