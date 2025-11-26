# Publish SEO improvements: featured snippet + Arc hub + Reddit post

Write-Host "Publishing SEO improvements for Azure Arc guide..." -ForegroundColor Green

# 1. Freeze site with updates
Write-Host "`nStep 1: Freezing site..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe .\freeze.py

# 2. Add all changes
Write-Host "`nStep 2: Adding changes..." -ForegroundColor Yellow
git add posts/2025-11-24-azure-arc-vcenter-implementation-guide.md
git add hubs_config.py
git add docs

# 3. Commit
Write-Host "`nStep 3: Committing..." -ForegroundColor Green
git commit -m "SEO: Add featured snippet section to Arc guide + create Arc hub page"

# 4. Push
Write-Host "`nStep 4: Pushing to GitHub..." -ForegroundColor Yellow
git push

Write-Host "`n✅ Published!" -ForegroundColor Green
Write-Host "New featured snippet section optimized for Google" -ForegroundColor Cyan
Write-Host "Arc hub page live at: https://azure-noob.com/hub/azure-arc/" -ForegroundColor Cyan
Write-Host "`nNext: Submit top 10 posts to Google Search Console for indexing" -ForegroundColor Yellow
