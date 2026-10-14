import re
import importlib.util
import os
import pytest

def get_gatekeeper_module():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "pre-commit-gatekeeper.py"))
    spec = importlib.util.spec_from_file_location("gatekeeper", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_gatekeeper_patterns_catch_stubs():
    gk = get_gatekeeper_module()
    stub_pattern = gk.PATTERNS[0][0]
    sample_code = "// " + "TODO" + ": implement logic"
    assert re.search(stub_pattern, sample_code) is not None

def test_gatekeeper_patterns_catch_silent_catch():
    gk = get_gatekeeper_module()
    catch_pattern = gk.PATTERNS[1][0]
    sample_code = "try { doSomething(); } catch (err) { }"
    assert re.search(catch_pattern, sample_code) is not None

def test_gatekeeper_patterns_catch_exposed_secrets():
    gk = get_gatekeeper_module()
    secret_pattern = gk.PATTERNS[2][0]
    sample_code = 'const apiKey = "' + 'sk-' + 'a' * 30 + '";'
    assert re.search(secret_pattern, sample_code) is not None

def test_gatekeeper_clean_code_passes():
    gk = get_gatekeeper_module()
    for pattern, _, _ in gk.PATTERNS:
        clean_code = "function add(a: number, b: number): number { return a + b; }"
        assert re.search(pattern, clean_code) is None
