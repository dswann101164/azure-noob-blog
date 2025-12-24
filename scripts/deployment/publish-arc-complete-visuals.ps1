# Add all three visual diagrams to Arc guide

Write-Host "Adding complete visual story to Arc guide..." -ForegroundColor Green

# Add all three images
git add "static/images/hero/arc-multi-vcenter-goal.png"
git add "static/images/hero/do-not-be-this-guy.png"
git add "static/images/hero/what-i-wish-i-knew.png"
Write-Host "Added all three diagrams" -ForegroundColor Cyan

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
git commit -m "Arc guide: Add complete visual story (goal → disaster → solution)"
Write-Host "`nCommitted changes" -ForegroundColor Green

# Push
Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
git push

Write-Host "`n✅ Published successfully!" -ForegroundColor Green
Write-Host "Visual narrative: The Goal → What Actually Happens → The Right Way → How to Fix It" -ForegroundColor Cyan
