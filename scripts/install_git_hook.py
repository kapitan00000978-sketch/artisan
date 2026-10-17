#!/usr/bin/env python3
"""
Hallwright Git Hook Installer
Installs pre-commit quality gate into .git/hooks/pre-commit
"""

import os
import sys
import stat

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

def install_hook(heal_by_default: bool = False):
    git_dir = os.path.join(".", ".git")
    if not os.path.isdir(git_dir):
        print("[-] Error: Not a git repository root (no .git directory found).")
        return False

    hooks_dir = os.path.join(git_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)

    hook_path = os.path.join(hooks_dir, "pre-commit")
    heal_flag = " --heal" if heal_by_default else ""
    hook_content = f"""#!/bin/sh
# Hallwright Pre-Commit Quality & Security Gate
if command -v hallwright >/dev/null 2>&1; then
    hallwright audit --staged{heal_flag}
elif [ -f scripts/pre-commit-gatekeeper.py ]; then
    if command -v python3 >/dev/null 2>&1; then
        python3 scripts/pre-commit-gatekeeper.py --staged{heal_flag}
    elif command -v python >/dev/null 2>&1; then
        python scripts/pre-commit-gatekeeper.py --staged{heal_flag}
    fi
elif command -v npx >/dev/null 2>&1 && [ -f package.json ]; then
    npx hallwright audit --staged{heal_flag}
else
    echo "[-] Notice: Hallwright audit skipped (neither 'hallwright' CLI nor local gatekeeper found)."
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

    heal_msg = " [Auto-Heal: ENABLED]" if heal_by_default else ""
    print(f"✅ [HALLWRIGHT HOOK]: Installed pre-commit hook into {hook_path}{heal_msg}")
    return True

if __name__ == "__main__":
    heal_mode = "--heal" in sys.argv
    success = install_hook(heal_by_default=heal_mode)
    sys.exit(0 if success else 1)
