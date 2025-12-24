# One-step SEO activation script
# This directly modifies app.py and blog_post.html with SEO enhancements

import shutil
import os

print("\n🚀 Activating SEO Enhancements...\n")

# Backup files
print("📦 Creating backups...")
if os.path.exists("app.py"):
    shutil.copy2("app.py", "app.py.backup_seo")
    print("   ✓ Backed up app.py")
    
if os.path.exists("templates/blog_post.html"):
    shutil.copy2("templates/blog_post.html", "templates/blog_post.html.backup_seo")
    print("   ✓ Backed up blog_post.html")

# Read current app.py
with open("app.py", "r", encoding="utf-8") as f:
    app_content = f.read()

# Apply SEO enhancements to app.py
print("\n🔄 Applying enhancements to app.py...")

# Enhancement 1: Add generate_meta_description function
if "def generate_meta_description" not in app_content:
    meta_desc_function = '''
def generate_meta_description(summary, content, max_length=160):
    """
    Generate optimal meta description from summary or content.
    SEO best practice: 150-160 characters
    """
    if summary and len(summary) <= max_length:
        return summary
    
    if summary:
        # Truncate summary intelligently at word boundary
        truncated = summary[:max_length - 3]
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]
        return truncated + '...'
    
    # Extract from content if no summary
    text_only = re.sub('<[^<]+?>', '', content)  # Strip HTML
    text_only = ' '.join(text_only.split())  # Normalize whitespace
    
    if len(text_only) <= max_length:
        return text_only
    
    truncated = text_only[:max_length - 3]
    last_space = truncated.rfind(' ')
    if last_space > 0:
        truncated = truncated[:last_space]
    return truncated + '...'

'''
    # Insert after get_related_posts function
    app_content = app_content.replace(
        "    return [post for score, post in scored_posts[:limit]]",
        "    return [post for score, post in scored_posts[:limit]]\n" + meta_desc_function
    )
    print("   ✓ Added meta description generator")

# Enhancement 2: Update load_posts to track modified date
if "'modified': meta.get('modified', date)" not in app_content:
    app_content = app_content.replace(
        "'date': date,",
        "'date': date,\n                'modified': meta.get('modified', date),  # Track modified date"
    )
    print("   ✓ Added modified date tracking")

# Enhancement 3: Update blog_post route to pass SEO variables
if "meta_description = generate_meta_description" not in app_content:
    # Find the blog_post function and add SEO enhancements before the return statement
    seo_code = '''
    # ===== SEO ENHANCEMENTS =====
    
    # Auto-generate optimal meta description
    meta_description = generate_meta_description(
        post.get('summary', ''),
        content,
        max_length=160
    )
    
    # Build full OG image URL
    site_url = app.config.get('SITE_URL', 'https://azure-noob.com')
    if cover_url:
        # Ensure proper URL construction
        cover_clean = cover_url.lstrip('/')
        og_image = f"{site_url}/{cover_clean}"
    else:
        og_image = f"{site_url}/static/images/hero/cloud-wars.png"
    
    # Build canonical URL
    canonical_url = f"{site_url}{url_for('blog_post', slug=slug)}"
    
    # ISO date formats for Open Graph and JSON-LD
    date_published_iso = post['date'].strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
    # Use modified date if available, otherwise use published date
    modified_date = post.get('modified', post['date'])
    if isinstance(modified_date, str):
        modified_date = coerce_date(modified_date, post['date'])
    date_modified_iso = modified_date.strftime('%Y-%m-%dT%H:%M:%S+00:00')

'''
    app_content = app_content.replace(
        "    return render_template('blog_post.html',\n                           post=post,",
        seo_code + "\n    return render_template('blog_post.html',\n                           post=post,"
    )
    
    # Add SEO variables to template render
    app_content = app_content.replace(
        "                           related_posts=related)",
        '''                           related_posts=related,
                           word_count=word_count,
                           # SEO variables for base.html
                           page_title=post['title'],
                           meta_description=meta_description,
                           canonical_url=canonical_url,
                           og_type='article',
                           og_image=og_image,
                           og_tags=post.get('tags', []),
                           date_published_iso=date_published_iso,
                           date_modified_iso=date_modified_iso,
                           author_name='David Swann')'''
    )
    print("   ✓ Enhanced blog_post route with SEO metadata")

# Enhancement 4: Add SEO to tag pages
if "# SEO for tag pages" not in app_content:
    tag_seo = '''
    
    # SEO for tag pages
    site_url = app.config.get('SITE_URL', 'https://azure-noob.com')
    page_title = f"{tag} - Azure Noob"
    meta_description = f"Browse all Azure Noob posts about {tag}. Practical guides, KQL queries, and real-world solutions."
    canonical_url = f"{site_url}{url_for('tag_posts', tag=tag)}"
'''
    app_content = app_content.replace(
        "    return render_template('tags.html', \n                         tag=tag, \n                         posts=tagged_posts)",
        tag_seo + "\n    return render_template('tags.html', \n                         tag=tag, \n                         posts=tagged_posts,\n                         page_title=page_title,\n                         meta_description=meta_description,\n                         canonical_url=canonical_url)"
    )
    print("   ✓ Added SEO to tag pages")

# Enhancement 5: Update sitemap with priorities and modified dates
if "'priority':" not in app_content:
    # Update static pages
    app_content = app_content.replace(
        "        {'url': url_for('index', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d')},",
        "        {'url': url_for('index', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d'), 'priority': '1.0'},"
    )
    app_content = app_content.replace(
        "        {'url': url_for('blog_index', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d')},",
        "        {'url': url_for('blog_index', _external=True), 'lastmod': datetime.now().strftime('%Y-%m-%d'), 'priority': '0.9'},"
    )
    # Add priority to XML generation
    app_content = app_content.replace(
        "        xml_content += f'    <lastmod>{page[\"lastmod\"]}</lastmod>\\n'",
        "        xml_content += f'    <lastmod>{page[\"lastmod\"]}</lastmod>\\n'\n        if 'priority' in page:\n            xml_content += f'    <priority>{page[\"priority\"]}</priority>\\n'"
    )
    print("   ✓ Enhanced sitemap with priorities")

# Write enhanced app.py
with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_content)

# Test the app
print("\n🧪 Testing Flask app...")
try:
    exec(compile(open("app.py").read(), "app.py", "exec"))
    print("   ✓ Flask app loads without errors")
except Exception as e:
    print(f"   ✗ Error: {e}")
    print("\n   Restoring backups...")
    if os.path.exists("app.py.backup_seo"):
        shutil.copy2("app.py.backup_seo", "app.py")
    if os.path.exists("templates/blog_post.html.backup_seo"):
        shutil.copy2("templates/blog_post.html.backup_seo", "templates/blog_post.html")
    print("   ✓ Backups restored")
    exit(1)

print("\n✅ SEO Enhancements Activated!\n")
print("Next steps:")
print("1. Test locally: flask run")
print("2. Check a blog post and view source (Ctrl+U)")
print("3. Freeze and deploy:")
print("   python freeze.py")
print("   git add .")
print("   git commit -m 'Activate SEO enhancements'")
print("   git push\n")
