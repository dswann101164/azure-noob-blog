# Fix Missing Product Image - RACI Matrix Pro
# The image is getting a 404 because it's not in the repo yet

Write-Host "`n🔧 FIXING MISSING PRODUCT IMAGE...`n" -ForegroundColor Cyan

$repoRoot = "C:\Users\dswann\Documents\GitHub\azure-noob-blog"

# Find the image - check multiple locations
$possibleLocations = @(
    "C:\Users\dswann\Downloads\Azure_CAF_Operations_RACI_Matrix_Pro.png",
    "C:\Users\dswann\Documents\GitHub\azure-noob-blog\digital-products\Azure_CAF_Operations_RACI_Matrix_Pro.png",
    "C:\Users\dswann\Desktop\Azure_CAF_Operations_RACI_Matrix_Pro.png"
)

$sourceImage = $null
foreach ($location in $possibleLocations) {
    if (Test-Path $location) {
        $sourceImage = $location
        Write-Host "✅ Found image at: $location" -ForegroundColor Green
        break
    }
}

if ($sourceImage) {
    # Copy to static/images/products/
    $targetImage = "$repoRoot\static\images\products\Azure_CAF_Operations_RACI_Matrix_Pro.png"
    
    # Ensure directory exists
    $targetDir = Split-Path -Parent $targetImage
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        Write-Host "✅ Created directory: static\images\products\" -ForegroundColor Green
    }
    
    # Copy file
    Copy-Item -Path $sourceImage -Destination $targetImage -Force
    Write-Host "✅ Copied image to: static\images\products\" -ForegroundColor Green
    
    # Freeze site
    Write-Host "`n🧊 Freezing site..." -ForegroundColor Yellow
    cd $repoRoot
    python freeze.py
    
    # Git add, commit, push
    Write-Host "`n📝 Committing to Git..." -ForegroundColor Yellow
    git add static/images/products/Azure_CAF_Operations_RACI_Matrix_Pro.png docs/
    git commit -m "Add RACI Matrix Pro product image"
    git push origin main
    
    Write-Host "`n✅ FIXED! Image will be live in 2-5 minutes.`n" -ForegroundColor Green
    Write-Host "🌍 Check: https://azure-noob.com/products/`n" -ForegroundColor Cyan
    
} else {
    Write-Host "❌ Could not find the image file!" -ForegroundColor Red
    Write-Host "`n📸 MANUAL FIX NEEDED:" -ForegroundColor Yellow
    Write-Host "  1. Find this file: Azure_CAF_Operations_RACI_Matrix_Pro.png" -ForegroundColor White
    Write-Host "  2. Copy it to: $repoRoot\static\images\products\" -ForegroundColor White
    Write-Host "  3. Run:" -ForegroundColor White
    Write-Host "     cd $repoRoot" -ForegroundColor Cyan
    Write-Host "     python freeze.py" -ForegroundColor Cyan
    Write-Host "     git add static/images/products/ docs/" -ForegroundColor Cyan
    Write-Host "     git commit -m 'Add RACI Matrix Pro product image'" -ForegroundColor Cyan
    Write-Host "     git push origin main`n" -ForegroundColor Cyan
}
