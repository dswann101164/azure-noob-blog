# Deploy Azure Arc Master Post

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEPLOYING AZURE ARC MASTER POST" -ForegroundColor Cyan
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

Write-Host "✓ Changes staged" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Committing..." -ForegroundColor Yellow
git commit -m "Add: Azure Arc at Enterprise Scale master post (comprehensive guide linking all Arc content)"

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
Write-Host "New post created:" -ForegroundColor White
Write-Host "  Title: Azure Arc at Enterprise Scale" -ForegroundColor Gray
Write-Host "  File: 2025-12-19-azure-arc-enterprise-scale-problems.md" -ForegroundColor Gray
Write-Host "  Length: ~5,000 words" -ForegroundColor Gray
Write-Host "  Links to: 3 existing Arc deep-dive posts" -ForegroundColor Gray
Write-Host ""
Write-Host "This post covers:" -ForegroundColor Yellow
Write-Host "  • Private Link complexity (links to your lab guide)" -ForegroundColor White
Write-Host "  • Ghost registrations problem (64% fake inventory)" -ForegroundColor White
Write-Host "  • vCenter integration reality" -ForegroundColor White
Write-Host "  • Update Manager confusion" -ForegroundColor White
Write-Host "  • Hidden costs at scale" -ForegroundColor White
Write-Host "  • Operational burden (1 FTE minimum)" -ForegroundColor White
Write-Host ""
Write-Host "Expected impact: +30-50 clicks/month within 60 days" -ForegroundColor Green
Write-Host "SEO targets: 'azure arc scale', 'azure arc enterprise', 'arc problems'" -ForegroundColor Green
Write-Host ""
Write-Host "URL: https://azure-noob.com/blog/azure-arc-enterprise-scale-problems" -ForegroundColor Cyan
