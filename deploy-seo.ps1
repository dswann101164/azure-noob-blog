# ====================================
# Deploy SEO Enhancements
# ====================================

Write-Host "`n🚀 Deploying SEO Enhancements...`n" -ForegroundColor Cyan

# Step 1: Freeze the site
Write-Host "📦 Freezing static site..." -ForegroundColor Yellow
python freeze.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "   ✗ Freeze failed!" -ForegroundColor Red
    exit 1
}
Write-Host "   ✓ Site frozen successfully" -ForegroundColor Green

# Step 2: Stage changes
Write-Host "`n📋 Staging changes..." -ForegroundColor Yellow
git add .

# Step 3: Commit
Write-Host "`n💾 Committing changes..." -ForegroundColor Yellow
git commit -m "Activate SEO: breadcrumbs, auto meta descriptions, enhanced schema"

if ($LASTEXITCODE -ne 0) {
    Write-Host "   ℹ No changes to commit (already committed)" -ForegroundColor Gray
}

# Step 4: Push to GitHub
Write-Host "`n🚀 Pushing to GitHub..." -ForegroundColor Yellow
git push

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ DEPLOYED SUCCESSFULLY!`n" -ForegroundColor Green
    Write-Host "Your SEO enhancements are now live at: https://azure-noob.com" -ForegroundColor Cyan
    Write-Host "`nNext steps:" -ForegroundColor White
    Write-Host "1. Wait 2-3 minutes for GitHub Pages to rebuild" -ForegroundColor Gray
    Write-Host "2. Visit any blog post and view source (Ctrl+U)" -ForegroundColor Gray
    Write-Host "3. Search for 'BreadcrumbList' - should have clean URLs now" -ForegroundColor Gray
    Write-Host "4. Submit sitemap to Google Search Console:" -ForegroundColor Gray
    Write-Host "   → https://search.google.com/search-console" -ForegroundColor Gray
    Write-Host "   → Add sitemap: https://azure-noob.com/sitemap.xml`n" -ForegroundColor Gray
} else {
    Write-Host "`n✗ Push failed!" -ForegroundColor Red
    Write-Host "Check your git configuration and try again." -ForegroundColor Yellow
}
