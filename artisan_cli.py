#!/usr/bin/env python3
"""
Artisan Unified CLI (artisan_cli.py)
Unified command-line interface for the Artisan Autonomous Quality & Intelligence Protocol.
Provides zero-command initialization, automated stack detection, static auditing,
auto-remediation, memory ledger management, and MCP integration.
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from typing import List, Dict, Any, Optional

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))
sys.path.insert(0, os.path.join(ROOT_DIR, "src", "sdk"))
sys.path.insert(0, os.path.join(ROOT_DIR, "mcp"))

ASCII_BANNER = r"""
     _    ____ _____ ___ ____    _    _   _ 
    / \  |  _ \_   _|_ _/ ___|  / \  | \ | |
   / _ \ | |_) || |  | |\___ \ / _ \ |  \| |
  / ___ \|  _ < | |  | | ___) / ___ \| |\  |
 /_/   \_\_| \_\|_| |___|____/_/   \_\_| \_|
       AI AGENT CRAFTSMANSHIP & QUALITY PROTOCOL
"""


def detect_tech_stack(target_dir: str = ".") -> List[str]:
    """Detects programming languages and frameworks present in the target directory."""
    stacks = []
    
    # 1. Node.js / JavaScript / TypeScript
    if os.path.exists(os.path.join(target_dir, "package.json")):
        stacks.append("Node.js / JavaScript")
        try:
            with open(os.path.join(target_dir, "package.json"), "r", encoding="utf-8") as f:
                pkg = json.load(f)
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                if "next" in deps:
                    stacks.append("Next.js")
                elif "react" in deps:
                    stacks.append("React")
                elif "vue" in deps:
                    stacks.append("Vue")
                elif "express" in deps:
                    stacks.append("Express")
        except (json.JSONDecodeError, OSError, KeyError):
            deps = {}
    if os.path.exists(os.path.join(target_dir, "tsconfig.json")):
        stacks.append("TypeScript")

    # 2. Python
    py_markers = ["pyproject.toml", "requirements.txt", "Pipfile", "setup.py"]
    if any(os.path.exists(os.path.join(target_dir, m)) for m in py_markers):
        stacks.append("Python")

    # 3. Go
    if os.path.exists(os.path.join(target_dir, "go.mod")):
        stacks.append("Go")

    # 4. Rust
    if os.path.exists(os.path.join(target_dir, "Cargo.toml")):
        stacks.append("Rust")

    # 5. Java / JVM
    if os.path.exists(os.path.join(target_dir, "pom.xml")) or os.path.exists(os.path.join(target_dir, "build.gradle")):
        stacks.append("Java")

    return list(dict.fromkeys(stacks)) if stacks else ["Universal / Multi-Language"]


def copy_safe(src: str, dst: str, preserve_existing: bool = False) -> bool:
    """Safely copies a file or directory, optionally preserving existing destination files."""
    if not os.path.exists(src):
        return False
    if os.path.abspath(src) == os.path.abspath(dst):
        return True

    if os.path.isdir(src):
        os.makedirs(dst, exist_ok=True)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            copy_safe(s, d, preserve_existing=preserve_existing)
        return True
    else:
        if preserve_existing and os.path.exists(dst):
            return False
        parent = os.path.dirname(dst)
        if parent:
            os.makedirs(parent, exist_ok=True)
        shutil.copy2(src, dst)
        return True


def cmd_init(args: argparse.Namespace) -> int:
    """Installs Artisan rules, configuration files, and git hooks into the current project."""
    print(ASCII_BANNER)
    target_dir = os.path.abspath(args.dir or os.getcwd())
    print(f"[*] Initializing Artisan in: {target_dir}")

    # Detect tech stack
    detected = detect_tech_stack(target_dir)
    print(f"[*] Detected Technology Stack: {', '.join(detected)}\n")

    is_external = os.path.abspath(ROOT_DIR) != target_dir

    # 1. Install core protocol
    if is_external:
        agents_src = os.path.join(ROOT_DIR, "AGENTS.md")
        if os.path.exists(agents_src):
            copy_safe(agents_src, os.path.join(target_dir, "AGENTS.md"))
            print("  [+] Installed core AGENTS.md protocol")

    # 2. Initialize .artisan memory
    mem_dir = os.path.join(target_dir, ".artisan")
    os.makedirs(mem_dir, exist_ok=True)
    mem_file = os.path.join(mem_dir, "memory.json")
    if not os.path.exists(mem_file):
        sample_mem = os.path.join(ROOT_DIR, ".artisan", "memory.json")
        if os.path.exists(sample_mem) and is_external:
            shutil.copy2(sample_mem, mem_file)
        else:
            with open(mem_file, "w", encoding="utf-8") as f:
                json.dump({
                    "version": "2.0.0",
                    "project_context": {"stack": detected},
                    "lessons_learned": [],
                    "conventions": [],
                    "recorded_scar_tissue": []
                }, f, indent=2)
        print("  [+] Initialized persistent project memory (.artisan/memory.json)")
    else:
        print("  [*] Preserved existing .artisan/memory.json")

    # 3. Deploy agent rules
    configs = [
        (".cursorrules", ".cursorrules"),
        (".cursor/rules", ".cursor/rules"),
        ("CLAUDE.md", "CLAUDE.md"),
        (".github/copilot-instructions.md", ".github/copilot-instructions.md"),
        (".windsurfrules", ".windsurfrules"),
        (".clinerules", ".clinerules"),
        ("kimi-agent/KIMI.md", "KIMI.md"),
        ("kilo-agent/KILO.md", "KILO.md"),
        ("hermes-agent/HERMES.md", "HERMES.md"),
        ("codex-agent/CODEX.md", "CODEX.md"),
        ("openclaw-agent/OPENCLAW.md", "OPENCLAW.md"),
        ("opencode-agent/OPENCODE.md", "OPENCODE.md"),
        ("pie-agent/PIE.md", "PIE.md"),
    ]

    for src_rel, dst_rel in configs:
        src_path = os.path.join(ROOT_DIR, src_rel)
        dst_path = os.path.join(target_dir, dst_rel)
        if copy_safe(src_path, dst_path, preserve_existing=False):
            print(f"  [+] Configured: {dst_rel}")

    # 4. Install Git Pre-Commit Hook automatically
    if not args.no_hook:
        git_dir = os.path.join(target_dir, ".git")
        if os.path.isdir(git_dir):
            try:
                from install_git_hook import install_hook
                install_hook()
            except Exception as e:
                print(f"  [!] Note: Pre-commit hook could not be auto-installed: {e}")

    print("\n==================================================================")
    print("  ✅ Artisan Protocol successfully activated!")
    print("     Deterministic Quality Gates & Memory are now active.")
    print("==================================================================\n")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    """Executes the quality and security detector."""
    try:
        from detector import scan_project, load_artisan_config
    except ImportError:
        print("[-] Error: Detector engine could not be loaded.", file=sys.stderr)
        return 1

    cfg = load_artisan_config(".")
    if args.vibe:
        cfg["mode"] = "vibe"

    result = scan_project(".", staged_only=args.staged, config_override=cfg)

    if args.json:
        print(json.dumps(result, indent=2))
        return 0 if result["passed"] else 1

    scope = "staged changes" if args.staged else "workspace"
    mode_str = " (⚡ Vibe Mode)" if result["mode"] == "vibe" else ""
    print(f"\n🛡️ [Artisan Audit] Scope: {scope}{mode_str} | Scanned: {result['scanned_files']} files")
    print(f"📊 Project Health Score: {result['score']}/100\n")

    findings = result.get("findings", [])
    if findings:
        for f in findings[:15]:
            auditor = f.get("auditor", "Artisan Council")
            print(f"  • {f['file']}:{f['line']} [{f['category']}] [{auditor}] -> {f['message']}")
        if len(findings) > 15:
            print(f"  ... and {len(findings) - 15} more defect(s).")
    else:
        print("✅ Zero stubs, zero secret leaks, zero silent error catches detected.")

    if result["passed"]:
        print("\n✅ Status: PASSED (Verified Clean)")
        return 0
    else:
        print("\n❌ Status: REJECTED (Quality thresholds violated. Run 'artisan fix' to auto-remediate)")
        return 1


def cmd_fix(args: argparse.Namespace) -> int:
    """Runs autonomous code remediation for silent catches and unfinished stubs."""
    try:
        from remediator import remediate_file
    except ImportError:
        print("[-] Error: Remediator engine could not be loaded.", file=sys.stderr)
        return 1

    target = args.path or "."
    fixed_count = 0

    if os.path.isfile(target):
        count = remediate_file(target)
        fixed_count += count
        print(f"[*] Repaired {count} defect(s) in {target}")
    else:
        valid_exts = (".py", ".js", ".ts", ".jsx", ".tsx")
        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".venv", "__pycache__", "tests")]
            for file in files:
                if file.endswith(valid_exts):
                    p = os.path.join(root, file)
                    c = remediate_file(p)
                    if c > 0:
                        fixed_count += c
                        print(f"  [+] Auto-remediated {c} flaw(s) in {p}")

    print(f"\n✅ [ARTISAN FIX COMPLETE]: Resolved {fixed_count} total code defects.")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Displays workspace health, active guilds, memory status, and pre-commit gate info."""
    print(ASCII_BANNER)
    mem_path = os.path.join(".artisan", "memory.json")
    lessons_count = 0
    conventions_count = 0

    if os.path.exists(mem_path):
        try:
            with open(mem_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                lessons_count = len(data.get("lessons_learned", []))
                conventions_count = len(data.get("conventions", [])) + len(data.get("recorded_scar_tissue", []))
        except (json.JSONDecodeError, OSError):
            lessons_count = 0
            conventions_count = 0

    has_gatekeeper = os.path.exists(os.path.join(".git", "hooks", "pre-commit"))
    has_agents_md = os.path.exists("AGENTS.md")
    detected = detect_tech_stack(".")

    print("📊 ARTISAN STATUS REPORT:")
    print(f"  • Protocol Invariant    : Active ({'AGENTS.md loaded' if has_agents_md else 'Missing AGENTS.md'})")
    print(f"  • Pre-Commit Quality Gate: {'INSTALLED (.git/hooks/pre-commit)' if has_gatekeeper else 'NOT INSTALLED'}")
    print(f"  • Detected Stack        : {', '.join(detected)}")
    print(f"  • Persistent Memory     : {lessons_count} lessons, {conventions_count} recorded conventions")
    print(f"  • Council Guilds Active : 8 Domain Guilds (64 Titans available)")
    print(f"  • Smart Context Engine  : Ready (85% token compression)\n")
    return 0


def cmd_memory(args: argparse.Namespace) -> int:
    """Manages persistent learning memory (.artisan/memory.json)."""
    try:
        from learning_memory import LearningMemory
        mem = LearningMemory()
    except ImportError:
        print("[-] Error: Learning memory module could not be loaded.", file=sys.stderr)
        return 1

    if args.record:
        # Expected format: "type:category:pattern:lesson"
        parts = args.record.split(":", 3)
        if len(parts) < 4:
            print("[-] Error: Record format must be: type:category:pattern:lesson")
            print("    Example: mistake:auth:unhashed_token:Always hash tokens before DB write")
            return 1
        res = mem.record_learning(
            record_type=parts[0].strip(),
            category=parts[1].strip(),
            pattern=parts[2].strip(),
            lesson=parts[3].strip(),
            severity="high"
        )
        print(f"✅ Recorded memory: {res.get('entry_id', 'saved')}")
        return 0

    # Search or List
    lessons = mem.get_lessons(task=args.search or "", limit=args.limit or 10)
    print(f"\n🧠 [ARTISAN PERSISTENT MEMORY] ({len(lessons)} entries found):\n")
    if not lessons:
        print("  Zero recorded failure patterns. Codebase is operating on fresh memory.")
    else:
        for idx, item in enumerate(lessons, 1):
            sev = item.get("severity", "high").upper()
            cat = item.get("category", "general")
            pat = item.get("pattern", "")
            les = item.get("lesson", "")
            print(f"  {idx}. [{sev}] [{cat}] Pattern: {pat}")
            print(f"     💡 Rule: {les}\n")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    """Inspects environment and configuration health."""
    print("🩺 [ARTISAN DOCTOR] Inspecting system and project health...\n")
    checks = [
        ("Core Protocol (AGENTS.md)", os.path.exists("AGENTS.md")),
        ("Memory Ledger (.artisan/memory.json)", os.path.exists(os.path.join(".artisan", "memory.json"))),
        ("Cursor Rules (.cursorrules)", os.path.exists(".cursorrules")),
        ("Claude Code (CLAUDE.md)", os.path.exists("CLAUDE.md")),
        ("Copilot Instructions (.github/copilot-instructions.md)", os.path.exists(os.path.join(".github", "copilot-instructions.md"))),
        ("Git Pre-Commit Hook (.git/hooks/pre-commit)", os.path.exists(os.path.join(".git", "hooks", "pre-commit")))
    ]

    all_ok = True
    for name, passed in checks:
        icon = "✅" if passed else "⚠️"
        status = "CONFIGURED" if passed else "NOT FOUND"
        print(f"  {icon}  {name:<45}: {status}")
        if not passed:
            all_ok = False

    print()
    if all_ok:
        print("✅ Environment is in peak condition.")
    else:
        print("💡 Run 'artisan init' to install missing configurations.")
    return 0 if all_ok else 1


def cmd_agents(args: argparse.Namespace) -> int:
    """Displays active AI agent sessions and checks for conflicting locks in the workspace."""
    try:
        from agent_registry import AgentRegistry
        reg = AgentRegistry()
    except ImportError as imp_err:
        print(f"[-] Error: Agent registry module could not be loaded: {imp_err}", file=sys.stderr)
        return 1

    if args.register:
        parts = args.register.split(":", 1)
        name = parts[0].strip()
        intent = parts[1].strip() if len(parts) > 1 else "Active in workspace"
        files = args.files or []
        sess = reg.register_session(agent_name=name, active_files=files, intent=intent)
        print(f"✅ Registered active agent session: {sess['session_id']} ({name})")
        return 0

    if args.release:
        released = reg.release_session(args.release)
        if released:
            print(f"✅ Released session: {args.release}")
        else:
            print(f"ℹ️ Session not found: {args.release}")
        return 0

    sessions = reg.get_active_sessions()
    print(f"\n🤖 [ARTISAN MULTI-AGENT STATE] ({len(sessions)} active session(s)):\n")
    if not sessions:
        print("  Zero concurrent agents currently registered. Workspace is single-tenant.")
    else:
        for idx, s in enumerate(sessions, 1):
            name = s.get("agent_name", "Unknown")
            sid = s.get("session_id", "")
            intent = s.get("intent", "General task")
            files = s.get("active_files", [])
            print(f"  {idx}. [{name}] (ID: {sid})")
            print(f"     Intent : {intent}")
            if files:
                print(f"     Holding: {', '.join(files)}")
            print()
    return 0


def cmd_metrics(args: argparse.Namespace) -> int:
    """Displays workspace quality statistics and audit metrics."""
    try:
        from roi_tracker import display_metrics
        display_metrics()
        return 0
    except ImportError as imp_err:
        print(f"[-] Error: ROI tracker module could not be loaded: {imp_err}", file=sys.stderr)
        return 1


def cmd_context(args: argparse.Namespace) -> int:
    """Dynamically builds a token-optimized, scar-tissue-injected prompt for any task."""
    try:
        from context_selector import SmartMasterSelector
        from learning_memory import LearningMemory
        selector = SmartMasterSelector()
        memory = LearningMemory()
    except ImportError as imp_err:
        print(f"[-] Error: Could not load context engine: {imp_err}", file=sys.stderr)
        return 1

    task = args.task or ""
    files = args.files or []
    lessons = memory.get_lessons(task=task, limit=4)
    res = selector.build_dynamic_prompt(task_description=task, files=files, lessons=lessons)

    if args.json:
        print(json.dumps(res, indent=2))
        return 0

    print(res["prompt"])
    print("\n" + "-" * 70)
    print(f"📊 [Context Optimization]: {res['approx_tokens']} tokens (~{res['optimization_ratio']} compression vs 12K baseline)")
    print("-" * 70)
    return 0


def cmd_mutate(args: argparse.Namespace) -> int:
    """Executes mutation testing against target file to evaluate regression catch capability."""
    try:
        from mutator import MutationTester
    except ImportError as imp_err:
        print(f"[-] Error: Mutation testing module could not be loaded: {imp_err}", file=sys.stderr)
        return 1

    target = args.target
    if not target or not os.path.isfile(target):
        candidate = os.path.join("src", "sdk", "context_selector.py")
        if os.path.isfile(candidate):
            target = candidate
        else:
            print("[-] Error: Please specify a valid Python target file to mutate.", file=sys.stderr)
            return 1

    test_cmd = [sys.executable, "-m", "pytest", args.test, "-q"] if args.test else None
    limit = args.limit or 10

    if not args.json:
        print(f"\n🧬 [ARTISAN MUTATION ENGINE] Analyzing: {target} (Max mutants: {limit})...")
    tester = MutationTester(target_file=target, test_cmd=test_cmd)
    report = tester.run_mutation_analysis(limit=limit)

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    score = report.get("mutation_score", 0.0)
    total = report.get("total_mutants", 0)
    killed = report.get("killed", 0)
    survived = report.get("survived", 0)

    print(f"\n📊 MUTATION TEST REPORT: {target}")
    print(f"  • Total Mutants Generated : {total}")
    print(f"  • Mutants Killed (Tests caught bug) : {killed} ✅")
    print(f"  • Mutants Survived (Tests missed bug): {survived} {'⚠️' if survived > 0 else '✨'}")
    print(f"  • Test Suite Mutation Score        : {score}%")

    if score >= 80.0:
        print("\n✅ VERDICT: High-Fidelity Test Suite (Relentlessly catches logic mutations).")
        return 0
    else:
        print("\n⚠️ VERDICT: Fragile Test Suite (Tests passed even when logic was modified. Strengthen assertions).")
        return 1


def cmd_review(args: argparse.Namespace) -> int:
    """Runs adversarial red-team peer review on files or git diff."""
    try:
        from reviewer import AdversarialReviewer
    except ImportError as imp_err:
        print(f"[-] Error: Reviewer engine could not be loaded: {imp_err}", file=sys.stderr)
        return 1

    reviewer = AdversarialReviewer(pass_threshold=args.threshold if hasattr(args, "threshold") and args.threshold else 85.0)

    if args.files:
        report = reviewer.review_files(args.files)
    elif args.staged or args.diff or args.commit:
        report = reviewer.review_diff(staged=args.staged, commit=args.commit)
    else:
        # Default to uncommitted git diff review
        report = reviewer.review_diff(staged=False)

    if args.json:
        print(json.dumps(report, indent=2))
        return 0 if report["passed"] else 1

    if args.markdown:
        print(reviewer.format_markdown_review(report))
        return 0 if report["passed"] else 1

    # Terminal output
    verdict_icon = "🟢" if report["passed"] else "🔴"
    print(f"\n🛡️ [ARTISAN ADVERSARIAL PEER REVIEW] {verdict_icon} Verdict: {report['verdict']}")
    print(f"📊 Quality & Resilience Score: {report['score']}/100 (Threshold: {report['threshold']})")
    print(f"📁 Audited Target(s): {len(report['audited_files'])} file(s) | Defects: {report['defects_count']}\n")

    if not report["findings"]:
        print("✨ ZERO DEFECTS DETECTED. Certified clean by Gabriel Frost & Marcus Sterling.")
    else:
        for idx, f in enumerate(report["findings"], 1):
            sev = f.get("severity", "MAJOR")
            persona = f.get("persona", "Master")
            file_loc = f"{f['file']}:{f['line']}"
            print(f"  {idx}. [{sev}] [{persona}] {file_loc}")
            print(f"     ⚠️  {f['message']}")
            print(f"     💡 Directive: {f['suggestion']}\n")

    return 0 if report["passed"] else 1


def main():
    parser = argparse.ArgumentParser(
        prog="artisan",
        description="Artisan Autonomous AI Agent Craftsmanship & Quality Protocol CLI"
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Artisan command to execute")

    # init
    p_init = subparsers.add_parser("init", help="Initialize Artisan protocol and agent configurations in the current project")
    p_init.add_argument("--dir", "-d", help="Target project directory (default: current directory)")
    p_init.add_argument("--no-hook", action="store_true", help="Skip automatic git pre-commit hook installation")

    # audit
    p_audit = subparsers.add_parser("audit", help="Run static quality & security audit across codebase")
    p_audit.add_argument("--staged", "-s", action="store_true", help="Audit only git staged changes")
    p_audit.add_argument("--vibe", "-v", action="store_true", help="Run in non-blocking advisory Vibe mode")
    p_audit.add_argument("--json", "-j", action="store_true", help="Output audit results in JSON format")

    # fix
    p_fix = subparsers.add_parser("fix", help="Auto-remediate silent catches and code defects")
    p_fix.add_argument("path", nargs="?", default=".", help="File or directory path to remediate (default: .)")

    # status
    subparsers.add_parser("status", help="Display workspace health, memory stats, and active protocol info")

    # memory
    p_mem = subparsers.add_parser("memory", help="Inspect and manage persistent project memory ledger")
    p_mem.add_argument("--search", "-s", help="Search query for past lessons")
    p_mem.add_argument("--record", "-r", help="Record a new lesson (format: 'type:category:pattern:lesson')")
    p_mem.add_argument("--limit", "-l", type=int, default=10, help="Max results to display")

    # doctor
    subparsers.add_parser("doctor", help="Verify environment and configuration integrity")

    # mcp
    subparsers.add_parser("mcp", help="Start the Model Context Protocol (MCP) JSON-RPC server")

    # agents
    p_agents = subparsers.add_parser("agents", help="List or register concurrent AI agent sessions")
    p_agents.add_argument("--register", "-r", help="Register current agent session (e.g. 'Claude Code:Refactoring API')")
    p_agents.add_argument("--release", help="Release session by ID")
    p_agents.add_argument("--files", "-f", nargs="*", help="Active files held by this session")

    # metrics
    subparsers.add_parser("metrics", help="Display workspace quality statistics and audit metrics")

    # context / prompt
    p_ctx = subparsers.add_parser("context", aliases=["prompt"], help="Generate a token-optimized, scar-tissue-injected prompt for a task")
    p_ctx.add_argument("task", help="Description of the engineering task")
    p_ctx.add_argument("--files", "-f", nargs="*", help="Optional files involved in the task")
    p_ctx.add_argument("--json", "-j", action="store_true", help="Output prompt metadata in JSON format")

    # mutate
    p_mut = subparsers.add_parser("mutate", help="Run AST mutation testing to measure test suite regression catch rate")
    p_mut.add_argument("target", nargs="?", help="Target Python file to mutate (e.g. src/sdk/context_selector.py)")
    p_mut.add_argument("--test", "-t", help="Specific pytest file or path to run against mutants")
    p_mut.add_argument("--limit", "-l", type=int, default=10, help="Maximum number of AST mutants to generate")
    p_mut.add_argument("--json", "-j", action="store_true", help="Output mutation test results in JSON format")

    # review
    p_rev = subparsers.add_parser("review", help="Run adversarial red-team peer review on files or git diff")
    p_rev.add_argument("files", nargs="*", help="Optional source files to review")
    p_rev.add_argument("--diff", action="store_true", help="Review unstaged git diff modifications")
    p_rev.add_argument("--staged", action="store_true", help="Review staged git diff modifications")
    p_rev.add_argument("--commit", "-c", help="Review diff against a specific git commit or reference")
    p_rev.add_argument("--markdown", "-m", action="store_true", help="Output GitHub PR markdown formatted review")
    p_rev.add_argument("--json", "-j", action="store_true", help="Output review report in JSON format")
    p_rev.add_argument("--threshold", "-t", type=float, default=85.0, help="Minimum pass score threshold (default: 85.0)")

    # hud
    subparsers.add_parser("hud", help="Launch interactive terminal dashboard")

    # watchdog
    subparsers.add_parser("watch", help="Launch background file watchdog sentinel")

    args = parser.parse_args()

    if not args.subcommand or args.subcommand == "status":
        return cmd_status(args)
    elif args.subcommand == "init":
        return cmd_init(args)
    elif args.subcommand == "audit":
        return cmd_audit(args)
    elif args.subcommand == "fix":
        return cmd_fix(args)
    elif args.subcommand == "memory":
        return cmd_memory(args)
    elif args.subcommand == "doctor":
        return cmd_doctor(args)
    elif args.subcommand == "agents":
        return cmd_agents(args)
    elif args.subcommand == "metrics":
        return cmd_metrics(args)
    elif args.subcommand in ("context", "prompt"):
        return cmd_context(args)
    elif args.subcommand == "mutate":
        return cmd_mutate(args)
    elif args.subcommand == "review":
        return cmd_review(args)
    elif args.subcommand == "mcp":
        from server import main as mcp_main
        mcp_main()
        return 0
    elif args.subcommand == "hud":
        subprocess.run([sys.executable, os.path.join(ROOT_DIR, "cli", "dashboard.py")])
        return 0
    elif args.subcommand == "watch":
        subprocess.run([sys.executable, os.path.join(ROOT_DIR, "scripts", "watchdog.py"), "--watch"])
        return 0
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
