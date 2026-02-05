# Deploy Arc Checklist CTAs

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEPLOYING ARC CHECKLIST CTAS" -ForegroundColor Cyan
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
git add docs/
git add static/downloads/

Write-Host "✓ Changes staged" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Committing..." -ForegroundColor Yellow
git commit -m "Add Arc Enterprise Readiness Checklist CTAs to master post"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Commit successful" -ForegroundColor Green
} else {
    Write-Host "✗ Commit failed (might be nothing to commit)" -ForegroundColor Yellow
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
Write-Host "What was deployed:" -ForegroundColor White
Write-Host "  • Arc Enterprise Readiness Checklist (PDF + Excel)" -ForegroundColor Gray
Write-Host "  • CTA after Problem 6" -ForegroundColor Gray
Write-Host "  • CTA at end of post" -ForegroundColor Gray
Write-Host ""
Write-Host "Checklist URLs:" -ForegroundColor Yellow
Write-Host "  • https://azure-noob.com/static/downloads/Azure-Arc-Enterprise-Readiness-Checklist.pdf" -ForegroundColor White
Write-Host "  • https://azure-noob.com/static/downloads/Azure-Arc-Enterprise-Readiness-Checklist.xlsx" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Test the download links on your live site" -ForegroundColor White
Write-Host "  2. Share the Arc post on Reddit/LinkedIn" -ForegroundColor White
Write-Host "  3. Monitor download stats in GitHub" -ForegroundColor White
Write-Host ""
Write-Host "Your first lead magnet is LIVE! 🚀" -ForegroundColor Green
