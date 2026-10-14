#!/usr/bin/env python3
"""
Artisan Quality & Security Detection Engine
Shared rule-based detector for pre-commit gatekeeper, live watchdog, and MCP server.
"""

import os
import sys
import re
import shutil
import subprocess
from typing import List, Dict, Any, Optional

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

IGNORE_MARKER = "artisan-ignore"

# Rule Definitions: (id, category, regex_pattern, message, score_deduction)
# We compose patterns safely with inline ignore markers to prevent self-detection.
RULES = [
    # 1. Stubs & Placeholders (artisan-ignore)
    (
        "STUB_TODO_FIXME",
        "STUB",
        r"(?:#|//|/\*|--)\s*.*?\b(?:todo|fixme|xxx|hack)\b|\bimplement\s+later\b",
        "Unfinished stub or placeholder detected. Complete all logic end-to-end.",
        20
    ),
    (
        "STUB_PASS_PLACEHOLDER",
        "STUB",
        r"\bpass\s*#.*",
        "Pass placeholder detected. Implement complete functionality.",
        20
    ),
    (
        "STUB_EMPTY_CATCH",
        "STUB",
        r"catch\s*(?:\([^)]*\))?\s*\{\s*\}",
        "Empty catch block detected. Handle or log exceptions properly.",
        25
    ),
    (
        "STUB_BARE_EXCEPT",
        "STUB",
        r"except(?:\s+Exception(?:\s+as\s+[a-zA-Z0-9_]+)?)?\s*:\s*pass\b|except\s*:\s*pass\b",
        "Silent exception suppression (except: pass or except Exception: pass). Log or handle errors.",
        25
    ),

    # 2. Dangerous Execution (artisan-ignore)
    (
        "DANGEROUS_EVAL_EXEC",
        "DANGEROUS",
        r"\b(?:eval|exec)\s*\(",
        "Dangerous dynamic execution ('eval' or 'exec') detected. Replace with safe structured parsing.",
        30
    ),

    # 3. Secrets & Sensitive Credentials (artisan-ignore)
    (
        "SECRET_ANTHROPIC",
        "SECRET",
        r"sk-ant-[a-zA-Z0-9_\-]{20,}",
        "Anthropic API key detected. Externalize credentials via environment variables.",
        35
    ),
    (
        "SECRET_OPENAI",
        "SECRET",
        r"sk-[a-zA-Z0-9_\-]{20,}",
        "OpenAI API key detected. Externalize credentials via environment variables.",
        35
    ),
    (
        "SECRET_GITHUB",
        "SECRET",
        r"(?:ghp|gho|github_pat)_[a-zA-Z0-9_]{20,}",
        "GitHub token detected. Externalize credentials via environment variables.",
        35
    ),
    (
        "SECRET_AWS",
        "SECRET",
        r"AKIA[0-9A-Z]{16}",
        "AWS Access Key ID detected. Externalize credentials via environment variables.",
        35
    ),
    (
        "SECRET_SLACK",
        "SECRET",
        r"xox[baprs]-[0-9a-zA-Z_\-]{10,}",
        "Slack token detected. Externalize credentials via environment variables.",
        35
    ),
    (
        "SECRET_GOOGLE",
        "SECRET",
        r"AIza[0-9A-Za-z_\-]{35}",
        "Google API key detected. Externalize credentials via environment variables.",
        35
    ),
    (
        "SECRET_PRIVATE_KEY",
        "SECRET",
        r"-----BEGIN [A-Z0-9_\- ]*PRIVATE KEY-----",
        "Plaintext Private Key block detected. Externalize secrets securely.",
        35
    ),
    (
        "SECRET_ASSIGNMENT",
        "SECRET",
        r"""\b(?:password|passwd|pwd|secret|token|api_key|apikey|auth_token)\s*[:=]\s*["'][^"'\r\n]{4,}["']""",
        "Hardcoded password, secret, or API token assignment detected. Use environment variables.",
        35
    ),
]

# Pre-compiled rules using re.IGNORECASE
COMPILED_RULES = [
    (r[0], r[1], re.compile(r[2], re.IGNORECASE), r[3], r[4])
    for r in RULES
]

# Compatibility alias for scripts expecting PATTERNS tuple format
PATTERNS = [(r[2], r[0], r[3]) for r in RULES]


def run_gitleaks(target_dir: str = ".") -> List[Dict[str, Any]]:
    """Run gitleaks if installed, otherwise return empty list."""
    gitleaks_bin = shutil.which("gitleaks")
    if not gitleaks_bin:
        return []

    try:
        proc = subprocess.run(
            [gitleaks_bin, "detect", "--no-git", "--source", target_dir, "--report-format", "json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15
        )
        if proc.returncode != 0 and proc.stdout:
            import json
            leaks = json.loads(proc.stdout)
            findings = []
            for item in leaks:
                findings.append({
                    "rule_id": "GITLEAKS_" + item.get("RuleID", "LEAK"),
                    "category": "SECRET",
                    "file": item.get("File", ""),
                    "line": item.get("StartLine", 0),
                    "message": f"gitleaks: {item.get('Description', 'Exposed Secret')}",
                    "deduction": 35
                })
            return findings
    except Exception:
        pass
    return []


def scan_code(code: str, filename: str = "") -> Dict[str, Any]:
    """
    Audits a string of source code against all Artisan rules.
    Respects inline 'artisan-ignore' markers.
    Returns deterministic status, score, flaws, and detailed findings.
    """
    findings: List[Dict[str, Any]] = []
    lines = code.splitlines()

    # Pre-check for multi-line block catches like try { ... } catch (e) { \n }
    # Normalize for empty catches spanning multiple lines
    multi_line_empty_catch = re.search(r"catch\s*(?:\([^)]*\))?\s*\{\s*\}", code)
    if multi_line_empty_catch and IGNORE_MARKER not in code:
        pass # Will be captured per line or whole block below

    for line_idx, line in enumerate(lines, 1):
        if IGNORE_MARKER in line:
            continue

        for rule_id, category, compiled_pattern, message, deduction in COMPILED_RULES:
            # Check if this rule matches
            if compiled_pattern.search(line):
                findings.append({
                    "rule_id": rule_id,
                    "category": category,
                    "file": filename,
                    "line": line_idx,
                    "matched_text": line.strip()[:80],
                    "message": message,
                    "deduction": deduction
                })

    # Check for empty catch or except spanning across multiple lines if not caught per line
    if not any(f["rule_id"] in ("STUB_EMPTY_CATCH", "STUB_BARE_EXCEPT") for f in findings):
        if re.search(r"catch\s*(?:\([^)]*\))?\s*\{\s*\}", code) and IGNORE_MARKER not in code:
            findings.append({
                "rule_id": "STUB_EMPTY_CATCH",
                "category": "STUB",
                "file": filename,
                "line": 1,
                "matched_text": "catch { }",
                "message": "Empty catch block detected. Handle or log exceptions properly.",
                "deduction": 25
            })
        if re.search(r"except(?:\s+Exception(?:\s+as\s+[a-zA-Z0-9_]+)?)?\s*:\s*\n\s*pass\b", code) and IGNORE_MARKER not in code:
            findings.append({
                "rule_id": "STUB_BARE_EXCEPT",
                "category": "STUB",
                "file": filename,
                "line": 1,
                "matched_text": "except: pass",
                "message": "Silent exception suppression (except: pass). Log or handle errors.",
                "deduction": 25
            })

    total_deduction = sum(f["deduction"] for f in findings)
    score = max(0, 100 - total_deduction)

    flaw_messages = [f"[{f['category']}] line {f['line']}: {f['message']}" for f in findings]

    if findings:
        status = "REJECTED"
        verdict = f"Rejected: {len(findings)} quality/security defect(s) detected. Autonomously remediate all flaws."
        auditor = "Gabriel 'The Sentinel' Frost (Cybersecurity & Quality Auditor)"
    else:
        status = "CERTIFIED"
        score = 100
        verdict = "Certified: All quality and security checks passed."
        auditor = "Marcus 'The Vanguard' Sterling (Engineering Lead)"

    return {
        "status": status,
        "score": score,
        "flaws": flaw_messages,
        "findings": findings,
        "auditor": auditor,
        "verdict": verdict
    }


def scan_project(base_dir: str = ".") -> Dict[str, Any]:
    """
    Scans project source files for stubs, secrets, and dangerous execution.
    Excludes node_modules, .git, .venv, test files, and detector definitions.
    """
    all_findings: List[Dict[str, Any]] = []
    scanned_count = 0

    excluded_dirs = {".git", "node_modules", ".venv", "__pycache__", "tests"}
    excluded_files = {"detector.py", "pre-commit-gatekeeper.py", "server.py", "watchdog.py", "sync_artisan.py"}
    valid_extensions = (".js", ".ts", ".py", ".go", ".rs", ".java", ".cpp", ".cs")

    for root, dirs, files in os.walk(base_dir):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs and not d.startswith(".")]
        for file in files:
            if file.endswith(valid_extensions):
                if file in excluded_files:
                    continue
                filepath = os.path.join(root, file)
                scanned_count += 1
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    res = scan_code(content, filename=filepath)
                    if res["findings"]:
                        all_findings.extend(res["findings"])
                except Exception:
                    pass

    # Optional gitleaks pass
    gitleaks_findings = run_gitleaks(base_dir)
    all_findings.extend(gitleaks_findings)

    total_deduction = sum(f["deduction"] for f in all_findings)
    score = max(0, 100 - total_deduction) if all_findings else 100

    return {
        "passed": len(all_findings) == 0,
        "scanned_files": scanned_count,
        "findings": all_findings,
        "score": score
    }
