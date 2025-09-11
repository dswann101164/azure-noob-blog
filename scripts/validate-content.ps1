param(
  [string]$RepoRoot = (Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent)
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Fail($msg) {
  Write-Host "❌ $msg" -ForegroundColor Red
  exit 1
}

function Warn($msg) {
  Write-Host "⚠️  $msg" -ForegroundColor Yellow
}

# Paths
$postsDir = Join-Path $RepoRoot 'posts'
$staticDownloads = Join-Path $RepoRoot 'static\downloads'
$staticHero = Join-Path $RepoRoot 'static\images\hero'

if(!(Test-Path $postsDir)){ Fail "Posts directory not found: $postsDir" }

# Results
$errors = @()
$warnings = @()

# Helper: parse front matter (--- ... ---) using regex groups
function Parse-FrontMatter {
  param([string]$Text)

  # Strip BOM if present
  if($Text.Length -gt 0 -and $Text[0] -eq [char]0xFEFF){
    $Text = $Text.Substring(1)
  }

  # (?ms) -> multiline + singleline
  $rx = [regex]'(?ms)^\s*---\s*\r?\n(.*?)\r?\n---\s*\r?\n?(.*)$'
  $m = $rx.Match($Text)
  if($m.Success){
    $fm = $m.Groups[1].Value
    $body = $m.Groups[2].Value
    try {
      $meta = $fm | ConvertFrom-Yaml -ErrorAction Stop
      if($null -eq $meta){ $meta = @{} }
    } catch {
      throw "Invalid YAML front-matter: $($_.Exception.Message)"
    }
    return @($meta, $body)
  } else {
    return @(@{}, $Text)
  }
}

# Validate all posts
$seenSlugs = @{}
Get-ChildItem $postsDir -Filter *.md | ForEach-Object {
  $md = $_
  $raw = Get-Content -Path $md.FullName -Raw -Encoding UTF8
  try {
    $res = Parse-FrontMatter -Text $raw
  } catch {
    $errors += "[$($md.Name)] $_"
    return
  }
  $meta = $res[0]
  $body = $res[1]

  # slug
  $fileSlug = [System.IO.Path]::GetFileNameWithoutExtension($md.Name)
  $slug = $meta.slug
  if([string]::IsNullOrWhiteSpace($slug)){ $slug = $fileSlug }
  if($slug -ne $fileSlug){
    $errors += "[$($md.Name)] slug '$slug' does not match filename '$fileSlug'. Either set slug: $fileSlug or rename the file."
  }
  if($seenSlugs.ContainsKey($slug)){
    $errors += "[$($md.Name)] duplicate slug '$slug' also used by '$($seenSlugs[$slug])'."
  } else {
    $seenSlugs[$slug] = $md.Name
  }

  # title
  if([string]::IsNullOrWhiteSpace([string]$meta.title)){
    $errors += "[$($md.Name)] missing required 'title' in front-matter."
  }

  # date
  $dateOk = $false
  if($meta.date){
    $dateStr = [string]$meta.date
    $formats = @('yyyy-MM-dd','yyyy-MM-dd HH:mm','yyyy-MM-dd HH:mm:ss','o')
    foreach($fmt in $formats){
      try {
        [void][DateTime]::ParseExact($dateStr, $fmt, $null)
        $dateOk = $true; break
      } catch {}
    }
    if(-not $dateOk){
      try {
        [void][DateTime]::Parse($dateStr)
        $dateOk = $true
      } catch {}
    }
  }
  if(-not $dateOk){ $errors += "[$($md.Name)] invalid or missing 'date' (use YYYY-MM-DD or ISO8601)." }

  # summary (your site uses summary, not description)
  if([string]::IsNullOrWhiteSpace([string]$meta.summary)){
    $errors += "[$($md.Name)] missing required 'summary' in front-matter."
  }

  # tags
  $tags = @()
  if($meta.tags -is [System.Array]){ $tags = @($meta.tags) }
  elseif($meta.tags){ $tags = @([string]$meta.tags) }
  if($tags.Count -eq 0){
    $errors += "[$($md.Name)] missing required 'tags' (must be a non-empty list)."
  }

  # cover (warn only) — if provided, check exists under static/images/hero
  if($meta.cover){
    $coverFile = [string]$meta.cover
    if([System.IO.Path]::GetFileName($coverFile) -ne $coverFile){
      # They gave a path; normalize to filename for the site
      $coverFile = [System.IO.Path]::GetFileName($coverFile)
    }
    $coverPath = Join-Path $staticHero $coverFile
    if(!(Test-Path $coverPath)){
      $warnings += "[$($md.Name)] cover '$($meta.cover)' not found under static/images/hero/ (warning)."
    }
  }

  # downloads referenced in body must exist (static/downloads/*)
  $pattern = '(?:href|src)\s*=\s*["'']\/?static\/downloads\/([^"''>]+)["'']'
  $matches = [System.Text.RegularExpressions.Regex]::Matches($raw, $pattern, 'IgnoreCase')
  foreach($m in $matches){
    $fname = $m.Groups[1].Value
    $fpath = Join-Path $staticDownloads $fname
    if(!(Test-Path $fpath)){
      $errors += "[$($md.Name)] download referenced but missing: static/downloads/$fname"
    }
  }
}

# Print summary
if($warnings.Count){ $warnings | ForEach-Object { Warn $_ } }
if($errors.Count){
  $errors | ForEach-Object { Write-Host "❌ $_" -ForegroundColor Red }
  Fail "Validation failed with $($errors.Count) error(s)."
} else {
  Write-Host "✅ Validation passed." -ForegroundColor Green
}
