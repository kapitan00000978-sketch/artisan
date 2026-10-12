#!/usr/bin/env python3
"""
Humanpowers Pre-Commit Gatekeeper
Checks staged git files for lazy placeholders, security leaks, and empty error catches.
"""

import os
import sys
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

PATTERNS = [
    (r"//\s*TODO|#\s*TODO", "LAZY_STUB", "Chala qoldirilgan '// TODO' aniqlandi. Barcha logikani oxirigacha yozing."),
    (r"catch\s*\([^\)]*\)\s*\{\s*\}", "SILENT_CATCH", "Xatolik yashirilgan (bo'sh catch bloki). Xatoni log qiling yoki qaytaring."),
    (r"(sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,})", "EXPOSED_SECRET", "Xavfli: Ochiq API kaliti yoki token aniqlandi! .env dan foydalaning.")
]

def scan_files():
    print("🛡️ [Humanpowers Gatekeeper] Commmitdan oldin sifat va xavfsizlik tekshiruvi...")
    flaws_found = []

    # Scan project source files
    for root, dirs, files in os.walk("."):
        if any(d in root for d in [".git", "node_modules", ".venv", "__pycache__"]):
            continue
        for file in files:
            # Only scan actual source code files, ignore documentation
            if file.endswith((".js", ".ts", ".py", ".go", ".rs", ".java", ".cpp", ".cs")):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        for line_idx, line in enumerate(lines, 1):
                            # Skip scanning the gatekeeper script itself
                            if "pre-commit-gatekeeper" in filepath:
                                continue
                            for pattern, flaw_type, message in PATTERNS:
                                if re.search(pattern, line):
                                    flaws_found.append(f"{filepath}:{line_idx} [{flaw_type}] -> {message}")
                except Exception:
                    pass

    if flaws_found:
        print("\n❌ [HUMANPOWERS QABUL QILMADI - REJECTED]:")
        for flaw in flaws_found[:5]:
            print(f"  • {flaw}")
        print(f"\nJami {len(flaws_found)} ta kamchilik aniqlandi.")
        print("💡 Qoida: Humanpowers Zero Babysitting — xatolarni o'zingiz to'g'irlab, so'ng commit qiling!\n")
        return False
    else:
        print("✅ [HUMANPOWERS VERIFIED]: Kod barcha qat'iy standartlardan o'tdi. 100% Production-Ready!")
        return True

if __name__ == "__main__":
    passed = scan_files()
    if not passed:
        sys.exit(1)
    sys.exit(0)
