$ErrorActionPreference = 'Stop'

# Resolve paths relative to this script
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $here
$docs = Join-Path $root 'docs'
$staticSrc = Join-Path $root 'static'
$staticDst = Join-Path $docs 'static'

Write-Host "🔍 Running content validation..."
& pwsh -File (Join-Path $here 'validate-content.ps1') -RepoRoot $root
if ($LASTEXITCODE -ne 0) { throw "Content validation failed. Aborting publish." }
Write-Host "✅ Validation passed."

Write-Host "❄️  Freezing site to docs/..."
# Prefer venv python if present
$py = Join-Path $root '.venv\Scripts\python.exe'
if(!(Test-Path $py)) { $py = 'python' }
& $py (Join-Path $root 'freeze.py')

# (Optional) legacy static sync — freezer already includes static; keep as no-op fallback
if (Test-Path $staticSrc) {
  Write-Host "📦 Ensuring static/ mirrored to docs/static/..."
  robocopy $staticSrc $staticDst /MIR | Out-Null
}

# Guarantee minimal 404/index for Pages
$docs404 = Join-Path $docs '404.html'
if (!(Test-Path $docs404)) {
@'
<!doctype html><meta charset="utf-8"><title>404</title>
<h1>Not Found</h1><p>Try the <a href="/">home</a> or <a href="/blog/">blog</a>.</p>
'@ | Set-Content -Encoding UTF8 $docs404
}

$hash = $null
try { $hash = (git -C $root rev-parse --short HEAD) 2>$null } catch {}
if (-not $hash) { $hash = Get-Date -Format 'yyyyMMddHHmmss' }

if (!(Test-Path (Join-Path $root '.git'))) {
  Write-Host "ℹ️  No .git folder found. Skipping commit/push." -ForegroundColor Yellow
  Write-Host "✅ Publish complete (local). Build ID: $hash"
  exit 0
}

Write-Host "📝 Committing and pushing..."
Push-Location $root
try {
  git add .
  & git commit -m "Publish: $hash" 2>&1 | Write-Host
  $branch = (& git rev-parse --abbrev-ref HEAD).Trim()
  if (-not $branch) { $branch = 'main' }
  $hasUpstream = $true
  try { & git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>$null | Out-Null; if ($LASTEXITCODE -ne 0) { $hasUpstream = $false } } catch { $hasUpstream = $false }
  if (-not $hasUpstream) { & git push -u origin $branch 2>&1 | Write-Host } else { & git push 2>&1 | Write-Host }
  if ($LASTEXITCODE -ne 0) { throw "Git push failed." }
  Write-Host "✅ Pushed. Build ID: $hash"
} finally {
  Pop-Location
}
