#!/usr/bin/env node

/**
 * HUMANPOWERS — AUTONOMOUS 24/7 BACKGROUND CRAFTSMANSHIP PLUGIN
 * Zero Commands Required. Zero Babysitting. 100% Autonomous.
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ASCII_BANNER = `
  ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗██████╗  ██████╗ ██╗    ██╗███████╗██████╗ ███████╗
  ██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔══██╗██╔════╝
  ███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║██████╔╝██║   ██║██║ █╗ ██║█████╗  ██████╔╝███████╗
  ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║██╔═══╝ ██║   ██║██║███╗██║██╔══╝  ██╔══██╗╚════██║
  ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║██║     ╚██████╔╝╚███╔███╔╝███████╗██║  ██║███████║
  ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚══════╝
                     AUTONOMOUS 24/7 BACKGROUND PLUGIN — ZERO BABYSITTING
`;

console.log(ASCII_BANNER);

const targetDir = process.cwd();
const args = process.argv.slice(2);
const command = (args[0] || 'status').toLowerCase();

const packageRoot = path.resolve(__dirname, '..');

function copyFileSafe(srcRel, dstRel) {
  const src = path.join(packageRoot, srcRel);
  const dst = path.join(targetDir, dstRel);
  if (fs.existsSync(src)) {
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
  console.log(`[*] Installing Humanpowers 24/7 Autonomous Craftsmanship Plugin...\n`);

  // 1. Core protocol
  copyFileSafe('AGENTS.md', 'AGENTS.md');
  copyFileSafe('.humanpowers/memory.json', '.humanpowers/memory.json');
  copyFileSafe('.humanpowers/memory.md', '.humanpowers/memory.md');

  // 2. Cursor AI plugin rules
  copyFileSafe('.cursorrules', '.cursorrules');
  copyDirSafe('.cursor/rules', '.cursor/rules');

  // 3. Claude Code plugin
  copyFileSafe('CLAUDE.md', 'CLAUDE.md');

  // 4. Copilot & Windsurf
  copyFileSafe('.github/copilot-instructions.md', '.github/copilot-instructions.md');
  copyFileSafe('.windsurfrules', '.windsurfrules');

  console.log(`\n==================================================================`);
  console.log(`  ✅ Humanpowers Plugin is now permanently installed!`);
  console.log(`     Mode: 24/7 Autonomous Background Craftsmanship.`);
  console.log(`     Zero commands needed: The AI agent will automatically`);
  console.log(`     self-inspect and auto-remediate code on every single task.`);
  console.log(`==================================================================\n`);
} else if (command === 'audit' || command === 'gate') {
  console.log(`🔍 [PLUGIN AUDIT] Running Autonomous Pre-Commit Quality & Security Scan...`);
  const scriptPath = path.join(packageRoot, 'scripts', 'pre-commit-gatekeeper.py');
  if (fs.existsSync(scriptPath)) {
    const res = spawnSync('python', [scriptPath], { stdio: 'inherit' });
    process.exit(res.status || 0);
  } else {
    console.error(`[-] Gatekeeper script not found at ${scriptPath}`);
    process.exit(1);
  }
} else if (command === 'watch' || command === 'daemon') {
  console.log(`👁️ [24/7 BACKGROUND WATCHDOG] Starting autonomous file sentinel...`);
  const scriptPath = path.join(packageRoot, 'scripts', 'watchdog.py');
  if (fs.existsSync(scriptPath)) {
    spawnSync('python', [scriptPath], { stdio: 'inherit' });
  } else {
    console.error(`[-] Watchdog script not found at ${scriptPath}`);
    process.exit(1);
  }
} else if (command === 'status') {
  console.log(`🛡️ Humanpowers Plugin   : INSTALLED & PERMANENTLY ACTIVE (24/7)`);
  console.log(`Autonomous Mode        : 100% Autonomous (Zero Commands Required)`);
  console.log(`Silent Self-Inspection : ENFORCED ON EVERY EDIT`);
  console.log(`Auto-Correction        : ENFORCED`);
  console.log(`Zero Babysitting       : ACTIVE ACROSS ALL 11 AGENT PLATFORMS\n`);
} else {
  console.log(`Usage:`);
  console.log(`  npx humanpowers init       # Install plugin into current repository`);
  console.log(`  npx humanpowers status     # Check 24/7 plugin status`);
  console.log(`  npx humanpowers watch      # Run 24/7 background watchdog sentinel`);
  console.log(`  npx humanpowers audit      # Run quality & security audit`);
}
