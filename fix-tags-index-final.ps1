# FINAL FIX: tags_index() must pass slugified tags to template
Write-Host "Fixing tags_index() route..." -ForegroundColor Cyan

# Backup
Copy-Item "app.py" "app.py.backup-tags-index-$(Get-Date -Format 'yyyyMMdd-HHmmss')" -Force
Write-Host "✓ Backed up app.py" -ForegroundColor Green

# Read file
$content = Get-Content "app.py" -Raw

# Fix tags_index() to pass slugified tags and match posts correctly
$old_tags_index = @'
@app.route('/tags/')
def tags_index():
    all_tags = get_all_tags()
    posts = load_posts()

    # Group posts by tag and create (tag, count) tuples
    tag_posts = {}
    tags_with_counts = []

    for tag in all_tags:
        tag_posts[tag] = [p for p in posts if tag in p['tags']]
        tags_with_counts.append((tag, len(tag_posts[tag])))

    return render_template('tags_index.html', 
                         tags=tags_with_counts, 
                         tag_posts=tag_posts,
                         canonical_url=get_canonical_url(),
                         page_title='Tags - Azure Noob',
                         meta_description='Browse Azure tutorials by tag.')
'@

$new_tags_index = @'
@app.route('/tags/')
def tags_index():
    all_tags = get_all_tags()  # Returns slugified tags
    posts = load_posts()

    # Group posts by tag and create (tag_slug, count) tuples
    tag_posts = {}
    tags_with_counts = []

    for tag_slug in all_tags:
        # Match posts by slugified tag comparison
        tag_posts[tag_slug] = [p for p in posts if any(slugify_tag(t) == tag_slug for t in p['tags'])]
        tags_with_counts.append((tag_slug, len(tag_posts[tag_slug])))

    return render_template('tags_index.html', 
                         tags=tags_with_counts, 
                         tag_posts=tag_posts,
                         canonical_url=get_canonical_url(),
                         page_title='Tags - Azure Noob',
                         meta_description='Browse Azure tutorials by tag.')
'@

$content = $content.Replace($old_tags_index, $new_tags_index)
Write-Host "✓ Fixed tags_index() to use slugified tags" -ForegroundColor Green

# Save
Set-Content "app.py" $content -NoNewline

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Green  
Write-Host "TAGS_INDEX() FIXED" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Green
Write-Host ""
Write-Host "Now template will receive slugified tags only" -ForegroundColor Yellow
Write-Host ""
Write-Host "Run: python freeze.py" -ForegroundColor Cyan
Write-Host ""
