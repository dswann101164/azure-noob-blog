# ============================================================================
# PHASE 2 CLEANUP - Get to under 15 root files
# ============================================================================

Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "PHASE 2 CLEANUP - Final Organization" -ForegroundColor Cyan
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""

$repoRoot = "C:\Users\dswann\Documents\GitHub\azure-noob-blog"
Set-Location $repoRoot

# Move remaining documentation
Write-Host "[PHASE 2.1] Moving remaining documentation..." -ForegroundColor Yellow

$remainingDocs = @(
    "azure-noob-status.md",
    "BANGER_SUMMARY.md", 
    "BLOG-POST-READY.md",
    "CONVERT-LEAD-MAGNETS-TO-PDF.md",
    "CRITICAL-SEO-FIXES-NOT-INDEXED.md",
    "DEPLOY-GSC-OPTIMIZATION.md",
    "DEPLOY-NOW.md",
    "DEPLOYMENT-SUMMARY-DEC18-2025.md",
    "DIRECTORY-LISTING-FIX.md",
    "GITHUB-CALLOUT-USAGE.md",
    "GITHUB_REPO_PLAN.md",
    "GSC-OPTIMIZATION-2025-12-18.md",
    "HERO_IMAGES_INSTRUCTIONS.md",
    "HERO_IMAGES_NEEDED.md",
    "HERO_IMAGE_CONCEPT.md",
    "HOW-TO-GET-GSC-EXCLUSION-DATA.md",
    "HUB-STRUCTURE-VISUAL.md",
    "INTERNAL-LINKING-AUDIT.md",
    "INTERNAL-LINKING-IMPLEMENTATION.md",
    "INTERNAL-LINKING-QUICK-START.md",
    "INTERNAL-LINKING-UPDATES.md",
    "MONETIZATION-ROADMAP.md",
    "PROJECT_TRACKER.md",
    "PROMOTION_STRATEGY.md",
    "QUICK_START_SEO.md",
    "READY-TO-DEPLOY.md",
    "repo-structure.txt",
    "SEO-AUTOMATION-SETUP.md",
    "SEO-EMERGENCY-FIXES.md",
    "SEO-IMPROVEMENTS-NOVEMBER-2025.md",
    "SEO-OPTIMIZATION-2025-12-12.md",
    "SEO_IMPLEMENTATION_GUIDE.md",
    "SERIES_COMPLETE.md",
    "social-media-promotion-cost-optimization.md",
    "SYSTEM_ARCHITECTURE.md",
    "TECHNICAL-SEO-FIXES.md",
    "TOOL-SELECTION-COMPLETE-PACKAGE.md",
    "TOOL-SELECTION-EMAIL-CAMPAIGN.md",
    "TOOL-SELECTION-REDDIT-PROMOTION.md",
    "URGENT-REFREEZE-NEEDED.md"
)

foreach ($file in $remainingDocs) {
    if (Test-Path "$repoRoot\$file") {
        Write-Host "  Moving: $file" -ForegroundColor Gray
        Move-Item -Path "$repoRoot\$file" -Destination "$repoRoot\docs-internal\deployment-guides\" -Force
    }
}

Write-Host "  ✓ Remaining documentation organized" -ForegroundColor Green
Write-Host ""

# Move remaining Python scripts
Write-Host "[PHASE 2.2] Moving remaining Python scripts..." -ForegroundColor Yellow

$remainingPython = @(
    "create_hero_images.py",
    "fix-404-redirects.py",
    "update_seo_frontmatter.py"
)

foreach ($file in $remainingPython) {
    if (Test-Path "$repoRoot\$file") {
        Write-Host "  Moving: $file" -ForegroundColor Gray
        Move-Item -Path "$repoRoot\$file" -Destination "$repoRoot\scripts\content\" -Force
    }
}

Write-Host "  ✓ Python scripts organized" -ForegroundColor Green
Write-Host ""

# Move PowerShell utility scripts
Write-Host "[PHASE 2.3] Moving PowerShell utility scripts..." -ForegroundColor Yellow

$remainingPS1 = @(
    "Add-Icons-To-Excel.ps1",
    "publish-series.bat",
    "run-all-optimizations.ps1"
)

foreach ($file in $remainingPS1) {
    if (Test-Path "$repoRoot\$file") {
        Write-Host "  Moving: $file" -ForegroundColor Gray
        Move-Item -Path "$repoRoot\$file" -Destination "$repoRoot\scripts\content\" -Force
    }
}

Write-Host "  ✓ PowerShell utilities organized" -ForegroundColor Green
Write-Host ""

# Move cleanup files
Write-Host "[PHASE 2.4] Moving cleanup files..." -ForegroundColor Yellow

$cleanupFiles = @(
    "CLEANUP-REPO.ps1",
    "CLEANUP-GUIDE.md",
    "README-NEW.md"
)

foreach ($file in $cleanupFiles) {
    if (Test-Path "$repoRoot\$file") {
        Write-Host "  Moving: $file" -ForegroundColor Gray
        Move-Item -Path "$repoRoot\$file" -Destination "$repoRoot\docs-internal\" -Force
    }
}

Write-Host "  ✓ Cleanup files archived" -ForegroundColor Green
Write-Host ""

# FINAL COUNT
Write-Host ""
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "PHASE 2 COMPLETE!" -ForegroundColor Cyan
Write-Host "===================================================================" -ForegroundColor Cyan

$rootFiles = (Get-ChildItem -Path $repoRoot -File).Count

Write-Host ""
Write-Host "ROOT FILES NOW: $rootFiles" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Test: python freeze.py" -ForegroundColor White
Write-Host "  2. Test: python app.py" -ForegroundColor White
Write-Host "  3. Commit: git add -A" -ForegroundColor White
Write-Host "  4. Commit: git commit -m 'chore: organize repo structure (phase 2)'" -ForegroundColor White
Write-Host "  5. Push: git push" -ForegroundColor White
Write-Host ""
Write-Host "===================================================================" -ForegroundColor Cyan
