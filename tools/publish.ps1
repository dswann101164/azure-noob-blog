$ErrorActionPreference = 'Stop'
function Run($c){ Write-Host "• $c"; iex $c }

if (Test-Path ".\.venv\Scripts\Activate.ps1") { . .\.venv\Scripts\Activate.ps1 }
$env:SITE_URL = "https://azure-noob.com"

Run 'git add -A'
if (git status --porcelain) { Run 'git commit -m "Update content/templates/code (pre-freeze)"' }

Write-Host "❄️  Freezing..." -ForegroundColor Cyan
Run 'python freeze.py'

Run 'git add docs'
if (git status --porcelain docs) { 
  Run 'git commit -m "Publish frozen site (search/sitemap/robots/content)"'
} else {
  Run 'git commit --allow-empty -m "Publish (no doc changes)"'
}

Run 'git pull --rebase origin main'
Run 'git push origin main'
Write-Host "✅ Published." -ForegroundColor Green
