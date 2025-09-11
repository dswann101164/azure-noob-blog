param(
  [Parameter(Mandatory = $true)]
  [string]$PostPath,                       # e.g. .\posts\2025-09-08-my-post.md
  [string]$Message = "Publish blog post"   # commit message prefix
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Normalize-Post([string]$fp) {
  if (-not (Test-Path $fp)) { throw "Post not found: $fp" }

  $raw = Get-Content -Raw $fp -Encoding UTF8

  # Re-decode common mojibake (cp1252→utf8), then normalize punctuation
  $bytes1252 = [Text.Encoding]::GetEncoding(1252).GetBytes($raw)
  $txt = [Text.Encoding]::UTF8.GetString($bytes1252)

  $map = @{
    ([char]0xFEFF) = ''     # BOM
    ([char]0x00A0) = ' '    # NBSP
    ([char]0x2018) = "'"    # ‘
    ([char]0x2019) = "'"    # ’
    ([char]0x2032) = "'"    # ′
    ([char]0x201C) = '"'    # “
    ([char]0x201D) = '"'    # ”
    ([char]0x2033) = '"'    # ″
    ([char]0x2013) = '-'    # –
    ([char]0x2014) = '--'   # —
  }
  foreach ($k in $map.Keys) {
    $txt = $txt -replace [regex]::Escape([string]$k), [string]$map[$k]
  }

  # Normalize a common heading we use
  $txt = $txt -replace "##\s*.*Download.*Matrix.*", "## Download the Matrix"

  Set-Content $fp $txt -Encoding UTF8
}

function Get-Slug([string]$fp) {
  $content = Get-Content -Raw $fp -Encoding UTF8
  if ($content -match "(?ms)^---\s*.*?^slug:\s*([^\r\n#]+)\s*.*?^---") {
    return ($matches[1].Trim())
  }
  return [IO.Path]::GetFileNameWithoutExtension($fp)
}

function Find-DuplicateSlugs([string]$targetSlug) {
  $dupes = @()
  Get-ChildItem .\posts\*.md | ForEach-Object {
    $c = Get-Content -Raw $_.FullName -Encoding UTF8
    $s = $null
    if ($c -match "(?ms)^---\s*.*?^slug:\s*([^\r\n#]+)\s*.*?^---") {
      $s = $matches[1].Trim()
    } else {
      $s = [IO.Path]::GetFileNameWithoutExtension($_.FullName)
    }
    if ($s -eq $targetSlug) { $dupes += $_.FullName }
  }
  return $dupes
}

# --- run ---
Normalize-Post $PostPath
$slug = Get-Slug $PostPath
Write-Host "✓ Post normalized. Slug: $slug"

# Guard: duplicate slugs
$dupes = Find-DuplicateSlugs $slug
if ($dupes.Count -gt 1) {
  throw "Duplicate slug '$slug' in:`n - " + ($dupes -join "`n - ") + "`nFix by renaming or marking one as draft."
}

# Freeze with full error capture
$freezeLog = ".\freeze.log"
Write-Host "Freezing site..."
$null = python .\freeze.py 2>&1 | Tee-Object -File $freezeLog

# Verify the page was emitted
$dest = Join-Path ".\docs\blog" "$slug\index.html"
if (-not (Test-Path $dest)) {
  Write-Host "`n❌ Freeze did not emit $dest"
  Write-Host "See $freezeLog for details."
  exit 1
}

# Ensure CNAME is present (if freeze.py didn’t write it)
if (-not (Test-Path .\docs\CNAME)) { Set-Content .\docs\CNAME 'azure-noob.com' }

# Commit & push
git add $PostPath
git add -f .\docs\
git commit -m ("{0}: {1}" -f $Message, $slug)
git push origin main

Write-Host "✓ Published: https://azure-noob.com/blog/$slug/"
