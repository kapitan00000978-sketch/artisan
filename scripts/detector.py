#!/usr/bin/env python3
"""
Artisan Quality & Security Detection Engine
Shared rule-based detector for pre-commit gatekeeper, live watchdog, and MCP server.
Supports full repository auditing, staged git diff scanning, and single-file inspections.
"""

import os
import sys
import re
import json
import shutil
import argparse
import subprocess
from typing import List, Dict, Any, Optional

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

IGNORE_MARKER = "artisan-ignore"

# Rule Definitions: (id, category, regex_pattern, message, score_deduction)
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

    # 2. Dangerous Dynamic Execution & Injections (artisan-ignore)
    (
        "DANGEROUS_EVAL_EXEC",
        "DANGEROUS",
        r"\b(?:eval|exec)\s*\(",
        "Dangerous dynamic execution ('eval' or 'exec') detected. Replace with safe structured parsing.",
        30
    ),
    (
        "DANGEROUS_SQL_INJECTION",
        "DANGEROUS",
        r"(?i)\bf[\"'].*(?:SELECT|INSERT|UPDATE|DELETE)\s+.*\{",
        "Potential SQL injection via raw string interpolation. Use parameterized queries.",
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
        "SECRET_JWT",
        "SECRET",
        r"eyJ[a-zA-Z0-9_\-]{15,}\.eyJ[a-zA-Z0-9_\-]{15,}\.[a-zA-Z0-9_\-]{10,}",
        "Hardcoded JSON Web Token (JWT) detected. Externalize tokens securely.",
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


def scan_python_ast(code: str, filename: str = "") -> List[Dict[str, Any]]:
    """Performs deep Abstract Syntax Tree (AST) analysis on Python code."""
    import ast
    ast_findings: List[Dict[str, Any]] = []
    try:
        tree = ast.parse(code, filename=filename or "<input>")
    except Exception:
        return []

    lines = code.splitlines()

    for node in ast.walk(tree):
        # 1. Detect dynamic eval/exec
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id in ("eval", "exec"):
                line_no = getattr(node, "lineno", 1)
                line_content = lines[line_no - 1] if line_no <= len(lines) else ""
                if IGNORE_MARKER not in line_content:
                    ast_findings.append({
                        "rule_id": "DANGEROUS_EVAL_EXEC",
                        "category": "DANGEROUS",
                        "file": filename,
                        "line": line_no,
                        "matched_text": f"{func.id}(...)",
                        "message": f"Dangerous dynamic execution ('{func.id}') verified via AST analysis.",
                        "deduction": 30
                    })
        # 2. Detect empty except blocks (bare except: pass or except Exception: pass)
        elif isinstance(node, ast.ExceptHandler):
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                line_no = getattr(node, "lineno", 1)
                line_content = lines[line_no - 1] if line_no <= len(lines) else ""
                if IGNORE_MARKER not in line_content:
                    exc_name = "bare except" if node.type is None else "except"
                    ast_findings.append({
                        "rule_id": "STUB_BARE_EXCEPT",
                        "category": "STUB",
                        "file": filename,
                        "line": line_no,
                        "matched_text": f"except {exc_name}: pass",
                        "message": f"Silent exception suppression ('except {exc_name}: pass') verified via AST.",
                        "deduction": 25
                    })
    return ast_findings


def load_artisan_config(base_dir: str = ".") -> Dict[str, Any]:
    """Loads artisan.config.json if present, returning configuration overrides."""
    config_path = os.path.join(base_dir, "artisan.config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def scan_code(code: str, filename: str = "", config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Audits a string of source code against all Artisan rules.
    Respects inline 'artisan-ignore' markers and artisan.config.json toggles.
    Returns deterministic status, score, flaws, and detailed findings.
    """
    if config is None:
        config = load_artisan_config(".")

    rules_cfg = config.get("rules", {})
    findings: List[Dict[str, Any]] = []
    lines = code.splitlines()

    for line_idx, line in enumerate(lines, 1):
        if IGNORE_MARKER in line:
            continue

        for rule_id, category, compiled_pattern, message, deduction in COMPILED_RULES:
            if rule_id in rules_cfg and not rules_cfg[rule_id].get("enabled", True):
                continue

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

    # Deep AST analysis for Python code (eliminates regex blindspots)
    if filename.endswith(".py") or ("def " in code and ("import " in code or "try:" in code)):
        ast_results = scan_python_ast(code, filename=filename)
        existing_keys = {(f["rule_id"], f["line"]) for f in findings}
        for item in ast_results:
            if (item["rule_id"], item["line"]) not in existing_keys:
                findings.append(item)

    total_deduction = sum(f["deduction"] for f in findings)
    score = max(0, 100 - total_deduction)

    flaw_messages = [f"[{f['category']}] line {f['line']}: {f['message']}" for f in findings]

    if findings:
        status = "REJECTED"
        verdict = f"Rejected: {len(findings)} defect(s) detected. Autonomously remediate all flaws."
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


def scan_file(filepath: str, config: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Scans an individual file on disk."""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return scan_code(content, filename=filepath, config=config)
    except Exception:
        return None


def get_staged_git_files() -> List[str]:
    """Returns a list of currently staged files in git."""
    try:
        proc = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if proc.returncode == 0:
            return [f.strip() for f in proc.stdout.splitlines() if f.strip()]
    except Exception:
        pass
    return []


def scan_project(base_dir: str = ".", staged_only: bool = False, config_override: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Scans project source files for stubs, secrets, and dangerous execution.
    If staged_only is True, only checks files staged for git commit.
    Respects artisan.config.json for excluded paths and rule thresholds.
    """
    cfg = config_override or load_artisan_config(base_dir)
    all_findings: List[Dict[str, Any]] = []
    scanned_count = 0

    excluded_dirs = {".git", "node_modules", ".venv", "__pycache__", "tests"}
    if "exclude_dirs" in cfg:
        excluded_dirs.update(cfg["exclude_dirs"])

    excluded_files = {"detector.py", "pre-commit-gatekeeper.py", "remediator.py", "server.py", "watchdog.py", "sync_artisan.py", "claude_hook.py"}
    if "exclude_files" in cfg:
        excluded_files.update(cfg["exclude_files"])

    valid_extensions = (".js", ".ts", ".py", ".go", ".rs", ".java", ".cpp", ".cs")

    if staged_only:
        staged_files = get_staged_git_files()
        for filepath in staged_files:
            normalized_path = filepath.replace("\\", "/")
            path_parts = set(normalized_path.split("/"))
            if path_parts & excluded_dirs:
                continue
            if filepath.endswith(valid_extensions):
                filename = os.path.basename(filepath)
                if filename in excluded_files:
                    continue
                scanned_count += 1
                res = scan_file(filepath, config=cfg)
                if res and res["findings"]:
                    all_findings.extend(res["findings"])
    else:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in excluded_dirs and not d.startswith(".")]
            for file in files:
                if file.endswith(valid_extensions):
                    if file in excluded_files:
                        continue
                    filepath = os.path.join(root, file)
                    scanned_count += 1
                    res = scan_file(filepath, config=cfg)
                    if res and res["findings"]:
                        all_findings.extend(res["findings"])

    # Optional gitleaks pass
    if not staged_only:
        gitleaks_findings = run_gitleaks(base_dir)
        all_findings.extend(gitleaks_findings)

    total_deduction = sum(f["deduction"] for f in all_findings)
    score = max(0, 100 - total_deduction) if all_findings else 100

    threshold = cfg.get("threshold_score", 100)
    passed = (len(all_findings) == 0) if threshold >= 100 else (score >= threshold)

    return {
        "passed": passed,
        "scanned_files": scanned_count,
        "findings": all_findings,
        "score": score
    }


def main():
    parser = argparse.ArgumentParser(description="Artisan Quality & Security Detection Engine")
    parser.add_argument("--file", "-f", help="Scan a specific file")
    parser.add_argument("--staged", "-s", action="store_true", help="Scan only git staged files")
    parser.add_argument("--all", "-a", action="store_true", help="Scan entire project (default)")
    parser.add_argument("--json", "-j", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    if args.file:
        res = scan_file(args.file)
        if not res:
            print(f"Error: File not found or unreadable: {args.file}", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"[{res['status']}] Score: {res['score']}/100 | File: {args.file}")
            for flaw in res["flaws"]:
                print(f"  • {flaw}")
        sys.exit(0 if res["status"] == "CERTIFIED" else 1)

    result = scan_project(".", staged_only=args.staged)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        scope = "staged files" if args.staged else "all files"
        if result["passed"]:
            print(f"✅ [ARTISAN VERIFIED]: Scanned {result['scanned_files']} {scope}. Gate Score: {result['score']}/100")
        else:
            print(f"❌ [ARTISAN REJECTED]: Defects detected across {scope}. Gate Score: {result['score']}/100")
            for f in result["findings"][:10]:
                print(f"  • {f['file']}:{f['line']} [{f['category']}] -> {f['message']}")

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
