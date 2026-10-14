#!/usr/bin/env python3
"""
Artisan Git Hook Installer
Installs pre-commit quality gate into .git/hooks/pre-commit
"""

import os
import sys
import stat

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

def install_hook():
    git_dir = os.path.join(".", ".git")
    if not os.path.isdir(git_dir):
        print("[-] Error: Not a git repository root (no .git directory found).")
        return False

    hooks_dir = os.path.join(git_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)

    hook_path = os.path.join(hooks_dir, "pre-commit")
    hook_content = """#!/bin/sh
# Artisan Pre-Commit Quality & Security Gate
if command -v python3 >/dev/null 2>&1; then
    python3 scripts/pre-commit-gatekeeper.py --staged
elif command -v python >/dev/null 2>&1; then
    python scripts/pre-commit-gatekeeper.py --staged
else
    echo "[-] Python not found; skipping Artisan pre-commit audit."
fi
"""

    with open(hook_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(hook_content)

    # Make executable on Unix
    try:
        current_stat = os.stat(hook_path)
        os.chmod(hook_path, current_stat.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except OSError as err:
        if sys.platform != "win32":
            print(f"Notice: Could not set executable permission: {err}", file=sys.stderr)

    print(f"✅ [ARTISAN HOOK]: Installed pre-commit hook into {hook_path}")
    return True

if __name__ == "__main__":
    success = install_hook()
    sys.exit(0 if success else 1)
