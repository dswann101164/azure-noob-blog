# DEPLOY-INTERNAL-LINKS.ps1
# Automated deployment script for internal linking changes

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEPLOYING INTERNAL LINKS" -ForegroundColor Cyan
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
git add posts/2025-11-03-powershell-7-enterprise-migration.md
git add posts/2025-10-29-four-logic-apps-every-azure-admin-needs.md
git add posts/2025-11-25-azure-openai-pricing-real-costs.md
git add docs/

Write-Host "✓ Changes staged" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Committing..." -ForegroundColor Yellow
git commit -m "Add: 11 strategic internal links across top posts (PowerShell 7, Logic Apps, OpenAI Pricing)"

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
Write-Host "  • PowerShell 7 Migration: +3 internal links" -ForegroundColor Gray
Write-Host "  • Logic Apps: +6 internal links" -ForegroundColor Gray
Write-Host "  • OpenAI Pricing: +2 internal links" -ForegroundColor Gray
Write-Host "  • Total: 11 strategic internal links added" -ForegroundColor Gray
Write-Host ""
Write-Host "Expected impact: +10-20 clicks/month" -ForegroundColor Green
Write-Host ""
Write-Host "Next: Request indexing in GSC for Logic Apps post" -ForegroundColor Yellow
Write-Host "URL: https://azure-noob.com/blog/four-logic-apps-every-azure-admin-needs" -ForegroundColor White
