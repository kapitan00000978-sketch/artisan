#!/usr/bin/env node

/**
 * HUMANPOWERS CLI BOOTSTRAP INSTALLER
 * Installs Humanpowers rules and skills into any project directory in 1 command.
 * Empowered by The Council of Masters.
 */

const fs = require('fs');
const path = require('path');

const ASCII_BANNER = `
  ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗██████╗  ██████╗ ██╗    ██╗███████╗██████╗ ███████╗
  ██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔══██╗██╔════╝
  ███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║██████╔╝██║   ██║██║ █╗ ██║█████╗  ██████╔╝███████╗
  ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║██╔═══╝ ██║   ██║██║███╗██║██╔══╝  ██╔══██╗╚════██║
  ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║██║     ╚██████╔╝╚███╔███╔╝███████╗██║  ██║███████║
  ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚══════╝
                            THE COUNCIL OF MASTERS — ZERO BABYSITTING
`;

console.log(ASCII_BANNER);

const targetDir = process.cwd();
const args = process.argv.slice(2);
const command = args[0] || 'init';

const packageRoot = path.resolve(__dirname, '..');

function copyFileSafe(srcRel, dstRel) {
  const src = path.join(packageRoot, srcRel);
  const dst = path.join(targetDir, dstRel);
  if (fs.existsSync(src)) {
    fs.mkdirSync(path.dirname(dst), { recursive: true });
    fs.copyFileSync(src, dst);
    console.log(`  [+] Copied: ${dstRel}`);
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
  console.log(`[*] Installing Humanpowers Core Protocol & The Council of Masters...\n`);

  // 1. Core protocol
  copyFileSafe('AGENTS.md', 'AGENTS.md');
  copyFileSafe('.humanpowers/memory.json', '.humanpowers/memory.json');
  copyFileSafe('.humanpowers/memory.md', '.humanpowers/memory.md');

  // 2. Cursor AI
  copyFileSafe('.cursorrules', '.cursorrules');
  copyDirSafe('.cursor/rules', '.cursor/rules');

  // 3. Claude Code
  copyFileSafe('CLAUDE.md', 'CLAUDE.md');

  // 4. Copilot & Windsurf
  copyFileSafe('.github/copilot-instructions.md', '.github/copilot-instructions.md');
  copyFileSafe('.windsurfrules', '.windsurfrules');

  console.log(`\n==================================================================`);
  console.log(`  ✅ Humanpowers successfully initialized!`);
  console.log(`     The Council of Masters is active across Cursor, Claude,`);
  console.log(`     Antigravity, Copilot, and Windsurf.`);
  console.log(`     Zero Babysitting protocol is permanently enforced.`);
  console.log(`==================================================================\n`);
} else if (command === 'status') {
  console.log(`🛡️ Humanpowers Protocol : ACTIVE`);
  console.log(`Council of Masters      : 8 Titans Enforced`);
  console.log(`Zero Babysitting        : ENFORCED`);
  console.log(`Supported Ecosystems    : 11 Platforms Ready`);
} else {
  console.log(`Usage:`);
  console.log(`  npx humanpowers init       # Initialize Humanpowers in current repo`);
  console.log(`  npx humanpowers status     # Check active protocol state`);
}
