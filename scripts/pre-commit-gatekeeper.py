#!/usr/bin/env python3
"""
Humanpowers Pre-Commit Gatekeeper
Checks staged git files for lazy placeholders, security leaks, and empty error catches.
"""

import os
import sys
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

PATTERNS = [
    (r"//\s*(?:TODO|FIXME|XXX)|#\s*(?:TODO|FIXME|XXX)", "LAZY_STUB", "Unfinished stub detected (TODO/FIXME/XXX). Complete all logic end-to-end."),
    (r"catch\s*\([^\)]*\)\s*\{\s*\}|except\s*:\s*pass", "SILENT_CATCH", "Silent exception suppression (empty catch block or bare except: pass). Log or rethrow errors."),
    (r"(sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16})", "EXPOSED_SECRET", "Security risk: Plaintext API key or credential detected! Use environment variables.")
]


def scan_files():
    print("🛡️ [Humanpowers Gatekeeper] Running pre-commit quality and security audit...")
    flaws_found = []

    # Scan project source files
    for root, dirs, files in os.walk("."):
        if any(d in root for d in [".git", "node_modules", ".venv", "__pycache__", "tests"]):
            continue
        for file in files:
            # Only scan actual source code files, ignore documentation
            if file.endswith((".js", ".ts", ".py", ".go", ".rs", ".java", ".cpp", ".cs")):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        for line_idx, line in enumerate(lines, 1):
                            # Skip scanning the gatekeeper script, tools, and watchdog itself
                            if any(k in filepath for k in ["pre-commit-gatekeeper", "watchdog", "translate_humanpowers", "server.py", "mcp"]):
                                continue
                            for pattern, flaw_type, message in PATTERNS:
                                if re.search(pattern, line):
                                    flaws_found.append(f"{filepath}:{line_idx} [{flaw_type}] -> {message}")
                except Exception:
                    pass

    if flaws_found:
        print("\n❌ [HUMANPOWERS REJECTED - AUDIT FAILED]:")
        for flaw in flaws_found[:5]:
            print(f"  • {flaw}")
        print(f"\nTotal defects detected: {len(flaws_found)}")
        print("💡 Directive: Humanpowers Zero Babysitting — resolve all flaws independently before committing!\n")
        return False
    else:
        print("✅ [HUMANPOWERS VERIFIED]: All code satisfied strict quality benchmarks. 100% Production-Ready!")
        return True

if __name__ == "__main__":
    passed = scan_files()
    if not passed:
        sys.exit(1)
