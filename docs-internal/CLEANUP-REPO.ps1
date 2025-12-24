# ============================================================================
# AZURE NOOB BLOG - REPOSITORY CLEANUP SCRIPT
# ============================================================================
# This script organizes 164 root-level files into a clean structure
# 
# BEFORE: 164 files in root
# AFTER:  ~10 files in root (core only)
#
# Run this once, then commit the reorganized structure
# ============================================================================

Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "AZURE NOOB BLOG - REPOSITORY CLEANUP" -ForegroundColor Cyan
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""

$repoRoot = "C:\Users\dswann\Documents\GitHub\azure-noob-blog"
Set-Location $repoRoot

# ============================================================================
# PHASE 1: MOVE DEPLOYMENT SCRIPTS
# ============================================================================

Write-Host "[PHASE 1] Moving deployment scripts..." -ForegroundColor Yellow

$deploymentScripts = @(
    "deploy-*.ps1",
    "publish-*.ps1",
    "DEPLOY-*.ps1",
    "verify-and-push.ps1",
    "push-updates.bat",
    "init_push.sh",
    "MANUAL-PUBLISH.ps1"
)

foreach ($pattern in $deploymentScripts) {
    Get-ChildItem -Path $repoRoot -Filter $pattern -File | ForEach-Object {
        Write-Host "  Moving: $($_.Name)" -ForegroundColor Gray
        Move-Item -Path $_.FullName -Destination "$repoRoot\scripts\deployment\" -Force
    }
}

Write-Host "  ✓ Deployment scripts organized" -ForegroundColor Green
Write-Host ""

# ============================================================================
# PHASE 2: MOVE SEO SCRIPTS
# ============================================================================

Write-Host "[PHASE 2] Moving SEO scripts..." -ForegroundColor Yellow

$seoScripts = @(
    "activate-seo*.py",
    "activate-seo*.ps1",
    "fix-*.ps1",
    "update_*_metadata.py",
    "analyze-*.ps1",
    "validate-*.ps1",
    "search_console_rankings.py",
    "run_rankings_daily.*",
    "fix_*.py",
    "validate_*.py"
)

foreach ($pattern in $seoScripts) {
    Get-ChildItem -Path $repoRoot -Filter $pattern -File | ForEach-Object {
        Write-Host "  Moving: $($_.Name)" -ForegroundColor Gray
        Move-Item -Path $_.FullName -Destination "$repoRoot\scripts\seo\" -Force
    }
}

Write-Host "  ✓ SEO scripts organized" -ForegroundColor Green
Write-Host ""

# ============================================================================
# PHASE 3: MOVE CONTENT SCRIPTS
# ============================================================================

Write-Host "[PHASE 3] Moving content scripts..." -ForegroundColor Yellow

$contentScripts = @(
    "create_*_hero.py",
    "create-*.ps1",
    "generate-*.bat",
    "Optimize-*.ps1",
    "write-*.ps1",
    "convert-*.ps1"
)

foreach ($pattern in $contentScripts) {
    Get-ChildItem -Path $repoRoot -Filter $pattern -File | ForEach-Object {
        Write-Host "  Moving: $($_.Name)" -ForegroundColor Gray
        Move-Item -Path $_.FullName -Destination "$repoRoot\scripts\content\" -Force
    }
}

Write-Host "  ✓ Content scripts organized" -ForegroundColor Green
Write-Host ""

# ============================================================================
# PHASE 4: MOVE DOCUMENTATION FILES
# ============================================================================

Write-Host "[PHASE 4] Moving documentation files..." -ForegroundColor Yellow

$docPatterns = @(
    "*-SUMMARY.md",
    "*-COMPLETE.md",
    "*-GUIDE.md",
    "*-PLAN.md",
    "*-CHECKLIST.md",
    "*-TRACKER.md",
    "*-NOTES.md",
    "*-README.md",
    "*-STRATEGY.md",
    "SESSION_*.md",
    "TODAY_*.md",
    "WEEK-*.md"
)

foreach ($pattern in $docPatterns) {
    Get-ChildItem -Path $repoRoot -Filter $pattern -File | ForEach-Object {
        Write-Host "  Moving: $($_.Name)" -ForegroundColor Gray
        Move-Item -Path $_.FullName -Destination "$repoRoot\docs-internal\deployment-guides\" -Force
    }
}

Write-Host "  ✓ Documentation organized" -ForegroundColor Green
Write-Host ""

# ============================================================================
# PHASE 5: MOVE RANKING FILES
# ============================================================================

Write-Host "[PHASE 5] Moving ranking files..." -ForegroundColor Yellow

Get-ChildItem -Path $repoRoot -Filter "rankings_*.md" -File | ForEach-Object {
    Write-Host "  Moving: $($_.Name)" -ForegroundColor Gray
    Move-Item -Path $_.FullName -Destination "$repoRoot\archives\rankings\" -Force
}

Write-Host "  ✓ Rankings archived" -ForegroundColor Green
Write-Host ""

# ============================================================================
# PHASE 6: MOVE CONFIG FILES
# ============================================================================

Write-Host "[PHASE 6] Moving config files..." -ForegroundColor Yellow

$configFiles = @(
    "credentials.json",
    "token.pickle",
    "hubs_config.py"
)

foreach ($file in $configFiles) {
    if (Test-Path "$repoRoot\$file") {
        Write-Host "  Moving: $file" -ForegroundColor Gray
        Move-Item -Path "$repoRoot\$file" -Destination "$repoRoot\config\" -Force
    }
}

Write-Host "  ✓ Config files organized" -ForegroundColor Green
Write-Host ""

# ============================================================================
# PHASE 7: MOVE CSV FILES
# ============================================================================

Write-Host "[PHASE 7] Moving CSV files..." -ForegroundColor Yellow

Get-ChildItem -Path $repoRoot -Filter "*.csv" -File | ForEach-Object {
    Write-Host "  Moving: $($_.Name)" -ForegroundColor Gray
    Move-Item -Path $_.FullName -Destination "$repoRoot\docs-internal\deployment-guides\" -Force
}

Write-Host "  ✓ CSV files organized" -ForegroundColor Green
Write-Host ""

# ============================================================================
# PHASE 8: MOVE BACKUP FILES
# ============================================================================

Write-Host "[PHASE 8] Moving backup files..." -ForegroundColor Yellow

Get-ChildItem -Path $repoRoot -Filter "*.backup*" -File | ForEach-Object {
    Write-Host "  Moving: $($_.Name)" -ForegroundColor Gray
    Move-Item -Path $_.FullName -Destination "$repoRoot\archives\" -Force
}

Write-Host "  ✓ Backup files archived" -ForegroundColor Green
Write-Host ""

# ============================================================================
# PHASE 9: MOVE TEST SCRIPTS
# ============================================================================

Write-Host "[PHASE 9] Moving test scripts..." -ForegroundColor Yellow

Get-ChildItem -Path $repoRoot -Filter "test-*.ps1" -File | ForEach-Object {
    Write-Host "  Moving: $($_.Name)" -ForegroundColor Gray
    Move-Item -Path $_.FullName -Destination "$repoRoot\scripts\content\" -Force
}

Get-ChildItem -Path $repoRoot -Filter "test-*.bat" -File | ForEach-Object {
    Write-Host "  Moving: $($_.Name)" -ForegroundColor Gray
    Move-Item -Path $_.FullName -Destination "$repoRoot\scripts\content\" -Force
}

Write-Host "  ✓ Test scripts organized" -ForegroundColor Green
Write-Host ""

# ============================================================================
# PHASE 10: MOVE REMAINING UTILITY SCRIPTS
# ============================================================================

Write-Host "[PHASE 10] Moving remaining utility scripts..." -ForegroundColor Yellow

$utilityScripts = @(
    "check-*.ps1",
    "show-*.bat",
    "stop *.ps1",
    "update-*.ps1",
    "get-*.js",
    "post_process_sitemap.py",
    "publish_with_validation.py"
)

foreach ($pattern in $utilityScripts) {
    Get-ChildItem -Path $repoRoot -Filter $pattern -File | ForEach-Object {
        Write-Host "  Moving: $($_.Name)" -ForegroundColor Gray
        Move-Item -Path $_.FullName -Destination "$repoRoot\scripts\" -Force
    }
}

Write-Host "  ✓ Utility scripts organized" -ForegroundColor Green
Write-Host ""

# ============================================================================
# FINAL REPORT
# ============================================================================

Write-Host ""
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "CLEANUP COMPLETE!" -ForegroundColor Cyan
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""

$rootFiles = (Get-ChildItem -Path $repoRoot -File).Count
$scriptsDeployment = (Get-ChildItem -Path "$repoRoot\scripts\deployment" -File -ErrorAction SilentlyContinue).Count
$scriptsSEO = (Get-ChildItem -Path "$repoRoot\scripts\seo" -File -ErrorAction SilentlyContinue).Count
$scriptsContent = (Get-ChildItem -Path "$repoRoot\scripts\content" -File -ErrorAction SilentlyContinue).Count
$docsInternal = (Get-ChildItem -Path "$repoRoot\docs-internal\deployment-guides" -File -ErrorAction SilentlyContinue).Count
$rankings = (Get-ChildItem -Path "$repoRoot\archives\rankings" -File -ErrorAction SilentlyContinue).Count

Write-Host "BEFORE: 164 files in root" -ForegroundColor Red
Write-Host "AFTER:  $rootFiles files in root" -ForegroundColor Green
Write-Host ""
Write-Host "FILES ORGANIZED:"
Write-Host "  scripts/deployment/        : $scriptsDeployment files" -ForegroundColor Gray
Write-Host "  scripts/seo/               : $scriptsSEO files" -ForegroundColor Gray
Write-Host "  scripts/content/           : $scriptsContent files" -ForegroundColor Gray
Write-Host "  docs-internal/             : $docsInternal files" -ForegroundColor Gray
Write-Host "  archives/rankings/         : $rankings files" -ForegroundColor Gray
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Review the organized structure" -ForegroundColor White
Write-Host "  2. Update any hardcoded paths in scripts" -ForegroundColor White
Write-Host "  3. Test freeze.py and app.py still work" -ForegroundColor White
Write-Host "  4. Commit changes: git add -A && git commit -m 'chore: organize repo structure'" -ForegroundColor White
Write-Host ""
Write-Host "===================================================================" -ForegroundColor Cyan
