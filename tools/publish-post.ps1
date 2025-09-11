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

Write-Host "📦 Syncing static assets to docs/..."
if (!(Test-Path $docs)) { New-Item -ItemType Directory $docs | Out-Null }
if (Test-Path $staticSrc) {
  robocopy $staticSrc $staticDst /MIR | Out-Null
} else {
  Write-Host "ℹ️  No 'static/' folder found; skipping static sync." -ForegroundColor Yellow
}

# Ensure docs/404.html exists (good for GitHub Pages)
$docs404 = Join-Path $docs '404.html'
if (!(Test-Path $docs404)) {
  @'
<!doctype html><meta charset="utf-8"><title>404</title>
<h1>Not Found</h1><p>Try the <a href="/">home page</a> or <a href="/blog/">blog</a>.</p>
'@ | Set-Content -Encoding UTF8 $docs404
}

# Optional: ensure docs/index.html if you plan to serve from /docs directly
$docsIndex = Join-Path $docs 'index.html'
if (!(Test-Path $docsIndex)) {
  @'
<!doctype html><meta charset="utf-8"><title>Azure Noob</title>
<meta http-equiv="refresh" content="0; url=/">
<p><a href="/">Go to site</a></p>
'@ | Set-Content -Encoding UTF8 $docsIndex
}

# Try to get a commit hash from the repo, even if we're running elsewhere
$hash = $null
try { $hash = (git -C $root rev-parse --short HEAD) 2>$null } catch {}
if (-not $hash) { $hash = Get-Date -Format 'yyyyMMddHHmmss' }

# If not a git repo, stop here successfully with a note
if (!(Test-Path (Join-Path $root '.git'))) {
  Write-Host "ℹ️  No .git folder found. Skipping commit/push." -ForegroundColor Yellow
  Write-Host "   Assets synced to 'docs/'. Configure hosting as needed."
  Write-Host "✅ Publish complete (local). Build ID: $hash"
  exit 0
}

Write-Host "📝 Committing and pushing..."
Push-Location $root
try {
  git add .
  # Commit even if nothing changed shouldn't be an error—check exit code
  & git commit -m "Publish: $hash" 2>&1 | Write-Host
  $commitCode = $LASTEXITCODE
  if ($commitCode -ne 0) {
    # Git returns non-zero when there’s nothing to commit; that's fine
    Write-Host "ℹ️  Commit may be empty or already up to date." -ForegroundColor Yellow
  }

  # Determine current branch and upstream
  $branch = (& git rev-parse --abbrev-ref HEAD).Trim()
  if (-not $branch) { $branch = "main" }

  $hasUpstream = $true
  try {
    & git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) { $hasUpstream = $false }
  } catch { $hasUpstream = $false }

  if (-not $hasUpstream) {
    Write-Host "ℹ️  No upstream set. Pushing with -u origin $branch..." -ForegroundColor Yellow
    $pushOutput = & git push -u origin $branch 2>&1
  } else {
    $pushOutput = & git push 2>&1
  }
  $pushOutput | Write-Host
  if ($LASTEXITCODE -ne 0) {
    throw "Git push failed (exit $LASTEXITCODE). See output above."
  }

  Write-Host "✅ Pushed. Build ID: $hash"
}
finally {
  Pop-Location
}
