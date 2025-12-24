# Test Content Hubs - Quick Verification Script

Write-Host "Testing Content Hubs Implementation..." -ForegroundColor Cyan
Write-Host ""

# Check if required files exist
$requiredFiles = @(
    "hubs_config.py",
    "templates\hub.html",
    "templates\hubs_index.html"
)

Write-Host "Checking required files..." -ForegroundColor Yellow
$missingFiles = @()
foreach ($file in $requiredFiles) {
    $fullPath = Join-Path $PSScriptRoot $file
    if (Test-Path $fullPath) {
        Write-Host "  OK $file" -ForegroundColor Green
    } else {
        Write-Host "  MISSING $file" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "Missing files! Cannot proceed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Checking Python dependencies..." -ForegroundColor Yellow

# Activate virtual environment
$venvPath = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "  OK Virtual environment found" -ForegroundColor Green
    & $venvPath
} else {
    Write-Host "  ERROR Virtual environment not found at .venv\" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Testing Python imports..." -ForegroundColor Yellow

# Simple test without f-strings to avoid PowerShell escaping issues
$testResult = python -c "import sys; from hubs_config import get_all_hubs; hubs = get_all_hubs(); print('OK: ' + str(len(hubs)) + ' hubs loaded'); sys.exit(0)" 2>&1
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "  $testResult" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Python import test failed" -ForegroundColor Red
    Write-Host "  $testResult" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Starting Flask development server..." -ForegroundColor Yellow
Write-Host "  Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""
Write-Host "Test these URLs:" -ForegroundColor Cyan
Write-Host "  - http://127.0.0.1:5000/hubs/" -ForegroundColor White
Write-Host "  - http://127.0.0.1:5000/hub/finops/" -ForegroundColor White
Write-Host "  - http://127.0.0.1:5000/hub/kql/" -ForegroundColor White
Write-Host "  - http://127.0.0.1:5000/hub/governance/" -ForegroundColor White
Write-Host "  - http://127.0.0.1:5000/hub/monitoring/" -ForegroundColor White
Write-Host ""

# Start Flask
flask run
