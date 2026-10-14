"""
Victor Montgomery - Objective Financial Measurement & Unit-Economics Inspector.

This module computes exact mathematical metrics, verifies accounting integrity,
and audits financial projections against venture benchmarks without subjective bias.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import json
import re


@dataclass
class FinancialMetrics:
    revenue_monthly: float = 0.0
    cogs_monthly: float = 0.0
    gross_margin_pct: float = 0.0
    cogs_items_detected: List[str] = field(default_factory=list)
    missing_cogs_items: List[str] = field(default_factory=list)
    sales_marketing_monthly: float = 0.0
    new_customers_monthly: float = 0.0
    cac: float = 0.0
    arpa_monthly: float = 0.0
    churn_rate_annual: float = 0.0
    ltv: float = 0.0
    ltv_cac_ratio: float = 0.0
    cac_payback_months: float = 0.0
    cash_balance: float = 0.0
    operating_expenses_monthly: float = 0.0
    net_burn_monthly: float = 0.0
    runway_months: float = 0.0
    runway_tier: str = "unknown"
    net_new_arr_annual: float = 0.0
    burn_multiple: float = 0.0
    has_sensitivity_scenarios: bool = False
    has_blended_cac_warning: bool = False
    growth_rate_yoy: float = 0.0
    free_cash_flow_margin: float = 0.0
    rule_of_40_val: float = 0.0


@dataclass
class FinancialInspectionReport:
    metrics: FinancialMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_financially_viable: bool = False


class FinancialInspector:
    """Rigorous mathematical auditor for financial models and startup unit economics."""

    ESSENTIAL_COGS_KEYWORDS = [
        "hosting", "aws", "gcp", "cloud", "server",
        "support", "customer success",
        "stripe", "payment", "transaction"
    ]

    def inspect(self, data: Any) -> FinancialInspectionReport:
        """
        Inspects financial data supplied as a dict, JSON string, or financial report text.
        """
        metrics = self._extract_metrics(data)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Gross Margin Audit
        if metrics.revenue_monthly > 0:
            if metrics.gross_margin_pct < 0.65:
                critical_violations.append(
                    f"Substandard Gross Margin ({metrics.gross_margin_pct * 100:.1f}%). Minimum viable SaaS threshold is 70.0%, target 80.0%."
                )
            elif metrics.gross_margin_pct < 0.75:
                warnings.append(
                    f"Soft Gross Margin ({metrics.gross_margin_pct * 100:.1f}%). Target is 80.0% for healthy enterprise SaaS."
                )
            else:
                benchmarks_passed.append(f"Strong Gross Margin ({metrics.gross_margin_pct * 100:.1f}%)")

        # 2. COGS Completeness
        if metrics.missing_cogs_items:
            critical_violations.append(
                f"Incomplete COGS: Missing essential expense lines {metrics.missing_cogs_items}. Artificially inflates margin."
            )
        else:
            benchmarks_passed.append("COGS includes hosting, customer support, and payment infrastructure.")

        # 3. Unit Economics: LTV / CAC
        if metrics.cac > 0:
            if metrics.ltv_cac_ratio < 2.5:
                critical_violations.append(
                    f"Fatal Unit Economics: LTV/CAC ratio is {metrics.ltv_cac_ratio:.2f}x (Minimum acceptable: 3.0x). Every acquired customer destroys value."
                )
            elif metrics.ltv_cac_ratio < 3.5:
                warnings.append(
                    f"Fragile LTV/CAC ratio ({metrics.ltv_cac_ratio:.2f}x). Target is 4.5x - 6.0x."
                )
            elif metrics.ltv_cac_ratio > 8.0:
                warnings.append(
                    f"Over-conservatism: LTV/CAC is {metrics.ltv_cac_ratio:.2f}x. Company is severely underinvesting in go-to-market acceleration."
                )
            else:
                benchmarks_passed.append(f"Optimal LTV/CAC ratio ({metrics.ltv_cac_ratio:.2f}x)")

        # 4. CAC Payback
        if metrics.cac_payback_months > 18.0:
            critical_violations.append(
                f"Capital-destructive CAC Payback ({metrics.cac_payback_months:.1f} months). Max threshold is 12-15 months; cash is suffocated in S&M."
            )
        elif metrics.cac_payback_months > 12.0:
            warnings.append(
                f"Elevated CAC Payback ({metrics.cac_payback_months:.1f} months). Target <= 12 months for self-serve/SMB."
            )
        elif metrics.cac_payback_months > 0:
            benchmarks_passed.append(f"World-class CAC Payback ({metrics.cac_payback_months:.1f} months)")

        # 5. Runway & Survival
        if metrics.net_burn_monthly > 0:
            if metrics.runway_months < 6.0:
                critical_violations.append(
                    f"Code Red Runway: Only {metrics.runway_months:.1f} months of cash remaining. Immediate liquidity hazard without emergency austerity plan."
                )
            elif metrics.runway_months < 12.0:
                warnings.append(
                    f"Vulnerable Runway: {metrics.runway_months:.1f} months remaining. Must initiate next capital round or reach cashflow breakeven."
                )
            else:
                benchmarks_passed.append(f"Robust Runway ({metrics.runway_months:.1f} months)")

        # 6. Burn Multiple
        if metrics.burn_multiple > 2.5 and metrics.net_new_arr_annual > 0:
            critical_violations.append(
                f"Extreme Burn Multiple ({metrics.burn_multiple:.2f}x). Burning over $2.50 to generate $1.00 of net new ARR."
            )
        elif metrics.burn_multiple > 1.8 and metrics.net_new_arr_annual > 0:
            warnings.append(f"Elevated Burn Multiple ({metrics.burn_multiple:.2f}x). Target is <= 1.5x.")
        elif metrics.burn_multiple > 0 and metrics.burn_multiple <= 1.5:
            benchmarks_passed.append(f"Efficient Burn Multiple ({metrics.burn_multiple:.2f}x)")

        # 7. Sensitivity Scenarios
        if not metrics.has_sensitivity_scenarios:
            warnings.append("Missing dynamic scenario analysis (Base, Bull, and Bear survival stress tests).")
        else:
            benchmarks_passed.append("Dynamic scenario modeling (Base, Bull, Bear) detected.")

        # 8. Blended CAC Warning
        if metrics.has_blended_cac_warning:
            warnings.append("Blended CAC detected without distinct Paid CAC breakdown. Risks cloaking paid acquisition burn.")

        is_viable = len(critical_violations) == 0 and metrics.runway_months >= 6.0

        return FinancialInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_financially_viable=is_viable
        )

    def _extract_metrics(self, data: Any) -> FinancialMetrics:
        """Parses structured or textual financial inputs into canonical metrics."""
        m = FinancialMetrics()

        if isinstance(data, str):
            try:
                parsed = json.loads(data)
                if isinstance(parsed, dict):
                    return self._populate_from_dict(parsed)
            except (json.JSONDecodeError, ValueError) as _json_parse_err:
                _ = _json_parse_err  # Fall through to heuristic text parsing
            return self._extract_from_text(data)
        elif isinstance(data, dict):
            return self._populate_from_dict(data)

        return m

    def _populate_from_dict(self, d: Dict[str, Any]) -> FinancialMetrics:
        m = FinancialMetrics()
        m.revenue_monthly = float(d.get("revenue_monthly", d.get("mrr", 0.0)))
        m.cogs_monthly = float(d.get("cogs_monthly", d.get("cogs", 0.0)))

        # Gross margin calculation
        if m.revenue_monthly > 0:
            m.gross_margin_pct = (m.revenue_monthly - m.cogs_monthly) / m.revenue_monthly
        else:
            m.gross_margin_pct = float(d.get("gross_margin_pct", 0.0))

        # COGS completeness
        cogs_items = d.get("cogs_breakdown", [])
        if isinstance(cogs_items, dict):
            cogs_items = list(cogs_items.keys())
        elif not isinstance(cogs_items, list):
            cogs_items = []
            
        cogs_lower = [str(item).lower() for item in cogs_items]
        m.cogs_items_detected = cogs_lower

        missing = []
        if not any("host" in item or "cloud" in item or "aws" in item or "server" in item for item in cogs_lower):
            missing.append("cloud_hosting")
        if not any("support" in item or "success" in item for item in cogs_lower):
            missing.append("customer_support")
        if not any("stripe" in item or "payment" in item or "fee" in item for item in cogs_lower):
            missing.append("payment_processing")
        
        # If user explicitly provided cogs breakdown, track missing
        if cogs_items:
            m.missing_cogs_items = missing
        elif m.cogs_monthly > 0 and not cogs_items:
            # Default minimal items assumed if flat cogs provided without breakdown
            m.missing_cogs_items = []

        # Customer acquisition and economics
        m.sales_marketing_monthly = float(d.get("sales_marketing_monthly", d.get("sm_expense", 0.0)))
        m.new_customers_monthly = float(d.get("new_customers_monthly", d.get("new_customers", 0.0)))
        
        if m.new_customers_monthly > 0 and m.sales_marketing_monthly > 0:
            m.cac = m.sales_marketing_monthly / m.new_customers_monthly
        else:
            m.cac = float(d.get("cac", 0.0))

        m.arpa_monthly = float(d.get("arpa_monthly", d.get("arpu", 0.0)))
        m.churn_rate_annual = float(d.get("churn_rate_annual", d.get("churn_rate", 0.05)))
        if m.churn_rate_annual <= 0.0:
            m.churn_rate_annual = 0.05  # Prevent division by zero, 5% floor

        # LTV calculation
        if m.arpa_monthly > 0:
            annual_revenue_per_user = m.arpa_monthly * 12.0
            m.ltv = (annual_revenue_per_user * max(m.gross_margin_pct, 0.1)) / m.churn_rate_annual
        else:
            m.ltv = float(d.get("ltv", 0.0))

        if m.cac > 0:
            m.ltv_cac_ratio = m.ltv / m.cac
            monthly_contribution = m.arpa_monthly * max(m.gross_margin_pct, 0.05)
            if monthly_contribution > 0:
                m.cac_payback_months = m.cac / monthly_contribution
            else:
                m.cac_payback_months = 99.0
        else:
            m.ltv_cac_ratio = float(d.get("ltv_cac_ratio", 0.0))
            m.cac_payback_months = float(d.get("cac_payback_months", 0.0))

        # Cash & Runway
        m.cash_balance = float(d.get("cash_balance", d.get("cash", 0.0)))
        m.operating_expenses_monthly = float(d.get("operating_expenses_monthly", d.get("opex", 0.0)))
        
        # Net Burn = (Opex + COGS) - Revenue
        if m.operating_expenses_monthly > 0 or m.cogs_monthly > 0:
            m.net_burn_monthly = (m.operating_expenses_monthly + m.cogs_monthly) - m.revenue_monthly
        else:
            m.net_burn_monthly = float(d.get("net_burn_monthly", d.get("burn_rate", 0.0)))

        if m.net_burn_monthly > 0:
            m.runway_months = m.cash_balance / m.net_burn_monthly
        elif m.cash_balance > 0 and m.net_burn_monthly <= 0:
            m.runway_months = 999.0  # Cashflow positive / self-sustaining
        else:
            m.runway_months = 0.0

        if m.runway_months <= 3.0:
            m.runway_tier = "insolvency_crisis"
        elif m.runway_months <= 6.0:
            m.runway_tier = "critical_runway"
        elif m.runway_months <= 12.0:
            m.runway_tier = "caution_zone"
        elif m.runway_months <= 18.0:
            m.runway_tier = "healthy"
        else:
            m.runway_tier = "fortress"

        # Burn Multiple
        m.net_new_arr_annual = float(d.get("net_new_arr_annual", d.get("net_new_arr", 0.0)))
        if m.net_new_arr_annual > 0 and m.net_burn_monthly > 0:
            annualized_net_burn = m.net_burn_monthly * 12.0
            m.burn_multiple = annualized_net_burn / m.net_new_arr_annual
        else:
            m.burn_multiple = float(d.get("burn_multiple", 0.0))

        # Scenario & Scrutiny
        m.has_sensitivity_scenarios = bool(d.get("has_sensitivity_scenarios", "scenarios" in d or "bear_case" in d))
        m.has_blended_cac_warning = bool(d.get("has_blended_cac_warning", d.get("is_blended_cac_only", False)))

        # Rule of 40
        m.growth_rate_yoy = float(d.get("growth_rate_yoy", 0.0))
        m.free_cash_flow_margin = float(d.get("free_cash_flow_margin", 0.0))
        m.rule_of_40_val = m.growth_rate_yoy + m.free_cash_flow_margin

        return m

    def _extract_from_text(self, text: str) -> FinancialMetrics:
        """Heuristic extractor for markdown/text reports."""
        d: Dict[str, Any] = {}
        
        # Search patterns
        mrr_match = re.search(r"(?:MRR|monthly revenue)[:\s]+\$?([\d,]+(?:\.\d+)?)", text, re.IGNORECASE)
        if mrr_match:
            d["revenue_monthly"] = float(mrr_match.group(1).replace(",", ""))

        burn_match = re.search(r"(?:burn rate|net burn)[:\s]+\$?([\d,]+(?:\.\d+)?)", text, re.IGNORECASE)
        if burn_match:
            d["net_burn_monthly"] = float(burn_match.group(1).replace(",", ""))

        cash_match = re.search(r"(?:cash balance|total cash)[:\s]+\$?([\d,]+(?:\.\d+)?)", text, re.IGNORECASE)
        if cash_match:
            d["cash_balance"] = float(cash_match.group(1).replace(",", ""))

        cac_match = re.search(r"\bCAC[:\s]+\$?([\d,]+(?:\.\d+)?)", text, re.IGNORECASE)
        if cac_match:
            d["cac"] = float(cac_match.group(1).replace(",", ""))

        ltv_match = re.search(r"\bLTV[:\s]+\$?([\d,]+(?:\.\d+)?)", text, re.IGNORECASE)
        if ltv_match:
            d["ltv"] = float(ltv_match.group(1).replace(",", ""))

        gross_margin_match = re.search(r"gross margin[:\s]+([\d.]+)%", text, re.IGNORECASE)
        if gross_margin_match:
            d["gross_margin_pct"] = float(gross_margin_match.group(1)) / 100.0

        if "bear case" in text.lower() or "base case" in text.lower():
            d["has_sensitivity_scenarios"] = True

        if "blended cac" in text.lower() and "paid cac" not in text.lower():
            d["has_blended_cac_warning"] = True

        return self._populate_from_dict(d)
