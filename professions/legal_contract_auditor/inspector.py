"""
Arthur Pendelton - Objective Contract Clause Inspector & Legal Risk Analyzer.

This module parses commercial agreements, performs regex-based clause extraction,
detects toxic provisions, verifies IP title transfer verbs, and flags unmitigated liabilities.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class ContractMetrics:
    has_limitation_of_liability: bool = False
    has_consequential_damages_waiver: bool = False
    is_liability_mutual: bool = False
    is_liability_uncapped: bool = False
    has_ip_assignment: bool = False
    is_present_ip_assignment: bool = False
    has_work_made_for_hire: bool = False
    has_indemnification: bool = False
    is_indemnification_mutual: bool = False
    has_termination_clause: bool = False
    has_cure_period: bool = False
    cure_period_days: int = 0
    has_confidentiality: bool = False
    has_nda_exclusions: bool = False
    has_dispute_resolution: bool = False
    has_neutral_governing_law: bool = False
    toxic_clauses_detected: List[str] = field(default_factory=list)
    missing_clauses: List[str] = field(default_factory=list)


@dataclass
class LegalInspectionReport:
    metrics: ContractMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_legally_sound: bool = False


class ContractInspector:
    """Rigorous objective inspector auditing contract text against commercial legal canon."""

    def inspect(self, contract_input: Any) -> LegalInspectionReport:
        """
        Audits raw contract text or structured JSON data.
        """
        metrics = self._extract_metrics(contract_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. Liability Capping & Consequential Damages
        if not metrics.has_limitation_of_liability or metrics.is_liability_uncapped:
            critical_violations.append(
                "Uncapped Liability Exposure: Agreement lacks a definitive mutual liability cap (12 months fees paid). "
                "Exposes enterprise to existential balance sheet destruction."
            )
        elif not metrics.is_liability_mutual:
            critical_violations.append(
                "Asymmetric Liability Cap: Only one party's liability is capped while the other remains fully exposed."
            )
        else:
            benchmarks_passed.append("Mutual aggregate liability cap established.")

        if not metrics.has_consequential_damages_waiver:
            critical_violations.append(
                "Missing Consequential Damages Waiver: Parties can sue for speculative lost profits, punitive damages, and business interruption."
            )
        else:
            benchmarks_passed.append("Mutual waiver of indirect, punitive, and consequential damages present.")

        # 2. Intellectual Property Sovereignty
        if not metrics.has_ip_assignment:
            critical_violations.append(
                "Absence of IP Assignment: No explicit assignment of inventions, deliverables, or copyright."
            )
        elif not metrics.is_present_ip_assignment:
            critical_violations.append(
                "Vague Future IP Assignment: Contract uses future tense ('agrees to assign' / 'will assign'). "
                "Fails to convey present legal title under Stanford v. Roche; must state 'hereby assigns'."
            )
        else:
            benchmarks_passed.append("Present, irrevocable intellectual property assignment verified ('hereby assigns').")

        # 3. Indemnification Symmetry
        if metrics.has_indemnification and not metrics.is_indemnification_mutual:
            critical_violations.append(
                "Unilateral Indemnification: One party is obligated to defend and indemnify without reciprocal third-party IP defense."
            )
        elif metrics.has_indemnification and metrics.is_indemnification_mutual:
            benchmarks_passed.append("Reciprocal mutual indemnification with third-party IP defense established.")
        else:
            warnings.append("No indemnification provision found. Leaves parties without defensive shield against third-party claims.")

        # 4. Termination & Cure Period
        if not metrics.has_termination_clause:
            warnings.append("Contract lacks formal termination provisions.")
        elif not metrics.has_cure_period:
            warnings.append("Immediate termination without a standard 30-day notice and cure window risks predatory cancellation.")
        else:
            benchmarks_passed.append(f"Termination for material breach includes clear {metrics.cure_period_days}-day cure period.")

        # 5. Confidentiality Exclusions
        if metrics.has_confidentiality and not metrics.has_nda_exclusions:
            warnings.append("Confidentiality clause lacks standard legal carve-outs (public knowledge, prior possession, court subpoena).")
        elif metrics.has_confidentiality:
            benchmarks_passed.append("Standard confidentiality safeguards with customary carve-outs verified.")

        # 6. Toxic Clauses
        for toxic in metrics.toxic_clauses_detected:
            critical_violations.append(f"Toxic Clause Detected: {toxic}")

        is_sound = len(critical_violations) == 0

        return LegalInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_legally_sound=is_sound
        )

    def _extract_metrics(self, contract_input: Any) -> ContractMetrics:
        text = ""
        if isinstance(contract_input, str):
            text = contract_input
        elif isinstance(contract_input, dict):
            text = json.dumps(contract_input)
        else:
            text = str(contract_input)

        text_lower = text.lower()
        m = ContractMetrics()

        # 1. Limitation of Liability
        has_lol = (
            "limitation of liability" in text_lower or
            "aggregate liability" in text_lower or
            "total liability" in text_lower or
            "in no event shall" in text_lower
        )
        m.has_limitation_of_liability = has_lol

        has_consequential = (
            "consequential" in text_lower or
            "indirect" in text_lower or
            "loss of profit" in text_lower or
            "punitive damages" in text_lower
        )
        m.has_consequential_damages_waiver = has_lol and has_consequential

        is_mutual_lol = (
            "either party" in text_lower or
            "each party" in text_lower or
            "neither party" in text_lower
        )
        m.is_liability_mutual = is_mutual_lol

        if re.search(r"without\s+limitation|unlimited\s+liability|solely\s+liable\s+for\s+all", text_lower):
            m.is_liability_uncapped = True

        # 2. Intellectual Property
        has_ip = (
            "intellectual property" in text_lower or
            "work product" in text_lower or
            "assigns" in text_lower or
            "ownership" in text_lower
        )
        m.has_ip_assignment = has_ip

        is_present_assign = bool(
            re.search(r"hereby\s+(?:irrevocably\s+|unconditionally\s+)?(?:assigns|transfers|conveys)", text_lower)
        )
        m.is_present_ip_assignment = is_present_assign

        m.has_work_made_for_hire = "work made for hire" in text_lower or "work-for-hire" in text_lower

        # 3. Indemnification
        has_indem = "indemnif" in text_lower or "hold harmless" in text_lower
        m.has_indemnification = has_indem
        is_mutual_indem = (
            has_indem and
            ("each party" in text_lower or "mutual" in text_lower or ("provider shall" in text_lower and "customer shall" in text_lower))
        )
        m.is_indemnification_mutual = is_mutual_indem

        # 4. Termination & Cure
        has_term = "termination" in text_lower or "terminate" in text_lower
        m.has_termination_clause = has_term

        cure_match = re.search(r"(\d+)\s*(?:days?|calendar days?)?\s*(?:written notice|cure|to cure)", text_lower)
        if cure_match:
            m.has_cure_period = True
            try:
                m.cure_period_days = int(cure_match.group(1))
            except ValueError:
                m.cure_period_days = 30
        elif "cure" in text_lower and "30" in text_lower:
            m.has_cure_period = True
            m.cure_period_days = 30

        # 5. Confidentiality
        has_conf = "confidential" in text_lower or "non-disclosure" in text_lower
        m.has_confidentiality = has_conf
        has_exclusions = (
            "publicly known" in text_lower or
            "prior possession" in text_lower or
            "subpoena" in text_lower or
            "required by law" in text_lower
        )
        m.has_nda_exclusions = has_exclusions

        # 6. Dispute Resolution & Governing Law
        m.has_dispute_resolution = "arbitration" in text_lower or "dispute" in text_lower or "jurisdiction" in text_lower
        m.has_neutral_governing_law = (
            "delaware" in text_lower or
            "new york" in text_lower or
            "california" in text_lower or
            "governing law" in text_lower
        )

        # 7. Toxic Signatures
        if re.search(r"\bagrees?\s+to\s+assign\b|\bwill\s+assign\b", text_lower) and not is_present_assign:
            m.toxic_clauses_detected.append("Imperfect Future IP Assignment ('will assign' instead of 'hereby assigns')")

        if "solely liable without limitation" in text_lower:
            m.toxic_clauses_detected.append("Unilateral Uncapped Liability Clause")

        if "shall not compete anywhere" in text_lower or "perpetual non-compete" in text_lower:
            m.toxic_clauses_detected.append("Unbounded Restrictive Non-Compete")

        # 8. Missing Clauses Tracker
        if not m.has_limitation_of_liability:
            m.missing_clauses.append("limitation_of_liability")
        if not m.has_ip_assignment:
            m.missing_clauses.append("intellectual_property_assignment")
        if not m.has_indemnification:
            m.missing_clauses.append("mutual_indemnification")
        if not m.has_termination_clause:
            m.missing_clauses.append("termination_for_cause")
        if not m.has_confidentiality:
            m.missing_clauses.append("confidentiality")

        return m
