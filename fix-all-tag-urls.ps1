# Fix ALL templates to slugify tags in URL generation
Write-Host "Fixing ALL templates with tag URLs..." -ForegroundColor Cyan

$files = @(
    "templates\blog_post.html",
    "templates\blog_index.html",
    "templates\index.html",
    "templates\blog_post_new.html"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "Processing $file..." -ForegroundColor Yellow
        
        # Backup
        $backupName = $file -replace '\.html$', ".html.backup-tag-fix-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Copy-Item $file $backupName -Force
        
        # Read content
        $content = Get-Content $file -Raw
        
        # Fix: url_for('tag_posts', tag=tag) → url_for('tag_posts', tag=tag|lower|replace(' ', '-'))
        $content = $content -replace "url_for\('tag_posts', tag=tag\)", "url_for('tag_posts', tag=tag|lower|replace(' ', '-'))"
        
        # Save
        Set-Content $file $content -NoNewline
        Write-Host "  ✓ Fixed $file" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Green  
Write-Host "ALL TEMPLATES FIXED" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Green
Write-Host ""
Write-Host "Tag URLs now use slugified versions in ALL templates" -ForegroundColor Yellow
Write-Host ""
Write-Host "Run: python freeze.py" -ForegroundColor Cyan
Write-Host "Then: Get-ChildItem docs\tags\ | Select-Object Name | Select-String -Pattern 'Active Directory|Azure AD'" -ForegroundColor Cyan
Write-Host ""
