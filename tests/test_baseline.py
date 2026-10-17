"""
Tests for Hallwright Baseline Technical Debt Management (.hallwright/baseline.json).
Verifies baseline generation, debt tolerance on legacy code, and rejection of new regressions.
"""

import os
import sys
import json
import tempfile
import argparse
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))

from detector import scan_project, generate_baseline, load_baseline, is_flaw_in_baseline
import hallwright_cli


def test_generate_and_apply_baseline():
    """Verifies that generate_baseline records debt and scan_project tolerates baseline items."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create legacy files containing stubs
        legacy_file = os.path.join(tmpdir, "legacy_service.py")
        with open(legacy_file, "w", encoding="utf-8") as f:
            f.write("# " + "TODO" + ": implement legacy payment logic\n")
            f.write("def run_old():\n    try:\n        pass\n    except:\n        pass\n")

        # 1. Without baseline, scan must fail
        res_pre = scan_project(tmpdir, ignore_baseline=True)
        assert res_pre["passed"] is False
        assert len(res_pre["findings"]) >= 1

        # 2. Generate baseline
        baseline_file = generate_baseline(tmpdir)
        assert os.path.exists(baseline_file)
        assert os.path.basename(baseline_file) == "baseline.json"

        # Verify baseline JSON format
        with open(baseline_file, "r", encoding="utf-8") as f:
            base_data = json.load(f)
            assert "version" in base_data
            assert "total_flaws" in base_data
            assert len(base_data["flaws"]) >= 1

        # 3. Scan with baseline enabled -> MUST PASS
        res_post = scan_project(tmpdir, ignore_baseline=False)
        assert res_post["passed"] is True, f"Expected pass with baseline, got: {res_post['findings']}"
        assert len(res_post["findings"]) == 0
        assert len(res_post["baseline_findings"]) >= 1
        assert res_post["score"] == 100

        # 4. Introduce a brand new regression
        new_vuln_file = os.path.join(tmpdir, "new_vuln.py")
        with open(new_vuln_file, "w", encoding="utf-8") as f:
            f.write("result = eval(user_input)\n")

        # Scan must now FAIL because the new flaw is not in baseline
        res_regression = scan_project(tmpdir, ignore_baseline=False)
        assert res_regression["passed"] is False
        assert len(res_regression["findings"]) == 1
        assert res_regression["findings"][0]["rule_id"] == "DANGEROUS_EVAL_EXEC"
        assert len(res_regression["baseline_findings"]) >= 1


def test_cli_audit_with_generate_baseline(capsys):
    """Verifies hallwright audit --generate-baseline via CLI."""
    with tempfile.TemporaryDirectory() as tmpdir:
        orig_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            sample = os.path.join(tmpdir, "sample.py")
            with open(sample, "w", encoding="utf-8") as f:
                f.write("// " + "FIXME" + ": legacy stub\n")

            # Run CLI audit --generate-baseline
            args_gen = argparse.Namespace(
                staged=False,
                vibe=False,
                json=False,
                sarif=False,
                format="text",
                baseline=None,
                generate_baseline=True
            )
            ret_gen = hallwright_cli.cmd_audit(args_gen)
            assert ret_gen == 0
            captured_gen = capsys.readouterr()
            assert "Generated technical debt baseline" in captured_gen.out

            # Run CLI audit -- MUST PASS with baseline
            args_audit = argparse.Namespace(
                staged=False,
                vibe=False,
                json=True,
                sarif=False,
                format="json",
                baseline=None,
                generate_baseline=False
            )
            ret_audit = hallwright_cli.cmd_audit(args_audit)
            assert ret_audit == 0
            captured_audit = capsys.readouterr()
            data = json.loads(captured_audit.out)
            assert data["passed"] is True
            assert len(data["baseline_findings"]) >= 1
            assert len(data["findings"]) == 0
        finally:
            os.chdir(orig_cwd)
