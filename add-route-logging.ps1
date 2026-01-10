# Debug app.py tags_index route to see what it's passing
$content = Get-Content "app.py" -Raw

$old_route = @'
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

$new_route = @'
@app.route('/tags/')
def tags_index():
    all_tags = get_all_tags()  # Returns slugified tags
    posts = load_posts()

    # Group posts by tag and create (tag_slug, count) tuples
    tag_posts = {}
    tags_with_counts = []

    print(f"\n=== TAGS_INDEX ROUTE DEBUG ===")
    print(f"Total slugified tags: {len(all_tags)}")
    
    for tag_slug in all_tags:
        # Match posts by slugified tag comparison
        tag_posts[tag_slug] = [p for p in posts if any(slugify_tag(t) == tag_slug for t in p['tags'])]
        tags_with_counts.append((tag_slug, len(tag_posts[tag_slug])))
    
    # Check what we're passing
    problem_tags = ['Active Directory', 'active-directory', 'Azure AD', 'azure-ad']
    for pt in problem_tags:
        found = any(t == pt for t, c in tags_with_counts)
        if found:
            print(f"  WARNING: Passing '{pt}' to template")
    
    print(f"First 10 tags being passed: {[t for t, c in tags_with_counts[:10]]}")
    print("=== END TAGS_INDEX DEBUG ===\n")

    return render_template('tags_index.html', 
                         tags=tags_with_counts, 
                         tag_posts=tag_posts,
                         canonical_url=get_canonical_url(),
                         page_title='Tags - Azure Noob',
                         meta_description='Browse Azure tutorials by tag.')
'@

$content = $content.Replace($old_route, $new_route)
Set-Content "app.py" $content -NoNewline

Write-Host "Added logging to tags_index() route" -ForegroundColor Green
Write-Host "Run: python freeze.py 2>&1 | Select-String -Pattern 'TAGS_INDEX|WARNING'" -ForegroundColor Cyan
