#!/usr/bin/env python3
"""
Humanpowers Live Watchdog Daemon
Monitors file changes and flags code flaws, unfinished stubs, and secret leaks.
Supports both single-pass scan (--once) and continuous background watch loop (--watch).
"""

import sys
import os
import time
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

PATTERNS = [
    (r"(?i)(?://|#)\s*(?:todo|fixme|xxx|hack)", "LAZY_STUB", "Unfinished stub detected (TODO/FIXME/XXX). Complete all logic end-to-end."),
    (r"catch\s*\([^\)]*\)\s*\{\s*\}|except\s*:\s*pass", "SILENT_CATCH", "Silent exception suppression (empty catch block or bare except: pass). Log or rethrow errors."),
    (r"(?i)(?:password|passwd|pwd|secret|api_key|token|auth_token)\s*[:=]\s*[\"'][^\"'\s]{4,}[\"']|(?:sk-[a-zA-Z0-9]{20,}|gh[pousr]_[A-Za-z0-9_]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)", "EXPOSED_SECRET", "Security risk: Plaintext API key, hardcoded password, or credential detected! Use environment variables.")
]


def check_file(filepath):
    if not os.path.exists(filepath):
        return []
    flaws = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line_idx, line in enumerate(f, 1):
                for pattern, flaw_type, msg in PATTERNS:
                    if re.search(pattern, line):
                        flaw = f"{filepath}:{line_idx} [{flaw_type}] -> {msg}"
                        flaws.append(flaw)
                        print(f"⚠️  [WATCHDOG ALERT]: {flaw}")
    except Exception:
        pass
    return flaws

def get_watched_files():
    watched = {}
    for root, dirs, files in os.walk("."):
        if any(d in root for d in [".git", "node_modules", ".venv", "__pycache__", "tests"]):
            continue
        for file in files:
            if file.endswith((".js", ".ts", ".py", ".go", ".rs", ".java", ".cs")):
                if not any(k in file for k in ["watchdog", "pre-commit", "server", "translate_humanpowers"]):
                    path = os.path.join(root, file)
                    try:
                        watched[path] = os.path.getmtime(path)
                    except OSError:
                        pass
    return watched

def scan_once():
    print("🛡️  [Artisan Watchdog] Running workspace code scan...")
    files = get_watched_files()
    total_flaws = 0
    for path in files:
        flaws = check_file(path)
        total_flaws += len(flaws)
    if total_flaws == 0:
        print("✅ [Artisan Watchdog] All active workspace files are clean.")
    else:
        print(f"❌ [Artisan Watchdog] {total_flaws} quality/security defect(s) detected.")

def watch_continuous(interval=2.0):
    print("🛡️  [Artisan Watchdog Daemon] Continuous real-time file monitoring active (Press Ctrl+C to stop)...")
    file_mtimes = get_watched_files()
    try:
        while True:
            time.sleep(interval)
            current_files = get_watched_files()
            # Check for modified or new files
            for path, mtime in current_files.items():
                if path not in file_mtimes or mtime > file_mtimes[path]:
                    check_file(path)
                    file_mtimes[path] = mtime
    except KeyboardInterrupt:
        print("\n[Artisan Watchdog Daemon] Stopped.")


if __name__ == "__main__":
    if "--watch" in sys.argv:
        watch_continuous()
    else:
        scan_once()
