param(
  [string]$RepoRoot = (Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent)
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Fail($msg) { Write-Host "❌ $msg" -ForegroundColor Red; exit 1 }
function Warn($msg) { Write-Host "⚠️  $msg" -ForegroundColor Yellow }

# ---- Paths ----
$postsDir        = Join-Path $RepoRoot 'posts'
$staticDownloads = Join-Path $RepoRoot 'static\downloads'
$staticHero      = Join-Path $RepoRoot 'static\images\hero'
if(!(Test-Path $postsDir)){ Fail "Posts directory not found: $postsDir" }

# ---- Utils ----
function Parse-FrontMatter {
  param([string]$Text)
  if($Text.Length -gt 0 -and $Text[0] -eq [char]0xFEFF){ $Text = $Text.Substring(1) }  # strip BOM
  $rx = [regex]'(?ms)^\s*---\s*\r?\n(.*?)\r?\n---\s*\r?\n?(.*)$'
  $m = $rx.Match($Text)
  if(-not $m.Success){ return @(@{}, $Text) }
  $fm = $m.Groups[1].Value
  $body = $m.Groups[2].Value
  try {
    $meta = $fm | ConvertFrom-Yaml -ErrorAction Stop
    if($null -eq $meta){ $meta = @{} }
  } catch { throw "Invalid YAML front-matter: $($_.Exception.Message)" }
  return @($meta, $body)
}

# Case-insensitive getter that works for Hashtable or PSCustomObject
function FM {
  param($meta, [string]$name)
  if($meta -is [hashtable]){
    foreach($k in $meta.Keys){
      if([string]::Equals($k, $name, 'InvariantCultureIgnoreCase')){ return $meta[$k] }
    }
    return $null
  } else {
    # PSCustomObject / other
    $prop = $meta.PSObject.Properties | Where-Object { $_.Name -ieq $name } | Select-Object -First 1
    if($prop){ return $prop.Value } else { return $null }
  }
}

# ---- Validation ----
$errors   = @()
$warnings = @()
$seenSlugs = @{}

Get-ChildItem $postsDir -Filter *.md | ForEach-Object {
  $md  = $_
  $raw = Get-Content -Path $md.FullName -Raw -Encoding UTF8

  try {
    $res  = Parse-FrontMatter -Text $raw
  } catch {
    $errors += "[$($md.Name)] $_"
    return
  }
  $meta = $res[0]
  $body = $res[1]

  $fileSlug = [System.IO.Path]::GetFileNameWithoutExtension($md.Name)
  $slug     = FM $meta 'slug'
  if([string]::IsNullOrWhiteSpace([string]$slug)){ $slug = $fileSlug }
  if($slug -ne $fileSlug){
    $errors += "[$($md.Name)] slug '$slug' does not match filename '$fileSlug'. Either set slug: $fileSlug or rename the file."
  }
  if($seenSlugs.ContainsKey($slug)){
    $errors += "[$($md.Name)] duplicate slug '$slug' also used by '$($seenSlugs[$slug])'."
  } else { $seenSlugs[$slug] = $md.Name }

  $title = [string](FM $meta 'title')
  if([string]::IsNullOrWhiteSpace($title)){
    $errors += "[$($md.Name)] missing required 'title' in front-matter."
  }

  $dateVal = FM $meta 'date'
  $dateOk = $false
  if($null -ne $dateVal){
    $dateStr = [string]$dateVal
    $formats = @('yyyy-MM-dd','yyyy-MM-dd HH:mm','yyyy-MM-dd HH:mm:ss','o')
    foreach($fmt in $formats){
      try { [void][DateTime]::ParseExact($dateStr, $fmt, $null); $dateOk = $true; break } catch {}
    }
    if(-not $dateOk){
      try { [void][DateTime]::Parse($dateStr); $dateOk = $true } catch {}
    }
  }
  if(-not $dateOk){ $errors += "[$($md.Name)] invalid or missing 'date' (use YYYY-MM-DD or ISO8601)." }

  $summary = [string](FM $meta 'summary')
  if([string]::IsNullOrWhiteSpace($summary)){
    # allow 'description' but nudge to 'summary'
    $desc = [string](FM $meta 'description')
    if([string]::IsNullOrWhiteSpace($desc)){
      $errors += "[$($md.Name)] missing required 'summary' in front-matter."
    } else {
      $warnings += "[$($md.Name)] uses 'description' — prefer 'summary'."
    }
  }

  # tags (accept array or comma string)
  $tagsVal = FM $meta 'tags'
  $tags = @()
  if($tagsVal -is [System.Array]){ $tags = @($tagsVal) }
  elseif($tagsVal){ $tags = [string]$tagsVal -split '\s*,\s*' }
  if($tags.Count -eq 0){
    $errors += "[$($md.Name)] missing required 'tags' (must be a non-empty list)."
  }

  # cover (warn only)
  $coverVal = FM $meta 'cover'
  if($coverVal){
    $coverFile = [string]$coverVal
    if([System.IO.Path]::GetFileName($coverFile) -ne $coverFile){ $coverFile = [System.IO.Path]::GetFileName($coverFile) }
    $coverPath = Join-Path $staticHero $coverFile
    if(!(Test-Path $coverPath)){
      $warnings += "[$($md.Name)] cover '$coverVal' not found under static/images/hero/ (warning)."
    }
  }

  # downloads referenced in body must exist: static/downloads/*
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

# ---- Summary ----
if($warnings.Count){ $warnings | ForEach-Object { Warn $_ } }
if($errors.Count){
  $errors | ForEach-Object { Write-Host "❌ $_" -ForegroundColor Red }
  Fail "Validation failed with $($errors.Count) error(s)."
} else {
  Write-Host "✅ Validation passed." -ForegroundColor Green
}
