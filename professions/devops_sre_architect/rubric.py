"""
Gareth Drake's Weighted SRE & DevOps Rubric
Mathematical, operational evaluation of container isolation, health probes, resource limits, and lifecycle idempotency.
"""

from typing import Dict, Any, List, Optional


class GarethDevOpsRubric:
    """Gareth Drake's 100-point weighted DevOps & SRE evaluation rubric."""

    DIMENSIONS: Dict[str, Dict[str, Any]] = {
        "container_security_nonroot": {
            "title": "Container Security & Non-Root Context",
            "weight": 0.25,
            "benchmark": "Explicit non-root user (USER non-root or runAsNonRoot: true); zero root containers."
        },
        "health_probes_diagnostics": {
            "title": "Health Probes & Liveness Diagnostics",
            "weight": 0.25,
            "benchmark": "Presence of HEALTHCHECK directive, liveness/readiness probes, or /healthz endpoint."
        },
        "resource_boundaries_oom": {
            "title": "Resource Boundaries & OOM Prevention",
            "weight": 0.20,
            "benchmark": "Explicit CPU and Memory resource limits configured to prevent noisy-neighbor crashes."
        },
        "dependency_pinning_determinism": {
            "title": "Image Tag Pinning & Determinism",
            "weight": 0.15,
            "benchmark": "Zero unpinned :latest tags; explicit version tags or SHA256 digests."
        },
        "lifecycle_idempotency": {
            "title": "Graceful Lifecycle & Script Idempotency",
            "weight": 0.15,
            "benchmark": "Graceful SIGTERM shutdown handlers; fail-fast error traps (set -e or $ErrorActionPreference)."
        }
    }

    def evaluate(self, metrics: Dict[str, Any], benchmark_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculates itemized and composite SRE reliability score out of 100."""
        scores: Dict[str, Any] = {}

        # 1. Non-Root Context (0-10)
        has_nonroot = metrics.get("has_non_root_user", True)
        nr_score = 10.0 if has_nonroot else 2.0
        scores["container_security_nonroot"] = {
            "score": nr_score,
            "measured": "Non-root user isolation certified" if has_nonroot else "Runs as root (UID 0)",
            "benchmark": "Explicit non-root execution context",
            "status": "PASS" if nr_score >= 8.0 else "FAIL"
        }

        # 2. Health Probes (0-10)
        has_health = metrics.get("has_healthcheck", True)
        h_score = 10.0 if has_health else 2.0
        scores["health_probes_diagnostics"] = {
            "score": h_score,
            "measured": "Healthcheck / liveness probes certified" if has_health else "Missing healthcheck or liveness probe",
            "benchmark": "Container HEALTHCHECK or /healthz endpoint present",
            "status": "PASS" if h_score >= 8.0 else "FAIL"
        }

        # 3. Resource Limits (0-10)
        has_res = metrics.get("has_resource_limits", True)
        res_score = 10.0 if has_res else 4.0
        scores["resource_boundaries_oom"] = {
            "score": res_score,
            "measured": "Resource boundaries configured" if has_res else "Missing CPU/Memory limits (OOM risk)",
            "benchmark": "Explicit container resource limits",
            "status": "PASS" if res_score >= 8.0 else "FAIL"
        }

        # 4. Dependency Pinning (0-10)
        unpinned = metrics.get("has_unpinned_latest_tag", False)
        pin_score = 10.0 if not unpinned else 3.0
        scores["dependency_pinning_determinism"] = {
            "score": pin_score,
            "measured": "Pinned deterministic versions" if not unpinned else "Unpinned :latest tag detected",
            "benchmark": "Zero unpinned tags",
            "status": "PASS" if pin_score >= 8.0 else "FAIL"
        }

        # 5. Lifecycle Idempotency (0-10)
        has_shutdown = metrics.get("has_graceful_shutdown", True)
        has_trap = metrics.get("has_script_error_trap", True)
        if has_shutdown and has_trap:
            life_score = 10.0
        elif has_shutdown or has_trap:
            life_score = 6.0
        else:
            life_score = 2.0

        scores["lifecycle_idempotency"] = {
            "score": life_score,
            "measured": f"SIGTERM Handler: {has_shutdown}, Script Trap: {has_trap}",
            "benchmark": "SIGTERM graceful termination + fail-fast error traps",
            "status": "PASS" if life_score >= 8.0 else "FAIL"
        }

        # Composite calculation
        total_score = round(sum(
            scores[dim]["score"] * self.DIMENSIONS[dim]["weight"]
            for dim in self.DIMENSIONS
        ) * 10, 1)

        return {
            "evaluator": "Gareth Drake (DevOps & Cloud SRE Architect)",
            "total_score": total_score,
            "passing_threshold": 85.0,
            "passed": total_score >= 85.0,
            "dimensions": scores
        }
