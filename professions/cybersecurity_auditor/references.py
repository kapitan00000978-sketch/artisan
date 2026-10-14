"""
Gabriel Frost's Empirical Cybersecurity & Zero-Trust Benchmarks
Quantitative security standards derived from OWASP Top 10, NIST SP 800-207, and CWE/SANS Top 25.
Grounds security review in zero-tolerance invariants against credentials in code, injection vulnerabilities, and insecure transports.
"""

from typing import Dict, Any, List


class GabrielSecurityReferences:
    """Gabriel Frost's Curated Empirical Cybersecurity Benchmarks."""

    BENCHMARK_PROFILES: Dict[str, Dict[str, Any]] = {
        "owasp_top_10_production": {
            "name": "OWASP Top 10 Production Defense",
            "description": "Enterprise production baseline ensuring zero critical injection, secret leakage, or deserialization flaws.",
            "metrics": {
                "max_allowed_hardcoded_secrets": 0,
                "max_allowed_injections": 0,
                "max_allowed_dangerous_exec": 0,
                "max_allowed_insecure_deserialization": 0,
                "max_allowed_transport_flaws": 0,
                "requires_parameterized_queries": True,
                "requires_safe_link_isolation": True,
                "requires_tls_verification": True
            }
        },
        "fintech_zero_trust_strict": {
            "name": "Fintech Zero-Trust High-Assurance",
            "description": "Ultra-strict financial grade security: absolute zero trust, verified cryptosystems, externalized secrets.",
            "metrics": {
                "max_allowed_hardcoded_secrets": 0,
                "max_allowed_injections": 0,
                "max_allowed_dangerous_exec": 0,
                "max_allowed_insecure_deserialization": 0,
                "max_allowed_transport_flaws": 0,
                "requires_parameterized_queries": True,
                "requires_safe_link_isolation": True,
                "requires_tls_verification": True
            }
        },
        "api_perimeter_hardened": {
            "name": "Hardened API Perimeter Defense",
            "description": "Defensive API gateway and microservice boundary verification.",
            "metrics": {
                "max_allowed_hardcoded_secrets": 0,
                "max_allowed_injections": 0,
                "max_allowed_dangerous_exec": 0,
                "max_allowed_insecure_deserialization": 0,
                "max_allowed_transport_flaws": 0,
                "requires_parameterized_queries": True,
                "requires_safe_link_isolation": True,
                "requires_tls_verification": True
            }
        }
    }

    def __init__(self, profile_name: str = "owasp_top_10_production"):
        self.profile_name = profile_name
        self.active_profile = self.BENCHMARK_PROFILES.get(
            profile_name,
            self.BENCHMARK_PROFILES["owasp_top_10_production"]
        )

    def get_benchmarks(self) -> Dict[str, Any]:
        """Returns the active quantitative benchmark profile."""
        return self.active_profile

    def get_available_profiles(self) -> List[str]:
        """Lists all security benchmark profiles known to Gabriel."""
        return list(self.BENCHMARK_PROFILES.keys())
