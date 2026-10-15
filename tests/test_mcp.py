import sys
import os
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mcp")))
import server

def test_mcp_list_council():
    res = server.handle_list_council({})
    assert "masters" in res
    assert res["council_size"] == 64
    names = [m["name"] for m in res["masters"]]
    assert any("Marcus" in n for n in names)
    assert any("Diana" in n for n in names)
    assert any("Elena" in n for n in names)
    assert any("Gabriel" in n for n in names)

def test_mcp_get_persona():
    marcus = server.handle_get_persona({"profession": "software_architect"})
    assert "Marcus" in marcus["name"]
    assert "Systems Sovereign" in marcus["archetype"]
    assert len(marcus["criteria"]) > 0

def test_mcp_inspect_code_clean():
    clean_code = "def calculate_total(price, tax):\n    return price + (price * tax)\n"
    res = server.handle_inspect_code({"code": clean_code})
    assert res["status"] == "CERTIFIED"
    assert res["score"] == 100
    assert len(res["flaws"]) == 0

def test_mcp_inspect_code_flawed():
    flawed_code = "try:\n    pass\nexcept:\n    pass\n"
    res = server.handle_inspect_code({"code": flawed_code})
    assert res["status"] == "REJECTED"
    assert len(res["flaws"]) > 0

def test_mcp_initialize_schema():
    req = {"jsonrpc": "2.0", "id": 1, "method": "initialize"}
    res = server.dispatch_request(req)
    assert res["result"]["protocolVersion"] == "2024-11-05"
    assert res["result"]["serverInfo"]["name"] == "artisan-mcp"
    assert res["result"]["serverInfo"]["version"] == "1.0.0"

def test_mcp_tools_list_contains_artisan_tools():
    req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    res = server.dispatch_request(req)
    tool_names = [t["name"] for t in res["result"]["tools"]]
    assert "artisan_inspect_code" in tool_names
    assert "artisan_get_persona" in tool_names
    assert "artisan_list_council" in tool_names
    assert "artisan_recall_memory" in tool_names

def test_mcp_inspect_code_catches_secrets_and_fixme():
    # Test the exact edge case from prompt: hardcoded password, FIXME, and Anthropic API key
    dangerous_code = """
    # FIXME: implement this later
    password = "hunter2"
    anthropic_key = "sk-ant-api03-abcdef123456789012345678"
    """
    res = server.handle_inspect_code({"code": dangerous_code})
    assert res["status"] == "REJECTED"
    assert len(res["flaws"]) >= 2
    flaw_text = " ".join(res["flaws"])
    assert "stub" in flaw_text.lower() or "todo" in flaw_text.lower() or "fixme" in flaw_text.lower()
    assert "secret" in flaw_text.lower() or "password" in flaw_text.lower() or "key" in flaw_text.lower()

def test_mcp_unknown_tool_returns_jsonrpc_32601_error():
    req = {
        "jsonrpc": "2.0",
        "id": 42,
        "method": "tools/call",
        "params": {
            "name": "non_existent_tool",
            "arguments": {}
        }
    }
    res = server.dispatch_request(req)
    assert "error" in res
    assert res["error"]["code"] == -32601
    assert "Tool not found" in res["error"]["message"]
    assert "result" not in res

def test_mcp_unknown_method_returns_jsonrpc_32601_error():
    req = {
        "jsonrpc": "2.0",
        "id": 43,
        "method": "unknown/method",
        "params": {}
    }
    res = server.dispatch_request(req)
    assert "error" in res
    assert res["error"]["code"] == -32601
    assert "Method not found" in res["error"]["message"]
