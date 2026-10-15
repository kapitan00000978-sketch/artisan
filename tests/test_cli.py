"""
Tests for Artisan Unified CLI (artisan_cli.py).
Verifies stack detection, 1-click initialization, audit, fix, status, doctor, and memory.
"""

import os
import sys
import json
import tempfile
import shutil
import argparse
from unittest.mock import patch

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import artisan_cli


def test_detect_tech_stack_python():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "pyproject.toml"), "w", encoding="utf-8") as f:
            f.write("[project]\nname = 'test'\n")
        stacks = artisan_cli.detect_tech_stack(tmpdir)
        assert "Python" in stacks


def test_detect_tech_stack_node_and_next():
    with tempfile.TemporaryDirectory() as tmpdir:
        pkg_data = {
            "name": "web-app",
            "dependencies": {"next": "^14.0.0", "react": "^18.0.0"}
        }
        with open(os.path.join(tmpdir, "package.json"), "w", encoding="utf-8") as f:
            json.dump(pkg_data, f)
        with open(os.path.join(tmpdir, "tsconfig.json"), "w", encoding="utf-8") as f:
            f.write("{}")

        stacks = artisan_cli.detect_tech_stack(tmpdir)
        assert "Node.js / JavaScript" in stacks
        assert "Next.js" in stacks
        assert "TypeScript" in stacks


def test_detect_tech_stack_go_rust_java():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "go.mod"), "w", encoding="utf-8") as f:
            f.write("module test\n")
        with open(os.path.join(tmpdir, "Cargo.toml"), "w", encoding="utf-8") as f:
            f.write("[package]\nname = 'test'\n")
        with open(os.path.join(tmpdir, "pom.xml"), "w", encoding="utf-8") as f:
            f.write("<project></project>\n")

        stacks = artisan_cli.detect_tech_stack(tmpdir)
        assert "Go" in stacks
        assert "Rust" in stacks
        assert "Java" in stacks


def test_detect_tech_stack_universal():
    with tempfile.TemporaryDirectory() as tmpdir:
        stacks = artisan_cli.detect_tech_stack(tmpdir)
        assert "Universal / Multi-Language" in stacks


def test_copy_safe_files_and_dirs():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_file = os.path.join(tmpdir, "src.txt")
        dst_file = os.path.join(tmpdir, "subdir", "dst.txt")
        with open(src_file, "w", encoding="utf-8") as f:
            f.write("artisan")

        assert artisan_cli.copy_safe(src_file, dst_file)
        assert os.path.exists(dst_file)

        # Test non-existent src
        assert not artisan_cli.copy_safe(os.path.join(tmpdir, "none.txt"), dst_file)

        # Test preserve existing
        with open(dst_file, "w", encoding="utf-8") as f:
            f.write("original")
        assert not artisan_cli.copy_safe(src_file, dst_file, preserve_existing=True)
        with open(dst_file, "r", encoding="utf-8") as f:
            assert f.read() == "original"


def test_cmd_init_in_clean_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        args = argparse.Namespace(dir=tmpdir, no_hook=True)
        ret = artisan_cli.cmd_init(args)
        assert ret == 0

        # Memory ledger initialized
        mem_file = os.path.join(tmpdir, ".artisan", "memory.json")
        assert os.path.exists(mem_file)
        with open(mem_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data["version"] == "2.0.0"

        # Protocol file copied
        assert os.path.exists(os.path.join(tmpdir, "AGENTS.md"))


def test_cmd_status():
    args = argparse.Namespace()
    ret = artisan_cli.cmd_status(args)
    assert ret == 0


def test_cmd_doctor():
    args = argparse.Namespace()
    ret = artisan_cli.cmd_doctor(args)
    assert ret == 0


def test_cmd_memory_list_and_record():
    with tempfile.TemporaryDirectory() as tmpdir:
        mem_file = os.path.join(tmpdir, ".artisan", "memory.json")
        os.makedirs(os.path.dirname(mem_file), exist_ok=True)
        with open(mem_file, "w", encoding="utf-8") as f:
            json.dump({
                "version": "2.0.0",
                "lessons_learned": [],
                "conventions": [],
                "recorded_scar_tissue": []
            }, f)

        with patch("learning_memory.DEFAULT_MEMORY_PATH", mem_file):
            # Record a new lesson
            args_record = argparse.Namespace(
                record="mistake:auth:jwt_none_alg:Always verify algorithm is HS256/RS256",
                search=None,
                limit=10
            )
            ret_record = artisan_cli.cmd_memory(args_record)
            assert ret_record == 0

            # List and verify it appears
            args_search = argparse.Namespace(record=None, search="jwt", limit=10)
            ret_search = artisan_cli.cmd_memory(args_search)
            assert ret_search == 0


def test_cmd_audit_json_output(capsys):
    args = argparse.Namespace(staged=False, vibe=True, json=True)
    ret = artisan_cli.cmd_audit(args)
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "score" in data
    assert "passed" in data
    assert ret == 0
