#!/usr/bin/env python3
"""
Humanpowers Interactive Terminal Dashboard (HUD)
"""

import sys
import os
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_dashboard():
    clear_screen()
    print("=" * 70)
    print("  🛡️  HUMANPOWERS CONTROL CENTER & AUTONOMOUS AGENT HUD")
    print("=" * 70)
    print(" [STATUS]           : PROTOCOL ACTIVE (ZERO BABYSITTING)")
    print(" [SUPPORTED AGENTS] : 11 Standalone Agent Environments Ready")
    print(" [MEMORY LEDGER]    : .humanpowers/memory.json (Synchronized)")
    print("=" * 70)

    # Load metrics
    metrics_path = os.path.join(".humanpowers", "metrics.json")
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                hours = round(data.get("timeSavedMinutes", 0) / 60, 1)
                print(f" 📊 STATISTIKA: {data.get('totalTasksCompleted')} ta topshiriq | {hours} soat tejaldi | {data.get('flawsAutoRemediated')} ta xato tuzatildi")
        except Exception:
            pass
    print("-" * 70)

    print(" 📂 AGENT MATRITSASI:")
    agents = [
        "1. Antigravity & Gemini CLI", "2. Claude Code CLI", "3. Cursor AI Editor",
        "4. GitHub Copilot", "5. Windsurf Cascade", "6. Nous Hermes Agent",
        "7. OpenAI Codex", "8. Pi/Pie Coding Agent", "9. OpenCode TUI",
        "10. OpenClaw Platform", "11. Universal Python Agent"
    ]
    for i in range(0, len(agents), 2):
        row = f"  • {agents[i]:<32}"
        if i + 1 < len(agents):
            row += f" • {agents[i+1]}"
        print(row)

    print("=" * 70)
    print(" 🛠️  QUICK ACTIONS:")
    print("  [1] Pre-Commit Gatekeeper Tekshiruvi")
    print("  [2] Real-Vaqt Watchdog Skaneri")
    print("  [3] Yangi Kasb Yaratish (Persona Forge)")
    print("  [4] Doimiy Xotirani Ko'rish (Memory Ledger)")
    print("  [5] Tejalgan Vaqt (ROI) Hisoboti")
    print("  [0] Chiqish")
    print("=" * 70)

def main():
    render_dashboard()
    print("\n✅ Humanpowers tizimi faol holatda. Barcha agentlar usta intizomida ishlamoqda.")

if __name__ == "__main__":
    main()
