#!/usr/bin/env python3
"""
Hallwright Git Hook Installer
Installs pre-commit quality gate into .git/hooks/pre-commit
"""

import os
import sys
import stat
import shutil

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

def vendor_gatekeeper(target_dir: str = ".") -> bool:
    """Vendors self-contained gate files (detector, remediator, gatekeeper) into .hallwright/gate."""
    base_scripts = os.path.dirname(os.path.abspath(__file__))
    gate_dir = os.path.join(target_dir, ".hallwright", "gate")
    os.makedirs(gate_dir, exist_ok=True)

    files_to_vendor = [
        ("detector.py", "detector.py"),
        ("remediator.py", "remediator.py"),
        ("pre-commit-gatekeeper.py", "gatekeeper.py"),
        ("detector.js", "gatekeeper.js")
    ]
    for src_name, dst_name in files_to_vendor:
        src_path = os.path.join(base_scripts, src_name)
        dst_path = os.path.join(gate_dir, dst_name)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)

    # Vendor compiled Go standalone binary if available
    root_dir = os.path.dirname(base_scripts)
    for bin_candidate in ["hallwright.exe", "hallwright"]:
        bin_path = os.path.join(root_dir, "bin", bin_candidate)
        if os.path.exists(bin_path):
            shutil.copy2(bin_path, os.path.join(gate_dir, bin_candidate))
    return True

def install_hook(target_dir: str = ".", heal_by_default: bool = False, vendor_gate: bool = True):
    git_dir = os.path.join(target_dir, ".git")
    if not os.path.isdir(git_dir):
        print("[-] Error: Not a git repository root (no .git directory found).")
        return False

    if vendor_gate:
        vendor_gatekeeper(target_dir)

    hooks_dir = os.path.join(git_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)

    hook_path = os.path.join(hooks_dir, "pre-commit")
    heal_flag = " --heal" if heal_by_default else ""
    hook_content = f"""#!/bin/sh
# Hallwright Multi-Runtime Pre-Commit Quality & Security Gate
# 1. Native Go Standalone Binary (fastest, zero-runtime dependency)
if [ -f .hallwright/gate/hallwright ]; then
    .hallwright/gate/hallwright -s
    exit $?
elif [ -f .hallwright/gate/hallwright.exe ]; then
    .hallwright/gate/hallwright.exe -s
    exit $?
# 2. Vendored Python Gatekeeper (deep AST verification)
elif [ -f .hallwright/gate/gatekeeper.py ] && (command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1); then
    if command -v python3 >/dev/null 2>&1; then
        python3 .hallwright/gate/gatekeeper.py --staged{heal_flag}
        exit $?
    elif command -v python >/dev/null 2>&1; then
        python .hallwright/gate/gatekeeper.py --staged{heal_flag}
        exit $?
    fi
# 3. Vendored Node.js Gatekeeper (pure JS, zero npm dependencies)
elif [ -f .hallwright/gate/gatekeeper.js ] && command -v node >/dev/null 2>&1; then
    node .hallwright/gate/gatekeeper.js --staged
    exit $?
# 4. Global CLI or npx fallback
elif command -v hallwright >/dev/null 2>&1; then
    hallwright audit --staged{heal_flag}
    exit $?
elif [ -f scripts/pre-commit-gatekeeper.py ]; then
    if command -v python3 >/dev/null 2>&1; then
        python3 scripts/pre-commit-gatekeeper.py --staged{heal_flag}
        exit $?
    elif command -v python >/dev/null 2>&1; then
        python scripts/pre-commit-gatekeeper.py --staged{heal_flag}
        exit $?
    fi
elif command -v npx >/dev/null 2>&1 && [ -f package.json ]; then
    npx hallwright audit --staged{heal_flag}
    exit $?
else
    echo "[-] Notice: Hallwright audit skipped (no compatible runtime found)."
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
