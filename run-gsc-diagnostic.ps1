# Run GSC Diagnostic Tool
# This analyzes your frozen site for indexing issues

$ErrorActionPreference = "Stop"

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "Azure Noob - GSC Indexing Diagnostic Tool" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".\.venv\Scripts\python.exe") {
    Write-Host "✓ Found virtual environment" -ForegroundColor Green
    $python = ".\.venv\Scripts\python.exe"
} else {
    Write-Host "⚠ No virtual environment found, using system Python" -ForegroundColor Yellow
    $python = "python"
}

# Install BeautifulSoup4 if needed
Write-Host "Checking dependencies..." -ForegroundColor Cyan
& $python -m pip install beautifulsoup4 --quiet --disable-pip-version-check

# Run diagnostic
Write-Host ""
Write-Host "Running diagnostic..." -ForegroundColor Cyan
Write-Host ""
& $python diagnose-gsc-issues.py

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Green
Write-Host "Diagnostic complete!" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
