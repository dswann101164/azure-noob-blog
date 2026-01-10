# Fix freeze.py to use slugified tags only
# This prevents duplicate tag directories

Write-Host "Fixing freeze.py..." -ForegroundColor Cyan

# Backup
Copy-Item "freeze.py" "freeze.py.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')" -Force
Write-Host "✓ Backed up freeze.py" -ForegroundColor Green

# Read file
$content = Get-Content "freeze.py" -Raw

# Fix 1: Update import
$content = $content.Replace(
    "from app import app, load_posts, build_tags",
    "from app import app, load_posts, build_tags, slugify_tag"
)
Write-Host "✓ Added slugify_tag import" -ForegroundColor Green

# Fix 2: Update tag_posts generator
$old_generator = @'
@freezer.register_generator
def tag_posts():
    tags = build_tags()
    for tag in tags.keys():
        yield {"tag": tag}
'@

$new_generator = @'
@freezer.register_generator
def tag_posts():
    tags = build_tags()
    # Only yield slugified tag names to avoid duplicates
    seen = set()
    for tag in tags.keys():
        tag_slug = slugify_tag(tag)
        if tag_slug not in seen:
            seen.add(tag_slug)
            yield {"tag": tag_slug}
'@

$content = $content.Replace($old_generator, $new_generator)
Write-Host "✓ Updated tag_posts() generator to use slugs" -ForegroundColor Green

# Fix 3: Update sitemap generation
$old_sitemap = @'
    # Tag pages (WITH trailing slashes)
    for t in tags.keys():
        urls.append({"loc": f"{base}/tags/{t}/", "changefreq": "monthly", "priority": "0.6"})
'@

$new_sitemap = @'
    # Tag pages (WITH trailing slashes) - use slugified versions only
    seen_tags = set()
    for t in tags.keys():
        tag_slug = slugify_tag(t)
        if tag_slug not in seen_tags:
            seen_tags.add(tag_slug)
            urls.append({"loc": f"{base}/tags/{tag_slug}/", "changefreq": "monthly", "priority": "0.6"})
'@

$content = $content.Replace($old_sitemap, $new_sitemap)
Write-Host "✓ Updated sitemap generation to use slugs" -ForegroundColor Green

# Save
Set-Content "freeze.py" $content -NoNewline
Write-Host ""
Write-Host "=" * 80 -ForegroundColor Green
Write-Host "FREEZE.PY FIXED" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Green
Write-Host ""
Write-Host "Changes:" -ForegroundColor Yellow
Write-Host "  1. Added slugify_tag import" -ForegroundColor White
Write-Host "  2. Tag generator now uses slugified versions only" -ForegroundColor White
Write-Host "  3. Sitemap generation deduplicates tags" -ForegroundColor White
Write-Host ""
Write-Host "Next: python freeze.py" -ForegroundColor Yellow
Write-Host ""
