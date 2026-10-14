"""
Gareth Drake's Autonomous DevOps & SRE Elevation Engine
Hardens infrastructure artifacts: injects non-root container contexts, pins version tags,
configures health probes, and registers graceful termination lifecycle traps.
"""

import os
import re
from typing import Dict, Any, List


class GarethElevationEngine:
    """Gareth Drake's SRE & DevOps Elevation Engine."""

    DOCKERFILE_HEALTHCHECK = "HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD wget -qO- http://localhost:8080/healthz || exit 1\n"
    DOCKERFILE_USER = "USER 10001:10001\n"

    def elevate(self, file_path: str) -> str:
        """Applies Gareth's signature SRE hardening directly to the target file."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        elevated = content
        fname = os.path.basename(file_path).lower()
        ext = os.path.splitext(file_path)[1].lower()

        if "dockerfile" in fname:
            elevated = self._elevate_dockerfile(elevated)
        elif ext in (".yaml", ".yml"):
            elevated = self._elevate_yaml(elevated)
        elif ext in (".sh", ".bash"):
            elevated = self._elevate_bash(elevated)
        elif ext == ".ps1":
            elevated = self._elevate_powershell(elevated)
        elif ext in (".py", ".js", ".ts"):
            elevated = self._elevate_service(elevated, ext)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(elevated)

        return elevated

    def _elevate_dockerfile(self, content: str) -> str:
        elevated = content

        # 1. Pin :latest to stable version
        elevated = re.sub(r"(?i)(FROM\s+[a-zA-Z0-9_\-\./]+):latest", r"\1:stable", elevated)
        elevated = re.sub(r"(?i)(FROM\s+node)(?:\s+AS|\s*$)", r"\1:20-alpine", elevated)
        elevated = re.sub(r"(?i)(FROM\s+python)(?:\s+AS|\s*$)", r"\1:3.12-slim", elevated)

        # 2. Inject HEALTHCHECK and USER before the container CMD or ENTRYPOINT
        has_health = "HEALTHCHECK" in elevated
        has_user = bool(re.search(r"(?m)^\s*USER\s+", elevated))

        injection = ""
        if not has_health:
            injection += self.DOCKERFILE_HEALTHCHECK
        if not has_user:
            injection += self.DOCKERFILE_USER

        if injection:
            if re.search(r"(?m)^(CMD|ENTRYPOINT)\s+", elevated):
                elevated = re.sub(r"(?m)^(CMD|ENTRYPOINT)\s+", f"{injection}\\1 ", elevated, count=1)
            else:
                elevated += f"\n{injection}"

        return elevated

    def _elevate_yaml(self, content: str) -> str:
        elevated = content
        # Inject resources if missing
        if "resources:" not in elevated:
            res_block = """
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
          requests:
            memory: "128Mi"
            cpu: "100m"
"""
            elevated += res_block

        # Inject probes if missing
        if "livenessProbe" not in elevated:
            probe_block = """
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
"""
            elevated += probe_block

        # Inject non-root securityContext if missing
        if "securityContext:" not in elevated:
            sec_block = """
        securityContext:
          runAsNonRoot: true
          runAsUser: 10001
"""
            elevated += sec_block

        return elevated

    def _elevate_bash(self, content: str) -> str:
        if "set -e" not in content and "set -euo pipefail" not in content:
            if content.startswith("#!"):
                lines = content.splitlines()
                lines.insert(1, "set -euo pipefail")
                return "\n".join(lines) + "\n"
            else:
                return "set -euo pipefail\n" + content
        return content

    def _elevate_powershell(self, content: str) -> str:
        if "$ErrorActionPreference" not in content:
            return "$ErrorActionPreference = 'Stop'\n" + content
        return content

    def _elevate_service(self, content: str, ext: str) -> str:
        elevated = content
        if ext == ".py":
            # Add healthz endpoint if missing
            if "/healthz" not in elevated and "/health" not in elevated:
                health_py = """
# ⚡ Healthcheck endpoint for Kubernetes liveness & readiness
def healthz():
    return {"status": "ok", "uptime": "healthy"}
"""
                elevated += health_py

            # Add SIGTERM signal handler if missing
            if "SIGTERM" not in elevated:
                sig_py = """
import signal
import sys

def _graceful_shutdown(sig, frame):
    sys.stderr.write("Gracefully shutting down on SIGTERM\\n")
    sys.exit(0)

signal.signal(signal.SIGTERM, _graceful_shutdown)
"""
                elevated = sig_py + "\n" + elevated

        return elevated
