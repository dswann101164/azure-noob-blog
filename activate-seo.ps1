# ============================================
# Azure Noob Blog - SEO Enhancement Activation
# ============================================

Write-Host "`n🚀 Activating SEO Enhancements...`n" -ForegroundColor Cyan

# Step 1: Backup current files
Write-Host "📦 Creating backups..." -ForegroundColor Yellow
if (Test-Path "app.py") {
    Copy-Item "app.py" "app.py.backup" -Force
    Write-Host "   ✓ Backed up app.py" -ForegroundColor Green
}
if (Test-Path "templates\blog_post.html") {
    Copy-Item "templates\blog_post.html" "templates\blog_post.html.backup" -Force
    Write-Host "   ✓ Backed up blog_post.html" -ForegroundColor Green
}

# Step 2: Activate enhanced files
Write-Host "`n🔄 Activating enhanced versions..." -ForegroundColor Yellow
if (Test-Path "app_enhanced.py") {
    Move-Item "app_enhanced.py" "app.py" -Force
    Write-Host "   ✓ Activated app_enhanced.py → app.py" -ForegroundColor Green
} else {
    Write-Host "   ✗ app_enhanced.py not found!" -ForegroundColor Red
    exit 1
}

if (Test-Path "templates\blog_post_enhanced.html") {
    Move-Item "templates\blog_post_enhanced.html" "templates\blog_post.html" -Force
    Write-Host "   ✓ Activated blog_post_enhanced.html → blog_post.html" -ForegroundColor Green
} else {
    Write-Host "   ✗ blog_post_enhanced.html not found!" -ForegroundColor Red
    exit 1
}

# Step 3: Test the app
Write-Host "`n🧪 Testing Flask app..." -ForegroundColor Yellow

# Create a simple test script
$testScript = @"
try:
    from app import app
    print('OK')
except Exception as e:
    print('ERROR:', str(e))
    import sys
    sys.exit(1)
"@

# Save to temp file
$testScript | Out-File -FilePath "test_import.py" -Encoding utf8

# Run the test
$testResult = & .\.venv\Scripts\python.exe test_import.py 2>&1
$exitCode = $LASTEXITCODE

# Clean up temp file
Remove-Item "test_import.py" -ErrorAction SilentlyContinue

if ($exitCode -eq 0 -and $testResult -match "OK") {
    Write-Host "   ✓ Flask app loads without errors" -ForegroundColor Green
} else {
    Write-Host "   ✗ Flask app has errors:" -ForegroundColor Red
    Write-Host "   $testResult" -ForegroundColor Red
    Write-Host "`n   Restoring backups..." -ForegroundColor Yellow
    if (Test-Path "app.py.backup") {
        Move-Item "app.py.backup" "app.py" -Force
    }
    if (Test-Path "templates\blog_post.html.backup") {
        Move-Item "templates\blog_post.html.backup" "templates\blog_post.html" -Force
    }
    exit 1
}

# Step 4: Instructions
Write-Host "`n✅ SEO Enhancements Activated!`n" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Test locally:" -ForegroundColor White
Write-Host "   flask run" -ForegroundColor Gray
Write-Host "   Open: http://127.0.0.1:5000`n" -ForegroundColor Gray
Write-Host "2. Check a blog post and view source (Ctrl+U):" -ForegroundColor White
Write-Host "   - Look for BreadcrumbList schema" -ForegroundColor Gray
Write-Host "   - Check meta description length (150-160 chars)" -ForegroundColor Gray
Write-Host "   - Verify OG image is full URL`n" -ForegroundColor Gray
Write-Host "3. Freeze and deploy:" -ForegroundColor White
Write-Host "   python freeze.py" -ForegroundColor Gray
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "   git commit -m `"Activate SEO enhancements: breadcrumbs, meta, schema`"" -ForegroundColor Gray
Write-Host "   git push`n" -ForegroundColor Gray

Write-Host "📖 Read SEO_IMPLEMENTATION_GUIDE.md for validation steps`n" -ForegroundColor Cyan
