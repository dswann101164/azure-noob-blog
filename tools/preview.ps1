# tools\preview.ps1
param(
  [int]$Port = 5050,
  [string]$BindHost = "127.0.0.1",
  [switch]$Open
)

# Don't treat native stderr as a terminating error (Flask prints a dev warning on stderr)
$PSNativeCommandUseErrorActionPreference = $false
$ErrorActionPreference = 'Continue'

# Resolve paths relative to this script
$ScriptDir   = $PSScriptRoot
$ProjectRoot = (Resolve-Path "$ScriptDir\..").Path
$VenvActivate = Join-Path $ProjectRoot ".venv\Scripts\Activate.ps1"
$Runner       = Join-Path $ScriptDir "run_local.py"

# Activate venv if present
if (Test-Path $VenvActivate) { . $VenvActivate }

# Environment for local run
$env:SITE_URL = "http://$BindHost`:$Port"
$env:PYTHONUNBUFFERED = "1"
$env:PYTHONPATH = $ProjectRoot
$env:PYTHONIOENCODING = "utf-8"
$env:RUN_HOST = $BindHost
$env:RUN_PORT = "$Port"

Write-Host "SITE_URL=$($env:SITE_URL)"
Write-Host "Starting Flask via $Runner" -ForegroundColor Cyan

# Always run from project root so static/template paths behave predictably
Set-Location $ProjectRoot

# Optionally open the browser after a tiny delay
if ($Open) {
  Start-Job -ScriptBlock {
    Start-Sleep -Seconds 1
    Start-Process $env:SITE_URL
  } | Out-Null
}

# Run the local server (no reloader). Route stderr to stdout so PS won't treat it as fatal.
python "$Runner" 2>&1 | ForEach-Object { $_ }

# USAGE:
#   .\tools\preview.ps1
#   .\tools\preview.ps1 -Port 5051
#   .\tools\preview.ps1 -Open
#   .\tools\preview.ps1 -BindHost localhost -Port 5050 -Open
