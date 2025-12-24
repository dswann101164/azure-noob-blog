# Fix Missing Portal Screenshot
# Re-freeze and deploy to include the portal screenshot

Write-Host "🖼️  Fixing missing Azure Portal screenshot..." -ForegroundColor Cyan

# Navigate to blog directory
Set-Location "C:\Users\dswann\Documents\GitHub\azure-noob-blog"

# Freeze the site (this will copy static images to docs)
Write-Host "`n📦 Re-freezing site..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe .\freeze.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Site frozen successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Freeze failed" -ForegroundColor Red
    exit 1
}

# Stage docs
Write-Host "`n📝 Staging docs..." -ForegroundColor Yellow
git add docs/static/images/azure-portal-resources.png

# Check status
Write-Host "`n📊 Git status:" -ForegroundColor Yellow
git status --short

# Commit
Write-Host "`n💾 Committing..." -ForegroundColor Yellow
git commit -m "Add Azure Portal screenshot to frozen site"

# Push
Write-Host "`n🚀 Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host "`n✅ Screenshot deployed!" -ForegroundColor Green
Write-Host "📍 Image will be live at: https://azure-noob.com/static/images/azure-portal-resources.png" -ForegroundColor Cyan
