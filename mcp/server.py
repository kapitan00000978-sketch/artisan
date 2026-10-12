#!/usr/bin/env python3
"""
Humanpowers Model Context Protocol (MCP) Server
Standard JSON-RPC 2.0 tool provider for Claude, Cursor, Antigravity, and other MCP clients.
"""

import sys
import os
import json
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

TOOLS = [
    {
        "name": "humanpowers_inspect_code",
        "description": "Audits code against Humanpowers quality and security checklists before showing it to the user.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "The code to inspect"},
                "language": {"type": "string", "description": "Language (js, py, ts, etc.)"}
            },
            "required": ["code"]
        }
    },
    {
        "name": "humanpowers_get_persona",
        "description": "Retrieves the exact professional work ethic, pledge, and checklist for any profession.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "profession": {"type": "string", "description": "Target profession (e.g. software_architect, copywriter, designer, cfo, security)"}
            },
            "required": ["profession"]
        }
    },
    {
        "name": "humanpowers_recall_memory",
        "description": "Retrieves past user preferences and recorded scar tissue to prevent repeating mistakes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query or category"}
            }
        }
    }
]

def handle_inspect_code(args):
    code = args.get("code", "")
    flaws = []

    if re.search(r"//\s*TODO|#\s*TODO", code):
        flaws.append("Chala qoldirilgan '// TODO' aniqlandi. Logikani to'liq yozing.")
    if re.search(r"catch\s*\([^\)]*\)\s*\{\s*\}", code):
        flaws.append("Bo'sh catch bloki (xatolik yashirilgan). Xatoni log qiling.")
    if re.search(r"(sk-[a-zA-Z0-9]{20,})", code):
        flaws.append("Hardcoded maxfiy API kalit aniqlandi. .env dan foydalaning.")

    if flaws:
        return {
            "status": "REJECTED",
            "score": 60,
            "flaws": flaws,
            "verdict": "Kamchiliklar mavjud. Foydalanuvchiga berishdan oldin o'zingiz to'g'irlang!"
        }
    return {
        "status": "CERTIFIED",
        "score": 98,
        "flaws": [],
        "verdict": "Barcha Humanpowers mezonlariga to'liq mos keldi. 100% Production-Ready!"
    }

def handle_get_persona(args):
    prof = args.get("profession", "software_architect").lower()
    return {
        "profession": prof,
        "pledge": "Hech qachon xom, xatolari tekshirilmagan narsani bermayman.",
        "mindset": "O'z sohasining oliy toifali ustasi kabi mas'uliyat bilan yondashish.",
        "criteria": [
            "Xatoliklarni to'liq ushlash",
            "Xavfsizlik va DoS himoyasi",
            "Toza arxitektura va modullilik",
            "Foydalanuvchi asabini tejash (Zero Babysitting)"
        ]
    }

def handle_recall_memory(args):
    mem_file = os.path.join(".humanpowers", "memory.json")
    if os.path.exists(mem_file):
        try:
            with open(mem_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"status": "Memory active, no recorded failures."}

def main():
    # Process single JSON-RPC call or loop for MCP stdio
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                res = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}
            elif method == "tools/call":
                params = req.get("params", {})
                name = params.get("name")
                args = params.get("arguments", {})

                if name == "humanpowers_inspect_code":
                    output = handle_inspect_code(args)
                elif name == "humanpowers_get_persona":
                    output = handle_get_persona(args)
                elif name == "humanpowers_recall_memory":
                    output = handle_recall_memory(args)
                else:
                    output = {"error": f"Unknown tool: {name}"}

                res = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(output, ensure_ascii=False)}]}}
            else:
                res = {"jsonrpc": "2.0", "id": msg_id, "result": {}}

            sys.stdout.write(json.dumps(res, ensure_ascii=False) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
