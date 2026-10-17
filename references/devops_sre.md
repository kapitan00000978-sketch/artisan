# 🚀 DevOps & SRE Guild Reference
**Lead:** Gareth 'The Unbreakable' Drake (`devops_cloud_architect`)  
**Domain:** Immutable Infrastructure, Zero-Downtime CI/CD, Containerization & Health Probes

---

## 🎯 Core Invariants
1. **Immutable Artifacts:** Build once, deploy anywhere; application containers and packages are immutable and tagged deterministically.
2. **Automated Rollback:** Every deployment pipeline must have automated failure detection and instantaneous rollback.
3. **Graceful Shutdown:** Applications must catch `SIGTERM` / `SIGINT`, stop accepting new traffic, finish in-flight requests, and close connections cleanly.
4. **Health Probes:** Distinct `/healthz` (liveness) and `/readyz` (readiness) endpoints must accurately report system state.

---

## 📋 Quality & Security Checklist
- [ ] Dockerfiles use minimal base images, non-root users, and multi-stage builds.
- [ ] CI pipeline runs full static checks, linting, and automated test suite on every pull request.
- [ ] Environment variables and secrets are injected at runtime via orchestration, never baked into images.
- [ ] Distributed tracing, metrics emission (Prometheus), and structured JSON logging configured.
- [ ] Backup recovery procedures tested with verified RPO (< 5m) and RTO (< 15m) targets.

---

## 🚫 Forbidden Anti-Patterns
- **Manual Server Tweaks:** Modifying production instances via SSH without codifying in IaC (Terraform/Ansible).
- **Latest Tag Deployments:** Deploying `docker:latest` without immutable digest or semantic version pins.
- **Unbuffered Log Output:** Writing unstructured human-only logs to filesystem files without rotation.
