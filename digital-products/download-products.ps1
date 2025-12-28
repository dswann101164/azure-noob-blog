# PowerShell Script to Download Your Digital Products
# Run this script to get your Excel files

Write-Host "`n🚀 DOWNLOADING YOUR DIGITAL PRODUCTS...`n" -ForegroundColor Cyan

$outputFolder = "C:\Users\dswann\Documents\GitHub\azure-noob-blog\digital-products"

# Ensure folder exists
if (-not (Test-Path $outputFolder)) {
    New-Item -ItemType Directory -Path $outputFolder -Force | Out-Null
}

Write-Host "📁 Saving files to: $outputFolder`n" -ForegroundColor Yellow

# Product 1: RACI Toolkit (base64 encoded - will be inserted below)
Write-Host "📥 Downloading RACI Toolkit..." -ForegroundColor Green

# NOTE: The actual base64 data is too large for a single script
# I'll create a simpler method for you...

Write-Host "`n❌ WAIT - Let me create an easier method for you!`n" -ForegroundColor Red
