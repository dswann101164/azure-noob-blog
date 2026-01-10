# Fix blog_post.html to slugify tags in URL generation
Write-Host "Fixing blog_post.html..." -ForegroundColor Cyan

# Backup
Copy-Item "templates\blog_post.html" "templates\blog_post.html.backup-tag-url-$(Get-Date -Format 'yyyyMMdd-HHmmss')" -Force
Write-Host "✓ Backed up blog_post.html" -ForegroundColor Green

# Read file
$content = Get-Content "templates\blog_post.html" -Raw

# Fix the tag URL to use slugified version
# Original: <li><a href="{{ url_for('tag_posts', tag=tag) }}" class="tag-badge">{{ tag }}</a></li>
# Fixed: <li><a href="{{ url_for('tag_posts', tag=tag|lower|replace(' ', '-')) }}" class="tag-badge">{{ tag }}</a></li>

$old_pattern = '<li><a href="{{ url_for(''tag_posts'', tag=tag) }}" class="tag-badge">{{ tag }}</a></li>'
$new_pattern = '<li><a href="{{ url_for(''tag_posts'', tag=tag|lower|replace('' '', ''-'')) }}" class="tag-badge">{{ tag }}</a></li>'

$content = $content.Replace($old_pattern, $new_pattern)
Write-Host "✓ Fixed tag URLs in blog_post.html" -ForegroundColor Green

# Save
Set-Content "templates\blog_post.html" $content -NoNewline

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Green  
Write-Host "BLOG_POST.HTML FIXED" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Green
Write-Host ""
Write-Host "Tag URLs now use slugified versions" -ForegroundColor Yellow
Write-Host ""
Write-Host "Run: python freeze.py" -ForegroundColor Cyan
Write-Host ""
