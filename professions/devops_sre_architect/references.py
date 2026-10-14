"""
Gareth Drake's Empirical DevOps & Cloud SRE Benchmarks
Quantitative reliability standards derived from Google SRE, The 12-Factor App, and Chaos Engineering.
Measures container security, health probe coverage, resource limits, and lifecycle idempotency.
"""

from typing import Dict, Any, List


class GarethDevOpsReferences:
    """Gareth Drake's Curated Empirical DevOps Benchmarks."""

    BENCHMARK_PROFILES: Dict[str, Dict[str, Any]] = {
        "production_kubernetes_resilient": {
            "name": "Production Resilient Kubernetes (99.99% SLO)",
            "description": "Hardened container standard: non-root UID, pinned image digests, probes, and resource boundaries.",
            "metrics": {
                "forbid_root_user": True,
                "forbid_unpinned_latest_tag": True,
                "requires_liveness_readiness_probes": True,
                "requires_resource_limits": True,
                "requires_graceful_shutdown": True,
                "requires_script_error_trap": True
            }
        },
        "cloud_native_docker_hardened": {
            "name": "Cloud-Native Hardened Container",
            "description": "Multi-stage Dockerfile with non-root security context, explicit HEALTHCHECK, and pinned tags.",
            "metrics": {
                "forbid_root_user": True,
                "forbid_unpinned_latest_tag": True,
                "requires_liveness_readiness_probes": True,
                "requires_resource_limits": False,
                "requires_graceful_shutdown": True,
                "requires_script_error_trap": True
            }
        },
        "idempotent_ci_cd_pipeline": {
            "name": "Idempotent CI/CD Pipeline Automation",
            "description": "Fail-fast automation with deterministic caching, lockfile enforcement, and automated rollback.",
            "metrics": {
                "forbid_root_user": True,
                "forbid_unpinned_latest_tag": True,
                "requires_liveness_readiness_probes": False,
                "requires_resource_limits": False,
                "requires_graceful_shutdown": False,
                "requires_script_error_trap": True
            }
        }
    }

    def __init__(self, profile_name: str = "production_kubernetes_resilient"):
        self.profile_name = profile_name
        self.active_profile = self.BENCHMARK_PROFILES.get(
            profile_name,
            self.BENCHMARK_PROFILES["production_kubernetes_resilient"]
        )

    def get_benchmarks(self) -> Dict[str, Any]:
        """Returns the active quantitative benchmark profile."""
        return self.active_profile

    def get_available_profiles(self) -> List[str]:
        """Lists all SRE benchmark profiles known to Gareth."""
        return list(self.BENCHMARK_PROFILES.keys())
