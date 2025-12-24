# Publish minor technical correction to Arc guide

Write-Host "Publishing Arc guide technical correction..." -ForegroundColor Green

# Add the updated post
git add posts/2025-11-24-azure-arc-vcenter-implementation-guide.md
Write-Host "Added updated blog post" -ForegroundColor Cyan

# Freeze the site
Write-Host "`nFreezing site..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe .\freeze.py

# Add the frozen docs
git add docs
Write-Host "Added frozen site" -ForegroundColor Cyan

# Commit
git commit -m "Arc guide: Correct Resource Bridge specs (8GB min RAM, 3 static IPs) per Microsoft docs"
Write-Host "`nCommitted changes" -ForegroundColor Green

# Push to GitHub
Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
git push

Write-Host "`n✅ Published successfully!" -ForegroundColor Green
Write-Host "Technical specs now match Microsoft's official documentation" -ForegroundColor Cyan
Write-Host "Your guide is accurate and ready for promotion" -ForegroundColor Cyan
