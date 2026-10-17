"""
End-to-End Integration Tests for Hallwright Gatekeeper Hook:
Tests repository initialization -> vendored gatekeeper setup -> secret commit attempt -> commit blocked -> clean commit succeeds.
"""

import os
import sys
import shutil
import tempfile
import subprocess
import argparse
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import hallwright_cli


def _run_git(cmd: list, cwd: str) -> subprocess.CompletedProcess:
    """Helper to execute git commands in a specified working directory."""
    return subprocess.run(
        ["git"] + cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )


def test_e2e_init_and_secret_commit_rejection():
    """Verifies that hallwright init vendors gatekeeper and git hook blocks commits with secrets."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # 1. Initialize empty git repository
        res_init = _run_git(["init"], cwd=tmpdir)
        assert res_init.returncode == 0, f"git init failed: {res_init.stderr}"

        # Set local git user identity for testing
        _run_git(["config", "user.email", "ci-bot@hallwright.org"], cwd=tmpdir)
        _run_git(["config", "user.name", "Hallwright CI Bot"], cwd=tmpdir)

        # 2. Run hallwright init
        init_args = argparse.Namespace(dir=tmpdir, no_hook=False, force=True, backup=False)
        ret_init = hallwright_cli.cmd_init(init_args)
        assert ret_init == 0

        # Verify hook and vendored gate files exist
        hook_path = os.path.join(tmpdir, ".git", "hooks", "pre-commit")
        assert os.path.exists(hook_path), "pre-commit hook was not installed"

        gate_dir = os.path.join(tmpdir, ".hallwright", "gate")
        assert os.path.exists(os.path.join(gate_dir, "gatekeeper.py"))
        assert os.path.exists(os.path.join(gate_dir, "detector.py"))
        assert os.path.exists(os.path.join(gate_dir, "remediator.py"))

        # 3. Create a file containing an exposed API secret
        leaked_secret_file = os.path.join(tmpdir, "credentials.py")
        fake_secret = "sk-" + "abcdef1234567890abcdef1234567890abcdef"
        with open(leaked_secret_file, "w", encoding="utf-8") as f:
            f.write(f'# Production keys\nAPI_SECRET = "{fake_secret}"\n')

        # Stage the secret file
        res_add = _run_git(["add", "credentials.py"], cwd=tmpdir)
        assert res_add.returncode == 0

        # 4. Attempt to commit the secret -> MUST BE BLOCKED BY PRE-COMMIT HOOK
        res_commit = _run_git(["commit", "-m", "add credentials"], cwd=tmpdir)
        assert res_commit.returncode != 0, "Git commit should have been rejected by the pre-commit hook!"
        combined_output = res_commit.stdout + res_commit.stderr
        assert "Hallwright" in combined_output or "DEFECT_DETECTED" in combined_output or "CRITICAL" in combined_output or "REJECTED" in combined_output

        # Verify no commit was made
        res_log = _run_git(["log", "-1"], cwd=tmpdir)
        assert res_log.returncode != 0, "No commits should exist in the repository"

        # 5. Fix the file by removing the secret and staging clean code
        with open(leaked_secret_file, "w", encoding="utf-8") as f:
            f.write('def get_environment_config():\n    return {"mode": "production"}\n')

        res_add_clean = _run_git(["add", "credentials.py"], cwd=tmpdir)
        assert res_add_clean.returncode == 0

        # 6. Commit the clean code -> MUST SUCCEED
        res_commit_clean = _run_git(["commit", "-m", "add clean credentials config"], cwd=tmpdir)
        assert res_commit_clean.returncode == 0, f"Clean commit failed: {res_commit_clean.stderr}"

        # Verify commit succeeded
        res_log_ok = _run_git(["log", "-1", "--oneline"], cwd=tmpdir)
        assert res_log_ok.returncode == 0
        assert "add clean credentials config" in res_log_ok.stdout
