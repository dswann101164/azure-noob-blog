# Add logging to freeze.py to see exactly what's being frozen
$content = Get-Content "freeze.py" -Raw

# Add logging after the tag_posts generator
$old_generator = @'
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

$new_generator = @'
@freezer.register_generator
def tag_posts():
    tags = build_tags()
    # Only yield slugified tag names to avoid duplicates
    seen = set()
    print("\n=== TAG_POSTS GENERATOR DEBUG ===")
    for tag in tags.keys():
        tag_slug = slugify_tag(tag)
        if tag_slug not in seen:
            seen.add(tag_slug)
            print(f"  Yielding tag: '{tag_slug}'")
            yield {"tag": tag_slug}
    print("=== END TAG_POSTS GENERATOR ===\n")
'@

$content = $content.Replace($old_generator, $new_generator)
Set-Content "freeze.py" $content -NoNewline

Write-Host "Added debug logging to freeze.py" -ForegroundColor Green
Write-Host "Run: python freeze.py 2>&1 | Select-String -Pattern 'tag'" -ForegroundColor Cyan
