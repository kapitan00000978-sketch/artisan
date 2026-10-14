"""
Arthur Pendelton - Commercial Counsel & Contract Auditor Subsystem.
"""

from .references import ContractReferenceLibrary, STANDARD_CLAUSES, TOXIC_CLAUSE_SIGNATURES
from .inspector import ContractInspector, ContractMetrics, LegalInspectionReport
from .rubric import ContractRubric, LegalRubricEvaluation
from .blind_critic import BlindLegalCritic, LegalDefectLedger, LegalDefect
from .elevation_engine import ContractElevationEngine
from .master import ArthurPendeltonMaster

__all__ = [
    "ContractReferenceLibrary",
    "STANDARD_CLAUSES",
    "TOXIC_CLAUSE_SIGNATURES",
    "ContractInspector",
    "ContractMetrics",
    "LegalInspectionReport",
    "ContractRubric",
    "LegalRubricEvaluation",
    "BlindLegalCritic",
    "LegalDefectLedger",
    "LegalDefect",
    "ContractElevationEngine",
    "ArthurPendeltonMaster"
]
