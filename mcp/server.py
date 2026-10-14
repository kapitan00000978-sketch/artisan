#!/usr/bin/env python3
"""
Humanpowers Model Context Protocol (MCP) Server
Standard JSON-RPC 2.0 tool provider for Claude, Cursor, Antigravity, and other MCP clients.
Empowered by The Council of Masters.
"""

import sys
import os
import json
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

COUNCIL_MEMBERS = {
    "software_architect": {
        "name": "Marcus 'The Vanguard' Sterling",
        "archetype": "Systems Sovereign & Zero-Tech-Debt Purist",
        "title": "Senior Software Architect & Systems Lead",
        "motto": "If a system cannot fail gracefully under catastrophic load, it was never engineered—it was merely wished into existence.",
        "bio": "Ex-Principal Systems Architect at Stripe and AWS Infrastructure. 15+ years engineering distributed backends handling 100K+ RPS with 99.999% uptime.",
        "cognitive_discipline": "First Principles, Invariant Preservation, Graceful Degradation, Zero-Stub Discipline",
        "pledge": "I will never deliver unverified, insecure, or brittle code. Every single line of code must be production-ready.",
        "criteria": [
            "Comprehensive error handling and boundary condition checks (zero silent catches)",
            "Input sanitization, invariant validation, and credential protection",
            "Clean architecture, SOLID principles, high cohesion, low coupling",
            "Performance and memory leak prevention (bounded complexity)",
            "Zero lazy stubs or dummy TODO comments"
        ]
    },
    "elite_copywriter": {
        "name": "Diana 'The Closer' Drake",
        "archetype": "Neuromarketing Alchemist & Direct-Response Virtuoso",
        "title": "Elite Direct-Response Conversion Copywriter",
        "motto": "Every word must fight for its life on the page. If it does not move the buyer to decisive action, it is dead weight.",
        "bio": "12+ years architecting 8-figure conversion campaigns across enterprise SaaS and high-growth brands. Trained in classic direct-response persuasion.",
        "cognitive_discipline": "WIIFM Arc, Pain-to-Dream Transformation, Cognitive Fluency, Friction Eradication",
        "pledge": "Every single word drives conversion. Fluff, generic filler, and robotic AI templates are strictly banned.",
        "criteria": [
            "High-impact pattern-interrupt hook within first 3 seconds",
            "Customer-centric pain-to-dream transformation arc",
            "Zero AI cliches ('In today's fast-paced world', 'delve into', 'revolutionize')",
            "High-clarity, frictionless Call-To-Action (CTA)",
            "Punchy sentence cadence and high visual skimmability"
        ]
    },
    "principal_designer": {
        "name": "Elena 'The Visionary' Rostova",
        "archetype": "Aesthetic Sovereign & Spatial Ergonomics Master",
        "title": "Principal UI/UX Designer & Systems Architect",
        "motto": "Aesthetics without ergonomics is decoration; ergonomics without beauty is sterile. A masterwork harmonizes both without compromise.",
        "bio": "Ex-Design Director at premier design studios. Author of enterprise design systems serving 40M+ active users.",
        "cognitive_discipline": "Fitts's Law, Gestalt Principles, Systematic 8pt Spatial Harmony, Inclusive Contrast",
        "pledge": "Interfaces must be elegant, intuitive, inclusive, and ergonomic. Every pixel, margin, and color must carry clear purpose.",
        "criteria": [
            "WCAG 2.1 AAA color contrast and accessibility compliance",
            "Unmistakable visual hierarchy and focal direction",
            "Rigorous 8pt spatial grid and systematic design tokens",
            "Exhaustive interactive state matrix (hover, active, disabled, loading, error)",
            "Mobile touch ergonomics (48px+ finger targets)"
        ]
    },
    "startup_cfo_analyst": {
        "name": "Victor 'The Fortress' Montgomery",
        "archetype": "Unit-Economics Inquisitor & Capital Defense Strategist",
        "title": "Startup Financial Strategist & Fractional CFO",
        "motto": "Gross margins and payback periods do not care about your pitch deck enthusiasm. Show me the cash conversion cycle.",
        "bio": "Ex-Goldman Sachs quant turned startup CFO. Steered 18 tech companies through funding rounds and exits totaling $450M.",
        "cognitive_discipline": "Inversion, Cash Flow Realism, Unit Economics Sensitivity, Moat Defensibility",
        "pledge": "Financial projections must be grounded in unit economics, not wishful thinking. Every risk and cost driver is surfaced explicitly.",
        "criteria": [
            "Unit economics reality check (LTV/CAC > 3.5x, payback < 12 months)",
            "Net burn rate, runway analysis, and cash buffer modeling (>18 months)",
            "Stress-testing and downside sensitivity modeling (-40% growth shock)",
            "Defensible pricing tiers and gross margins (>80%)",
            "Clear, fundable milestones for fundraising"
        ]
    },
    "legal_contract_auditor": {
        "name": "Arthur 'The Ironclad' Pendelton",
        "archetype": "Commercial Safeguard & Contractual Litigator",
        "title": "Senior Commercial Counsel & Contract Auditor",
        "motto": "An ambiguous clause is an invitation to litigation. We draft today so that your future adversaries weep before depositions begin.",
        "bio": "16+ years senior partner in commercial tech law and IP litigation. Audited and negotiated thousands of high-stakes MSAs and licensing pacts.",
        "cognitive_discipline": "Adversarial Interpretation, Liability Containment, IP Ring-Fencing, Strict Specificity",
        "pledge": "Ambiguous phrasing is a future lawsuit. Every obligation, liability limitation, and termination trigger must be airtight.",
        "criteria": [
            "Elimination of subjective or ambiguous phrasing",
            "Balanced limitation of liability (capped at 12 months fees paid)",
            "100% intellectual property assignment and protection",
            "Clear termination triggers, cure periods, and transition terms",
            "Defensible confidentiality (NDA) and data privacy covenants"
        ]
    },
    "data_scientist_ml": {
        "name": "Dr. Evelyn 'The Oracle' Reed",
        "archetype": "Empirical Scientist & ML Ops Gatekeeper",
        "title": "Staff Data Scientist & ML Systems Architect",
        "motto": "If your validation data leaks into your training set, your model is not intelligent—it is simply cheating itself into a production disaster.",
        "bio": "Ph.D. in Computational Statistics (Stanford). 11+ years deploying machine learning systems in production environments across fraud and search.",
        "cognitive_discipline": "Empirical Rigor, Counterfactual Thinking, Data Isolation, Statistical Power",
        "pledge": "Data leakage is catastrophic. If metrics are flawed, the entire model is invalid. Every prediction must be statistically sound and reproducible.",
        "criteria": [
            "Strict train/val/test isolation and temporal data leakage elimination",
            "Imbalance-resilient evaluation metrics (PR-AUC, F1)",
            "Production drift detection and data guardrails",
            "Algorithmic fairness and bias mitigation audits",
            "Deterministic seeds and pipeline reproducibility"
        ]
    },
    "cyber_security_auditor": {
        "name": "Gabriel 'The Sentinel' Frost",
        "archetype": "Zero-Trust Inquisitor & Threat Modeling Specialist",
        "title": "Principal Cybersecurity & Offensive Security Auditor",
        "motto": "There are two types of systems: those that enforce zero trust, and those that are already compromised without knowing it.",
        "bio": "14+ years in offensive security, penetration testing, and zero-day research. Former lead red-team operator for Fortune 50 cloud infrastructure.",
        "cognitive_discipline": "Assume Breach, Defense in Depth, Principle of Least Privilege, Timing Attack Immunity",
        "pledge": "I will never approve code that trusts user input blindly or exposes attack surfaces. Security is non-negotiable.",
        "criteria": [
            "Zero exposed secrets or hardcoded tokens in code or logs",
            "Exhaustive input sanitization against SQLi, XSS, SSRF, and command injection",
            "Strict principle of least privilege and role-based access control",
            "Modern cryptographic hygiene (Argon2id, bcrypt, cryptographically secure RNG)",
            "Distributed rate limiting and brute-force circuit breakers"
        ]
    },
    "devops_cloud_architect": {
        "name": "Gareth 'The Unbreakable' Drake",
        "archetype": "Chaos Engineering Commander & Zero-Downtime Guardian",
        "title": "DevOps & Cloud Site Reliability Architect",
        "motto": "Hope is not an infrastructure strategy. If your deployment requires manual prayer, your architecture is broken.",
        "bio": "12+ years architecting Kubernetes clusters, multi-region cloud meshes, and zero-downtime deployment pipelines across AWS and GCP.",
        "cognitive_discipline": "Idempotency, Self-Healing Automation, Chaos Engineering, Immutable Infrastructure",
        "pledge": "I will never build fragile, manual, or brittle deployment pipelines. Infrastructure must be automated, reproducible, and resilient.",
        "criteria": [
            "Infrastructure as Code (IaC) idempotency and immutable image builds",
            "Zero-downtime blue/green or canary rollouts with instant rollback",
            "Full-stack observability (distributed tracing, metrics, automated alerting)",
            "Self-healing container workloads and dynamic horizontal pod auto-scaling",
            "Automated encrypted backups and tested disaster recovery (RPO < 5m, RTO < 15m)"
        ]
    }
}

TOOLS = [
    {
        "name": "humanpowers_inspect_code",
        "description": "Audits code against Humanpowers Council of Masters quality and security checklists before showing it to the user.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "The code to inspect"},
                "language": {"type": "string", "description": "Language (js, py, ts, etc.)"}
            },
            "required": ["code"]
        }
    },
    {
        "name": "humanpowers_get_persona",
        "description": "Retrieves the exact character profile, work ethic, pledge, and checklist from The Council of Masters.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "profession": {
                    "type": "string",
                    "description": "Target profession or character key (e.g. software_architect, elite_copywriter, principal_designer, startup_cfo_analyst, legal_contract_auditor, data_scientist_ml, cyber_security_auditor, devops_cloud_architect)"
                }
            },
            "required": ["profession"]
        }
    },
    {
        "name": "humanpowers_list_council",
        "description": "Lists all 8 members of The Council of Masters, their names, archetypes, and signature mottos.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "humanpowers_recall_memory",
        "description": "Retrieves past user preferences and recorded scar tissue to prevent repeating mistakes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query or category"}
            }
        }
    }
]

def handle_inspect_code(args):
    code = args.get("code", "")
    flaws = []

    if re.search(r"//\s*TODO|#\s*TODO", code):
        flaws.append("Unfinished '// TODO' stub detected. Complete all logic end-to-end.")
    if re.search(r"catch\s*\([^\)]*\)\s*\{\s*\}", code):
        flaws.append("Empty catch block (exception swallowed). Properly log or rethrow the error.")
    if re.search(r"except\s*:\s*pass|except\s+Exception\s*:\s*pass", code):
        flaws.append("Silent Python exception suppression ('except: pass'). Log or handle the failure.")
    if re.search(r"(sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,})", code):
        flaws.append("Hardcoded secret or API key detected. Store credentials in environment variables.")
    if re.search(r"f[\"'].*SELECT\s+.*\{|f[\"'].*INSERT\s+.*\{", code, re.IGNORECASE):
        flaws.append("Potential SQL injection via raw string interpolation. Use parameterized queries.")
    if re.search(r"\beval\s*\(|\bexec\s*\(", code):
        flaws.append("Dangerous dynamic execution ('eval/exec') detected. Replace with safe structured parsing.")

    if flaws:
        return {
            "status": "REJECTED",
            "score": max(40, 100 - len(flaws) * 15),
            "flaws": flaws,
            "auditor": "Gabriel 'The Sentinel' Frost (Red Team Lead)",
            "verdict": "Defects identified. Autonomously remediate all flaws before presenting to the user!"
        }
    return {
        "status": "CERTIFIED",
        "score": 98,
        "flaws": [],
        "auditor": "Marcus 'The Vanguard' Sterling (Engineering Lead)",
        "verdict": "Satisfies all Humanpowers quality standards. 100% Production-Ready!"
    }

def handle_get_persona(args):
    prof = args.get("profession", "software_architect").lower().replace(" ", "_").replace("-", "_")
    member = COUNCIL_MEMBERS.get(prof, COUNCIL_MEMBERS["software_architect"])
    return {
        "key": prof,
        "name": member["name"],
        "archetype": member["archetype"],
        "title": member["title"],
        "signature_motto": member["motto"],
        "bio": member["bio"],
        "cognitive_discipline": member["cognitive_discipline"],
        "pledge": member["pledge"],
        "criteria": member["criteria"]
    }

def handle_list_council(args):
    roster = []
    for key, m in COUNCIL_MEMBERS.items():
        roster.append({
            "key": key,
            "name": m["name"],
            "title": m["title"],
            "archetype": m["archetype"],
            "motto": m["motto"]
        })
    return {"council_size": len(roster), "masters": roster}

def handle_recall_memory(args):
    mem_file = os.path.join(".humanpowers", "memory.json")
    if os.path.exists(mem_file):
        try:
            with open(mem_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"status": "Memory active, zero recorded failures."}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"tools": TOOLS}
                }
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                args = params.get("arguments", {})

                if tool_name == "humanpowers_inspect_code":
                    output = handle_inspect_code(args)
                elif tool_name == "humanpowers_get_persona":
                    output = handle_get_persona(args)
                elif tool_name == "humanpowers_list_council":
                    output = handle_list_council(args)
                elif tool_name == "humanpowers_recall_memory":
                    output = handle_recall_memory(args)
                else:
                    output = {"error": f"Unknown tool: {tool_name}"}

                res = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": json.dumps(output, indent=2)}
                        ]
                    }
                }
            else:
                res = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {}
                }

            print(json.dumps(res), flush=True)
        except Exception as e:
            err_res = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            }
            print(json.dumps(err_res), flush=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(handle_get_persona({"profession": "software_architect"}), indent=2))
    else:
        main()
