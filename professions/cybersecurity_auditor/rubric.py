"""
Gabriel Frost's Weighted Cybersecurity & Zero-Trust Rubric
Mathematical, uncompromising evaluation of credentials, injection vectors, deserialization, and transport layer security.
"""

from typing import Dict, Any, List, Optional


class GabrielSecurityRubric:
    """Gabriel Frost's 100-point weighted cybersecurity evaluation rubric."""

    DIMENSIONS: Dict[str, Dict[str, Any]] = {
        "secret_credential_protection": {
            "title": "Secret Management & Credential Protection",
            "weight": 0.25,
            "benchmark": "Zero hardcoded API keys, passwords, private keys, or tokens in source code."
        },
        "injection_defense": {
            "title": "Injection Defense (SQLi, Command, Dynamic Exec)",
            "weight": 0.25,
            "benchmark": "Zero SQL string formatting, zero raw shell=True calls, zero dynamic execution vulnerabilities."
        },
        "deserialization_safety": {
            "title": "Safe Deserialization & Object Hydration",
            "weight": 0.20,
            "benchmark": "Zero un-sandboxed pickle.loads() or unsafe yaml.load() calls."
        },
        "transport_network_hardening": {
            "title": "Transport Layer & Client Isolation",
            "weight": 0.15,
            "benchmark": "Enforced TLS certificate verification; link isolation (rel='noopener noreferrer')."
        },
        "defense_in_depth_hygiene": {
            "title": "Defense-in-Depth & Attack Surface Hygiene",
            "weight": 0.15,
            "benchmark": "Zero cumulative vulnerabilities across all perimeter layers."
        }
    }

    def evaluate(self, metrics: Dict[str, Any], benchmark_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculates itemized and composite security score out of 100."""
        scores: Dict[str, Any] = {}

        # 1. Secret Protection (0-10)
        secrets = metrics.get("secret_leaks", [])
        if len(secrets) == 0:
            s_score = 10.0
        elif len(secrets) == 1:
            s_score = 2.0
        else:
            s_score = 0.0

        scores["secret_credential_protection"] = {
            "score": s_score,
            "measured": f"{len(secrets)} hardcoded secrets detected" if secrets else "Zero hardcoded credentials",
            "benchmark": "Zero credentials in source code",
            "status": "PASS" if s_score >= 8.0 else "FAIL"
        }

        # 2. Injection Defense (0-10)
        injections = metrics.get("injections_found", [])
        if len(injections) == 0:
            i_score = 10.0
        elif len(injections) == 1:
            i_score = 2.0
        else:
            i_score = 0.0

        scores["injection_defense"] = {
            "score": i_score,
            "measured": f"{len(injections)} injection vectors detected" if injections else "Zero injection vectors detected",
            "benchmark": "Zero SQLi, Command Injection, or eval/exec vulnerabilities",
            "status": "PASS" if i_score >= 8.0 else "FAIL"
        }

        # 3. Deserialization Safety (0-10)
        deser = metrics.get("deserialization_flaws", [])
        if len(deser) == 0:
            d_score = 10.0
        elif len(deser) == 1:
            d_score = 2.0
        else:
            d_score = 0.0

        scores["deserialization_safety"] = {
            "score": d_score,
            "measured": f"{len(deser)} deserialization vulnerabilities" if deser else "Zero unsafe deserialization calls",
            "benchmark": "Zero unsafe object hydration calls",
            "status": "PASS" if d_score >= 8.0 else "FAIL"
        }

        # 4. Transport Hardening (0-10)
        transport = metrics.get("transport_flaws", [])
        if len(transport) == 0:
            t_score = 10.0
        elif len(transport) == 1:
            t_score = 6.0
        else:
            t_score = 2.0

        scores["transport_network_hardening"] = {
            "score": t_score,
            "measured": f"{len(transport)} transport flaws" if transport else "Hardened transport & link isolation verified",
            "benchmark": "Enforced TLS and reverse tab-nabbing defenses",
            "status": "PASS" if t_score >= 8.0 else "FAIL"
        }

        # 5. Attack Surface Hygiene (0-10)
        total_vulns = metrics.get("total_vulnerabilities", 0)
        if total_vulns == 0:
            h_score = 10.0
        elif total_vulns == 1:
            h_score = 6.0
        elif total_vulns <= 3:
            h_score = 3.0
        else:
            h_score = 0.0

        scores["defense_in_depth_hygiene"] = {
            "score": h_score,
            "measured": f"{total_vulns} total security defects",
            "benchmark": "Zero cumulative vulnerabilities",
            "status": "PASS" if h_score >= 8.0 else "FAIL"
        }

        # Composite score calculation
        total_score = round(sum(
            scores[dim]["score"] * self.DIMENSIONS[dim]["weight"]
            for dim in self.DIMENSIONS
        ) * 10, 1)

        has_blocker = metrics.get("has_critical_blocker", False)

        return {
            "evaluator": "Gabriel Frost (Principal Cybersecurity Auditor)",
            "total_score": total_score,
            "passing_threshold": 85.0,
            "passed": (total_score >= 85.0 and not has_blocker),
            "dimensions": scores
        }
