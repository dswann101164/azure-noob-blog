# tools\publish-post.ps1
# Freeze site to docs/ and push to GitHub Pages (current branch).
# Safe on Windows + PowerShell (location-aware, UTF-8, tolerant of native stderr).

$PSNativeCommandUseErrorActionPreference = $false
$ErrorActionPreference = 'Continue'

function Run($c) { Write-Host "• $c" -ForegroundColor DarkGray; iex $c }

# --- Resolve paths and cd to project root ---
$ScriptDir   = $PSScriptRoot
$ProjectRoot = (Resolve-Path "$ScriptDir\..").Path
Set-Location $ProjectRoot

# --- Activate venv if present ---
$VenvActivate = Join-Path $ProjectRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $VenvActivate) { . $VenvActivate }

# --- Environment for build ---
$env:SITE_URL = "https://azure-noob.com"
$env:PYTHONUNBUFFERED = "1"
$env:PYTHONIOENCODING = "utf-8"

# --- Git sanity check ---
Run 'git rev-parse --is-inside-work-tree > $null'
$branch = (git rev-parse --abbrev-ref HEAD).Trim()
if (-not $branch) { $branch = "main" }
Write-Host "Publishing on branch: $branch" -ForegroundColor Cyan

# --- Commit any source changes (pre-freeze) ---
Run 'git add -A'
if (git status --porcelain) {
  Run 'git commit -m "Update content/templates/code (pre-freeze)"'
} else {
  Write-Host "ℹ No source changes to commit." -ForegroundColor Yellow
}

# --- Freeze the site (build docs/) ---
Write-Host "❄ Freezing site to docs/…" -ForegroundColor Cyan
try {
  Run 'python freeze.py'
} catch {
  Write-Host "💥 Freeze failed. See error above." -ForegroundColor Red
  exit 1
}

# --- Stage and commit docs/ (or force a no-op publish commit) ---
Run 'git add docs'
if (git status --porcelain docs) {
  Run 'git commit -m "Publish frozen site (search/sitemap/robots/content)"'
} else {
  Write-Host "ℹ No docs changes detected; creating empty publish commit." -ForegroundColor Yellow
  Run 'git commit --allow-empty -m "Publish (no doc changes)"'
}

# --- Rebase & push ---
Run "git pull --rebase origin $branch"
Run "git push origin $branch"

Write-Host "✅ Published." -ForegroundColor Green
