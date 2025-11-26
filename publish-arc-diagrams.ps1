# Add visual diagrams to Arc guide

Write-Host "Adding visual diagrams to Arc guide..." -ForegroundColor Green

# Add images
git add "static/images/hero/do-not-be-this-guy.png"
git add "static/images/hero/what-i-wish-i-knew.png"
Write-Host "Added images" -ForegroundColor Cyan

# Add updated post
git add posts/2025-11-24-azure-arc-vcenter-implementation-guide.md
Write-Host "Added updated blog post" -ForegroundColor Cyan

# Freeze the site
Write-Host "`nFreezing site..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe .\freeze.py

# Add frozen docs
git add docs
Write-Host "Added frozen site" -ForegroundColor Cyan

# Commit
git commit -m "Arc guide: Add visual diagrams showing wrong vs right deployment patterns"
Write-Host "`nCommitted changes" -ForegroundColor Green

# Push
Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
git push

Write-Host "`n✅ Published successfully!" -ForegroundColor Green
Write-Host "Visual storytelling: wrong way → right way → how to fix it" -ForegroundColor Cyan
