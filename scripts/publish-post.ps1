# publish-post.ps1 - Azure Noob Publishing Pipeline
# Enhanced with SEO validation and error handling

param(
    [switch]$SkipValidation = $false
)

$ErrorActionPreference = "Stop"

Write-Host "`n" -NoNewline
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Azure Noob Publishing Pipeline" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check we're in the right directory
if (-not (Test-Path "posts")) {
    Write-Host "❌ Error: posts/ directory not found" -ForegroundColor Red
    Write-Host "   Run this script from your blog root directory" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path ".venv")) {
    Write-Host "❌ Error: .venv not found" -ForegroundColor Red
    Write-Host "   Run: python -m venv .venv first" -ForegroundColor Yellow
    exit 1
}

# Step 1: SEO Validation
if (-not $SkipValidation) {
    Write-Host "[1/3] Validating SEO..." -ForegroundColor Yellow
    Write-Host "--------------------------------------" -ForegroundColor DarkGray
    
    .\.venv\Scripts\python.exe .\scripts\validate-seo.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n❌ SEO validation failed. Fix issues above before publishing." -ForegroundColor Red
        Write-Host "   Or run with -SkipValidation flag to bypass (not recommended)" -ForegroundColor Yellow
        exit 1
    }
    Write-Host ""
} else {
    Write-Host "[1/3] Skipping SEO validation (forced)" -ForegroundColor Yellow
    Write-Host ""
}

# Step 2: Freeze Site
Write-Host "[2/3] Freezing static site..." -ForegroundColor Yellow
Write-Host "--------------------------------------" -ForegroundColor DarkGray

.\.venv\Scripts\python.exe .\freeze.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Site freeze failed. Check freeze.py output above." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Site frozen to docs/" -ForegroundColor Green
Write-Host ""

# Step 3: Git Commit and Push
Write-Host "[3/3] Publishing to GitHub..." -ForegroundColor Yellow
Write-Host "--------------------------------------" -ForegroundColor DarkGray

# Get the most recently modified post for commit message
$latestPost = Get-ChildItem -Path "posts\*.md" | 
              Sort-Object LastWriteTime -Descending | 
              Select-Object -First 1

if ($latestPost) {
    $postSlug = $latestPost.BaseName -replace '^\d{4}-\d{2}-\d{2}-', ''
    $commitMsg = "Publish: $postSlug"
} else {
    $commitMsg = "Update site: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
}

# Stage files
git add posts docs static\images\hero

# Check if there are changes to commit
$status = git status --porcelain
if (-not $status) {
    Write-Host "⚠️  No changes to publish" -ForegroundColor Yellow
    exit 0
}

# Commit and push
git commit -m $commitMsg
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Git commit failed" -ForegroundColor Red
    exit 1
}

git push
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Git push failed" -ForegroundColor Red
    Write-Host "   Run 'git push' manually to retry" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Pushed to GitHub" -ForegroundColor Green
Write-Host ""

# Success summary
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✓ PUBLISHED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Site will be live in ~60 seconds:" -ForegroundColor Cyan
Write-Host "   https://azure-noob.com" -ForegroundColor White
Write-Host ""
Write-Host "📱 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Tweet the link (30 seconds)" -ForegroundColor White
Write-Host "   2. Check GitHub Actions for Google indexing" -ForegroundColor White
Write-Host ""
