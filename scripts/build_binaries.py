#!/usr/bin/env python3
"""
Hallwright Go Gatekeeper Multi-Platform Cross-Compiler
Builds standalone, static, zero-dependency binaries for Windows, Linux, and macOS.
"""

import os
import sys
import shutil
import subprocess

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

TARGETS = [
    ("windows", "amd64", "hallwright-windows-amd64.exe"),
    ("windows", "arm64", "hallwright-windows-arm64.exe"),
    ("linux", "amd64", "hallwright-linux-amd64"),
    ("linux", "arm64", "hallwright-linux-arm64"),
    ("darwin", "amd64", "hallwright-darwin-amd64"),
    ("darwin", "arm64", "hallwright-darwin-arm64"),
]

def build_all(root_dir: str = ".") -> int:
    bin_dir = os.path.join(root_dir, "bin")
    os.makedirs(bin_dir, exist_ok=True)

    print("🚀 [HALLWRIGHT GO COMPILER] Cross-compiling standalone gatekeepers...")

    # Check go command
    go_cmd = shutil.which("go")
    if not go_cmd:
        print("[-] Error: 'go' toolchain is not found in PATH.", file=sys.stderr)
        return 1

    success_count = 0
    for goos, goarch, output_name in TARGETS:
        output_path = os.path.join(bin_dir, output_name)
        env = os.environ.copy()
        env["GOOS"] = goos
        env["GOARCH"] = goarch
        env["CGO_ENABLED"] = "0"

        cmd = [
            go_cmd,
            "build",
            "-trimpath",
            "-ldflags=-s -w",
            "-o",
            output_path,
            "./cmd/hallwright"
        ]

        try:
            res = subprocess.run(cmd, cwd=root_dir, env=env, capture_output=True, text=True)
            if res.returncode == 0 and os.path.exists(output_path):
                size_mb = os.path.getsize(output_path) / (1024 * 1024)
                print(f"  [+] Built: {output_name} ({goos}/{goarch}) -> {size_mb:.2f} MB")
                success_count += 1
            else:
                print(f"  [-] Failed: {output_name} ({goos}/{goarch}): {res.stderr.strip()}", file=sys.stderr)
        except Exception as e:
            print(f"  [-] Exception building {output_name}: {e}", file=sys.stderr)

    # Also vendor/link local host binary for git hook installer
    host_exe = os.path.join(bin_dir, "hallwright.exe" if sys.platform == "win32" else "hallwright")
    host_target = "hallwright-windows-amd64.exe" if sys.platform == "win32" else "hallwright-linux-amd64"
    built_host = os.path.join(bin_dir, host_target)
    if os.path.exists(built_host):
        shutil.copy2(built_host, host_exe)
        print(f"  [*] Host binary synced to: {os.path.basename(host_exe)}")

    print(f"\n✅ Completed: {success_count}/{len(TARGETS)} multi-platform binaries generated in ./bin/\n")
    return 0 if success_count == len(TARGETS) else 1


if __name__ == "__main__":
    sys.exit(build_all())
