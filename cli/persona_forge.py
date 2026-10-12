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
    print(f"🛡️ [Persona Forge] Yangi kasb yaratilmoqda: '{title}'...")

    persona_id = title.lower().replace(" ", "_").replace("-", "_")

    template = {
        "id": persona_id,
        "title": title,
        "domain": domain,
        "pledge": f"Hech qachon xom, tekshirilmagan yoki mas'uliyatsiz yechimni foydalanuvchiga bermayman. {title} sifatida 100% professional darajada javob beraman.",
        "checklists": [
            f"1. {title} sohasidagi qat'iy standartlar va qonun-qoidalarga to'liq muvofiqlik.",
            f"2. Barcha yashirin risklar va nozik jihatlarni oldindan aniqlash.",
            f"3. Tushunarli, aniq va ortiqcha 'suv'siz amaliy ko'rsatmalar.",
            f"4. Sanoatning ilg'or tajribalari (Best Practices) asosida tuzilganlik.",
            f"5. Yakuniy tekshiruv va 100% tayyor mahsulot sifatida topshirish."
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
            f.write(f"\n\n---\n\n### 🎭 {title} (Persona Forge orqali qo'shildi)\n")
            f.write(f"* **Qasamyod:** \"{template['pledge']}\"\n")
            f.write("* **Tekshiruv mezonlari:**\n")
            for ch in template["checklists"]:
                f.write(f"  - [ ] {ch}\n")

    print(f"✅ [MUVAFFAQIN]: '{title}' kasbi muvaffaqiyatli yaratildi va ro'yxatga olindi!")
    print(f"   Fayl: {file_path}")
    print(f"   Qasamyod: \"{template['pledge']}\"")
    return template

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Humanpowers Persona Forge")
    parser.add_argument("--create", help="Kasb nomi (masalan: 'Soliq Maslahatchisi')")
    args = parser.parse_args()

    if args.create:
        create_persona(args.create)
    else:
        # Default demo create
        create_persona("Kripto va Blokcheyn Auditori", "security")
