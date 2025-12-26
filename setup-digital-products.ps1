# Copy Digital Products to Local Directory
# Run this from: C:\Users\dswann\Documents\GitHub\azure-noob-blog

Write-Host "Setting up digital products directory..." -ForegroundColor Cyan

# Create directory structure
$productsDir = "digital-products"
if (-not (Test-Path $productsDir)) {
    New-Item -ItemType Directory -Path $productsDir
    Write-Host "✓ Created $productsDir directory" -ForegroundColor Green
}

# Copy logo to digital products
Copy-Item -Path "static\images\logo.png" -Destination "$productsDir\logo.png" -Force
Write-Host "✓ Copied logo.png" -ForegroundColor Green

Write-Host "`nDigital products directory ready!" -ForegroundColor Green
Write-Host "Location: $(Get-Location)\$productsDir" -ForegroundColor Yellow

Write-Host "`nFiles in directory:" -ForegroundColor Cyan
Get-ChildItem $productsDir | Format-Table Name, Length, LastWriteTime

Write-Host "`nTo export PDFs:" -ForegroundColor Yellow
Write-Host "1. Open Complete-KQL-Query-Library.md in VS Code" -ForegroundColor White
Write-Host "2. Press Ctrl+Shift+P" -ForegroundColor White
Write-Host "3. Type 'Markdown PDF: Export (pdf)'" -ForegroundColor White
Write-Host "4. Select PDF" -ForegroundColor White
Write-Host "`nThe azure-noob-pdf-styles.css will be automatically applied!" -ForegroundColor Green
