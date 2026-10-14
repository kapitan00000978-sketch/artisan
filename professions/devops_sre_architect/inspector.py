"""
Gareth Drake's DevOps & SRE Inspector
Deep empirical reliability inspector for Dockerfiles, Kubernetes manifests, CI/CD pipelines, and cloud services.
Measures non-root isolation, health probes, resource limits, dependency pinning, and graceful shutdown.
"""

import os
import re
from typing import Dict, Any, List, Optional


class GarethDevOpsInspector:
    """Gareth Drake's Site Reliability & Infrastructure Inspection Engine."""

    def __init__(self, target_file: str):
        self.target_file = os.path.abspath(target_file)

    def inspect(self) -> Dict[str, Any]:
        """
        Executes an objective, deep SRE inspection:
        - Non-root container security context
        - Deterministic image pinning (forbids :latest)
        - Liveness, readiness, and container HEALTHCHECK probes
        - CPU/Memory resource boundaries
        - Graceful SIGTERM lifecycle handling
        - Shell script error traps
        """
        metrics: Dict[str, Any] = {
            "target": self.target_file,
            "file_type": "unknown",
            "has_non_root_user": True,
            "has_unpinned_latest_tag": False,
            "has_healthcheck": True,
            "has_resource_limits": True,
            "has_graceful_shutdown": True,
            "has_script_error_trap": True,
            "flaws_detected": []
        }

        if not os.path.exists(self.target_file):
            metrics["error"] = f"File {self.target_file} does not exist"
            return metrics

        fname = os.path.basename(self.target_file).lower()
        ext = os.path.splitext(self.target_file)[1].lower()

        try:
            with open(self.target_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if "dockerfile" in fname:
                metrics["file_type"] = "dockerfile"
                self._inspect_dockerfile(content, metrics)
            elif ext in (".yaml", ".yml"):
                metrics["file_type"] = "kubernetes_or_compose_yaml"
                self._inspect_yaml(content, metrics)
            elif ext in (".sh", ".bash"):
                metrics["file_type"] = "bash_script"
                self._inspect_bash(content, metrics)
            elif ext == ".ps1":
                metrics["file_type"] = "powershell_script"
                self._inspect_powershell(content, metrics)
            elif ext in (".py", ".js", ".ts"):
                metrics["file_type"] = "service_application"
                self._inspect_service(content, metrics)
            else:
                metrics["file_type"] = "generic_infra"
                self._inspect_dockerfile(content, metrics)

        except Exception as e:
            metrics["inspection_error"] = str(e)

        return metrics

    def _inspect_dockerfile(self, content: str, metrics: Dict[str, Any]):
        """Inspects Dockerfile reliability and security invariants."""
        # 1. Non-root user
        user_matches = re.findall(r"^\s*USER\s+([^\s\n]+)", content, re.MULTILINE)
        if not user_matches or any(u.lower() in ("root", "0") for u in user_matches):
            metrics["has_non_root_user"] = False
            metrics["flaws_detected"].append("Dockerfile runs as root: missing explicit non-root USER instruction")

        # 2. Unpinned latest tag
        from_matches = re.findall(r"^\s*FROM\s+([^\s\n]+)", content, re.MULTILINE)
        for img in from_matches:
            if ":latest" in img.lower() or ":" not in img:
                metrics["has_unpinned_latest_tag"] = True
                metrics["flaws_detected"].append(f"Unpinned base image tag: '{img}' risks broken builds")

        # 3. Healthcheck
        if not re.search(r"^\s*HEALTHCHECK\s+", content, re.MULTILINE):
            metrics["has_healthcheck"] = False
            metrics["flaws_detected"].append("Missing HEALTHCHECK directive in Dockerfile")

    def _inspect_yaml(self, content: str, metrics: Dict[str, Any]):
        """Inspects Kubernetes or Docker Compose YAML manifests."""
        # Check resources
        if "limits:" not in content and "resources:" not in content:
            metrics["has_resource_limits"] = False
            metrics["flaws_detected"].append("Missing CPU and Memory resource limits: vulnerable to OOM kills")

        # Check probes
        if "livenessProbe" not in content and "readinessProbe" not in content and "healthcheck:" not in content:
            metrics["has_healthcheck"] = False
            metrics["flaws_detected"].append("Missing livenessProbe or readinessProbe in container manifest")

        # Check non-root
        if "runAsNonRoot" not in content and "runAsUser" not in content and "user:" not in content:
            metrics["has_non_root_user"] = False
            metrics["flaws_detected"].append("Missing runAsNonRoot securityContext in container definition")

    def _inspect_bash(self, content: str, metrics: Dict[str, Any]):
        """Inspects Bash shell deployment scripts."""
        if not re.search(r"set\s+-(?:[a-zA-Z]*e[a-zA-Z]*)", content):
            metrics["has_script_error_trap"] = False
            metrics["flaws_detected"].append("Bash script missing 'set -e' or 'set -euo pipefail' fail-fast error trap")

    def _inspect_powershell(self, content: str, metrics: Dict[str, Any]):
        """Inspects PowerShell deployment scripts."""
        if "$ErrorActionPreference" not in content:
            metrics["has_script_error_trap"] = False
            metrics["flaws_detected"].append("PowerShell script missing $ErrorActionPreference = 'Stop' trap")

    def _inspect_service(self, content: str, metrics: Dict[str, Any]):
        """Inspects backend service entry points for health routes and signal handling."""
        # Health endpoint
        has_health_route = bool(re.search(r"['\"]/(?:health|healthz|livez|status)['\"]", content))
        if not has_health_route:
            metrics["has_healthcheck"] = False
            metrics["flaws_detected"].append("Web service missing standard /health or /healthz probe endpoint")

        # Graceful shutdown
        has_signal = bool(re.search(r"SIGTERM|SIGINT|signal\.signal|process\.on\(['\"]SIG", content))
        if not has_signal:
            metrics["has_graceful_shutdown"] = False
            metrics["flaws_detected"].append("Missing graceful termination handler for SIGTERM process signals")
