# Fix robots.txt - remove Disallow rule since we use X-Robots-Tag header instead
Write-Host "Fixing robots.txt in app.py..." -ForegroundColor Cyan

# Backup first
Copy-Item "app.py" "app.py.backup-robots-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# Read the file
$lines = Get-Content "app.py"
$output = @()
$inRobotsFunction = $false
$skip = $false

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    
    # Detect the robots() function
    if ($line -match '@app\.route\(''/robots\.txt''\)') {
        $inRobotsFunction = $true
    }
    
    # If we're in the robots function and see the Disallow line, skip it
    if ($inRobotsFunction -and $line -match 'Disallow: /search\.json') {
        Write-Host "  Removing line: $line" -ForegroundColor Yellow
        # Also skip the blank line after it if present
        continue
    }
    
    # Exit robots function when we hit the next @app.route
    if ($inRobotsFunction -and $line -match '@app\.route' -and $line -notmatch '/robots\.txt') {
        $inRobotsFunction = $false
    }
    
    $output += $line
}

# Write back
$output | Set-Content "app.py" -Encoding UTF8

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Green
Write-Host "ROBOTS.TXT FIXED" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Green
Write-Host ""
Write-Host "Removed 'Disallow: /search.json' line" -ForegroundColor Yellow
Write-Host "/search.json is already blocked via X-Robots-Tag header" -ForegroundColor Green
Write-Host "All other .json files (like lead magnets) are now crawlable" -ForegroundColor Green
Write-Host ""
Write-Host "Run: python freeze.py" -ForegroundColor Cyan
