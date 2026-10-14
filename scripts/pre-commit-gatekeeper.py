#!/usr/bin/env python3
"""
Artisan Pre-Commit Gatekeeper
Audits repository files for secrets, lazy stubs, and empty error catches using the shared detector.
Supports both full repository audit and fast staged git diff checks.
"""

import os
import sys

# Ensure scripts dir is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from detector import scan_project, PATTERNS

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def scan_files(staged_only: bool = False):
    scope = "staged changes" if staged_only else "workspace"
    print(f"🛡️ [Artisan Gatekeeper] Running pre-commit quality and security audit ({scope})...")
    result = scan_project(".", staged_only=staged_only)
    
    findings = result["findings"]
    if findings:
        print("\n❌ [ARTISAN REJECTED - AUDIT FAILED]:")
        for flaw in findings[:10]:
            print(f"  • {flaw['file']}:{flaw['line']} [{flaw['category']}] -> {flaw['message']}")
        print(f"\nTotal defects detected: {len(findings)} | Gate Score: {result['score']}/100")
        print("💡 Directive: Artisan Quality Protocol — resolve all flaws before committing!\n")
        return False
    else:
        print(f"✅ [ARTISAN VERIFIED]: All code satisfied quality and security benchmarks. (Scanned {result['scanned_files']} files, Score: 100/100)")
        return True


if __name__ == "__main__":
    staged = "--staged" in sys.argv or "-s" in sys.argv
    passed = scan_files(staged_only=staged)
    if not passed:
        sys.exit(1)
