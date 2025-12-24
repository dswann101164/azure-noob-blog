# ============================================
# Azure Noob Blog - SEO Validation Script
# ============================================

Write-Host "`n🔍 Validating SEO Enhancements...`n" -ForegroundColor Cyan

# Activate virtual environment
. .\.venv\Scripts\Activate.ps1

# Start Flask in background
Write-Host "🌐 Starting Flask server..." -ForegroundColor Yellow
$flaskJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    . .\.venv\Scripts\Activate.ps1
    $env:FLASK_APP = "app.py"
    python -m flask run
}

# Wait for Flask to start
Start-Sleep -Seconds 3

# Function to check HTML content
function Test-SeoElement {
    param(
        [string]$Url,
        [string]$Pattern,
        [string]$Description
    )
    
    try {
        $response = Invoke-WebRequest -Uri $Url -UseBasicParsing
        $html = $response.Content
        
        if ($html -match $Pattern) {
            Write-Host "   ✓ $Description" -ForegroundColor Green
            return $true
        } else {
            Write-Host "   ✗ $Description - NOT FOUND" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "   ✗ $Description - ERROR: $_" -ForegroundColor Red
        return $false
    }
}

# Get a random blog post
Write-Host "`n📄 Finding a test post..." -ForegroundColor Yellow
try {
    $searchJson = Invoke-RestMethod -Uri "http://127.0.0.1:5000/search.json"
    $testPost = $searchJson[0]
    $testUrl = "http://127.0.0.1:5000" + $testPost.url
    Write-Host "   Testing: $($testPost.title)" -ForegroundColor Gray
    Write-Host "   URL: $testUrl`n" -ForegroundColor Gray
} catch {
    Write-Host "   ✗ Could not load posts - is Flask running?" -ForegroundColor Red
    Stop-Job $flaskJob
    Remove-Job $flaskJob
    exit 1
}

# Run SEO checks
Write-Host "🔍 Running SEO Checks:`n" -ForegroundColor Cyan

$checks = @{
    "Meta Description (150-160 chars)" = '<meta name="description" content=".{150,160}">'
    "Canonical URL" = '<link rel="canonical" href="https://azure-noob\.com'
    "OG Image (Full URL)" = '<meta property="og:image" content="https://azure-noob\.com'
    "OG Type: Article" = '<meta property="og:type" content="article">'
    "Article Published Time" = '<meta property="article:published_time"'
    "BlogPosting Schema" = '"@type":\s*"BlogPosting"'
    "BreadcrumbList Schema" = '"@type":\s*"BreadcrumbList"'
    "Word Count" = '"wordCount":\s*"\d+"'
    "Reading Time" = '"timeRequired":\s*"PT\d+M"'
    "Author Schema" = '"author":\s*\{'
}

$passed = 0
$total = $checks.Count

foreach ($check in $checks.GetEnumerator()) {
    if (Test-SeoElement -Url $testUrl -Pattern $check.Value -Description $check.Key) {
        $passed++
    }
}

# Additional check: meta description length
Write-Host "`n📏 Meta Description Analysis:" -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri $testUrl -UseBasicParsing
    $html = $response.Content
    
    if ($html -match '<meta name="description" content="([^"]*)"') {
        $metaDesc = $matches[1]
        $length = $metaDesc.Length
        
        Write-Host "   Length: $length characters" -ForegroundColor Gray
        Write-Host "   Content: $($metaDesc.Substring(0, [Math]::Min(80, $length)))..." -ForegroundColor Gray
        
        if ($length -ge 150 -and $length -le 160) {
            Write-Host "   ✓ Optimal length (150-160 chars)" -ForegroundColor Green
        } elseif ($length -ge 120 -and $length -lt 150) {
            Write-Host "   ⚠ Good but could be longer (120+ chars)" -ForegroundColor Yellow
        } else {
            Write-Host "   ✗ Length not optimal" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "   ✗ Could not extract meta description" -ForegroundColor Red
}

# Summary
Write-Host "`n📊 Summary:" -ForegroundColor Cyan
Write-Host "   Passed: $passed / $total checks" -ForegroundColor $(if ($passed -eq $total) { "Green" } else { "Yellow" })

if ($passed -eq $total) {
    Write-Host "`n✅ All SEO checks passed! Ready to deploy.`n" -ForegroundColor Green
} elseif ($passed -ge ($total * 0.8)) {
    Write-Host "`n⚠ Most checks passed. Review failed items above.`n" -ForegroundColor Yellow
} else {
    Write-Host "`n✗ Multiple issues found. Check implementation.`n" -ForegroundColor Red
}

# Cleanup
Write-Host "🛑 Stopping Flask server..." -ForegroundColor Yellow
Stop-Job $flaskJob
Remove-Job $flaskJob

Write-Host "`n✅ Validation complete!`n" -ForegroundColor Green
Write-Host "Next: Test in browser, then freeze & deploy:" -ForegroundColor Cyan
Write-Host "   flask run" -ForegroundColor Gray
Write-Host "   # Open http://127.0.0.1:5000 and view source" -ForegroundColor Gray
Write-Host "   python freeze.py" -ForegroundColor Gray
Write-Host "   git add . && git commit -m 'SEO enhancements' && git push`n" -ForegroundColor Gray
