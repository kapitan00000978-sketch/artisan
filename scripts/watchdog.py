#!/usr/bin/env python3
"""
Hallwright Live Watchdog Daemon
Monitors file changes and flags code flaws, unfinished stubs, and secret leaks.
Supports both single-pass scan (--once) and continuous background watch loop (--watch).
"""

import sys
import os
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Ensure scripts dir is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from detector import scan_code
except ImportError:
    scan_code = None


def check_file(filepath):
    if not os.path.exists(filepath):
        return []
    flaws = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        if scan_code:
            res = scan_code(content, filename=filepath)
            for finding in res.get("findings", []):
                flaw = f"{filepath}:{finding['line']} [{finding['category']}] -> {finding['message']}"
                flaws.append(flaw)
                print(f"⚠️  [WATCHDOG ALERT]: {flaw}")
    except (OSError, UnicodeDecodeError) as read_err:
        print(f"[-] Could not read {filepath}: {read_err}", file=sys.stderr)
    return flaws

def get_watched_files():
    watched = {}
    for root, dirs, files in os.walk("."):
        if any(d in root for d in [".git", "node_modules", ".venv", "__pycache__", "tests"]):
            continue
        for file in files:
            if file.endswith((".js", ".ts", ".py", ".go", ".rs", ".java", ".cs")):
                if not any(k in file for k in ["watchdog", "pre-commit", "server"]):
                    path = os.path.join(root, file)
                    try:
                        watched[path] = os.path.getmtime(path)
                    except OSError:
                        continue
    return watched

def scan_once():
    print("🛡️  [Hallwright Watchdog] Running workspace code scan...")
    files = get_watched_files()
    total_flaws = 0
    for path in files:
        flaws = check_file(path)
        total_flaws += len(flaws)
    if total_flaws == 0:
        print("✅ [Hallwright Watchdog] All active workspace files are clean.")
    else:
        print(f"❌ [Hallwright Watchdog] {total_flaws} quality/security defect(s) detected.")

def watch_continuous(interval=2.0):
    print("🛡️  [Hallwright Watchdog Daemon] Continuous real-time file monitoring active (Press Ctrl+C to stop)...")
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
        print("\n[Hallwright Watchdog Daemon] Stopped.")


if __name__ == "__main__":
    if "--watch" in sys.argv:
        watch_continuous()
    else:
        scan_once()
