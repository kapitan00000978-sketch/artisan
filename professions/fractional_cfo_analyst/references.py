"""
Victor Montgomery - Financial Reference Standards & Startup Unit Economics Canon.

This module codifies empirical financial benchmarks, venture capital metrics,
and capital defense standards across business models (B2B SaaS, Marketplace, FinTech, Enterprise).
"""

from typing import Dict, Any, List


SAAS_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "gross_margin": {
        "metric": "Gross Margin Percentage",
        "formula": "(Revenue - COGS) / Revenue",
        "min_acceptable": 0.70,
        "target": 0.80,
        "world_class": 0.85,
        "cogs_inclusions": ["hosting_cloud", "customer_support", "data_apis", "payment_fees"]
    },
    "ltv_cac_ratio": {
        "metric": "LTV to CAC Ratio",
        "formula": "LTV / Fully_Loaded_CAC",
        "min_acceptable": 3.0,
        "target": 4.5,
        "world_class": 6.0,
        "underinvestment_warning": 8.0
    },
    "cac_payback_months": {
        "metric": "CAC Payback Period (Months)",
        "formula": "CAC / (Monthly_ARPA * Gross_Margin)",
        "smb_max_months": 12.0,
        "mid_market_max_months": 15.0,
        "enterprise_max_months": 18.0,
        "world_class_months": 8.0
    },
    "net_revenue_retention": {
        "metric": "Net Revenue Retention (NRR)",
        "formula": "(Starting_ARR + Expansion - Contraction - Churn) / Starting_ARR",
        "min_acceptable": 1.00,
        "target": 1.15,
        "world_class": 1.30
    },
    "burn_multiple": {
        "metric": "Burn Multiple",
        "formula": "Net_Burn / Net_New_ARR",
        "exceptional": 1.0,
        "good": 1.5,
        "acceptable": 2.0,
        "distressed": 2.5
    },
    "rule_of_40": {
        "metric": "Rule of 40",
        "formula": "YoY_Revenue_Growth_Rate + Free_Cash_Flow_Margin",
        "target": 0.40,
        "strong": 0.50
    },
    "magic_number": {
        "metric": "SaaS Magic Number",
        "formula": "(Q_Revenue - Q_prev_Revenue) * 4 / Q_prev_SalesMarketingExpense",
        "min_acceptable": 0.75,
        "target": 1.0,
        "accelerate_investment": 1.2
    }
}

RUNWAY_TIERS: Dict[str, Dict[str, Any]] = {
    "insolvency_crisis": {
        "max_months": 3.0,
        "action": "Immediate emergency freeze, bridge financing or wind-down execution."
    },
    "critical_runway": {
        "max_months": 6.0,
        "action": "Activate austerity plan: freeze hiring, cut discretionary SaaS, prep investor bridge."
    },
    "caution_zone": {
        "max_months": 12.0,
        "action": "Initiate Series next round fundraising immediately (takes 4-6 months)."
    },
    "healthy": {
        "max_months": 18.0,
        "action": "Balanced growth and unit-economic optimization."
    },
    "fortress": {
        "max_months": 999.0,
        "action": "Defensive moat, opportunistic acquisitions, self-sustaining operations."
    }
}

RED_FLAG_PATTERNS: List[Dict[str, str]] = [
    {
        "id": "blended_cac_deception",
        "indicator": "Only reporting blended CAC instead of segmented Paid CAC vs Organic.",
        "risk": "Masks unsustainable paid acquisition unit economics."
    },
    {
        "id": "cogs_exclusion",
        "indicator": "Excluding cloud hosting, customer success, or transaction fees from COGS.",
        "risk": "Artificially inflates Gross Margin, resulting in false EBITDA projections."
    },
    {
        "id": "zero_churn_perpetuity",
        "indicator": "Assuming 0% annual churn or calculating LTV without decay curvature.",
        "risk": "Delusional customer lifetime values and premature over-hiring."
    },
    {
        "id": "top_down_tam_handwave",
        "indicator": "Claiming capture of 1% of a massive market without bottom-up conversion funnel.",
        "risk": "Total divorce between operational reality and sales execution."
    },
    {
        "id": "negative_gross_margin",
        "indicator": "Revenue lower than direct fulfillment costs.",
        "risk": "Business model bleeds more cash as it scales."
    }
]


class FinancialReferenceLibrary:
    """Provides empirical startup financial benchmarks and evaluation metrics."""

    @staticmethod
    def get_saas_benchmarks() -> Dict[str, Dict[str, Any]]:
        return SAAS_BENCHMARKS

    @staticmethod
    def get_runway_tiers() -> Dict[str, Dict[str, Any]]:
        return RUNWAY_TIERS

    @staticmethod
    def get_red_flag_patterns() -> List[Dict[str, str]]:
        return RED_FLAG_PATTERNS

    @staticmethod
    def evaluate_runway_tier(runway_months: float) -> str:
        if runway_months <= 3.0:
            return "insolvency_crisis"
        elif runway_months <= 6.0:
            return "critical_runway"
        elif runway_months <= 12.0:
            return "caution_zone"
        elif runway_months <= 18.0:
            return "healthy"
        return "fortress"
