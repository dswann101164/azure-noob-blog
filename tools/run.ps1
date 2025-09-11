param(
  [int]$Port = 5000
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

if (-not (Test-Path .\.venv\Scripts\Activate.ps1)) {
  Write-Host "Creating virtual environment..." -ForegroundColor Cyan
  py -m venv .venv
}

. .\.venv\Scripts\Activate.ps1

# Ensure deps
$req = Join-Path $here "requirements.txt"
if (Test-Path $req) {
  pip install -r $req | Out-Null
}

$env:FLASK_APP = "app.py"
Write-Host "Starting Flask on http://127.0.0.1:$Port ..." -ForegroundColor Green
flask run --port $Port