# Update Azure Arc vCenter Implementation Guide with jump box details

Write-Host "Updating Azure Arc vCenter guide..." -ForegroundColor Green

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
git commit -m "Update Arc guide: Add critical jump box deployment details and Kubernetes appliance explanation"
Write-Host "`nCommitted changes" -ForegroundColor Green

# Push to GitHub
Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
git push

Write-Host "`n✓ Updated successfully!" -ForegroundColor Green
Write-Host "Updates live at: https://azure-noob.com/blog/azure-arc-vcenter-implementation-guide" -ForegroundColor Cyan
