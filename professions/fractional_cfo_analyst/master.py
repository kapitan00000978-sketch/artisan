"""
🏛️ VICTOR MONTGOMERY — STARTUP FRACTIONAL CFO & CAPITAL DEFENSE MASTER
Autonomous financial conscience, unit-economics stress testing, blind outcome critique,
and automated financial fortress elevation engine.

Usage:
    python professions/fractional_cfo_analyst/master.py <financial_data_file> [--elevate]
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, List, Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception as _enc_err:
        sys.stderr.write(f"Note: UTF-8 stdout reconfiguration skipped: {_enc_err}\n")

try:
    from .references import FinancialReferenceLibrary
    from .inspector import FinancialInspector, FinancialInspectionReport
    from .rubric import FinancialRubric, RubricEvaluation
    from .blind_critic import BlindFinancialCritic, DefectLedger
    from .elevation_engine import FinancialElevationEngine
except ImportError:
    from references import FinancialReferenceLibrary
    from inspector import FinancialInspector, FinancialInspectionReport
    from rubric import FinancialRubric, RubricEvaluation
    from blind_critic import BlindFinancialCritic, DefectLedger
    from elevation_engine import FinancialElevationEngine

# Import global ActiveDecisionJournal from studio engine
try:
    from src.studio.active_memory import ActiveDecisionJournal
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.studio.active_memory import ActiveDecisionJournal


class VictorMontgomeryMaster:
    """
    Victor Montgomery: The living capital defense strategist, fiduciary inquisitor,
    and startup fractional CFO. Rejects spreadsheet optimism, certifies unit economics,
    and safeguards startup solvency.
    """

    def __init__(
        self,
        target_path: Optional[str] = None,
        passing_threshold: int = 85,
        max_cycles: int = 3
    ):
        self.target_path = os.path.abspath(target_path) if target_path else None
        self.passing_threshold = passing_threshold
        self.max_cycles = max_cycles
        self.inspector = FinancialInspector()
        self.rubric = FinancialRubric()
        self.critic = BlindFinancialCritic()
        self.elevation_engine = FinancialElevationEngine()
        self.journal = ActiveDecisionJournal()

    def run_autonomous_cycle(self, input_data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes the closed-loop autonomous financial audit & elevation lifecycle.
        1. Inspect -> 2. Rubric -> 3. Critic -> 4. Elevate (if < 85) -> 5. Certify & Journal
        """
        data = input_data
        if data is None and self.target_path:
            if os.path.exists(self.target_path):
                with open(self.target_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    try:
                        data = json.loads(content)
                    except Exception:
                        data = content
            else:
                raise FileNotFoundError(f"Financial target file not found: {self.target_path}")

        if data is None:
            # Default prototype baseline for testing or standalone demo
            data = {
                "mrr": 50000,
                "cogs": 10000,
                "cogs_breakdown": ["cloud_hosting_aws", "customer_support", "stripe_fees"],
                "sm_expense": 30000,
                "new_customers": 40,
                "arpu": 1250,
                "churn_rate": 0.05,
                "cash": 1200000,
                "opex": 70000
            }

        # Step 1: Initial Blind Critic Review
        ledger: DefectLedger = self.critic.review(data)
        initial_score = ledger.score
        elevated_result: Optional[Dict[str, Any]] = None

        # Step 2: Elevate if failed
        current_data = data
        if not ledger.is_certified:
            dict_data = current_data if isinstance(current_data, dict) else {"text_report": str(current_data)}
            elevated_result = self.elevation_engine.elevate(dict_data, max_iterations=self.max_cycles)
            current_data = elevated_result["elevated_model"]
            ledger = elevated_result["final_ledger"]

        # Step 3: Record in Journal
        self._record_journal_entry(
            initial_score=initial_score,
            final_score=ledger.score,
            is_certified=ledger.is_certified,
            fatal_defects=ledger.fatal_defects_count,
            verdict=ledger.verdict
        )

        # Step 4: Generate Executive Briefing
        briefing = self._generate_briefing(current_data, ledger)

        return {
            "is_certified": ledger.is_certified,
            "initial_score": initial_score,
            "final_score": ledger.score,
            "verdict": ledger.verdict,
            "fatal_defects_count": ledger.fatal_defects_count,
            "defects": ledger.defects,
            "elevated_model": current_data,
            "executive_briefing": briefing,
            "summary": ledger.critic_verdict_summary
        }

    def _record_journal_entry(
        self,
        initial_score: int,
        final_score: int,
        is_certified: bool,
        fatal_defects: int,
        verdict: str
    ) -> None:
        try:
            self.journal.record_decision(
                iteration=1,
                target_file=self.target_path if self.target_path else "financial_model.json",
                defects_before=[f"Fatal defects: {fatal_defects}"],
                actions_taken=["victor_cfo_capital_elevation"],
                score_before=float(initial_score),
                score_after=float(final_score)
            )
        except Exception as _journal_err:
            sys.stderr.write(f"Note: Decision journal record skipped: {_journal_err}\n")

    def _generate_briefing(self, model_data: Any, ledger: DefectLedger) -> str:
        report = self.inspector.inspect(model_data)
        m = report.metrics

        status_icon = "🏰 [FORTRESS CERTIFIED]" if ledger.is_certified else "⚠️ [REJECTED UNVIABLE]"

        briefing = [
            f"# {status_icon} EXECUTIVE CFO BRIEFING",
            f"**Auditor:** Victor 'The Fortress' Montgomery (Fractional CFO & Capital Defense Strategist)",
            f"**Final Score:** {ledger.score}/100 (Threshold: {ledger.passing_threshold})",
            f"**Verdict:** {ledger.verdict}",
            "",
            "## 📊 I. Core Unit Economics & Solvency Matrix",
            f"- **Monthly MRR:** ${m.revenue_monthly:,.2f}",
            f"- **Gross Margin:** {m.gross_margin_pct * 100:.1f}% (Benchmark: >= 80.0%)",
            f"- **LTV / CAC Ratio:** {m.ltv_cac_ratio:.2f}x (Benchmark: 3.5x - 6.0x)",
            f"- **CAC Payback Period:** {m.cac_payback_months:.1f} months (Benchmark: <= 12.0 mo)",
            f"- **Cash Reserves:** ${m.cash_balance:,.2f}",
            f"- **Monthly Net Burn:** ${m.net_burn_monthly:,.2f}",
            f"- **Runway Remaining:** {m.runway_months:.1f} months (Tier: {m.runway_tier.upper()})",
            "",
            "## 🛑 II. Defect & Remediation Ledger",
        ]

        if not ledger.defects:
            briefing.append("✅ Zero defects identified. Balance sheet and unit economics satisfy institutional criteria.")
        else:
            for d in ledger.defects:
                briefing.append(f"- **[{d.severity}] {d.title}:** {d.description}")
                briefing.append(f"  *Fix:* {d.actionable_fix}")

        briefing.extend([
            "",
            "## 🛡️ III. Victor's Fiduciary Directive",
            ledger.critic_verdict_summary,
            ""
        ])

        return "\n".join(briefing)


def main():
    parser = argparse.ArgumentParser(
        description="Victor Montgomery: Startup Fractional CFO Standalone Auditor"
    )
    parser.add_argument("target", nargs="?", default=None, help="Path to financial JSON or report file")
    parser.add_argument("--elevate", action="store_true", help="Automatically elevate flawed models")
    parser.add_argument("--threshold", type=int, default=85, help="Minimum passing score")

    args = parser.parse_args()

    master = VictorMontgomeryMaster(target_path=args.target, passing_threshold=args.threshold)
    result = master.run_autonomous_cycle()

    print(result["executive_briefing"])

    if not result["is_certified"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
