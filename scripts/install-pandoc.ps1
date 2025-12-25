# PANDOC INSTALLATION SCRIPT FOR WINDOWS
# Run this in PowerShell as Administrator

# Check if running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

Write-Host "=== PANDOC + LaTeX INSTALLATION ===" -ForegroundColor Cyan
Write-Host ""

# Install Chocolatey if not present
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey package manager..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    Write-Host "✓ Chocolatey installed" -ForegroundColor Green
} else {
    Write-Host "✓ Chocolatey already installed" -ForegroundColor Green
}

# Install Pandoc
Write-Host ""
Write-Host "Installing Pandoc..." -ForegroundColor Yellow
choco install pandoc -y
Write-Host "✓ Pandoc installed" -ForegroundColor Green

# Install MiKTeX (LaTeX distribution - this is the large download ~4GB)
Write-Host ""
Write-Host "Installing MiKTeX (LaTeX) - This is a large download (~4GB)" -ForegroundColor Yellow
Write-Host "This will take 10-30 minutes depending on your internet speed..." -ForegroundColor Yellow
choco install miktex -y
Write-Host "✓ MiKTeX installed" -ForegroundColor Green

# Refresh environment variables
Write-Host ""
Write-Host "Refreshing environment variables..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Verify installation
Write-Host ""
Write-Host "=== VERIFYING INSTALLATION ===" -ForegroundColor Cyan
Write-Host ""

$pandocVersion = pandoc --version 2>&1 | Select-String "pandoc" | Select-Object -First 1
if ($pandocVersion) {
    Write-Host "✓ Pandoc: $pandocVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Pandoc installation failed" -ForegroundColor Red
}

$latexVersion = pdflatex --version 2>&1 | Select-String "pdfTeX" | Select-Object -First 1
if ($latexVersion) {
    Write-Host "✓ LaTeX: $latexVersion" -ForegroundColor Green
} else {
    Write-Host "✗ LaTeX installation failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== INSTALLATION COMPLETE ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Close and reopen PowerShell (to load new PATH)" -ForegroundColor White
Write-Host "2. Navigate to your blog directory" -ForegroundColor White
Write-Host "3. Run: .\convert-all-pdfs.ps1" -ForegroundColor White
Write-Host ""
