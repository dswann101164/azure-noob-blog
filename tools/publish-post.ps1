# publish-post.ps1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# PS7+: ensure native tool stderr doesn't terminate the script
if ($PSVersionTable.PSVersion.Major -ge 7) {
  $global:PSNativeCommandUseErrorActionPreference = $false
}

# Resolve paths relative to this script
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $here
$docs = Join-Path $root 'docs'
$staticSrc = Join-Path $root 'static'
$staticDst = Join-Path $docs 'static'
$freezePy = Join-Path $root 'freeze.py'

Write-Host "🔍 Running content validation..."
& pwsh -File (Join-Path $here 'validate-content.ps1') -RepoRoot $root
if ($LASTEXITCODE -ne 0) { throw "Content validation failed. Aborting publish." }
Write-Host "✅ Validation passed."

Write-Host "❄️  Freezing site to docs/..."
# Prefer venv python if present
$py = Join-Path $root '.venv\Scripts\python.exe'
if (!(Test-Path $py)) { $py = 'python' }

# Run freeze.py (prints traceback itself if it fails)
if (!(Test-Path $freezePy)) { throw "freeze.py not found at $freezePy" }
& $py $freezePy

# Belt & suspenders: mirror static → docs/static
if (Test-Path $staticSrc) {
  Write-Host "📦 Ensuring static/ mirrored to docs/static/..."
  robocopy $staticSrc $staticDst /MIR | Out-Null
}

# Minimal 404 for Pages (handy for bad links)
$docs404 = Join-Path $docs '404.html'
if (!(Test-Path $docs404)) {
@'
<!doctype html><meta charset="utf-8"><title>404</title>
<h1>Not Found</h1><p>Try the <a href="/">home</a> or <a href="/blog/">blog</a>.</p>
'@ | Set-Content -Encoding UTF8 $docs404
}

# Build id for commit message
$hash = $null
try { $hash = (git -C $root rev-parse --short HEAD) 2>$null } catch {}
if (-not $hash) { $hash = Get-Date -Format 'yyyyMMddHHmmss' }

# If not a git repo, we're done locally
if (!(Test-Path (Join-Path $root '.git'))) {
  Write-Host "ℹ️  No .git folder found. Skipping commit/push." -ForegroundColor Yellow
  Write-Host "✅ Publish complete (local). Build ID: $hash"
  exit 0
}

Write-Host "📝 Committing and pushing..."
Push-Location $root
try {
  # 0) Make sure 'docs/' is actually tracked even if .gitignore is misconfigured
  & git add -f docs 2>&1 | Write-Host
  & git add .       2>&1 | Write-Host

  # 1) If remote has new commits, rebase before committing to avoid non-fast-forward rejections
  $branch = (& git rev-parse --abbrev-ref HEAD).Trim()
  if (-not $branch) { $branch = 'main' }

  Write-Host "🔄 Fetching & rebasing onto origin/$branch..."

  # Temporarily relax error handling so git's stderr chatter doesn't terminate the script
  $prevEAP = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try {
    & git fetch origin 2>&1 | Out-Host

    # If there are staged changes already, commit them before the rebase
    & git diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
      & git commit -m "Publish (pre-rebase stash): $hash" 2>&1 | Out-Host
    }

    & git pull --rebase origin $branch 2>&1 | Out-Host
  }
  finally {
    $ErrorActionPreference = $prevEAP
  }

  # 2) Stage again in case rebase changed anything + ensure docs forced
  & git add -f docs 2>&1 | Write-Host
  & git add .       2>&1 | Write-Host

  # 3) Commit if there are changes; else make an empty commit to trigger Pages redeploy
  & git diff --cached --quiet
  if ($LASTEXITCODE -ne 0) {
    & git commit -m "Publish: $hash" 2>&1 | Write-Host
  } else {
    Write-Host "ℹ️  No content changes detected. Creating an empty commit to trigger Pages..."
    & git commit --allow-empty -m "Publish (no changes): $hash" 2>&1 | Write-Host
  }

  # 4) Push (set upstream if needed)
  $hasUpstream = $true
  try {
    & git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>$null | Out-Host
    if ($LASTEXITCODE -ne 0) { $hasUpstream = $false }
  } catch { $hasUpstream = $false }

  if (-not $hasUpstream) {
    & git push -u origin $branch 2>&1 | Write-Host
  } else {
    & git push 2>&1 | Write-Host
  }
  if ($LASTEXITCODE -ne 0) { throw "Git push failed." }

  Write-Host "✅ Pushed. Build ID: $hash"
}
finally {
  Pop-Location
}
