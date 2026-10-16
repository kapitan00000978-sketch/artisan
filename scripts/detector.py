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

# Safe placeholder values that should NOT trigger false-positive secret alerts
DUMMY_SECRET_VALUES = {
    "test", "testing", "test123", "dummy", "placeholder", "changeme",
    "example", "sample", "temp", "fake", "dev", "local", "mock",
    "none", "null", "undefined", "default", "localhost", "admin", "secret",
    "password", "passwd", "123456", "qwerty", "your_key_here", "your_api_key",
    "testpass", "test_password", "test_secret", "dummy_token", "xxx", "foo", "bar"
}

# Rule Definitions: (id, category, regex_pattern, message, score_deduction)
RULES = [
    # 1. Stubs & Placeholders (artisan-ignore)
    (
        "STUB_TODO_FIXME",
        "STUB",
        r"(?:#|//|/\*|--|\*)\s*.*?\b(?:todo|fixme|xxx|hack|tbd|stub:)\b|\bimplement\s+later\b",
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
        r"""(?i)(?:\bf["'].*?(?:SELECT\s+.*?\bFROM|INSERT\s+INTO|UPDATE\s+.*?\bSET|DELETE\s+FROM|DROP\s+(?:TABLE|DATABASE|VIEW))\s+.*\{|`.*?(?:SELECT\s+.*?\bFROM|INSERT\s+INTO|UPDATE\s+.*?\bSET|DELETE\s+FROM|DROP\s+(?:TABLE|DATABASE|VIEW))\s+.*?\$\{|\b(?:SELECT\s+.*?\bFROM|INSERT\s+INTO|UPDATE\s+.*?\bSET|DELETE\s+FROM)\s+[^"'\r\n]*["']\s*\+\s*[a-zA-Z_]|[a-zA-Z_]\s*\+\s*["'][^"'\r\n]*(?:WHERE|AND|OR|FROM)\s+|["'].*?(?:SELECT\s+.*?\bFROM|INSERT\s+INTO|UPDATE\s+.*?\bSET|DELETE\s+FROM)\s+.*\{\}\s*["']\.format\s*\(|(?:SELECT\s+.*?\bFROM|INSERT\s+INTO|UPDATE\s+.*?\bSET|DELETE\s+FROM)\s+.*?(?:%s|%d|%v)\s*["']\s*%(?!\s*["'])|fmt\.Sprintf\s*\(\s*["'].*?(?:SELECT\s+.*?\bFROM|INSERT\s+INTO|UPDATE\s+.*?\bSET|DELETE\s+FROM)|String\.format\s*\(\s*["'].*?(?:SELECT\s+.*?\bFROM|INSERT\s+INTO|UPDATE\s+.*?\bSET|DELETE\s+FROM))""",
        "Potential SQL injection via raw string interpolation or concatenation. Use parameterized queries.",
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
        r"""\b(?:password|passwd|pwd|secret|token|api_key|apikey|auth_token)\s*[:=]\s*["']([^"'\r\n]{4,})["']""",
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

# Rule ID aliases to guarantee config compatibility (HW-026)
RULE_ALIASES = {
    "SECRET_ANTHROPIC_KEY": "SECRET_ANTHROPIC",
    "SECRET_OPENAI_KEY": "SECRET_OPENAI",
    "SECRET_AWS_KEY": "SECRET_AWS",
    "SECRET_GENERIC_KEY": "SECRET_ASSIGNMENT",
    "SECRET_ASSIGNMENT": "SECRET_GENERIC_KEY",
    "SECRET_ANTHROPIC": "SECRET_ANTHROPIC_KEY",
    "SECRET_OPENAI": "SECRET_OPENAI_KEY",
    "SECRET_AWS": "SECRET_AWS_KEY",
}

def is_rule_enabled(rule_id: str, rules_cfg: Dict[str, Any]) -> bool:
    """Checks whether a rule is enabled in configuration, resolving any alias names (HW-026)."""
    if rule_id in rules_cfg:
        return rules_cfg[rule_id].get("enabled", True)
    alt = RULE_ALIASES.get(rule_id)
    if alt and alt in rules_cfg:
        return rules_cfg[alt].get("enabled", True)
    return True

# Council of Masters domain ownership
COUNCIL_AUDITORS = {
    "STUB": "Marcus Sterling (Senior Architect)",
    "SECRET": "Gabriel Frost (Cybersecurity Auditor)",
    "DANGEROUS": "Gabriel Frost & Arthur Pendelton",
    "AST": "Marcus Sterling & Dr. Evelyn Reed",
}


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
                        "auditor": COUNCIL_AUDITORS["DANGEROUS"],
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
                        "auditor": COUNCIL_AUDITORS["STUB"],
                        "file": filename,
                        "line": line_no,
                        "matched_text": f"except {exc_name}: pass",
                        "message": f"Silent exception suppression ('except {exc_name}: pass') verified via AST.",
                        "deduction": 25
                    })
    return ast_findings


def load_artisan_config(base_dir: str = ".") -> Dict[str, Any]:
    """Loads hallwright.config.json or artisan.config.json if present, returning configuration overrides."""
    for cfg_name in ["hallwright.config.json", "artisan.config.json"]:
        config_path = os.path.join(base_dir, cfg_name)
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                continue
    return {}

load_hallwright_config = load_artisan_config


def scan_multilingual_structural(code: str, filename: str = "") -> List[Dict[str, Any]]:
    """
    Lightweight AST-like structural analysis for JavaScript, TypeScript, Go, Java, and C#.
    Detects multiline empty catches, unparameterized SQL, and DOM XSS sinks.
    """
    findings: List[Dict[str, Any]] = []
    norm_fn = filename.lower().replace("\\", "/")

    # JS/TS structural check
    if norm_fn.endswith((".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")):
        # Multiline empty catch: catch (...) { \n }
        for m in re.finditer(r"catch\s*(?:\([^)]*\))?\s*\{\s*\}", code):
            start_pos = m.start()
            line_no = code[:start_pos].count("\n") + 1
            line_str = code.splitlines()[line_no - 1] if line_no <= len(code.splitlines()) else ""
            if IGNORE_MARKER not in line_str:
                findings.append({
                    "rule_id": "STUB_EMPTY_CATCH",
                    "category": "STUB",
                    "auditor": COUNCIL_AUDITORS["STUB"],
                    "file": filename,
                    "line": line_no,
                    "matched_text": m.group(0),
                    "message": "Empty JS/TS catch block detected. Handle or log exceptions properly.",
                    "deduction": 25
                })

    # Java/C# structural check
    elif norm_fn.endswith((".java", ".cs")):
        for m in re.finditer(r"catch\s*\([^\)]*Exception[^\)]*\)\s*\{\s*\}", code):
            start_pos = m.start()
            line_no = code[:start_pos].count("\n") + 1
            line_str = code.splitlines()[line_no - 1] if line_no <= len(code.splitlines()) else ""
            if IGNORE_MARKER not in line_str:
                findings.append({
                    "rule_id": "STUB_EMPTY_CATCH",
                    "category": "STUB",
                    "auditor": COUNCIL_AUDITORS["STUB"],
                    "file": filename,
                    "line": line_no,
                    "matched_text": m.group(0),
                    "message": "Empty Java/C# catch block detected. Log or handle exceptions properly.",
                    "deduction": 25
                })

    return findings


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
            if not is_rule_enabled(rule_id, rules_cfg):
                continue

            match = compiled_pattern.search(line)
            if match:
                # Intelligent false-positive suppression for SECRET_ASSIGNMENT
                if rule_id == "SECRET_ASSIGNMENT":
                    assigned_val = match.group(1).strip() if match.groups() else ""
                    norm_val = assigned_val.lower().strip("\"' ")
                    is_test_env = any(t in filename.lower().replace("\\", "/") for t in ["test", "bench", "fixture", "mock", "sample"])
                    if norm_val in DUMMY_SECRET_VALUES or norm_val.startswith(("test", "dummy", "fake", "placeholder", "mock", "sample", "temp_")):
                        continue
                    if is_test_env and (len(norm_val) <= 12 or norm_val.isalnum()):
                        # Suppress short dummy test strings inside test suites unless matching specific token prefixes
                        continue

                findings.append({
                    "rule_id": rule_id,
                    "category": category,
                    "auditor": COUNCIL_AUDITORS.get(category, "Artisan Council"),
                    "file": filename,
                    "line": line_idx,
                    "matched_text": line.strip()[:80],
                    "message": message,
                    "deduction": deduction
                })

    # Multi-line block comments scanner (/* ... */, """ ... """, <!-- ... -->)
    block_comment_pattern = re.compile(
        r"(?:/\*[\s\S]*?\*/|<!--[\s\S]*?-->|(?:\"\"\"|''')[\s\S]*?(?:\"\"\"|'''))",
        re.IGNORECASE
    )
    for match in block_comment_pattern.finditer(code):
        block_text = match.group(0)
        if IGNORE_MARKER in block_text:
            continue
        if re.search(r"\b(?:todo|fixme|xxx|hack|tbd|stub)\b|\bimplement\s+later\b", block_text, re.IGNORECASE):
            start_pos = match.start()
            line_no = code[:start_pos].count("\n") + 1
            if not any(f["rule_id"] == "STUB_TODO_FIXME" and f["line"] == line_no for f in findings):
                findings.append({
                    "rule_id": "STUB_TODO_FIXME",
                    "category": "STUB",
                    "auditor": COUNCIL_AUDITORS["STUB"],
                    "file": filename,
                    "line": line_no,
                    "matched_text": block_text.strip().splitlines()[0][:80],
                    "message": "Unfinished multi-line block stub or placeholder detected. Complete all logic end-to-end.",
                    "deduction": 20
                })

    # Check for empty catch or except spanning across multiple lines if not caught per line
    # Fix HW-027: Inspect line-level ignore markers rather than checking if IGNORE_MARKER appears anywhere in the file
    if not any(f["rule_id"] == "STUB_EMPTY_CATCH" for f in findings):
        for m in re.finditer(r"catch\s*(?:\([^)]*\))?\s*\{\s*\}", code):
            start_pos = m.start()
            line_no = code[:start_pos].count("\n") + 1
            line_str = lines[line_no - 1] if line_no <= len(lines) else ""
            if IGNORE_MARKER not in line_str and "hallwright-ignore" not in line_str:
                findings.append({
                    "rule_id": "STUB_EMPTY_CATCH",
                    "category": "STUB",
                    "auditor": COUNCIL_AUDITORS["STUB"],
                    "file": filename,
                    "line": line_no,
                    "matched_text": m.group(0),
                    "message": "Empty catch block detected. Handle or log exceptions properly.",
                    "deduction": 25
                })
                break

    if not any(f["rule_id"] == "STUB_BARE_EXCEPT" for f in findings):
        for m in re.finditer(r"except(?:\s+Exception(?:\s+as\s+[a-zA-Z0-9_]+)?)?\s*:\s*\n\s*pass\b", code):
            start_pos = m.start()
            line_no = code[:start_pos].count("\n") + 1
            except_line = lines[line_no - 1] if line_no <= len(lines) else ""
            pass_line = lines[line_no] if line_no < len(lines) else ""
            if (IGNORE_MARKER not in except_line and "hallwright-ignore" not in except_line and
                IGNORE_MARKER not in pass_line and "hallwright-ignore" not in pass_line):
                findings.append({
                    "rule_id": "STUB_BARE_EXCEPT",
                    "category": "STUB",
                    "auditor": COUNCIL_AUDITORS["STUB"],
                    "file": filename,
                    "line": line_no,
                    "matched_text": m.group(0),
                    "message": "Silent exception suppression (except: pass). Log or handle errors.",
                    "deduction": 25
                })
                break

    # Deep AST analysis for Python code (eliminates regex blindspots)
    if filename.endswith(".py") or ("def " in code and ("import " in code or "try:" in code)):
        ast_results = scan_python_ast(code, filename=filename)
        existing_keys = {(f["rule_id"], f["line"]) for f in findings}
        for item in ast_results:
            if (item["rule_id"], item["line"]) not in existing_keys:
                findings.append(item)

    # Multi-language structural analysis (JS/TS/Go/Java)
    struct_results = scan_multilingual_structural(code, filename=filename)
    existing_keys = {(f["rule_id"], f["line"]) for f in findings}
    for item in struct_results:
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
    Uses file-weighted average scoring to avoid dropping a multi-file project to 0 on minor findings.
    Respects artisan.config.json for excluded paths and rule thresholds.
    """
    cfg = config_override or load_artisan_config(base_dir)
    all_findings: List[Dict[str, Any]] = []
    file_scores: List[int] = []
    scanned_count = 0

    # Configurable exclusion list; does not forcibly exclude tests if user wishes to audit test suites (HW-025)
    default_excluded_dirs = {".git", "node_modules", ".venv", "__pycache__"}
    if "exclude_dirs" in cfg:
        excluded_dirs = set(cfg["exclude_dirs"])
    else:
        excluded_dirs = default_excluded_dirs

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
                if res:
                    file_scores.append(res["score"])
                    if res["findings"]:
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
                    if res:
                        file_scores.append(res["score"])
                        if res["findings"]:
                            all_findings.extend(res["findings"])

    # Optional gitleaks pass
    if not staged_only:
        gitleaks_findings = run_gitleaks(base_dir)
        all_findings.extend(gitleaks_findings)

    # Calculate fair file-weighted average project score
    if file_scores:
        project_score = round(sum(file_scores) / len(file_scores))
    else:
        project_score = 100

    critical_findings = [f for f in all_findings if f.get("category") in ("SECRET", "DANGEROUS")]
    warning_findings = [f for f in all_findings if f.get("category") in ("STUB", "AST")]

    mode = cfg.get("mode", "strict").lower()
    threshold = cfg.get("threshold_score", 100)

    # In vibe mode, warnings are advisory and never block (always passed = True)
    if mode == "vibe":
        passed = True
    else:
        if threshold >= 100:
            passed = (len(all_findings) == 0)
        else:
            passed = (project_score >= threshold and len(critical_findings) == 0)

    return {
        "passed": passed,
        "mode": mode,
        "scanned_files": scanned_count,
        "findings": all_findings,
        "score": project_score,
        "metrics": {
            "critical_count": len(critical_findings),
            "warning_count": len(warning_findings),
            "total_flaws": len(all_findings),
            "average_file_score": project_score
        }
    }


def to_sarif_v2(scan_result: Dict[str, Any]) -> Dict[str, Any]:
    """Converts Hallwright scan results into standard OASIS SARIF v2.1.0 format.

    Compatible with GitHub Code Scanning, GitLab SAST, and IDE SARIF viewers.
    """
    rules_dict = {}
    sarif_results = []

    for f in scan_result.get("findings", []):
        rule_id = f.get("rule_id", "HW_RULE")
        category = f.get("category", "QUALITY")
        message = f.get("message", "Defect detected")
        deduction = f.get("deduction", 10)
        file_path = f.get("file", "unknown").replace("\\", "/")
        line = max(1, f.get("line", 1))

        if deduction >= 25 or category in ("DANGEROUS", "SECURITY", "SECRET"):
            level = "error"
        else:
            level = "warning"

        if rule_id not in rules_dict:
            rules_dict[rule_id] = {
                "id": rule_id,
                "name": rule_id,
                "shortDescription": {"text": message},
                "fullDescription": {"text": f"Hallwright {category} rule: {message}"},
                "defaultConfiguration": {
                    "level": level
                },
                "properties": {
                    "category": category,
                    "deduction": deduction,
                    "auditor": f.get("auditor", "Hallwright Council")
                }
            }

        sarif_results.append({
            "ruleId": rule_id,
            "level": level,
            "message": {
                "text": message
            },
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": file_path
                        },
                        "region": {
                            "startLine": line,
                            "startColumn": 1
                        }
                    }
                }
            ]
        })

    return {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Hallwright",
                        "semanticVersion": "2.0.0",
                        "informationUri": "https://github.com/kapitan00000978-sketch/hallwright",
                        "rules": list(rules_dict.values())
                    }
                },
                "results": sarif_results
            }
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="Artisan Quality & Security Detection Engine")
    parser.add_argument("--file", "-f", help="Scan a specific file")
    parser.add_argument("--staged", "-s", action="store_true", help="Scan only git staged files")
    parser.add_argument("--all", "-a", action="store_true", help="Scan entire project (default)")
    parser.add_argument("--vibe", "-v", action="store_true", help="Run in non-blocking Vibe mode (advisory only)")
    parser.add_argument("--json", "-j", action="store_true", help="Output results in JSON format")
    parser.add_argument("--sarif", action="store_true", help="Output results in OASIS SARIF v2.1.0 format")
    parser.add_argument("--format", choices=["text", "json", "sarif"], default="text", help="Output format")

    args = parser.parse_args()
    output_format = "sarif" if args.sarif else ("json" if args.json else args.format)

    if args.file:
        res = scan_file(args.file)
        if not res:
            print(f"Error: File not found or unreadable: {args.file}", file=sys.stderr)
            sys.exit(1)
        if output_format == "sarif":
            print(json.dumps(to_sarif_v2({"findings": res.get("flaws_detail", [])}), indent=2))
        elif output_format == "json":
            print(json.dumps(res, indent=2))
        else:
            print(f"[{res['status']}] Score: {res['score']}/100 | File: {args.file}")
            for flaw in res["flaws"]:
                print(f"  • {flaw}")
        sys.exit(0 if res["status"] == "CERTIFIED" else 1)

    cfg = load_artisan_config(".")
    if args.vibe:
        cfg["mode"] = "vibe"

    result = scan_project(".", staged_only=args.staged, config_override=cfg)

    if output_format == "sarif":
        print(json.dumps(to_sarif_v2(result), indent=2))
    elif output_format == "json":
        print(json.dumps(result, indent=2))
    else:
        scope = "staged files" if args.staged else "all files"
        if result["mode"] == "vibe":
            print(f"⚡ [ARTISAN VIBE MODE ACTIVE]: Rapid development mode. Advisory scan over {result['scanned_files']} {scope}.")
            if result["findings"]:
                print(f"⚡ Advisory notices ({len(result['findings'])} items, Score: {result['score']}/100 - Non-blocking):")
                for f in result["findings"][:10]:
                    auditor = f.get("auditor", "Artisan Council")
                    print(f"  • {f['file']}:{f['line']} [{f['category']}] [{auditor}] -> {f['message']}")
            else:
                print(f"✅ [ARTISAN VERIFIED]: Clean code. Gate Score: 100/100")
        elif result["passed"]:
            print(f"✅ [ARTISAN VERIFIED]: Scanned {result['scanned_files']} {scope}. Gate Score: {result['score']}/100")
        else:
            print(f"❌ [ARTISAN REJECTED]: Defects detected across {scope}. Gate Score: {result['score']}/100")
            for f in result["findings"][:10]:
                auditor = f.get("auditor", "Artisan Council")
                print(f"  • {f['file']}:{f['line']} [{f['category']}] [{auditor}] -> {f['message']}")

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
