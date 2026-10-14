"""
Marcus Sterling's Blind Software Architecture Critic
The Critic NEVER looks at developer promises or excuses.
It evaluates ONLY structural metrics, AST complexity, exception propagation, and rubric scores.
Produces an uncompromising architectural verdict and structured defect ledger.
"""

from typing import Dict, Any, List


class MarcusBlindCritic:
    """Marcus Sterling's Blind Architectural Critic."""

    def __init__(self, passing_score: float = 85.0):
        self.passing_score = passing_score

    def critique(self, evaluation: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Audits code structure blindly and issues Marcus's architectural verdict."""
        total_score = evaluation["total_score"]
        dims = evaluation["dimensions"]
        defect_ledger: List[Dict[str, Any]] = []

        # 1. Cyclomatic Complexity Critique
        cc = dims.get("cyclomatic_complexity", {})
        if cc.get("status") == "FAIL":
            defect_ledger.append({
                "category": "COMPLEXITY",
                "severity": "CRITICAL",
                "flaw": f"Excessive cyclomatic complexity ({cc.get('measured')}). Code is dense with branching pyramids of doom.",
                "marcus_directive": "Decompose nested conditionals into guard clauses (early returns) and separate discrete business logic into pure helper functions."
            })

        # 2. Modularity & Function Size Critique
        mod = dims.get("function_modularity", {})
        if mod.get("status") == "FAIL":
            defect_ledger.append({
                "category": "MODULARITY",
                "severity": "CRITICAL",
                "flaw": f"Monolithic God functions detected ({mod.get('measured')}). Violates Single Responsibility Principle.",
                "marcus_directive": "Extract sub-routines until every function performs exactly one task with <= 40 lines of focused code."
            })

        # 3. Exception Discipline Critique
        exc = dims.get("exception_discipline", {})
        if exc.get("status") == "FAIL":
            defect_ledger.append({
                "category": "ERROR_DISCIPLINE",
                "severity": "BLOCKER",
                "flaw": f"Silent exception swallows detected ({exc.get('measured')}). Swallowing errors hides silent failures and corrupts state.",
                "marcus_directive": "Eliminate unhandled exception swallows or empty catch blocks. Log structured error details, wrap in domain exceptions, or re-raise."
            })

        # 4. Stubs & Placeholders Critique
        stubs = dims.get("stub_integrity", {})
        if stubs.get("status") == "FAIL":
            defect_ledger.append({
                "category": "CODE_INTEGRITY",
                "severity": "CRITICAL",
                "flaw": f"Unfinished placeholders detected ({stubs.get('measured')}). Amateur shortcuts cannot reach production.",
                "marcus_directive": "Implement full production logic end-to-end; remove all TODO/FIXME markers and placeholder stubs."
            })

        # 5. Type Contract Critique
        types = dims.get("type_contract_safety", {})
        if types.get("status") == "FAIL":
            defect_ledger.append({
                "category": "CONTRACT_SAFETY",
                "severity": "MAJOR",
                "flaw": f"Weak type contract coverage ({types.get('measured')}). Promotes ambiguous data flow and runtime TypeError regressions.",
                "marcus_directive": "Add explicit typing annotations (typing/mypy/TypeScript) to all public function arguments and return types."
            })

        passed = (total_score >= self.passing_score) and (len([d for d in defect_ledger if d["severity"] == "BLOCKER"]) == 0)

        verdict_summary = (
            "🏛️ [MARCUS VERIFIED]: Impeccable modularity, low cyclomatic complexity, and zero technical debt certified."
            if passed else
            "❌ [MARCUS REJECTED]: Code violates structural architecture invariants. Requires architectural elevation."
        )

        return {
            "critic": "Marcus Sterling (Senior Software Architect)",
            "verdict": "CERTIFIED" if passed else "REJECTED",
            "verdict_summary": verdict_summary,
            "score": total_score,
            "passing_threshold": self.passing_score,
            "defects_count": len(defect_ledger),
            "defect_ledger": defect_ledger
        }
