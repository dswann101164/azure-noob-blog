# Add RSS feed and sitemap.xml to blog

Write-Host "Adding RSS feed and sitemap to azure-noob.com..." -ForegroundColor Green

# Test locally first
Write-Host "`nTesting RSS feed locally..." -ForegroundColor Yellow
flask run &
Start-Sleep -Seconds 3
$rssTest = Invoke-WebRequest -Uri "http://127.0.0.1:5000/feed.xml" -UseBasicParsing
Write-Host "RSS feed working: $($rssTest.Content.Length) bytes" -ForegroundColor Cyan

$sitemapTest = Invoke-WebRequest -Uri "http://127.0.0.1:5000/sitemap.xml" -UseBasicParsing
Write-Host "Sitemap working: $($sitemapTest.Content.Length) bytes" -ForegroundColor Cyan

Stop-Process -Name "flask" -Force -ErrorAction SilentlyContinue

# Freeze the site
Write-Host "`nFreezing site with RSS and sitemap..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe .\freeze.py

# Verify files were created
if (Test-Path "docs\feed.xml") {
    Write-Host "✓ RSS feed generated" -ForegroundColor Green
} else {
    Write-Host "✗ RSS feed missing!" -ForegroundColor Red
}

if (Test-Path "docs\sitemap.xml") {
    Write-Host "✓ Sitemap generated" -ForegroundColor Green
} else {
    Write-Host "✗ Sitemap missing!" -ForegroundColor Red
}

# Add and commit
git add app.py freeze.py docs/feed.xml docs/sitemap.xml
git commit -m "Add RSS feed and sitemap.xml for SEO and discoverability"
Write-Host "`nCommitted changes" -ForegroundColor Green

# Push
Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
git push

Write-Host "`n✅ RSS feed live at: https://azure-noob.com/feed.xml" -ForegroundColor Green
Write-Host "✅ Sitemap live at: https://azure-noob.com/sitemap.xml" -ForegroundColor Green
Write-Host "`nPeople can now subscribe to your blog!" -ForegroundColor Cyan
