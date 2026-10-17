"""Code-Blind Evaluator for Tokamak Magnetic Confinement & Fusion Plasma Stability.

Author: Dr. Silas 'The Plasma' Vance
Status: Production Adversarial Critic
"""

from typing import Any, Dict, List
from professions.fusion_plasma_architect.inspector import FusionPlasmaInspector
from professions.fusion_plasma_architect.rubric import FusionPlasmaRubric


class FusionPlasmaBlindCritic:
    """Impartial code-blind critic identifying tokamak disruption hazards and MHD instabilities."""

    @classmethod
    def evaluate(cls, code: str) -> Dict[str, Any]:
        """Perform unbiased audit of fusion plasma code and produce actionable defect ledger."""
        metrics = FusionPlasmaInspector.inspect(code)
        score, breakdown, passed, veto_reason = FusionPlasmaRubric.evaluate(metrics)

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

        if metrics.get("has_kink_disruption_hazard", False):
            defect_ledger.append({
                "rule": "KRUSKAL_SHAFRANOV_STABILITY",
                "severity": "FATAL",
                "description": "Detected edge safety factor q95 < 2.0 causing catastrophic external kink collapse.",
                "remediation": "Maintain edge safety factor q95 >= 3.0 via plasma current shaping.",
            })

        if metrics.get("has_density_limit_hazard", False):
            defect_ledger.append({
                "rule": "GREENWALD_DENSITY_LIMIT",
                "severity": "FATAL",
                "description": "Detected Greenwald density fraction f_G >= 1.0 triggering radiative disruption.",
                "remediation": "Bound electron density to f_G <= 0.85 of Greenwald limit.",
            })

        if not metrics.get("has_safety_factor_logic", False):
            defect_ledger.append({
                "rule": "SAFETY_FACTOR_Q95_MONITOR",
                "severity": "FATAL",
                "description": "Missing SafetyFactorProfile monitoring against Kruskal-Shafranov limits.",
                "remediation": "Implement SafetyFactorProfile enforcing q95 >= 3.0.",
            })

        if not metrics.get("has_troyon_beta_logic", False):
            defect_ledger.append({
                "rule": "TROYON_BETA_MONITOR",
                "severity": "CRITICAL",
                "description": "Missing normalized beta beta_N monitoring against ideal MHD limit (beta_N <= 3.5).",
                "remediation": "Implement TroyonBetaMonitor evaluating beta_N.",
            })

        if not metrics.get("has_greenwald_logic", False):
            defect_ledger.append({
                "rule": "GREENWALD_DENSITY_MONITOR",
                "severity": "FATAL",
                "description": "Missing Greenwald density limit calculation and fraction monitoring.",
                "remediation": "Implement GreenwaldDensityMonitor enforcing f_G <= 0.85.",
            })

        if not metrics.get("has_ntm_stabilization", False):
            defect_ledger.append({
                "rule": "NTM_TEARING_SUPPRESSION",
                "severity": "CRITICAL",
                "description": "Missing Neoclassical Tearing Mode magnetic island and ECCD suppression logic.",
                "remediation": "Implement verify_ntm_stabilization verifying island width w/a <= 0.05 or ECCD >= 5MW.",
            })

        if not metrics.get("has_divertor_protection", False):
            defect_ledger.append({
                "rule": "DIVERTOR_HEAT_FLUX_SAFETY",
                "severity": "CRITICAL",
                "description": "Missing divertor target heat flux check (<= 10 MW/m^2) and radiative fraction.",
                "remediation": "Implement verify_divertor_safety enforcing <= 10 MW/m^2 and f_rad >= 0.70.",
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
