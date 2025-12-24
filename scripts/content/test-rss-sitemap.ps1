# Quick test of RSS and sitemap

Write-Host "Testing RSS feed and sitemap generation..." -ForegroundColor Green

# Just freeze and check
Write-Host "`nFreezing site..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe .\freeze.py

# Check if files exist
Write-Host "`nChecking generated files:" -ForegroundColor Cyan

if (Test-Path "docs\feed.xml") {
    $rssSize = (Get-Item "docs\feed.xml").Length
    Write-Host "✓ RSS feed: $rssSize bytes" -ForegroundColor Green
    Write-Host "  Preview first 500 chars:" -ForegroundColor Gray
    Get-Content "docs\feed.xml" -Head 20
} else {
    Write-Host "✗ RSS feed not generated!" -ForegroundColor Red
}

Write-Host ""

if (Test-Path "docs\sitemap.xml") {
    $sitemapSize = (Get-Item "docs\sitemap.xml").Length
    Write-Host "✓ Sitemap: $sitemapSize bytes" -ForegroundColor Green
    $urlCount = (Select-String -Path "docs\sitemap.xml" -Pattern "<loc>" | Measure-Object).Count
    Write-Host "  Contains $urlCount URLs" -ForegroundColor Gray
} else {
    Write-Host "✗ Sitemap not generated!" -ForegroundColor Red
}

Write-Host "`nIf both files exist, run: .\publish-rss-sitemap.ps1" -ForegroundColor Cyan
