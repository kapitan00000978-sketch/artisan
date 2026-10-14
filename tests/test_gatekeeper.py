import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from detector import scan_code, RULES, run_gitleaks

# --- TASK 2: Unit tests for each stub rule ---

def test_stubs_todo():
    res = scan_code("// " + "TODO" + ": implement logic")
    assert res["status"] == "REJECTED"
    assert any("Unfinished stub" in f for f in res["flaws"])

def test_stubs_fixme():
    res = scan_code("# " + "FIXME" + " later: fix edge case")
    assert res["status"] == "REJECTED"
    assert any("Unfinished stub" in f for f in res["flaws"])

def test_stubs_xxx():
    res = scan_code("// " + "XXX" + ": refactor this routine")
    assert res["status"] == "REJECTED"
    assert any("Unfinished stub" in f for f in res["flaws"])

def test_stubs_hack():
    res = scan_code("# " + "HACK" + ": temporary bypass")
    assert res["status"] == "REJECTED"
    assert any("Unfinished stub" in f for f in res["flaws"])

def test_stubs_implement_later():
    res = scan_code("# please " + "implement later")
    assert res["status"] == "REJECTED"
    assert any("Unfinished stub" in f for f in res["flaws"])

def test_stubs_pass_placeholder():
    code = "def handle():\n    pass  # to be filled\n"
    res = scan_code(code)
    assert res["status"] == "REJECTED"
    assert any("Pass placeholder" in f for f in res["flaws"])

def test_stubs_empty_catch():
    code1 = "try { run(); } catch (err) {}"
    res1 = scan_code(code1)
    assert res1["status"] == "REJECTED"
    assert any("Empty catch" in f for f in res1["flaws"])

    code2 = "try { run(); } catch {}"
    res2 = scan_code(code2)
    assert res2["status"] == "REJECTED"
    assert any("Empty catch" in f for f in res2["flaws"])

def test_stubs_bare_except():
    code = "try:\n    run()\nexcept:\n    pass\n"
    res = scan_code(code)
    assert res["status"] == "REJECTED"
    assert any("Silent exception" in f for f in res["flaws"])

def test_stubs_except_exception_pass():
    code = "try:\n    run()\nexcept Exception:\n    pass\n"
    res = scan_code(code)
    assert res["status"] == "REJECTED"
    assert any("Silent exception" in f for f in res["flaws"])


# --- TASK 2: Dangerous Execution ---

def test_dangerous_eval():
    code = "result = eval(user_input)"
    res = scan_code(code)
    assert res["status"] == "REJECTED"
    assert any("Dangerous dynamic execution" in f for f in res["flaws"])

def test_dangerous_exec():
    code = "exec(payload)"
    res = scan_code(code)
    assert res["status"] == "REJECTED"
    assert any("Dangerous dynamic execution" in f for f in res["flaws"])


# --- TASK 2: Secrets & Credentials ---

def test_secrets_anthropic():
    code = 'key = "sk-ant-api03-abcdefghijklmnopqrstuvwx"'
    res = scan_code(code)
    assert res["status"] == "REJECTED"
    assert any("Anthropic API key" in f for f in res["flaws"])

def test_secrets_openai():
    code = 'token = "sk-abcdefghijklmnopqrstuvwxyz1234567890"'
    res = scan_code(code)
    assert res["status"] == "REJECTED"
    assert any("API key detected" in f for f in res["flaws"])

def test_secrets_github():
    code1 = 'gh = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"'
    assert scan_code(code1)["status"] == "REJECTED"

    code2 = 'gh = "gho_1234567890abcdefghijklmnopqrstuvwxyz"'
    assert scan_code(code2)["status"] == "REJECTED"

    code3 = 'gh = "github_pat_1234567890abcdefghijklmnopqrstuvwxyz"'
    assert scan_code(code3)["status"] == "REJECTED"

def test_secrets_aws():
    code = 'AWS_KEY = "AKIA1234567890ABCDEF"'
    res = scan_code(code)
    assert res["status"] == "REJECTED"
    assert any("AWS Access Key" in f for f in res["flaws"])

def test_secrets_slack():
    code = 'slack = "xoxb-1234567890-abcdefghij"'
    res = scan_code(code)
    assert res["status"] == "REJECTED"
    assert any("Slack token" in f for f in res["flaws"])

def test_secrets_google():
    code = 'google_key = "AIza' + 'a' * 35 + '"'
    res = scan_code(code)
    assert res["status"] == "REJECTED"
    assert any("Google API key" in f for f in res["flaws"])

def test_secrets_private_key():
    code = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA0\n-----END RSA PRIVATE KEY-----"
    res = scan_code(code)
    assert res["status"] == "REJECTED"
    assert any("Private Key" in f for f in res["flaws"])

def test_secrets_literal_assignments():
    assert scan_code('password="hunter2"')["status"] == "REJECTED"
    assert scan_code('secret = "super_classified_secret"')["status"] == "REJECTED"
    assert scan_code('api_key = "production_key_xyz"')["status"] == "REJECTED"
    assert scan_code('auth_token: "my-secure-token"')["status"] == "REJECTED"


# --- TASK 2: Inline ignore marker ---

def test_artisan_ignore_marker():
    code = 'password = "hunter2" # artisan-ignore\n'
    res = scan_code(code)
    assert res["status"] == "CERTIFIED"
    assert res["score"] == 100
    assert len(res["flaws"]) == 0


# --- TASK 2: Clean code passes ---

def test_clean_sample_passes():
    code = """
def calculate_tax(amount: float, rate: float) -> float:
    \"\"\"Calculates total tax based on the given rate.\"\"\"
    if amount < 0 or rate < 0:
        raise ValueError("Amount and rate must be non-negative")
    return amount * rate
"""
    res = scan_code(code)
    assert res["status"] == "CERTIFIED"
    assert res["score"] == 100
    assert len(res["flaws"]) == 0

def test_dangerous_sql_injection():
    code = 'query = f"SELECT * FROM users WHERE id = {user_id}"'
    res = scan_code(code)
    assert res["status"] == "REJECTED"
    assert any("SQL injection" in f for f in res["flaws"])

def test_secrets_jwt():
    # Header.Payload.Signature
    jwt_sample = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4ifQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    code = f'token = "{jwt_sample}"'
    res = scan_code(code)
    assert res["status"] == "REJECTED"
    assert any("JWT" in f for f in res["flaws"])

def test_scan_file_exists():
    from detector import scan_file
    res = scan_file("scripts/detector.py")
    assert res is not None
    assert "status" in res

def test_git_hook_installer():
    import importlib.util
    hook_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "install_git_hook.py"))
    spec = importlib.util.spec_from_file_location("install_git_hook", hook_script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.install_hook() is True

