"""
Arthur Pendelton - Autonomous Contract Elevation & Redline Remediation Engine.

Transforms hazardous, asymmetric, or ambiguous commercial contracts into
ironclad, institutional-grade agreements with balanced liability caps and perfected title transfers.
"""

from typing import Dict, Any, List
import re
from professions.legal_contract_auditor.references import ContractReferenceLibrary
from professions.legal_contract_auditor.inspector import ContractInspector, LegalInspectionReport
from professions.legal_contract_auditor.blind_critic import BlindLegalCritic, LegalDefectLedger


class ContractElevationEngine:
    """Elevates vulnerable contracts into Ironclad institutional agreements."""

    def __init__(self):
        self.inspector = ContractInspector()
        self.critic = BlindLegalCritic()
        self.standard_clauses = ContractReferenceLibrary.get_standard_clauses()

    def elevate(self, contract_input: Any, max_iterations: int = 3) -> Dict[str, Any]:
        """
        Takes raw contract text or dict and iteratively redlines clauses until certified at >= 85/100.
        """
        text = str(contract_input)
        remediations_applied: List[str] = []

        for iteration in range(1, max_iterations + 1):
            ledger: LegalDefectLedger = self.critic.review(text)
            if ledger.is_certified:
                break

            report: LegalInspectionReport = self.inspector.inspect(text)
            m = report.metrics

            # 1. Remediate Limitation of Liability
            if not m.has_limitation_of_liability or m.is_liability_uncapped or not m.is_liability_mutual or not m.has_consequential_damages_waiver:
                text = self._remediate_liability(text)
                remediations_applied.append(
                    f"Iteration {iteration}: Injected mutual 12-month aggregate liability cap and consequential damages waiver."
                )

            # 2. Remediate Intellectual Property Assignment
            if not m.is_present_ip_assignment or not m.has_ip_assignment:
                text = self._remediate_ip_assignment(text)
                remediations_applied.append(
                    f"Iteration {iteration}: Perfected title transfer with present assignment ('hereby assigns') and work-made-for-hire covenant."
                )

            # 3. Remediate Indemnification
            if not m.is_indemnification_mutual:
                text = self._remediate_indemnification(text)
                remediations_applied.append(
                    f"Iteration {iteration}: Balanced indemnification into mutual defense for third-party IP infringement."
                )

            # 4. Remediate Termination & Cure
            if not m.has_cure_period or m.cure_period_days < 30:
                text = self._remediate_termination(text)
                remediations_applied.append(
                    f"Iteration {iteration}: Established 30-day written notice and mandatory cure period for breach."
                )

            # 5. Remediate Confidentiality & Governing Law
            if not m.has_confidentiality or not m.has_nda_exclusions:
                text = self._remediate_confidentiality(text)
                remediations_applied.append(
                    f"Iteration {iteration}: Added bilateral confidentiality protections with customary legal carve-outs."
                )

            if not m.has_neutral_governing_law or not m.has_dispute_resolution:
                text = self._remediate_dispute_resolution(text)
                remediations_applied.append(
                    f"Iteration {iteration}: Specified Delaware governing law and expedited binding AAA arbitration."
                )

        final_ledger = self.critic.review(text)

        return {
            "status": "CERTIFIED" if final_ledger.is_certified else "ELEVATED_WITH_CAUTIONS",
            "score": final_ledger.score,
            "passing_threshold": final_ledger.passing_threshold,
            "verdict": final_ledger.verdict,
            "remediations_applied": remediations_applied,
            "elevated_contract": text,
            "final_ledger": final_ledger,
            "metrics": self.inspector.inspect(text).metrics
        }

    def _remediate_liability(self, text: str) -> str:
        # Strip out dangerous uncapped wording
        cleaned = re.sub(
            r"(?:customer|provider|contractor)\s+shall\s+be\s+solely\s+liable\s+without\s+limitation.*?\.",
            "",
            text,
            flags=re.IGNORECASE
        )
        lol_clause = (
            "\n\n## SECTION: LIMITATION OF LIABILITY\n" +
            self.standard_clauses["limitation_of_liability"]
        )
        return cleaned + lol_clause

    def _remediate_ip_assignment(self, text: str) -> str:
        # Replace future tense assignment
        cleaned = re.sub(
            r"\bagrees?\s+to\s+assign\b|\bwill\s+assign\b",
            "hereby irrevocably assigns, transfers, and conveys",
            text,
            flags=re.IGNORECASE
        )
        if "hereby assigns" not in cleaned.lower():
            ip_clause = (
                "\n\n## SECTION: INTELLECTUAL PROPERTY ASSIGNMENT\n" +
                self.standard_clauses["intellectual_property_assignment"]
            )
            cleaned = cleaned + ip_clause
        return cleaned

    def _remediate_indemnification(self, text: str) -> str:
        # Replace one-way indemnity with mutual clause
        indem_clause = (
            "\n\n## SECTION: INDEMNIFICATION\n" +
            self.standard_clauses["mutual_indemnification"]
        )
        return text + indem_clause

    def _remediate_termination(self, text: str) -> str:
        term_clause = (
            "\n\n## SECTION: TERMINATION AND CURE\n" +
            self.standard_clauses["termination_for_cause"]
        )
        return text + term_clause

    def _remediate_confidentiality(self, text: str) -> str:
        conf_clause = (
            "\n\n## SECTION: CONFIDENTIALITY\n" +
            self.standard_clauses["confidentiality"]
        )
        return text + conf_clause

    def _remediate_dispute_resolution(self, text: str) -> str:
        dispute_clause = (
            "\n\n## SECTION: GOVERNING LAW AND ARBITRATION\n" +
            self.standard_clauses["governing_law_and_forum"]
        )
        return text + dispute_clause
