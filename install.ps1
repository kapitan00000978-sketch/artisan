# ==============================================================================
# Humanpowers 1-Line PowerShell Bootstrap Installer
# Usage:
#   irm https://raw.githubusercontent.com/kapitan00000978-sketch/humanpowers/main/install.ps1 | iex
# ==============================================================================

$RepoRaw = "https://raw.githubusercontent.com/kapitan00000978-sketch/humanpowers/main"
$TargetDir = Get-Location

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  🛡️  HUMANPOWERS 1-LINE POWERSHELL BOOTSTRAP INSTALLER" -ForegroundColor Cyan
Write-Host "      Empowered by The Council of Masters (Zero Babysitting)" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "[*] Target Directory: $TargetDir" -ForegroundColor Yellow

# Ensure directories
New-Item -ItemType Directory -Force -Path "$TargetDir\.humanpowers" | Out-Null
New-Item -ItemType Directory -Force -Path "$TargetDir\.cursor\rules" | Out-Null
New-Item -ItemType Directory -Force -Path "$TargetDir\.github" | Out-Null

Write-Host "[+] Downloading core Humanpowers protocol..." -ForegroundColor Green
Invoke-RestMethod -Uri "$RepoRaw/AGENTS.md" -OutFile "$TargetDir\AGENTS.md"
Invoke-RestMethod -Uri "$RepoRaw/.humanpowers/memory.json" -OutFile "$TargetDir\.humanpowers\memory.json"
Invoke-RestMethod -Uri "$RepoRaw/.humanpowers/memory.md" -OutFile "$TargetDir\.humanpowers\memory.md"

Write-Host "[+] Installing Cursor AI Rules..." -ForegroundColor Green
Invoke-RestMethod -Uri "$RepoRaw/.cursorrules" -OutFile "$TargetDir\.cursorrules"
Invoke-RestMethod -Uri "$RepoRaw/.cursor/rules/01-craftsman.mdc" -OutFile "$TargetDir\.cursor\rules\01-craftsman.mdc"
Invoke-RestMethod -Uri "$RepoRaw/.cursor/rules/02-architecture-standards.mdc" -OutFile "$TargetDir\.cursor\rules\02-architecture-standards.mdc"
Invoke-RestMethod -Uri "$RepoRaw/.cursor/rules/03-security-directives.mdc" -OutFile "$TargetDir\.cursor\rules\03-security-directives.mdc"
Invoke-RestMethod -Uri "$RepoRaw/.cursor/rules/04-testing-tdd.mdc" -OutFile "$TargetDir\.cursor\rules\04-testing-tdd.mdc"
Invoke-RestMethod -Uri "$RepoRaw/.cursor/rules/05-design-standards.mdc" -OutFile "$TargetDir\.cursor\rules\05-design-standards.mdc"

Write-Host "[+] Installing Claude Code CLI..." -ForegroundColor Green
Invoke-RestMethod -Uri "$RepoRaw/CLAUDE.md" -OutFile "$TargetDir\CLAUDE.md"

Write-Host "[+] Installing GitHub Copilot & Windsurf Directives..." -ForegroundColor Green
Invoke-RestMethod -Uri "$RepoRaw/.github/copilot-instructions.md" -OutFile "$TargetDir\.github\copilot-instructions.md"
Invoke-RestMethod -Uri "$RepoRaw/.windsurfrules" -OutFile "$TargetDir\.windsurfrules"

Write-Host "`n==================================================================" -ForegroundColor Green
Write-Host "  ✅ Humanpowers successfully installed!" -ForegroundColor Green
Write-Host "     The Council of Masters is now permanently active." -ForegroundColor Green
Write-Host "     Prompt babysitting has been permanently eliminated." -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green
