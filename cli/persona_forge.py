#!/usr/bin/env python3
"""
Humanpowers Persona Forge
CLI tool to generate and register new professional personas with rigorous craftsmanship checklists.
"""

import sys
import os
import json
import argparse

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

def create_persona(title, domain="general"):
    print(f"🛡️ [Persona Forge] Generating new professional persona: '{title}'...")

    persona_id = title.lower().replace(" ", "_").replace("-", "_")

    template = {
        "id": persona_id,
        "title": title,
        "domain": domain,
        "pledge": f"I will never deliver unverified, incomplete, or irresponsible output. As a veteran {title}, I stand behind every artifact with 100% production-ready quality.",
        "checklists": [
            f"1. Strict compliance with {title} industry benchmarks and regulatory standards.",
            f"2. Pre-emptive identification of hidden downside risks and edge cases.",
            f"3. Clear, concise, and actionable instructions with zero cognitive fluff.",
            f"4. Built on battle-tested industry best practices.",
            f"5. Autonomous pre-delivery verification satisfying zero-babysitting criteria."
        ]
    }

    persona_dir = os.path.join(".humanpowers", "personas")
    os.makedirs(persona_dir, exist_ok=True)
    file_path = os.path.join(persona_dir, f"{persona_id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)

    # Append to professions directory rule if exists
    rule_path = os.path.join(".agents", "plugins", "craftsman-agent", "rules", "02-professions-directory.md")
    if os.path.exists(rule_path):
        with open(rule_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n---\n\n### 🎭 {title} (Registered via Persona Forge)\n")
            f.write(f"* **Pledge:** \"{template['pledge']}\"\n")
            f.write("* **Checklist:**\n")
            for ch in template["checklists"]:
                f.write(f"  - [ ] {ch}\n")

    print(f"✅ [SUCCESS]: '{title}' persona successfully registered!")
    print(f"   Saved to: {file_path}")
    print(f"   Pledge: \"{template['pledge']}\"")
    return template

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Humanpowers Persona Forge")
    parser.add_argument("--create", help="Profession title (e.g. 'Tax Strategist')")
    parser.add_argument("--domain", default="general", help="Domain category")
    args = parser.parse_args()

    if args.create:
        create_persona(args.create, args.domain)
    else:
        title = input("Enter profession title (e.g. 'Tax Strategist'): ").strip()
        if title:
            create_persona(title)
        else:
            parser.print_help()
