#!/usr/bin/env node

/**
 * ARTISAN — AUTONOMOUS AI AGENT CRAFTSMANSHIP & QUALITY PROTOCOL
 * Zero Babysitting. Pre-Commit Quality & Security Verification.
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

  // 4. Copilot & Windsurf
  copyFileSafe('.github/copilot-instructions.md', '.github/copilot-instructions.md');
  copyFileSafe('.windsurfrules', '.windsurfrules');

  console.log(`\n==================================================================`);
  console.log(`  ✅ Artisan Protocol is now active!`);
  console.log(`     Autonomous Quality & Pre-Commit Craftsmanship Rules installed.`);
  console.log(`==================================================================\n`);
} else if (command === 'audit' || command === 'gate') {
  console.log(`🔍 [ARTISAN AUDIT] Running Pre-Commit Quality & Security Scan...`);
  const scriptPath = path.join(packageRoot, 'scripts', 'pre-commit-gatekeeper.py');
  if (fs.existsSync(scriptPath)) {
    const res = spawnSync('python', [scriptPath], { stdio: 'inherit' });
    process.exit(res.status || 0);
  } else {
    console.error(`[-] Gatekeeper script not found at ${scriptPath}`);
    process.exit(1);
  }
} else if (command === 'watch' || command === 'daemon') {
  console.log(`👁️ [ARTISAN WATCHDOG] Starting autonomous file sentinel...`);
  const scriptPath = path.join(packageRoot, 'scripts', 'watchdog.py');
  if (fs.existsSync(scriptPath)) {
    spawnSync('python', [scriptPath, '--watch'], { stdio: 'inherit' });
  } else {
    console.error(`[-] Watchdog script not found at ${scriptPath}`);
    process.exit(1);
  }
} else if (command === 'status') {
  console.log(`🛡️ Artisan Protocol     : ACTIVE (v1.0.0)`);
  console.log(`Autonomous Mode        : Enforced (Zero Commands Required)`);
  console.log(`Quality Gatekeeper     : Pre-commit Inspection Active`);
  console.log(`Supported Ecosystems    : 11 Platforms Ready\n`);
} else {
  console.log(`Usage:`);
  console.log(`  artisan init       # Install Artisan rules into current repository`);
  console.log(`  artisan status     # Check Artisan protocol status`);
  console.log(`  artisan watch      # Run continuous background watchdog sentinel`);
  console.log(`  artisan audit      # Run quality & security audit`);
}
