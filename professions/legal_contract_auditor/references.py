"""
Arthur Pendelton - Commercial Contract Reference Standards & Legal Canon.

This module codifies empirical legal benchmarks, standardized institutional clauses,
and toxic provision signatures across commercial technology contracts (MSAs, SOWs, IP Agreements, NDAs).
"""

from typing import Dict, Any, List


STANDARD_CLAUSES: Dict[str, str] = {
    "limitation_of_liability": (
        "IN NO EVENT SHALL EITHER PARTY BE LIABLE TO THE OTHER FOR ANY INDIRECT, INCIDENTAL, "
        "SPECIAL, CONSEQUENTIAL, PUNITIVE, OR EXEMPLARY DAMAGES, INCLUDING LOSS OF PROFITS, "
        "REVENUE, DATA, OR BUSINESS INTERRUPTION, ARISING OUT OF OR IN CONNECTION WITH THIS AGREEMENT. "
        "EACH PARTY'S AGGREGATE LIABILITY ARISING UNDER OR RELATED TO THIS AGREEMENT SHALL BE STRICTLY "
        "LIMITED TO THE TOTAL FEES ACTUALLY PAID OR PAYABLE BY CUSTOMER TO PROVIDER IN THE TWELVE (12) "
        "MONTHS IMMEDIATELY PRECEDING THE EVENT GIVING RISE TO LIABILITY."
    ),
    "intellectual_property_assignment": (
        "Provider hereby irrevocably assigns, transfers, and conveys to Customer all worldwide right, "
        "title, and interest in and to all Work Product, deliverables, inventions, discoveries, designs, "
        "copyrights, patents, and trade secrets developed, authored, or created under this Agreement. "
        "To the extent any Work Product qualifies as a 'work made for hire' under United States copyright "
        "law, it shall be deemed such. Provider agrees to execute all formal documentation necessary "
        "to confirm or perfect Customer's sole and exclusive ownership."
    ),
    "mutual_indemnification": (
        "Each party ('Indemnifying Party') shall defend, indemnify, and hold harmless the other party "
        "and its officers, directors, employees, and agents from and against any third-party claims, "
        "demands, suits, liabilities, damages, or costs (including reasonable attorneys' fees) arising "
        "out of: (a) any allegation that the Indemnifying Party's technology, materials, or deliverables "
        "infringe or misappropriate any third party's valid patent, copyright, or trademark; or (b) the "
        "Indemnifying Party's gross negligence or willful misconduct."
    ),
    "termination_for_cause": (
        "Either party may terminate this Agreement immediately upon written notice if the other party: "
        "(a) materially breaches any provision of this Agreement and fails to cure such breach within "
        "thirty (30) days after receipt of written notice specifying the breach; or (b) becomes insolvent, "
        "enters bankruptcy proceedings, or executes an assignment for the benefit of creditors."
    ),
    "confidentiality": (
        "Each party agrees to safeguard the other party's Confidential Information with the same degree "
        "of care it uses for its own confidential materials (and no less than reasonable care), and "
        "shall not disclose such information to any third party for a period of three (3) years following "
        "termination, provided that trade secrets shall remain protected for so long as they retain "
        "trade secret status under applicable law. Confidential Information shall not include information "
        "that is or becomes publicly known through no breach of this Agreement."
    ),
    "governing_law_and_forum": (
        "This Agreement shall be governed by and construed in accordance with the laws of the State of "
        "Delaware, without regard to its conflict of law principles. Any dispute, controversy, or claim "
        "arising out of or relating to this Agreement shall be settled by binding arbitration administered "
        "by the American Arbitration Association (AAA) in accordance with its Commercial Arbitration Rules."
    )
}

TOXIC_CLAUSE_SIGNATURES: List[Dict[str, str]] = [
    {
        "id": "uncapped_unilateral_liability",
        "pattern": r"(?:customer|provider|contractor)\s+shall\s+be\s+solely\s+liable\s+without\s+limitation",
        "description": "Unilateral uncapped liability exposes the company to catastrophic existential damages.",
        "severity": "FATAL"
    },
    {
        "id": "vague_future_ip_assignment",
        "pattern": r"\bagrees?\s+to\s+assign\b|\bwill\s+assign\b",
        "description": "Future promise to assign ('will assign') fails to transfer present legal title under Stanford v. Roche.",
        "severity": "FATAL"
    },
    {
        "id": "one_way_indemnification",
        "pattern": r"(?:contractor|vendor|customer)\s+shall\s+defend\s+and\s+indemnify\s+(?:the\s+other|company)",
        "description": "One-sided indemnification creates an asymmetric liability black hole.",
        "severity": "HIGH"
    },
    {
        "id": "omitted_consequential_waiver",
        "pattern": r"missing_consequential_waiver",
        "description": "Absence of mutual consequential damages waiver allows speculative claims for lost profits.",
        "severity": "FATAL"
    },
    {
        "id": "hostile_arbitrary_termination",
        "pattern": r"terminate\s+immediately\s+without\s+(?:cause|notice|cure)",
        "description": "Immediate termination without a standard 30-day cure period permits predatory contract cancellation.",
        "severity": "HIGH"
    },
    {
        "id": "indefinite_non_compete",
        "pattern": r"shall\s+not\s+(?:engage|compete)\s+(?:anywhere|globally|in\s+perpetuity)",
        "description": "Unbounded non-compete covenants restrict corporate mobility and may trigger antitrust/enforceability litigation.",
        "severity": "HIGH"
    }
]

BENCHMARK_METRICS: Dict[str, Any] = {
    "recommended_liability_cap_months": 12,
    "standard_cure_period_days": 30,
    "standard_confidentiality_years": 3,
    "acceptable_governing_jurisdictions": ["Delaware", "New York", "California", "England and Wales"]
}


class ContractReferenceLibrary:
    """Provides empirical legal benchmarks and institutional clause definitions."""

    @staticmethod
    def get_standard_clauses() -> Dict[str, str]:
        return STANDARD_CLAUSES

    @staticmethod
    def get_toxic_signatures() -> List[Dict[str, str]]:
        return TOXIC_CLAUSE_SIGNATURES

    @staticmethod
    def get_benchmark_metrics() -> Dict[str, Any]:
        return BENCHMARK_METRICS
