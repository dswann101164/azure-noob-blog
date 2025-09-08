<#
Fix-And-Run-Flask_v2.ps1
Runs from your Flask project root (the folder with app.py).
- Ensures Python (via winget if available and python missing)
- Creates/activates .venv
- Upgrades pip
- Installs Flask (or requirements.txt if present)
- Removes UTF-8 BOM from app.py if present
- Verifies Flask import
- Launches app on http://127.0.0.1:5000
#>

param(
  [int]$Port = 5000,
  [switch]$SkipWingetInstall
)

$ErrorActionPreference = "Stop"

function Ensure-Python {
  if (Get-Command python -ErrorAction SilentlyContinue) { return }
  if ($SkipWingetInstall) { throw "Python not found. Install Python 3.12+ and re-run." }
  if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    throw "Python not found and winget is unavailable. Install Python 3.12+ from python.org, then re-run."
  }
  Write-Host "Installing Python 3.12 via winget..."
  winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
  # Refresh PATH for this session
  $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
              [System.Environment]::GetEnvironmentVariable("Path","User")
  if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python still not found after install. Close & reopen PowerShell, then re-run."
  }
}

function Ensure-Venv {
  if (-not (Test-Path ".\.venv")) {
    Write-Host "Creating virtual environment .venv ..."
    python -m venv .venv
  }
  # Allow activation just for this session
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
  . .\.venv\Scripts\Activate.ps1
}

function Install-Dependencies {
  python -m pip install --upgrade pip
  if (Test-Path ".\requirements.txt") {
    Write-Host "Installing from requirements.txt ..."
    pip install -r ".\requirements.txt"
  } else {
    Write-Host "Installing Flask ..."
    pip install flask
    "flask" | Out-File -Encoding ascii ".\requirements.txt"
  }
}

function Remove-BOM([string]$filePath) {
  if (-not (Test-Path $filePath)) { return }
  $bytes = [System.IO.File]::ReadAllBytes($filePath)
  if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    Write-Host "Removing UTF-8 BOM from $filePath ..."
    [System.IO.File]::WriteAllBytes($filePath, $bytes[3..($bytes.Length-1)])
  }
}

function Sanity-Check {
  Write-Host "Python:" (python --version)
  Write-Host "Pip:" (python -m pip --version)

  # PowerShell-safe way to feed code to Python via STDIN
  $py = @'
import sys
try:
    import flask
    print("Flask", flask.__version__, "OK  (Python:", sys.executable, ")")
except Exception as e:
    print("Flask import FAILED:", e)
    raise
'@
  $py | & python -
}

Write-Host "Project root: $(Get-Location)"

# 1) Python
Ensure-Python

# 2) venv
Ensure-Venv

# 3) deps
Install-Dependencies

# 4) Fix possible BOM in app.py
Remove-BOM ".\app.py"

# 5) Ensure app.py exists (won’t overwrite if already there)
if (-not (Test-Path ".\app.py")) {
  Write-Host "No app.py found; creating a minimal one ..."
  @'
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)  # http://127.0.0.1:5000
'@ | Out-File -Encoding utf8 ".\app.py"
}

# 6) Validate Flask import
Sanity-Check

# 7) Start dev server (simple)
Write-Host "`nStarting Flask dev server on http://127.0.0.1:$Port ..."
$env:FLASK_ENV = "development"
python app.py
