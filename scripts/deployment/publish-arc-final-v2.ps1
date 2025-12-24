# Final update based on Grok feedback: Add POC quick start and diagram explanation

Write-Host "Adding POC quick start and diagram explanation..." -ForegroundColor Green

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
git commit -m "Arc guide: Add POC quick start for single vCenter + explain architecture diagram upfront"
Write-Host "`nCommitted changes" -ForegroundColor Green

# Push to GitHub
Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
git push

Write-Host "`n✓ Updated successfully!" -ForegroundColor Green
Write-Host "Added: 30-minute POC script + architecture diagram explanation" -ForegroundColor Cyan
Write-Host "Now works for both POC testers AND enterprise deployments" -ForegroundColor Cyan
