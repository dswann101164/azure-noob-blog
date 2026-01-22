# Fix robots.txt to only block /search.json, not all JSON files
Write-Host "Fixing robots.txt route in app.py..." -ForegroundColor Cyan

# Read the file
$content = Get-Content "app.py" -Raw

# Find and replace the robots.txt route
$old = '@app.route(''/robots.txt'')
def robots():
    """Generate robots.txt file."""
    robots_content = """User-agent: *
Allow: /

# Don''t index API endpoint
Disallow: /search.json

Sitemap: https://azure-noob.com/sitemap.xml"""

    response = app.response_class(
        robots_content,
        mimetype=''text/plain''
    )
    return response'

$new = '@app.route(''/robots.txt'')
def robots():
    """Generate robots.txt file."""
    robots_content = """User-agent: *
Allow: /

# Block search API endpoint only (not all .json files)
Disallow: /search.json$

Sitemap: https://azure-noob.com/sitemap.xml"""

    response = app.response_class(
        robots_content,
        mimetype=''text/plain''
    )
    return response'

if ($content -match [regex]::Escape($old)) {
    $content = $content.Replace($old, $new)
    Set-Content "app.py" $content -NoNewline
    Write-Host "✓ Fixed robots.txt route" -ForegroundColor Green
} else {
    Write-Host "✗ Could not find the robots.txt route to replace" -ForegroundColor Red
    Write-Host "Manual fix required" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Now run: python freeze.py" -ForegroundColor Cyan
