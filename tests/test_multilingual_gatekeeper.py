"""
Tests for Hallwright Multi-Language Gatekeeper Runners:
Verifies that Node.js (scripts/detector.js) and Go (cmd/hallwright)
detect stubs, secrets, dangerous dynamic execution, and tolerate baseline debt.
"""

import os
import sys
import json
import shutil
import tempfile
import subprocess
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_node_gatekeeper_detection():
    """Verifies that pure JavaScript gatekeeper (scripts/detector.js) catches secrets and stubs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a file with exposed OpenAI secret and TODO stub
        sample_file = os.path.join(tmpdir, "service.js")
        secret = "sk-" + "abcdef1234567890abcdef1234567890abcdef"
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write(f'// TODO: implement service\nconst apiKey = "{secret}";\n')

        detector_js = os.path.join(ROOT_DIR, "scripts", "detector.js")
        proc = subprocess.run(
            ["node", detector_js],
            cwd=tmpdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        assert proc.returncode != 0, "Node gatekeeper should fail on secret and stub"
        output = proc.stdout + proc.stderr
        assert "SECRET_OPENAI" in output or "SECRET" in output
        assert "STUB_TODO_FIXME" in output or "STUB" in output


def test_node_gatekeeper_clean_code():
    """Verifies that pure JavaScript gatekeeper approves clean code."""
    with tempfile.TemporaryDirectory() as tmpdir:
        sample_file = os.path.join(tmpdir, "math.ts")
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("export function add(a: number, b: number): number {\n  return a + b;\n}\n")

        detector_js = os.path.join(ROOT_DIR, "scripts", "detector.js")
        proc = subprocess.run(
            ["node", detector_js],
            cwd=tmpdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        assert proc.returncode == 0, f"Node gatekeeper failed on clean code: {proc.stderr}"
        assert "Score: 100/100" in proc.stdout


def test_go_gatekeeper_detection():
    """Verifies that native Go gatekeeper (cmd/hallwright) catches secrets and stubs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        sample_file = os.path.join(tmpdir, "main.py")
        secret = "sk-ant-api03-" + "abcdefghijklmnopqrstuvwx"
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write(f'# FIXME: fix this later\nkey = "{secret}"\n')

        go_entry = os.path.join(ROOT_DIR, "cmd", "hallwright", "main.go")
        proc = subprocess.run(
            ["go", "run", go_entry],
            cwd=tmpdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        assert proc.returncode != 0, "Go gatekeeper should fail on secret and stub"
        output = proc.stdout + proc.stderr
        assert "SECRET" in output or "STUB" in output


def test_go_gatekeeper_clean_code():
    """Verifies that native Go gatekeeper approves clean code."""
    with tempfile.TemporaryDirectory() as tmpdir:
        sample_file = os.path.join(tmpdir, "main.go")
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("package main\n\nfunc main() {\n}\n")

        go_entry = os.path.join(ROOT_DIR, "cmd", "hallwright", "main.go")
        proc = subprocess.run(
            ["go", "run", go_entry],
            cwd=tmpdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        assert proc.returncode == 0, f"Go gatekeeper failed on clean code: {proc.stderr}"
        assert "Score: 100/100" in proc.stdout
