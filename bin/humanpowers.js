#!/usr/bin/env node

/**
 * HUMANPOWERS CLI BOOTSTRAP INSTALLER & COMMAND DISPATCHER
 * Empowered by The Council of Masters — Zero Babysitting
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
                            THE COUNCIL OF MASTERS — COMMAND-DRIVEN
`;

console.log(ASCII_BANNER);

const targetDir = process.cwd();
const args = process.argv.slice(2);
const command = (args[0] || 'help').toLowerCase();

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
  console.log(`     Command-Driven Mode: Fast & clean by default.`);
  console.log(`     Use slash commands in chat (e.g. /audit, /marcus, /security)`);
  console.log(`     to summon the Council of Masters on-demand.`);
  console.log(`==================================================================\n`);
} else if (command === 'audit' || command === 'gate') {
  console.log(`🔍 [CLI AUDIT] Running Humanpowers Pre-Commit Gatekeeper...`);
  const scriptPath = path.join(packageRoot, 'scripts', 'pre-commit-gatekeeper.py');
  if (fs.existsSync(scriptPath)) {
    const res = spawnSync('python', [scriptPath], { stdio: 'inherit' });
    process.exit(res.status || 0);
  } else {
    console.error(`[-] Gatekeeper script not found at ${scriptPath}`);
    process.exit(1);
  }
} else if (command === 'status') {
  console.log(`🛡️ Humanpowers Protocol : ACTIVE (Command-Driven)`);
  console.log(`Council of Masters      : 8 Domain Titans On-Demand`);
  console.log(`Zero Babysitting        : ENFORCED`);
  console.log(`Supported Ecosystems    : 11 Platforms Ready\n`);
} else if (command === 'council' || command === 'commands') {
  console.log(`⚡ HUMANPOWERS CHAT COMMANDS (Use directly in Cursor, Claude, Antigravity, Copilot, Windsurf):`);
  console.log(`--------------------------------------------------------------------------------------`);
  console.log(`  /council       -> Tri-party adversarial deliberation & 100% certified production sign-off`);
  console.log(`  /marcus, /arch -> Senior Architect Marcus Sterling (SOLID, zero tech debt, concurrency)`);
  console.log(`  /audit, /review-> Adversarial Red Team review (bugs, edge cases, regression probing)`);
  console.log(`  /security      -> Gabriel Frost (Zero-trust security audit, secrets, OWASP)`);
  console.log(`  /design        -> Elena Rostova (UI/UX design systems, accessibility, WCAG 2.1 AAA)`);
  console.log(`  /copy          -> Diana Drake (Direct-response conversion copywriting, messaging)`);
  console.log(`  /cfo           -> Victor Montgomery (Unit economics, burn rate, financial runway)`);
  console.log(`  /legal         -> Arthur Pendelton (Commercial contracts, liability containment)`);
  console.log(`  /ml            -> Dr. Evelyn Reed (ML systems, statistical validation, data leakage)`);
  console.log(`  /devops        -> Gareth Drake (Cloud & SRE, Docker, CI/CD, zero-downtime)`);
  console.log(`  /gate          -> Pre-commit quality gatekeeper scan\n`);
} else {
  console.log(`Usage:`);
  console.log(`  npx humanpowers init       # Initialize Humanpowers in current repo`);
  console.log(`  npx humanpowers audit      # Run code quality & security gatekeeper audit`);
  console.log(`  npx humanpowers council    # List Council of Masters and chat slash commands`);
  console.log(`  npx humanpowers status     # Check active protocol state`);
}
