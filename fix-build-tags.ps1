# Final fix for build_tags() in app.py to use slugified tags
Write-Host "Fixing build_tags() function..." -ForegroundColor Cyan

# Backup
Copy-Item "app.py" "app.py.backup-build-tags-$(Get-Date -Format 'yyyyMMdd-HHmmss')" -Force
Write-Host "✓ Backed up app.py" -ForegroundColor Green

# Read file
$content = Get-Content "app.py" -Raw

# Fix build_tags() to use slugified tags
$old_build_tags = @'
def build_tags():
    """Build tag pages for frozen site generation."""
    tags = get_all_tags()
    posts = load_posts()

    # Group posts by tag
    tag_posts = {}
    for tag in tags:
        tag_posts[tag] = [p for p in posts if tag in p['tags']]

    return tag_posts
'@

$new_build_tags = @'
def build_tags():
    """Build tag pages for frozen site generation."""
    tags = get_all_tags()  # Already returns slugified tags
    posts = load_posts()

    # Group posts by slugified tag
    tag_posts = {}
    for tag_slug in tags:
        # Find all posts that have a tag matching this slug
        tag_posts[tag_slug] = [p for p in posts if any(slugify_tag(t) == tag_slug for t in p['tags'])]

    return tag_posts
'@

$content = $content.Replace($old_build_tags, $new_build_tags)
Write-Host "✓ Fixed build_tags() to use slugified tags" -ForegroundColor Green

# Save
Set-Content "app.py" $content -NoNewline

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Green  
Write-Host "BUILD_TAGS() FIXED" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Green
Write-Host ""
Write-Host "Now freeze.py will only generate slugified tag directories" -ForegroundColor Yellow
Write-Host ""
Write-Host "Run: python freeze.py" -ForegroundColor Cyan
Write-Host ""
