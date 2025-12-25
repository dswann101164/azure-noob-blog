# ============================================================================
# LAUNCH KQL PRODUCT - Replace Blog Content
# ============================================================================

Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "LAUNCHING KQL PRODUCT" -ForegroundColor Cyan
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""

$repoRoot = "C:\Users\dswann\Documents\GitHub\azure-noob-blog"
Set-Location $repoRoot

Write-Host "[1/4] Backing up original full post..." -ForegroundColor Yellow

# Create archives directory if it doesn't exist
if (!(Test-Path "archives")) {
    New-Item -ItemType Directory -Path "archives" | Out-Null
}

# Backup the full version
Copy-Item "posts\2025-01-15-kql-cheat-sheet-complete.md" "archives\2025-01-15-kql-cheat-sheet-FULL.md" -Force

Write-Host "  ✓ Backup created: archives\2025-01-15-kql-cheat-sheet-FULL.md" -ForegroundColor Green
Write-Host ""

Write-Host "[2/4] Replacing with FREE version..." -ForegroundColor Yellow

# Check if FREE version exists
if (!(Test-Path "posts\2025-01-15-kql-cheat-sheet-FREE.md")) {
    Write-Host "  ✗ ERROR: FREE version not found!" -ForegroundColor Red
    Write-Host "  Expected: posts\2025-01-15-kql-cheat-sheet-FREE.md" -ForegroundColor Red
    Write-Host ""
    Write-Host "  You need to create this file first." -ForegroundColor Yellow
    Write-Host "  I created it earlier in the conversation." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Replace
Copy-Item "posts\2025-01-15-kql-cheat-sheet-FREE.md" "posts\2025-01-15-kql-cheat-sheet-complete.md" -Force

Write-Host "  ✓ Replaced with FREE version" -ForegroundColor Green
Write-Host ""

Write-Host "[3/4] Freezing site..." -ForegroundColor Yellow

python freeze.py

Write-Host "  ✓ Site frozen" -ForegroundColor Green
Write-Host ""

Write-Host "[4/4] Git operations..." -ForegroundColor Yellow

git add posts docs archives
git commit -m "feat: launch KQL product - trim free content to drive paid sales"

Write-Host "  ✓ Changes committed" -ForegroundColor Green
Write-Host ""

Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "READY TO PUSH!" -ForegroundColor Cyan
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Review changes, then run:" -ForegroundColor Yellow
Write-Host "  git push" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Push to GitHub" -ForegroundColor White
Write-Host "  2. Set up LemonSqueezy account" -ForegroundColor White
Write-Host "  3. Upload azure-kql-query-library-ENHANCED.zip" -ForegroundColor White
Write-Host "  4. Get payment link" -ForegroundColor White
Write-Host "  5. Update blog CTAs" -ForegroundColor White
Write-Host "  6. LAUNCH!" -ForegroundColor White
Write-Host ""
Write-Host "===================================================================" -ForegroundColor Cyan
