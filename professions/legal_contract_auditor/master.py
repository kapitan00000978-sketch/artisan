"""
🏛️ ARTHUR PENDELTON — SENIOR COMMERCIAL COUNSEL & CONTRACT AUDITOR
Autonomous legal conscience, litigation risk analysis, blind contract outcome critique,
and automated institutional contract elevation engine.

Usage:
    python professions/legal_contract_auditor/master.py <contract_file> [--elevate]
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
    from .references import ContractReferenceLibrary
    from .inspector import ContractInspector, LegalInspectionReport
    from .rubric import ContractRubric, LegalRubricEvaluation
    from .blind_critic import BlindLegalCritic, LegalDefectLedger
    from .elevation_engine import ContractElevationEngine
except ImportError:
    from references import ContractReferenceLibrary
    from inspector import ContractInspector, LegalInspectionReport
    from rubric import ContractRubric, LegalRubricEvaluation
    from blind_critic import BlindLegalCritic, LegalDefectLedger
    from elevation_engine import ContractElevationEngine

# Import global ActiveDecisionJournal from studio engine
try:
    from src.studio.active_memory import ActiveDecisionJournal
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.studio.active_memory import ActiveDecisionJournal


class ArthurPendeltonMaster:
    """
    Arthur Pendelton: The living contract defense litigator, commercial counsel,
    and sovereign IP auditor. Rejects vague covenants, enforces mutual liability caps,
    and eliminates toxic contract boobytraps.
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
        self.inspector = ContractInspector()
        self.rubric = ContractRubric()
        self.critic = BlindLegalCritic()
        self.elevation_engine = ContractElevationEngine()
        self.journal = ActiveDecisionJournal()

    def run_autonomous_cycle(self, input_data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes the closed-loop autonomous legal audit & elevation lifecycle.
        1. Inspect -> 2. Rubric -> 3. Critic -> 4. Elevate (if < 85) -> 5. Certify & Journal
        """
        data = input_data
        if data is None and self.target_path:
            if os.path.exists(self.target_path):
                with open(self.target_path, "r", encoding="utf-8") as f:
                    data = f.read()
            else:
                raise FileNotFoundError(f"Contract target file not found: {self.target_path}")

        if data is None:
            # Prototype baseline contract draft for testing or demo
            data = (
                "MASTER SERVICES AGREEMENT\n"
                "1. Services: Contractor will provide software development services.\n"
                "2. Ownership: Contractor agrees to assign deliverables upon final payment.\n"
                "3. Liability: Customer shall be solely liable without limitation for all damages.\n"
                "4. Indemnity: Contractor shall indemnify Company against all third party claims.\n"
                "5. Termination: Either party may terminate immediately."
            )

        # Step 1: Initial Blind Critic Review
        ledger: LegalDefectLedger = self.critic.review(data)
        initial_score = ledger.score
        elevated_result: Optional[Dict[str, Any]] = None

        # Step 2: Elevate if failed
        current_data = data
        if not ledger.is_certified:
            elevated_result = self.elevation_engine.elevate(current_data, max_iterations=self.max_cycles)
            current_data = elevated_result["elevated_contract"]
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
            "elevated_contract": current_data,
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
                target_file=self.target_path if self.target_path else "contract_agreement.md",
                defects_before=[f"Fatal defects: {fatal_defects}"],
                actions_taken=["arthur_contract_ironclad_elevation"],
                score_before=float(initial_score),
                score_after=float(final_score)
            )
        except Exception as _journal_err:
            sys.stderr.write(f"Note: Decision journal record skipped: {_journal_err}\n")

    def _generate_briefing(self, contract_data: Any, ledger: LegalDefectLedger) -> str:
        report = self.inspector.inspect(contract_data)
        m = report.metrics

        status_icon = "⚖️ [IRONCLAD CERTIFIED]" if ledger.is_certified else "⚠️ [REJECTED HIGH RISK]"

        briefing = [
            f"# {status_icon} EXECUTIVE LEGAL COUNSEL BRIEFING",
            f"**Auditor:** Arthur 'The Ironclad' Pendelton (Senior Commercial Counsel & Contract Litigator)",
            f"**Final Score:** {ledger.score}/100 (Threshold: {ledger.passing_threshold})",
            f"**Verdict:** {ledger.verdict}",
            "",
            "## 🛡️ I. Sovereign Contractual Safeguards Matrix",
            f"- **Limitation of Liability:** {'MUTUAL 12-MONTH CAP' if m.has_limitation_of_liability and m.is_liability_mutual else 'UNCAPPED / DANGEROUS'}",
            f"- **Consequential Damages Waiver:** {'EXPLICITLY WAIVED' if m.has_consequential_damages_waiver else 'MISSING (EXPOSED)'}",
            f"- **IP Title Conveyance:** {'PERFECTED (hereby assigns)' if m.is_present_ip_assignment else 'DEFECTIVE (agrees to assign / missing)'}",
            f"- **Indemnification Symmetry:** {'RECIPROCAL MUTUAL DEFENSE' if m.is_indemnification_mutual else 'UNILATERAL / ASYMMETRIC'}",
            f"- **Termination Cure Period:** {f'{m.cure_period_days} DAYS WRITTEN NOTICE' if m.has_cure_period else 'IMMEDIATE / ARBITRARY'}",
            f"- **Governing Law / Forum:** {'NEUTRAL JURISDICTION & ARBITRATION' if m.has_neutral_governing_law and m.has_dispute_resolution else 'DEFAULT / UNPROTECTED'}",
            "",
            "## 🛑 II. Defect & Remediation Redline Ledger",
        ]

        if not ledger.defects:
            briefing.append("✅ Zero critical exposures identified. Agreement provides robust institutional litigation defense.")
        else:
            for d in ledger.defects:
                briefing.append(f"- **[{d.severity}] {d.title}:** {d.description}")
                briefing.append(f"  *Exposure:* {d.exposure_impact}")
                briefing.append(f"  *Actionable Redline:* {d.actionable_redline}")

        briefing.extend([
            "",
            "## 🏛️ III. Arthur's Litigation Directive",
            ledger.critic_verdict_summary,
            ""
        ])

        return "\n".join(briefing)


def main():
    parser = argparse.ArgumentParser(
        description="Arthur Pendelton: Senior Commercial Counsel Standalone Contract Auditor"
    )
    parser.add_argument("target", nargs="?", default=None, help="Path to contract text or markdown file")
    parser.add_argument("--elevate", action="store_true", help="Automatically elevate flawed contracts")
    parser.add_argument("--threshold", type=int, default=85, help="Minimum passing score")

    args = parser.parse_args()

    master = ArthurPendeltonMaster(target_path=args.target, passing_threshold=args.threshold)
    result = master.run_autonomous_cycle()

    print(result["executive_briefing"])

    if not result["is_certified"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
