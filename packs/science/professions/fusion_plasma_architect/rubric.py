"""Evaluation Rubric for Tokamak Magnetic Confinement & Fusion Plasma Stability.

Author: Dr. Silas 'The Plasma' Vance
Status: Production 100-Point Weighted Rubric with Veto Accumulation
"""

from typing import Any, Dict, List, Tuple


class FusionPlasmaRubric:
    """100-point weighted evaluation rubric for tokamak MHD stability and disruption prevention."""

    PASSING_THRESHOLD: int = 85

    @classmethod
    def evaluate(cls, metrics: Dict[str, Any]) -> Tuple[int, Dict[str, int], bool, str]:
        """Evaluate code metrics against fusion plasma MHD stability standards.

        Returns:
            Tuple[int, Dict[str, int], bool, str]: (total_score, breakdown, passed, veto_reason)
        """
        breakdown: Dict[str, int] = {
            "safety_factor_q95": 0,
            "troyon_beta_limit": 0,
            "greenwald_density_margin": 0,
            "ntm_tearing_eccd_suppression": 0,
            "divertor_heat_flux_safety": 0,
        }
        veto_reasons: List[str] = []

        # Global Syntax Veto
        if not metrics.get("ast_valid", False):
            veto_reasons.append(f"SyntaxError: {metrics.get('syntax_error', 'Invalid Python AST')}")

        # Lazy Stubs Veto
        if metrics.get("has_lazy_stubs", False):
            veto_reasons.append("CraftsmanshipDefect: Found lazy placeholders or TODO/FIXME stubs")

        # 1. Safety Factor q95 & Kruskal-Shafranov (20 pts)
        q_score = 0
        if metrics.get("has_safety_factor_logic", False):
            q_score += 20
        if metrics.get("has_kink_disruption_hazard", False):
            veto_reasons.append("KruskalShafranovDisruption: Edge safety factor q95 < 2.0 triggers external kink collapse")
        elif not metrics.get("has_safety_factor_logic", False):
            veto_reasons.append("MHDStabilityDeficit: Missing safety factor profile q95 monitoring")
        breakdown["safety_factor_q95"] = q_score

        # 2. Troyon Beta Limit (20 pts)
        beta_score = 0
        if metrics.get("has_troyon_beta_logic", False):
            beta_score += 20
        else:
            veto_reasons.append("TroyonBetaDeficit: Missing normalized beta beta_N monitoring against ideal MHD limit")
        breakdown["troyon_beta_limit"] = beta_score

        # 3. Greenwald Density Margin (20 pts)
        density_score = 0
        if metrics.get("has_greenwald_logic", False):
            density_score += 20
        if metrics.get("has_density_limit_hazard", False):
            veto_reasons.append("GreenwaldDisruption: Density fraction f_G >= 1.0 triggers radiative collapse and MARFE")
        elif not metrics.get("has_greenwald_logic", False):
            veto_reasons.append("DensityLimitDeficit: Missing Greenwald density fraction f_G calculation")
        breakdown["greenwald_density_margin"] = density_score

        # 4. NTM Island Suppression & ECCD (20 pts)
        ntm_score = 0
        if metrics.get("has_ntm_stabilization", False):
            ntm_score += 20
        breakdown["ntm_tearing_eccd_suppression"] = ntm_score

        # 5. Divertor Heat Flux & Radiative Detachment (20 pts)
        div_score = 0
        if metrics.get("has_divertor_protection", False):
            div_score += 20
        breakdown["divertor_heat_flux_safety"] = div_score

        total_score = sum(breakdown.values())
        veto_reason = " | ".join(veto_reasons) if veto_reasons else ""
        passed = (total_score >= cls.PASSING_THRESHOLD) and (len(veto_reasons) == 0)

        return total_score, breakdown, passed, veto_reason
