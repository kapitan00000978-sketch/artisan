#!/usr/bin/env python3
"""
Artisan Pre-Commit Gatekeeper
Audits repository files for secrets, lazy stubs, and empty error catches using the shared detector.
Supports both full repository audit and fast staged git diff checks.
"""

import os
import sys

# Ensure scripts and sdk dirs are on sys.path
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPTS_DIR)
sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "src", "sdk"))
from detector import scan_project, load_artisan_config, PATTERNS

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def scan_files(staged_only: bool = False, vibe_override: bool = False):
    cfg = load_artisan_config(".")
    is_vibe = vibe_override or (cfg.get("mode", "strict").lower() == "vibe")
    if is_vibe:
        cfg["mode"] = "vibe"

    scope = "staged changes" if staged_only else "workspace"
    mode_str = " (⚡ Vibe Mode)" if is_vibe else ""
    print(f"🛡️ [Artisan Gatekeeper] Running pre-commit quality and security audit ({scope}){mode_str}...")
    result = scan_project(".", staged_only=staged_only, config_override=cfg)
    
    findings = result["findings"]
    if findings:
        if is_vibe:
            print("\n⚡ [ARTISAN VIBE MODE ACTIVE - ADVISORY NOTICES]:")
            for flaw in findings[:10]:
                auditor = flaw.get("auditor", "Artisan Council")
                print(f"  • {flaw['file']}:{flaw['line']} [{flaw['category']}] [{auditor}] -> {flaw['message']}")
            print(f"\n⚡ Total advisory notices: {len(findings)} | Score: {result['score']}/100")
            print("⚡ Directive: Vibe Mode is active. Commits are NON-BLOCKING for fast iteration.\n")
            return True
        else:
            print("\n❌ [ARTISAN REJECTED - AUDIT FAILED]:")
            for flaw in findings[:10]:
                auditor = flaw.get("auditor", "Artisan Council")
                print(f"  • {flaw['file']}:{flaw['line']} [{flaw['category']}] [{auditor}] -> {flaw['message']}")
            print(f"\nTotal defects detected: {len(findings)} | Gate Score: {result['score']}/100")
            print("💡 Directive: Artisan Quality Protocol — resolve all flaws before committing!\n")

            # Autonomously record detected flaws into persistent learning memory
            try:
                from learning_memory import LearningMemory
                mem = LearningMemory()
                for flaw in findings[:5]:
                    mem.record_learning(
                        record_type="mistake",
                        category=flaw.get("category", "code").lower(),
                        pattern=flaw.get("message", "code defect"),
                        lesson=f"Rejected in pre-commit audit ({flaw.get('file')}:{flaw.get('line')}). Resolve {flaw.get('message')} before committing.",
                        severity="high" if flaw.get("category") == "SECURITY" else "medium"
                    )
            except (ImportError, OSError, KeyError) as mem_err:
                import logging
                logging.debug("Memory record skipped: %s", mem_err)

            return False
    else:
        print(f"✅ [ARTISAN VERIFIED]: All code satisfied quality and security benchmarks. (Scanned {result['scanned_files']} files, Score: 100/100)")
        return True


if __name__ == "__main__":
    vibe = "--vibe" in sys.argv or "-v" in sys.argv
    staged = "--staged" in sys.argv or "-s" in sys.argv
    passed = scan_files(staged_only=staged, vibe_override=vibe)
    if not passed:
        sys.exit(1)

