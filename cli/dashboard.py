#!/usr/bin/env python3
"""
Artisan Interactive Terminal Dashboard (HUD)
Empowered by The Council of Masters
"""

import sys
import os
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

COUNCIL_MEMBERS = [
    ("Marcus 'The Vanguard' Sterling", "Senior Software Architect", "Systems Sovereign & Zero-Tech-Debt Purist", "If a system cannot fail gracefully under catastrophic load, it was never engineered—it was merely wished into existence."),
    ("Diana 'The Closer' Drake", "Elite Conversion Copywriter", "Neuromarketing Alchemist & Direct-Response Virtuoso", "Every word must fight for its life on the page. If it doesn't move the buyer to decisive action, it is dead weight."),
    ("Elena 'The Visionary' Rostova", "Principal UI/UX Designer", "Aesthetic Sovereign & Spatial Ergonomics Master", "Aesthetics without ergonomics is decoration; ergonomics without beauty is sterile. A masterwork harmonizes both."),
    ("Victor 'The Fortress' Montgomery", "Startup Fractional CFO", "Unit-Economics Inquisitor & Capital Defense Strategist", "Gross margins and payback periods do not care about your pitch deck enthusiasm. Show me the cash conversion cycle."),
    ("Arthur 'The Ironclad' Pendelton", "Senior Commercial Counsel", "Commercial Safeguard & Contractual Litigator", "An ambiguous clause is an invitation to litigation. We draft today so that your future adversaries weep before depositions begin."),
    ("Dr. Evelyn 'The Oracle' Reed", "Staff Data Scientist & ML Lead", "Empirical Scientist & ML Ops Gatekeeper", "If your validation data leaks into your training set, your model is simply cheating itself into a production disaster."),
    ("Gabriel 'The Sentinel' Frost", "Principal Cybersecurity Auditor", "Zero-Trust Inquisitor & Threat Modeling Specialist", "There are two types of systems: those that enforce zero trust, and those that are already compromised without knowing it."),
    ("Gareth 'The Unbreakable' Drake", "DevOps & Cloud SRE Architect", "Chaos Engineering Commander & Zero-Downtime Guardian", "Hope is not an infrastructure strategy. If your deployment requires manual prayer, your architecture is broken.")
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_dashboard():
    clear_screen()
    print("=" * 80)
    print("  🛡️  ARTISAN CONTROL CENTER & AGENT HUD")
    print("      Empowered by The Council of Masters — Quality & Security Protocol")
    print("=" * 80)
    print(" [STATUS]           : PROTOCOL ACTIVE")
    print(" [SUPPORTED AGENTS] : 11 Standalone Agent Environments Synchronized")
    print(" [MEMORY LEDGER]    : .artisan/memory.json (Synchronized)")
    print("=" * 80)

    # Load metrics
    metrics_path = os.path.join(".artisan", "metrics.json")
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                hours = round(data.get("timeSavedMinutes", 0) / 60, 1)
                print(f" 📊 METRICS: {data.get('totalTasksCompleted')} tasks | {hours} hrs saved | {data.get('flawsAutoRemediated')} flaws remediated | {data.get('averageQualityScore')}/100 quality")
        except (json.JSONDecodeError, OSError) as err:
            print(f" [!] Notice: Could not read metrics ledger: {err}")
    print("-" * 80)

    print(" 🏛️  THE COUNCIL OF MASTERS (ACTIVE CHARACTER ROSTER):")
    for name, title, archetype, _ in COUNCIL_MEMBERS:
        print(f"  • {name:<34} | {title:<28} | {archetype}")

    print("-" * 80)
    print(" 📂 SUPPORTED AGENT ECOSYSTEM:")
    agents = [
        "1. Antigravity & Gemini CLI", "2. Claude Code CLI", "3. Cursor AI Editor",
        "4. GitHub Copilot", "5. Windsurf Cascade", "6. Nous Hermes Agent",
        "7. OpenAI Codex", "8. Pi/Pie Coding Agent", "9. OpenCode TUI",
        "10. OpenClaw Platform", "11. Universal Python Agent"
    ]
    for i in range(0, len(agents), 2):
        row = f"  • {agents[i]:<36}"
        if i + 1 < len(agents):
            row += f" • {agents[i+1]}"
        print(row)

    print("=" * 80)
    print(" 🛠️  QUICK ACTIONS:")
    print("  [1] Run Pre-Commit Gatekeeper Audit")
    print("  [2] Run Live Watchdog Scanner")
    print("  [3] Inspect Council of Masters & Signature Mottos")
    print("  [4] Create Custom Domain Persona (Persona Forge)")
    print("  [5] Inspect Persistent Memory Ledger")
    print("  [6] View ROI & Audit Report")
    print("  [0] Exit")
    print("=" * 80)

def show_council_details():
    clear_screen()
    print("=" * 80)
    print("  🏛️  THE COUNCIL OF MASTERS — DOSSIERS & SIGNATURE MOTTOS")
    print("=" * 80)
    for idx, (name, title, archetype, motto) in enumerate(COUNCIL_MEMBERS, 1):
        print(f"\n[{idx}] {name}")
        print(f"    Title     : {title}")
        print(f"    Archetype : {archetype}")
        print(f"    Motto     : \"{motto}\"")
    print("\n" + "=" * 80)
    input("Press Enter to return to main dashboard...")

def main():
    while True:
        render_dashboard()
        choice = input("\n👉 Select an action [0-6]: ").strip()
        if choice == "1":
            os.system("python scripts/pre-commit-gatekeeper.py")
            input("\nPress Enter to return...")
        elif choice == "2":
            os.system("python scripts/watchdog.py")
            input("\nPress Enter to return...")
        elif choice == "3":
            show_council_details()
        elif choice == "4":
            name = input("Enter new profession title (e.g. 'Cloud Security Architect'): ").strip()
            if name:
                os.system(f'python cli/persona_forge.py --create "{name}"')
            input("\nPress Enter to return...")
        elif choice == "5":
            mem_path = os.path.join(".artisan", "memory.json")
            if os.path.exists(mem_path):
                with open(mem_path, "r", encoding="utf-8") as f:
                    print(json.dumps(json.load(f), indent=2))
            input("\nPress Enter to return...")
        elif choice == "6":
            os.system("python scripts/roi_tracker.py")
            input("\nPress Enter to return...")
        elif choice == "0":
            print("\nExiting Artisan Control Center. Happy Crafting!\n")
            break

if __name__ == "__main__":
    main()
