"""
Diana Drake's Blind Copywriting Critic
The Critic NEVER looks at developer prompts or excuses.
It evaluates ONLY reader metrics, Flesch scannability, AI cliche counts, and rubric scores.
Produces an uncompromising conversion verdict and structured defect ledger.
"""

from typing import Dict, Any, List


class DianaBlindCritic:
    """Diana Drake's Blind Copywriting Critic."""

    def __init__(self, passing_score: float = 85.0):
        self.passing_score = passing_score

    def critique(self, evaluation: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Audits copy blindly and issues Diana's direct-response verdict."""
        total_score = evaluation["total_score"]
        dims = evaluation["dimensions"]
        defect_ledger: List[Dict[str, Any]] = []

        # 1. Readability Critique
        flesch = dims.get("flesch_reading_ease", {})
        if flesch.get("status") == "FAIL":
            defect_ledger.append({
                "category": "READABILITY",
                "severity": "CRITICAL",
                "flaw": f"Cognitive drag detected ({flesch.get('measured')}). Sentences are too dense for human scanning.",
                "diana_directive": "Shorten sentences to under 18 words, eliminate academic polysyllabic words, and aim for a 7th-grade reading level."
            })

        # 2. Headline Hook Critique
        hook = dims.get("headline_hook_power", {})
        if hook.get("status") == "FAIL":
            defect_ledger.append({
                "category": "HEADLINE_HOOK",
                "severity": "CRITICAL",
                "flaw": f"Weak or generic headline detected ({hook.get('measured')}). Fails to capture human attention in 3 seconds.",
                "diana_directive": "Replace category label with an outcome-driven hook: [Desired Result] Without [Main Pain Point] in [Timeframe]."
            })

        # 3. AI Cliches Critique
        cliches = dims.get("ai_cliche_purity", {})
        if cliches.get("status") == "FAIL":
            defect_ledger.append({
                "category": "CLICHE_POLLUTION",
                "severity": "BLOCKER",
                "flaw": f"Sterile AI cliches detected ({cliches.get('measured')}). Signals laziness and destroys brand credibility.",
                "diana_directive": "Purge all filler buzzwords ('welcome to', 'in today's world', 'revolutionize', 'seamless'). Replace with concrete nouns and active verbs."
            })

        # 4. CTA Action Critique
        cta = dims.get("cta_action_psychology", {})
        if cta.get("status") == "FAIL":
            defect_ledger.append({
                "category": "CALL_TO_ACTION",
                "severity": "CRITICAL",
                "flaw": f"Passive or timid CTAs found ({cta.get('measured')}). Fails to create momentum.",
                "diana_directive": "Upgrade passive buttons ('Click here', 'Learn more') to value-first verbs ('Start Free', 'Claim Access', 'Launch Experience')."
            })

        # 5. Customer-Centricity Critique
        centricity = dims.get("customer_centricity", {})
        if centricity.get("status") == "FAIL":
            defect_ledger.append({
                "category": "PERSPECTIVE",
                "severity": "MAJOR",
                "flaw": f"Company-absorbed 'We-We-We' bias detected ({centricity.get('measured')}). Reader feels ignored.",
                "diana_directive": "Flip sentences to lead with 'You': transform 'We offer 24/7 backups' into 'You get automatic peace of mind with 24/7 backups'."
            })

        passed = (total_score >= self.passing_score) and (len([d for d in defect_ledger if d["severity"] == "BLOCKER"]) == 0)

        verdict_summary = (
            "✍️ [DIANA VERIFIED]: Razor-sharp clarity, high-velocity hook, customer-centric narrative, and high-intent CTAs certified."
            if passed else
            "❌ [DIANA REJECTED]: Copy suffers from corporate AI blandness and passive inertia. Requires conversion elevation."
        )

        return {
            "critic": "Diana Drake (Direct-Response Copywriter)",
            "verdict": "CERTIFIED" if passed else "REJECTED",
            "verdict_summary": verdict_summary,
            "score": total_score,
            "passing_threshold": self.passing_score,
            "defects_count": len(defect_ledger),
            "defect_ledger": defect_ledger
        }
