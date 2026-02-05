# Deploy Arc Checklist CTAs to All Arc Posts

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEPLOYING ARC CHECKLIST CTAS (4 POSTS)" -ForegroundColor Cyan
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
git add posts/2025-12-06-azure-arc-ghost-registrations.md
git add posts/2025-11-26-azure-arc-private-lab.md
git add posts/2025-11-24-azure-arc-vcenter-implementation-guide.md
git add docs/
git add static/downloads/

Write-Host "✓ Changes staged" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Committing..." -ForegroundColor Yellow
git commit -m "Add Arc Enterprise Readiness Checklist CTAs to all Arc posts"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Commit successful" -ForegroundColor Green
} else {
    Write-Host "✗ Commit failed (might be nothing new to commit)" -ForegroundColor Yellow
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
Write-Host "CTAs added to 4 Arc posts:" -ForegroundColor White
Write-Host "  1. Azure Arc at Enterprise Scale (master post)" -ForegroundColor Gray
Write-Host "  2. Ghost Registrations" -ForegroundColor Gray
Write-Host "  3. Private Lab Setup" -ForegroundColor Gray
Write-Host "  4. vCenter Implementation Guide" -ForegroundColor Gray
Write-Host ""
Write-Host "Checklist available at:" -ForegroundColor Yellow
Write-Host "  • https://azure-noob.com/static/downloads/Azure-Arc-Enterprise-Readiness-Checklist.pdf" -ForegroundColor White
Write-Host "  • https://azure-noob.com/static/downloads/Azure-Arc-Enterprise-Readiness-Checklist.xlsx" -ForegroundColor White
Write-Host ""
Write-Host "Expected monthly downloads: 3-11" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next: Monitor download stats and traffic to these posts" -ForegroundColor White
Write-Host ""
Write-Host "Your first lead magnet is fully deployed across all Arc content! 🚀" -ForegroundColor Green
