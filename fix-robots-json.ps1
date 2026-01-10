# Fix robots.txt to only block search.json, not all JSON files
# This unblocks /static/downloads/certificate-monitor-logic-app.json

Write-Host "Fixing robots.txt generation..." -ForegroundColor Cyan

# Backup
Copy-Item "app.py" "app.py.backup-robots-$(Get-Date -Format 'yyyyMMdd-HHmmss')" -Force
Write-Host "✓ Backed up app.py" -ForegroundColor Green

# Read file
$content = Get-Content "app.py" -Raw

# Fix robots.txt function
$old_robots = @'
@app.route('/robots.txt')
def robots():
    """Generate robots.txt file."""
    robots_content = """User-agent: *
Allow: /

# Don't index API endpoints
Disallow: /search.json
Disallow: /*.json

Sitemap: https://azure-noob.com/sitemap.xml"""

    response = app.response_class(
        robots_content,
        mimetype='text/plain'
    )
    return response
'@

$new_robots = @'
@app.route('/robots.txt')
def robots():
    """Generate robots.txt file."""
    robots_content = """User-agent: *
Allow: /

# Don't index API endpoint
Disallow: /search.json

Sitemap: https://azure-noob.com/sitemap.xml"""

    response = app.response_class(
        robots_content,
        mimetype='text/plain'
    )
    return response
'@

$content = $content.Replace($old_robots, $new_robots)
Write-Host "✓ Removed wildcard /*.json from robots.txt" -ForegroundColor Green

# Save
Set-Content "app.py" $content -NoNewline

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Green
Write-Host "ROBOTS.TXT FIXED" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Green
Write-Host ""
Write-Host "Changes:" -ForegroundColor Yellow
Write-Host "  - Removed 'Disallow: /*.json'" -ForegroundColor White
Write-Host "  - Kept 'Disallow: /search.json'" -ForegroundColor White
Write-Host ""
Write-Host "Result:" -ForegroundColor Yellow
Write-Host "  ✓ /search.json still blocked (API endpoint)" -ForegroundColor Green
Write-Host "  ✓ /static/downloads/*.json now ALLOWED" -ForegroundColor Green
Write-Host ""
Write-Host "Next: python freeze.py && git push" -ForegroundColor Yellow
Write-Host ""
