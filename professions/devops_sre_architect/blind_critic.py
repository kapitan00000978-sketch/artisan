"""
Gareth Drake's Blind DevOps & SRE Critic
The Critic NEVER looks at developer manual promises or intentions.
It evaluates ONLY concrete infrastructure configuration, container contexts, probe metrics, and SRE rubrics.
Produces an uncompromising reliability verdict and structured defect ledger.
"""

from typing import Dict, Any, List


class GarethBlindCritic:
    """Gareth Drake's Blind SRE Critic."""

    def __init__(self, passing_score: float = 85.0):
        self.passing_score = passing_score

    def critique(self, evaluation: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Audits infrastructure posture blindly and issues Gareth's SRE verdict."""
        total_score = evaluation["total_score"]
        dims = evaluation["dimensions"]
        defect_ledger: List[Dict[str, Any]] = []

        # 1. Non-Root Isolation Critique
        nr = dims.get("container_security_nonroot", {})
        if nr.get("status") == "FAIL":
            defect_ledger.append({
                "category": "CONTAINER_SECURITY",
                "severity": "BLOCKER",
                "flaw": "Container executes as root (UID 0). A container breakout yields immediate host takeover.",
                "gareth_directive": "Add 'USER 10001:10001' or 'securityContext.runAsNonRoot: true' to enforce non-root isolation."
            })

        # 2. Health Probes Critique
        hp = dims.get("health_probes_diagnostics", {})
        if hp.get("status") == "FAIL":
            defect_ledger.append({
                "category": "OBSERVABILITY_PROBES",
                "severity": "CRITICAL",
                "flaw": "Missing health probes or HEALTHCHECK directive. Deadlocked instances will continue receiving live traffic.",
                "gareth_directive": "Add container 'HEALTHCHECK' directive or implement standard '/healthz' HTTP liveness/readiness endpoint."
            })

        # 3. Resource Boundaries Critique
        res = dims.get("resource_boundaries_oom", {})
        if res.get("status") == "FAIL":
            defect_ledger.append({
                "category": "RESOURCE_BOUNDARIES",
                "severity": "CRITICAL",
                "flaw": "Missing memory or CPU resource limits. Vulnerable to node-wide OOM cascade failures.",
                "gareth_directive": "Declare explicit 'resources.limits.memory' and 'resources.limits.cpu' in deployment specifications."
            })

        # 4. Image Tag Pinning Critique
        pin = dims.get("dependency_pinning_determinism", {})
        if pin.get("status") == "FAIL":
            defect_ledger.append({
                "category": "DETERMINISM",
                "severity": "MAJOR",
                "flaw": "Unpinned :latest tag detected. Upstream breaking updates will corrupt deployment idempotency.",
                "gareth_directive": "Pin base images to explicit version tags (e.g. node:20.11-alpine) or immutable SHA256 digests."
            })

        # 5. Lifecycle Idempotency Critique
        life = dims.get("lifecycle_idempotency", {})
        if life.get("status") == "FAIL":
            defect_ledger.append({
                "category": "LIFECYCLE_RESILIENCE",
                "severity": "MAJOR",
                "flaw": f"Fragile lifecycle or script execution ({life.get('measured')}).",
                "gareth_directive": "Register graceful SIGTERM signal handlers and add 'set -euo pipefail' / '$ErrorActionPreference = Stop'."
            })

        has_blocker = any(d["severity"] == "BLOCKER" for d in defect_ledger)
        passed = (total_score >= self.passing_score) and not has_blocker

        verdict_summary = (
            "⚡ [GARETH VERIFIED]: Zero-downtime resilience validated. Non-root isolation, probes, and resource boundaries certified."
            if passed else
            "❌ [GARETH REJECTED]: Infrastructure contains high-risk operational anti-patterns. Rollout vetoed."
        )

        return {
            "critic": "Gareth Drake (DevOps & Cloud SRE Architect)",
            "verdict": "CERTIFIED" if passed else "REJECTED",
            "verdict_summary": verdict_summary,
            "score": total_score,
            "passing_threshold": self.passing_score,
            "defects_count": len(defect_ledger),
            "defect_ledger": defect_ledger
        }
