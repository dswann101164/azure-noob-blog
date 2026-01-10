# GSC Indexing Issues - Master Fix Script
# This guides you through the entire diagnostic and fix process

$ErrorActionPreference = "Stop"

function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host ("=" * 80) -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host ("=" * 80) -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step {
    param([string]$Text)
    Write-Host "  ➤ $Text" -ForegroundColor Yellow
}

function Write-Success {
    param([string]$Text)
    Write-Host "  ✓ $Text" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Text)
    Write-Host "  ⚠ $Text" -ForegroundColor Yellow
}

function Write-Error-Custom {
    param([string]$Text)
    Write-Host "  ✗ $Text" -ForegroundColor Red
}

# Check Python
Write-Header "GSC INDEXING ISSUES - MASTER FIX TOOLKIT"

if (Test-Path ".\.venv\Scripts\python.exe") {
    $python = ".\.venv\Scripts\python.exe"
    Write-Success "Using virtual environment Python"
} else {
    $python = "python"
    Write-Warning "Using system Python (consider creating venv)"
}

# Install dependencies
Write-Step "Installing dependencies..."
& $python -m pip install beautifulsoup4 --quiet --disable-pip-version-check 2>$null
Write-Success "Dependencies installed"

# Main menu
while ($true) {
    Write-Header "WHAT WOULD YOU LIKE TO DO?"
    
    Write-Host "  1. Run full site diagnostic (checks your docs/ folder)"
    Write-Host "  2. Analyze GSC redirects (requires gsc-redirects.csv export)"
    Write-Host "  3. Analyze GSC 404s (requires gsc-404s.csv export)"
    Write-Host "  4. View README and instructions"
    Write-Host "  5. Exit"
    Write-Host ""
    
    $choice = Read-Host "Enter choice (1-5)"
    
    switch ($choice) {
        "1" {
            Write-Header "RUNNING SITE DIAGNOSTIC"
            Write-Step "This analyzes your frozen site in docs/"
            Write-Host ""
            & $python diagnose-gsc-issues.py
            
            Write-Host ""
            Write-Host "Press any key to continue..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        
        "2" {
            Write-Header "ANALYZING GSC REDIRECTS"
            
            if (!(Test-Path "gsc-redirects.csv")) {
                Write-Error-Custom "File not found: gsc-redirects.csv"
                Write-Host ""
                Write-Step "To get this file:"
                Write-Host "  1. Go to Google Search Console"
                Write-Host "  2. Navigate to Indexing → Pages"
                Write-Host "  3. Click the 'Page with redirect' filter"
                Write-Host "  4. Click Export (top right)"
                Write-Host "  5. Save as gsc-redirects.csv in this folder"
                Write-Host ""
            } else {
                Write-Success "Found gsc-redirects.csv"
                Write-Host ""
                & $python analyze-gsc-redirects.py
            }
            
            Write-Host ""
            Write-Host "Press any key to continue..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        
        "3" {
            Write-Header "ANALYZING GSC 404 ERRORS"
            
            if (!(Test-Path "gsc-404s.csv")) {
                Write-Error-Custom "File not found: gsc-404s.csv"
                Write-Host ""
                Write-Step "To get this file:"
                Write-Host "  1. Go to Google Search Console"
                Write-Host "  2. Navigate to Indexing → Pages"
                Write-Host "  3. Click the 'Not found (404)' filter"
                Write-Host "  4. Click Export (top right)"
                Write-Host "  5. Save as gsc-404s.csv in this folder"
                Write-Host ""
            } else {
                Write-Success "Found gsc-404s.csv"
                Write-Host ""
                & $python analyze-gsc-404s.py
            }
            
            Write-Host ""
            Write-Host "Press any key to continue..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        
        "4" {
            Write-Header "VIEWING README"
            
            if (Test-Path "GSC-FIX-README.md") {
                Get-Content "GSC-FIX-README.md" | Out-Host
            } else {
                Write-Error-Custom "README not found"
            }
            
            Write-Host ""
            Write-Host "Press any key to continue..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        
        "5" {
            Write-Header "GOODBYE!"
            Write-Host "  Fix your GSC issues and watch those impressions climb!" -ForegroundColor Green
            Write-Host ""
            exit
        }
        
        default {
            Write-Warning "Invalid choice. Please enter 1-5."
            Start-Sleep -Seconds 1
        }
    }
}
