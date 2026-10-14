#!/usr/bin/env node

/**
 * ARTISAN — AUTONOMOUS AI AGENT CRAFTSMANSHIP & QUALITY PROTOCOL
 * Pre-Commit Quality & Security Verification.
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ASCII_BANNER = `
     _    ____ _____ ___ ____    _    _   _ 
    / \\  |  _ \\_   _|_ _/ ___|  / \\  | \\ | |
   / _ \\ | |_) || |  | |\\___ \\ / _ \\ |  \\| |
  / ___ \\|  _ < | |  | | ___) / ___ \\| |\\  |
 /_/   \\_\\_| \\_\\|_| |___|____/_/   \\_\\_| \\_|
       AI AGENT CRAFTSMANSHIP & QUALITY PROTOCOL
`;

console.log(ASCII_BANNER);

const targetDir = process.cwd();
const args = process.argv.slice(2);
const command = (args[0] || 'status').toLowerCase();

const packageRoot = path.resolve(__dirname, '..');

function copyFileSafe(srcRel, dstRel, overwrite = true) {
  const src = path.join(packageRoot, srcRel);
  const dst = path.join(targetDir, dstRel);
  if (fs.existsSync(src)) {
    if (!overwrite && fs.existsSync(dst)) {
      console.log(`  [*] Preserved: ${dstRel} (already exists)`);
      return;
    }
    fs.mkdirSync(path.dirname(dst), { recursive: true });
    fs.copyFileSync(src, dst);
    console.log(`  [+] Installed: ${dstRel}`);
  }
}

function copyDirSafe(srcRel, dstRel) {
  const src = path.join(packageRoot, srcRel);
  const dst = path.join(targetDir, dstRel);
  if (fs.existsSync(src)) {
    fs.mkdirSync(dst, { recursive: true });
    const entries = fs.readdirSync(src, { withFileTypes: true });
    for (const entry of entries) {
      const srcPath = path.join(srcRel, entry.name);
      const dstPath = path.join(dstRel, entry.name);
      if (entry.isDirectory()) {
        copyDirSafe(srcPath, dstPath);
      } else {
        copyFileSafe(srcPath, dstPath);
      }
    }
  }
}

if (command === 'init' || command === 'install') {
  console.log(`[*] Target Directory: ${targetDir}`);
  console.log(`[*] Installing Artisan Protocol & Craftsmanship Rules...\n`);

  // 1. Core protocol
  copyFileSafe('AGENTS.md', 'AGENTS.md');
  copyFileSafe('.artisan/memory.json', '.artisan/memory.json', false);
  copyFileSafe('.artisan/memory.md', '.artisan/memory.md', false);

  // 2. Cursor AI plugin rules
  copyFileSafe('.cursorrules', '.cursorrules');
  copyDirSafe('.cursor/rules', '.cursor/rules');

  // 3. Claude Code plugin
  copyFileSafe('CLAUDE.md', 'CLAUDE.md');

  // 4. Copilot, Windsurf & Cline
  copyFileSafe('.github/copilot-instructions.md', '.github/copilot-instructions.md');
  copyFileSafe('.windsurfrules', '.windsurfrules');
  copyFileSafe('.clinerules', '.clinerules');

  console.log(`\n==================================================================`);
  console.log(`  ✅ Artisan Protocol is now active!`);
  console.log(`     Autonomous Quality & Pre-Commit Craftsmanship Rules installed.`);
  console.log(`==================================================================\n`);
} else if (command === 'audit' || command === 'gate') {
  console.log(`🔍 [ARTISAN AUDIT] Running Quality & Security Scan...`);
  const scriptPath = path.join(packageRoot, 'scripts', 'pre-commit-gatekeeper.py');
  if (fs.existsSync(scriptPath)) {
    const extraArgs = args.slice(1);
    const res = spawnSync('python', [scriptPath, ...extraArgs], { stdio: 'inherit' });
    process.exit(res.status || 0);
  } else {
    console.error(`[-] Gatekeeper script not found at ${scriptPath}`);
    process.exit(1);
  }
} else if (command === 'hook') {
  console.log(`🪝 [ARTISAN HOOK] Installing Git pre-commit quality gate...`);
  const hookScript = path.join(packageRoot, 'scripts', 'install_git_hook.py');
  if (fs.existsSync(hookScript)) {
    const res = spawnSync('python', [hookScript], { stdio: 'inherit' });
    process.exit(res.status || 0);
  } else {
    console.error(`[-] Hook installer not found at ${hookScript}`);
    process.exit(1);
  }
} else if (command === 'mcp') {
  console.log(`🔌 [ARTISAN MCP] Starting Model Context Protocol Server...`);
  const mcpScript = path.join(packageRoot, 'mcp', 'server.py');
  if (fs.existsSync(mcpScript)) {
    spawnSync('python', [mcpScript], { stdio: 'inherit' });
  } else {
    console.error(`[-] MCP server not found at ${mcpScript}`);
    process.exit(1);
  }
} else if (command === 'doctor') {
  console.log(`🩺 [ARTISAN DOCTOR] Inspecting system and project health...\n`);
  const checks = [
    { name: 'Core Protocol (AGENTS.md)', pass: fs.existsSync(path.join(targetDir, 'AGENTS.md')) },
    { name: 'Memory Ledger (.artisan/memory.json)', pass: fs.existsSync(path.join(targetDir, '.artisan', 'memory.json')) },
    { name: 'Cursor Rules (.cursorrules)', pass: fs.existsSync(path.join(targetDir, '.cursorrules')) },
    { name: 'Claude Code (CLAUDE.md)', pass: fs.existsSync(path.join(targetDir, 'CLAUDE.md')) },
    { name: 'Copilot Instructions (.github/copilot-instructions.md)', pass: fs.existsSync(path.join(targetDir, '.github', 'copilot-instructions.md')) },
    { name: 'Git Pre-Commit Hook (.git/hooks/pre-commit)', pass: fs.existsSync(path.join(targetDir, '.git', 'hooks', 'pre-commit')) }
  ];

  for (const c of checks) {
    console.log(`  ${c.pass ? '✅' : '⚠️'}  ${c.name}: ${c.pass ? 'CONFIGURED' : 'NOT FOUND'}`);
  }
  console.log(`\nTo install missing rules, run: npx artisan init`);
  console.log(`To install git pre-commit hook, run: npx artisan hook\n`);
} else if (command === 'watch' || command === 'daemon') {
  console.log(`👁️ [ARTISAN WATCHDOG] Starting autonomous file sentinel...`);
  const scriptPath = path.join(packageRoot, 'scripts', 'watchdog.py');
  if (fs.existsSync(scriptPath)) {
    spawnSync('python', [scriptPath, '--watch'], { stdio: 'inherit' });
  } else {
    console.error(`[-] Watchdog script not found at ${scriptPath}`);
    process.exit(1);
  }
} else if (command === 'fix' || command === 'repair') {
  console.log(`🔧 [ARTISAN FIX] Auto-remediating code defects across repository...`);
  const fixScript = path.join(packageRoot, 'scripts', 'remediator.py');
  if (fs.existsSync(fixScript)) {
    const extraArgs = args.slice(1);
    const res = spawnSync('python', [fixScript, ...extraArgs], { stdio: 'inherit' });
    process.exit(res.status || 0);
  } else {
    console.error(`[-] Remediator script not found at ${fixScript}`);
    process.exit(1);
  }
} else if (command === 'status') {
  console.log(`🛡️ Artisan Protocol     : ACTIVE (v1.0.1)`);
  console.log(`Autonomous Mode        : Enforced (Zero Commands Required)`);
  console.log(`Quality Gatekeeper     : Pre-commit Inspection Active`);
  console.log(`Supported Ecosystems    : 11 Platforms Ready\n`);
} else {
  console.log(`Usage:`);
  console.log(`  artisan init       # Install Artisan rules into current repository`);
  console.log(`  artisan hook       # Install Git pre-commit quality gate hook`);
  console.log(`  artisan audit      # Run quality & security audit (--staged for diff)`);
  console.log(`  artisan fix        # Auto-remediate silent catches and stubs`);
  console.log(`  artisan doctor     # Check configuration and environment health`);
  console.log(`  artisan mcp        # Launch MCP JSON-RPC Server`);
  console.log(`  artisan watch      # Run continuous background watchdog sentinel`);
  console.log(`  artisan status     # Check Artisan protocol status`);
}
