# publish.ps1 - One-command publish for Azure Noob Blog
# Usage: .\publish.ps1 [-Message "custom commit message"]
# Usage: .\publish.ps1 -Quick   (skip freeze, just commit + push)

param(
    [string]$Message = "",
    [switch]$Quick
)

Write-Host ""
Write-Host "==============================" -ForegroundColor Cyan
Write-Host "  AZURE NOOB - PUBLISH" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

$repoRoot = $PSScriptRoot
if (-not $repoRoot) { $repoRoot = Get-Location }
Set-Location $repoRoot

# Step 1: Find the most recently modified post for auto-commit message
$latestPost = Get-ChildItem -Path "posts\*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$postTitle = ""
if ($latestPost) {
    $content = Get-Content $latestPost.FullName -Raw
    if ($content -match 'title:\s*"([^"]+)"') {
        $postTitle = $Matches[1]
    } elseif ($content -match "title:\s*'([^']+)'") {
        $postTitle = $Matches[1]
    } elseif ($content -match 'title:\s*(.+)') {
        $postTitle = $Matches[1].Trim()
    }
    Write-Host "`nLatest post: $($latestPost.Name)" -ForegroundColor Gray
    if ($postTitle) {
        Write-Host "Title: $postTitle" -ForegroundColor Gray
    }
}

# Step 2: Freeze the site (unless -Quick)
if (-not $Quick) {
    Write-Host "`n[1/4] Freezing site..." -ForegroundColor Yellow
    & .\.venv\Scripts\python.exe .\freeze.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`nFREEZE FAILED - aborting publish" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "`n[1/4] Skipping freeze (-Quick mode)" -ForegroundColor Gray
}

# Step 3: Stage ALL publishable files
Write-Host "`n[2/4] Staging files..." -ForegroundColor Yellow
git add `
    posts `
    docs `
    templates `
    static `
    app.py `
    freeze.py `
    hubs_config.py `
    requirements.txt `
    config `
    schema `
    tools `
    archives `
    scripts `
    .gitignore `
    CNAME `
    robots.txt `
    sitemap.xml `
    README.md `
    publish.ps1 `
    2>$null

# Step 4: Build commit message
if (-not $Message) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    if ($postTitle) {
        $Message = "publish: $postTitle"
    } else {
        # Check what changed for smarter message
        $changed = git diff --cached --name-only 2>$null
        if ($changed -match "templates/") {
            $Message = "update: template changes $timestamp"
        } elseif ($changed -match "static/styles") {
            $Message = "update: styling changes $timestamp"
        } elseif ($changed -match "app.py|freeze.py") {
            $Message = "update: build system $timestamp"
        } else {
            $Message = "publish: site update $timestamp"
        }
    }
}

# Step 5: Commit
Write-Host "`n[3/4] Committing: $Message" -ForegroundColor Yellow
git commit -m $Message

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nNothing to commit (no changes detected)" -ForegroundColor Gray
    exit 0
}

# Step 6: Push
Write-Host "`n[4/4] Pushing to GitHub..." -ForegroundColor Yellow
git push

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nPUSH FAILED - check your connection" -ForegroundColor Red
    exit 1
}

Write-Host "`n==============================" -ForegroundColor Green
Write-Host "  PUBLISHED SUCCESSFULLY" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green
Write-Host "Live at: https://azure-noob.com" -ForegroundColor Gray
Write-Host ""
