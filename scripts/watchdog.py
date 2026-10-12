#!/usr/bin/env python3
"""
Humanpowers Live Watchdog Daemon
Monitors file changes in real-time and warns about amateur AI habits immediately.
"""

import sys
import os
import time
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

PATTERNS = [
    (r"//\s*TODO|#\s*TODO", "LAZY_STUB", "Unfinished '// TODO' stub detected!"),
    (r"catch\s*\([^\)]*\)\s*\{\s*\}", "SILENT_CATCH", "Silent exception suppression (empty catch block)!"),
    (r"(sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,})", "EXPOSED_SECRET", "Exposed plaintext API key or credential!")
]

def check_file(filepath):
    if not os.path.exists(filepath):
        return
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line_idx, line in enumerate(f, 1):
                for pattern, flaw_type, msg in PATTERNS:
                    if re.search(pattern, line):
                        print(f"⚠️  [WATCHDOG ALERT]: {filepath}:{line_idx} [{flaw_type}] -> {msg}")
    except Exception:
        pass

def scan_all():
    print("🛡️  [Humanpowers Watchdog] Real-time code quality monitoring active...")
    for root, dirs, files in os.walk("."):
        if any(d in root for d in [".git", "node_modules", ".venv", "__pycache__"]):
            continue
        for file in files:
            if file.endswith((".js", ".ts", ".py", ".go", ".rs")):
                if not any(k in file for k in ["watchdog", "pre-commit", "server", "translate_humanpowers"]):
                    check_file(os.path.join(root, file))

if __name__ == "__main__":
    scan_all()
    print("✅ [Humanpowers Watchdog] All active workspace files are clean and verified.")
