"""
Gabriel Frost's Blind Cybersecurity Critic
The Critic NEVER looks at developer excuses or internal network justifications.
It evaluates ONLY detected vulnerability metrics, attack surfaces, and zero-trust rubrics.
Produces an uncompromising security verdict and structured defect ledger.
"""

from typing import Dict, Any, List


class GabrielBlindCritic:
    """Gabriel Frost's Blind Cybersecurity Critic."""

    def __init__(self, passing_score: float = 85.0):
        self.passing_score = passing_score

    def critique(self, evaluation: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Audits security posture blindly and issues Gabriel's zero-trust verdict."""
        total_score = evaluation["total_score"]
        dims = evaluation["dimensions"]
        defect_ledger: List[Dict[str, Any]] = []

        # 1. Secret Leakage Critique
        sec = dims.get("secret_credential_protection", {})
        if sec.get("status") == "FAIL":
            for leak in metrics.get("secret_leaks", []):
                defect_ledger.append({
                    "category": "CREDENTIAL_EXPOSURE",
                    "severity": "BLOCKER",
                    "flaw": leak["pattern_desc"],
                    "gabriel_directive": "Immediately revoke and rotate leaked credential. Externalize to hardened environment variable (os.environ.get) or secrets vault."
                })

        # 2. Injection Defense Critique
        inj = dims.get("injection_defense", {})
        if inj.get("status") == "FAIL":
            for item in metrics.get("injections_found", []):
                defect_ledger.append({
                    "category": "INJECTION_ATTACK_SURFACE",
                    "severity": "BLOCKER",
                    "flaw": item["pattern_desc"],
                    "gabriel_directive": "Eliminate dynamic string interpolation. Parameterize queries completely (cursor.execute('... WHERE id = %s', (id,))) or remove shell=True."
                })

        # 3. Deserialization Safety Critique
        deser = dims.get("deserialization_safety", {})
        if deser.get("status") == "FAIL":
            for item in metrics.get("deserialization_flaws", []):
                defect_ledger.append({
                    "category": "INSECURE_DESERIALIZATION",
                    "severity": "BLOCKER",
                    "flaw": item["pattern_desc"],
                    "gabriel_directive": "Never deserialize untrusted data with pickle.loads(). Use safe JSON parsing or yaml.safe_load()."
                })

        # 4. Transport Hardening Critique
        trans = dims.get("transport_network_hardening", {})
        if trans.get("status") == "FAIL":
            for item in metrics.get("transport_flaws", []):
                defect_ledger.append({
                    "category": "TRANSPORT_EXPOSURE",
                    "severity": "CRITICAL",
                    "flaw": item["pattern_desc"],
                    "gabriel_directive": "Enforce verified TLS (verify=True). Add rel='noopener noreferrer' to all target='_blank' hyperlinks."
                })

        has_blocker = any(d["severity"] == "BLOCKER" for d in defect_ledger)
        passed = (total_score >= self.passing_score) and not has_blocker

        verdict_summary = (
            "🛡️ [GABRIEL VERIFIED]: Defense-in-depth validated. Zero hardcoded secrets, zero injection vectors, and verified transport certified."
            if passed else
            "❌ [GABRIEL REJECTED]: Critical vulnerabilities and attack surface exposures detected. Immediate security hardening required."
        )

        return {
            "critic": "Gabriel Frost (Principal Cybersecurity Auditor)",
            "verdict": "CERTIFIED" if passed else "REJECTED",
            "verdict_summary": verdict_summary,
            "score": total_score,
            "passing_threshold": self.passing_score,
            "defects_count": len(defect_ledger),
            "defect_ledger": defect_ledger
        }
