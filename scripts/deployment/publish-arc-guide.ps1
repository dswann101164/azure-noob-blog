# Publish Azure Arc vCenter Implementation Guide

Write-Host "Publishing Azure Arc vCenter guide..." -ForegroundColor Green

# Add the new post
git add posts/2025-11-24-azure-arc-vcenter-implementation-guide.md
Write-Host "Added blog post" -ForegroundColor Cyan

# Add the hero image
git add static/images/hero/azure-arc-vcenter-guide.png
Write-Host "Added hero image" -ForegroundColor Cyan

# Freeze the site
Write-Host "`nFreezing site..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe .\freeze.py

# Add the frozen docs
git add docs
Write-Host "Added frozen site" -ForegroundColor Cyan

# Commit
git commit -m "Publish: The Azure Arc Multi-vCenter Implementation Guide That Actually Works"
Write-Host "`nCommitted changes" -ForegroundColor Green

# Push to GitHub
Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
git push

Write-Host "`n✓ Published successfully!" -ForegroundColor Green
Write-Host "Post will be live at: https://azure-noob.com/blog/2025-11-24-azure-arc-vcenter-implementation-guide" -ForegroundColor Cyan
