# Deploy Arc Master Post + Hub Update

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEPLOYING ARC MASTER POST + HUB UPDATE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repoPath = "C:\Users\dswann\Documents\GitHub\azure-noob-blog"
Set-Location $repoPath

Write-Host "Step 1: Freezing site..." -ForegroundColor Yellow
python freeze.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Site frozen successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Error freezing site" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Staging changes..." -ForegroundColor Yellow
git add posts/2025-12-19-azure-arc-enterprise-scale-problems.md
git add hubs_config.py
git add docs/

Write-Host "✓ Changes staged" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Committing..." -ForegroundColor Yellow
git commit -m "Add: Azure Arc at Enterprise Scale master post + update Arc hub navigation"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Commit successful" -ForegroundColor Green
} else {
    Write-Host "✗ Commit failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 4: Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Push failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Changes deployed:" -ForegroundColor White
Write-Host "  • New master post: Azure Arc at Enterprise Scale" -ForegroundColor Gray
Write-Host "  • Updated Arc hub with new section" -ForegroundColor Gray
Write-Host "  • 5,000+ words covering 6 major Arc problems" -ForegroundColor Gray
Write-Host "  • Links to 3 existing Arc deep-dive posts" -ForegroundColor Gray
Write-Host ""
Write-Host "Arc Hub sections:" -ForegroundColor Yellow
Write-Host "  0. Enterprise Scale Overview (NEW!)" -ForegroundColor Green
Write-Host "  1. Arc Fundamentals & Implementation" -ForegroundColor White
Write-Host "  2. Arc Inventory & Ghost Registration Management" -ForegroundColor White
Write-Host "  3. Hybrid Networking & DNS for Arc" -ForegroundColor White
Write-Host ""
Write-Host "Expected impact: +30-50 clicks/month" -ForegroundColor Green
Write-Host "SEO targets: 'azure arc scale', 'azure arc enterprise'" -ForegroundColor Green
Write-Host ""
Write-Host "URLs:" -ForegroundColor Yellow
Write-Host "  Post: https://azure-noob.com/blog/azure-arc-enterprise-scale-problems" -ForegroundColor Cyan
Write-Host "  Hub:  https://azure-noob.com/hub/arc/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next: Request indexing in GSC for the new post!" -ForegroundColor Yellow
