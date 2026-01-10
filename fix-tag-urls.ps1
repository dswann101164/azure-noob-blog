# GSC 404 Fix - Tag URL Slugification
# This patches app.py to fix tag URL issues causing 67 of 79 404s

# Backup current app.py
Copy-Item "app.py" "app.py.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')" -Force
Write-Host "✓ Backed up app.py" -ForegroundColor Green

# Read current app.py
$content = Get-Content "app.py" -Raw

# Add slugify function after the existing helper functions (around line 130)
$slugify_function = @'

def slugify_tag(tag):
    """
    Convert tag names to URL-safe slugs.
    Examples:
        'Hybrid Cloud' -> 'hybrid-cloud'
        'DNS Resolver' -> 'dns-resolver'
        'Azure' -> 'azure'
    """
    return tag.lower().replace(' ', '-').replace(',', '').strip()

'@

# Find insertion point (after generate_meta_description function)
$insert_point = $content.IndexOf("def load_faq_schema")
if ($insert_point -gt 0) {
    $content = $content.Insert($insert_point, $slugify_function)
    Write-Host "✓ Added slugify_tag() function" -ForegroundColor Green
}

# Fix get_all_tags() to return slugified versions
$old_get_all_tags = @'
def get_all_tags():
    """Get all unique tags from posts."""
    posts = load_posts()
    tags = set()
    for post in posts:
        tags.update(post['tags'])
    return sorted(tags)
'@

$new_get_all_tags = @'
def get_all_tags():
    """Get all unique tags from posts."""
    posts = load_posts()
    tags = set()
    for post in posts:
        # Slugify tags to ensure URL-safe versions
        tags.update([slugify_tag(tag) for tag in post['tags']])
    return sorted(tags)
'@

$content = $content.Replace($old_get_all_tags, $new_get_all_tags)
Write-Host "✓ Updated get_all_tags() to use slugs" -ForegroundColor Green

# Fix tag_posts route to handle slug lookup
$old_tag_posts = @'
@app.route('/tags/<tag>/')
def tag_posts(tag):
    posts = load_posts()
    tagged_posts = [p for p in posts if tag in p['tags']]
    
    site_url = app.config.get('SITE_URL', 'https://azure-noob.com')
    # Build canonical URL without URL encoding (spaces should remain as spaces)
    canonical_url = f"{site_url}/tags/{tag}"
    
    return render_template('tags.html', 
                         tag=tag, 
                         posts=tagged_posts,
                         canonical_url=canonical_url,
                         page_title=f'{tag} - Azure Noob',
                         meta_description=f'Azure tutorials and guides about {tag}.')
'@

$new_tag_posts = @'
@app.route('/tags/<tag>/')
def tag_posts(tag):
    posts = load_posts()
    # Match posts by slugified tag
    tag_slug = slugify_tag(tag)
    tagged_posts = [p for p in posts if any(slugify_tag(t) == tag_slug for t in p['tags'])]
    
    # Find original tag name (with proper casing) for display
    original_tag = tag
    for post in tagged_posts:
        for t in post['tags']:
            if slugify_tag(t) == tag_slug:
                original_tag = t
                break
    
    site_url = app.config.get('SITE_URL', 'https://azure-noob.com')
    canonical_url = f"{site_url}/tags/{tag_slug}/"
    
    return render_template('tags.html', 
                         tag=original_tag,  # Display name
                         tag_slug=tag_slug,  # URL slug
                         posts=tagged_posts,
                         canonical_url=canonical_url,
                         page_title=f'{original_tag} - Azure Noob',
                         meta_description=f'Azure tutorials and guides about {original_tag}.')
'@

$content = $content.Replace($old_tag_posts, $new_tag_posts)
Write-Host "✓ Updated tag_posts() route" -ForegroundColor Green

# Add redirects for old tag URLs with spaces
$redirect_section = @'
    
    # TAG URL REDIRECTS: Fix old URLs with spaces/mixed case
    if '/tags/' in path:
        # Extract tag from path
        tag_match = re.match(r'/tags/([^/]+)/?$', path)
        if tag_match:
            tag_from_url = tag_match.group(1)
            tag_slugified = slugify_tag(unquote(tag_from_url))
            
            # If the URL tag doesn't match the slugified version, redirect
            if tag_from_url != tag_slugified:
                return redirect(f'/tags/{tag_slugified}/', code=301)
'@

# Insert before the trailing slash check
$trailing_slash_line = "    # ADD trailing slash if missing (permanent 301)"
$content = $content.Replace($trailing_slash_line, $redirect_section + "`n" + $trailing_slash_line)
Write-Host "✓ Added tag URL redirect logic" -ForegroundColor Green

# Add unquote import
$content = $content.Replace("from urllib.parse import quote", "from urllib.parse import quote, unquote")
Write-Host "✓ Added unquote import" -ForegroundColor Green

# Save fixed app.py
Set-Content "app.py" $content -NoNewline
Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "FIX COMPLETE" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""
Write-Host "Changes made:" -ForegroundColor Yellow
Write-Host "  1. Added slugify_tag() function" -ForegroundColor White
Write-Host "  2. Updated get_all_tags() to return URL-safe slugs" -ForegroundColor White
Write-Host "  3. Modified tag_posts() to handle slug matching" -ForegroundColor White
Write-Host "  4. Added 301 redirects for old tag URLs with spaces" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Test locally: flask run" -ForegroundColor White
Write-Host "  2. Visit http://127.0.0.1:5000/tags/" -ForegroundColor White
Write-Host "  3. If OK, freeze site: python freeze.py" -ForegroundColor White
Write-Host "  4. Push to GitHub" -ForegroundColor White
Write-Host ""
Write-Host "This will fix 67 of 79 404s (85%)" -ForegroundColor Green
Write-Host ""
