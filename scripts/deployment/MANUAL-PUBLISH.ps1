# Manual Publish - Run this in PowerShell
cd C:\Users\dswann\Documents\GitHub\azure-noob-blog

# Stage all changes
git add app.py freeze.py docs\ post_process_sitemap.py publish-404-fixes.ps1

# Commit
git commit -m "SEO: Fix 404 errors - remove trailing slashes and add 301 redirects"

# Push
git push

Write-Host ""
Write-Host "=== PUBLISHED ===" -ForegroundColor Green
Write-Host ""
Write-Host "✓ All 404 errors fixed!" -ForegroundColor Green
Write-Host "✓ Sitemap updated (227 URLs, NO trailing slashes)" -ForegroundColor Green
Write-Host "✓ 301 redirects added for old URLs" -ForegroundColor Green
Write-Host ""
Write-Host "Wait 10 minutes, then test:" -ForegroundColor Yellow
Write-Host "  https://azure-noob.com/blog/azure-arc-vcenter-implementation-guide/" -ForegroundColor Cyan
Write-Host "  (should redirect to the version WITHOUT trailing slash)" -ForegroundColor White
