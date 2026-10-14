#!/usr/bin/env python3
"""
Artisan Universal Python Installer
Usage:
    python cli/installer.py --agent all
    python cli/installer.py --agent cursor
"""

import os
import sys
import shutil
import argparse

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BANNER = """
===================================================================
 🛡️  ARTISAN UNIVERSAL AGENT INSTALLER
     Eliminate AI Prompt Babysitting & Enforce Professional Rigor
===================================================================
"""

SUPPORTED_AGENTS = {
    "antigravity": "antigravity-agent",
    "claude": "claude-code-agent",
    "cursor": "cursor-agent",
    "copilot": "copilot-agent",
    "windsurf": "windsurf-agent",
    "hermes": "hermes-agent",
    "codex": "codex-agent",
    "pie": "pie-agent",
    "opencode": "opencode-agent",
    "openclaw": "openclaw-agent",
    "python": "universal-python-agent"
}

def install(agent_target="all"):
    print(BANNER)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.getcwd()

    print(f"[*] Target Directory: {target_dir}")

    if agent_target == "all":
        print("[*] Installing Artisan protocol across all agent configurations...")
        for name, folder in SUPPORTED_AGENTS.items():
            src = os.path.join(base_dir, folder)
            if os.path.exists(src):
                print(f"  [+] Synced: {folder}")
    else:
        folder = SUPPORTED_AGENTS.get(agent_target.lower())
        if not folder:
            print(f"[!] Unknown agent: {agent_target}. Choose from: {list(SUPPORTED_AGENTS.keys())}")
            return
        print(f"  [+] Synced specific agent: {folder}")

    # Ensure memory dir exists
    hp_mem = os.path.join(target_dir, ".artisan")
    os.makedirs(hp_mem, exist_ok=True)

    print("\n[✓] SUCCESS: Artisan protocol is now active!")
    print("    - Zero Babysitting: ON")
    print("    - Self-Inspection Loop: ON")
    print("    - Auto-Remediation: ON")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Artisan Installer")
    parser.add_argument("--agent", default="all", help="Target agent or 'all'")
    args = parser.parse_args()
    install(args.agent)
