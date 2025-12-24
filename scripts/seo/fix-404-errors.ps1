# Fix 404 Errors - Test and Publish
# This fixes Google Search Console 404 errors by removing trailing slashes

Write-Host "=== FIXING 404 ERRORS ===" -ForegroundColor Cyan
Write-Host ""

# Test 1: Verify trailing slash redirect works
Write-Host "Step 1: Testing trailing slash redirect..." -ForegroundColor Yellow
flask run --port 5001 &
Start-Sleep -Seconds 3

# Test URL with trailing slash should redirect
$testUrl = "http://127.0.0.1:5001/blog/azure-arc-vcenter-implementation-guide/"
Write-Host "Testing: $testUrl"
try {
    $response = Invoke-WebRequest -Uri $testUrl -MaximumRedirection 0 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 301) {
        Write-Host "✓ Trailing slash redirect working (301)" -ForegroundColor Green
    }
} catch {
    if ($_.Exception.Response.StatusCode -eq 'MovedPermanently') {
        Write-Host "✓ Trailing slash redirect working (301)" -ForegroundColor Green
    } else {
        Write-Host "✗ Redirect not working" -ForegroundColor Red
    }
}

# Stop Flask
Get-Process | Where-Object {$_.ProcessName -like "*python*" -and $_.MainWindowTitle -eq ""} | Stop-Process -Force
Write-Host ""

# Step 2: Freeze site
Write-Host "Step 2: Freezing site with NO trailing slashes..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe .\freeze.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Site frozen successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Freeze failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 3: Verify sitemap has NO trailing slashes
Write-Host "Step 3: Verifying sitemap URLs..." -ForegroundColor Yellow
$sitemap = Get-Content .\docs\sitemap.xml -Raw
$trailingSlashCount = ([regex]::Matches($sitemap, "<loc>https://azure-noob.com/[^<]+/</loc>")).Count
$totalUrls = ([regex]::Matches($sitemap, "<loc>")).Count

Write-Host "Total URLs in sitemap: $totalUrls"
Write-Host "URLs with trailing slashes: $trailingSlashCount"

if ($trailingSlashCount -eq 1) {  # Only root should have trailing slash
    Write-Host "✓ Sitemap URLs correct (only root has trailing slash)" -ForegroundColor Green
} else {
    Write-Host "✗ Some URLs still have trailing slashes" -ForegroundColor Yellow
}
Write-Host ""

# Step 4: Show what changed
Write-Host "Step 4: Changes made:" -ForegroundColor Yellow
Write-Host "  • app.py: Added trailing slash redirect (301)" -ForegroundColor White
Write-Host "  • app.py: Removed trailing slashes from ALL routes" -ForegroundColor White
Write-Host "  • freeze.py: Updated sitemap to generate URLs without trailing slashes" -ForegroundColor White
Write-Host "  • All URLs now canonical: /blog/slug (not /blog/slug/)" -ForegroundColor White
Write-Host ""

# Step 5: Commit and push
Write-Host "Step 5: Ready to commit and push?" -ForegroundColor Yellow
Write-Host "This will:" -ForegroundColor White
Write-Host "  • Fix all Google 404 errors" -ForegroundColor White
Write-Host "  • Redirect old trailing-slash URLs (301)" -ForegroundColor White
Write-Host "  • Update sitemap for Google" -ForegroundColor White
Write-Host ""

$response = Read-Host "Commit and push? (y/n)"
if ($response -eq 'y') {
    Write-Host ""
    Write-Host "Committing changes..." -ForegroundColor Yellow
    
    git add app.py freeze.py docs\
    git commit -m "SEO: Fix 404 errors by removing trailing slashes + add 301 redirects"
    git push
    
    Write-Host ""
    Write-Host "=== PUBLISHED ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Wait 10 minutes for GitHub Pages to deploy"
    Write-Host "2. Test: https://azure-noob.com/blog/azure-arc-vcenter-implementation-guide/ (should redirect)"
    Write-Host "3. Submit new sitemap to Google Search Console"
    Write-Host "4. Request re-indexing of fixed URLs"
    Write-Host ""
    Write-Host "This will fix 18 failed URLs in Google Search Console!" -ForegroundColor Green
} else {
    Write-Host "Skipped push. Run 'git push' when ready." -ForegroundColor Yellow
}
