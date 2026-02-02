# freeze.py
import os, shutil, sys, traceback
from datetime import datetime
from flask_frozen import Freezer
from app import app, load_posts, build_tags, slugify_tag, slugify_tag
from hubs_config import get_all_hubs   # import hub configuration

DEST = "docs"
BASE_URL = os.environ.get("SITE_URL", "https://azure-noob.com").rstrip("/")

# ---- Freezer config ----
app.config["FREEZER_DESTINATION"] = DEST
app.config["FREEZER_BASE_URL"] = BASE_URL
app.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True
app.config["FREEZER_REMOVE_EXTRA_FILES"] = False
# Use absolute root-relative URLs for static assets so pages under
# nested paths (e.g. /blog/<slug>/) reference `/static/...` instead
# of filesystem-relative paths like "../static/..." which break on
# some static hosts and in-browser asset resolution.
app.config["FREEZER_RELATIVE_URLS"] = False
app.config["FREEZER_DESTINATION_IGNORE"] = ['.git*']
app.config["FREEZER_STATIC_IGNORE"] = []

freezer = Freezer(app)

def log(msg): 
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        print(msg.encode('ascii', errors='replace').decode('ascii'), flush=True)

def prepare_dest():
    # Clean output dir and prep essentials
    shutil.rmtree(DEST, ignore_errors=True)
    os.makedirs(DEST, exist_ok=True)
    # No Jekyll so Pages serves JSON etc. verbatim
    open(os.path.join(DEST, ".nojekyll"), "w").close()
    # Custom domain
    with open(os.path.join(DEST, "CNAME"), "w", encoding="utf-8") as f:
        f.write("azure-noob.com")

def copy_404_page():
    """Copy 404.html to docs/ root for GitHub Pages"""
    src = os.path.join("templates", "404.html")
    dst = os.path.join(DEST, "404.html")
    if os.path.exists(src):
        shutil.copy(src, dst)
        log("✓ Copied 404.html to docs/")
    else:
        log("⚠ Warning: templates/404.html not found")

# ---- Generators for all routes we need to freeze ----
@freezer.register_generator
def index():
    yield {}

@freezer.register_generator
def blog_index():
    yield {}

@freezer.register_generator
def about():
    yield {}

@freezer.register_generator
def start_here():
    yield {}

@freezer.register_generator
def products():
    yield {}

@freezer.register_generator
def search():
    yield {}

@freezer.register_generator
def search_json():
    yield {}

# Blog posts
@freezer.register_generator
def blog_post():
    for p in load_posts():
        yield {"slug": p["slug"]}

# Tags index and each tag page
@freezer.register_generator
def tags_index():
    yield {}

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

# Content Hubs
@freezer.register_generator
def hubs_index():
    yield {}

@freezer.register_generator
def hub_page():
    hubs = get_all_hubs()
    for hub_slug in hubs.keys():
        yield {"slug": hub_slug}

# RSS Feed
@freezer.register_generator
def feed():
    yield {}

# Legacy RSS Feed
@freezer.register_generator
def rss_feed():
    yield {}

# Sitemap
@freezer.register_generator
def sitemap_xml():
    yield {}

# Robots.txt
@freezer.register_generator
def robots():
    yield {}

# Note: 404.html is copied manually via copy_404_page() - error handlers cannot be frozen via URL generation

# ---- Sitemap generation (NO trailing slashes) ----
def _fmt_lastmod(dt):
    try:
        if isinstance(dt, datetime):
            return dt.date().isoformat()
        return datetime.fromisoformat(str(dt)).date().isoformat()
    except Exception:
        return None

def write_sitemap():
    """Generate sitemap.xml with trailing slashes to match GitHub Pages behavior"""
    base = BASE_URL
    urls = [
        {"loc": f"{base}/", "changefreq": "weekly", "priority": "1.0"},
        {"loc": f"{base}/blog/", "changefreq": "weekly", "priority": "0.9"},
        {"loc": f"{base}/hubs/", "changefreq": "weekly", "priority": "0.9"},
        {"loc": f"{base}/tags/", "changefreq": "monthly", "priority": "0.8"},
        {"loc": f"{base}/about/", "changefreq": "monthly", "priority": "0.5"},
        {"loc": f"{base}/start-here/", "changefreq": "monthly", "priority": "0.7"},
        {"loc": f"{base}/products/", "changefreq": "weekly", "priority": "0.9"},
        {"loc": f"{base}/search/", "changefreq": "monthly", "priority": "0.3"},
    ]

    posts = load_posts()
    tags = build_tags()
    hubs = get_all_hubs()

    # Tag pages (WITH trailing slashes) - use slugified versions only
    seen_tags = set()
    for t in tags.keys():
        tag_slug = slugify_tag(t)
        if tag_slug not in seen_tags:
            seen_tags.add(tag_slug)
            urls.append({"loc": f"{base}/tags/{tag_slug}/", "changefreq": "monthly", "priority": "0.6"})
    
    # Hub pages (WITH trailing slashes)
    for hub_slug in hubs.keys():
        urls.append({"loc": f"{base}/hub/{hub_slug}/", "changefreq": "weekly", "priority": "0.9"})

    # Blog posts (WITH trailing slashes)
    for p in posts:
        urls.append({
            "loc": f"{base}/blog/{p['slug']}/",
            "lastmod": _fmt_lastmod(p.get("date")),
            "changefreq": "monthly",
            "priority": "0.7",
        })

    with open(os.path.join(DEST, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write("  <url>\n")
            f.write(f"    <loc>{u['loc']}</loc>\n")
            if u.get("lastmod"): 
                f.write(f"    <lastmod>{u['lastmod']}</lastmod>\n")
            f.write(f"    <changefreq>{u['changefreq']}</changefreq>\n")
            f.write(f"    <priority>{u['priority']}</priority>\n")
            f.write("  </url>\n")
        f.write("</urlset>\n")

    log(f"✓ Sitemap written with {len(urls)} URLs (WITH trailing slashes)")

def remove_trailing_slashes_from_sitemap():
    """DEPRECATED: We now KEEP trailing slashes to match GitHub Pages behavior"""
    pass

def generate_tag_redirects():
    """
    Generate HTML redirect shims for common wrong tag URL patterns.
    
    PROBLEM: External sites link to tags using display names with spaces/caps
    (e.g., /tags/Azure Arc/ instead of /tags/azure-arc/)
    
    SOLUTION: Create redirect HTML files that use meta refresh + JavaScript
    to redirect to the correct canonical URL.
    
    CRITICAL: Only create redirects for non-canonical URLs. Never overwrite
    the canonical tag pages generated by Flask-Frozen.
    """
    posts = load_posts()
    
    # Extract all unique tag display names from posts
    display_names = set()
    for post in posts:
        for tag in post.get('tags', []):
            display_names.add(tag)
    
    redirects_created = 0
    redirect_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex, follow">
  <meta http-equiv="refresh" content="0; url={canonical_url}">
  <link rel="canonical" href="{canonical_url}">
  <title>Redirecting...</title>
  <script>window.location.href = "{canonical_url}";</script>
</head>
<body>
  <p>Redirecting to <a href="{canonical_url}">{canonical_url}</a>...</p>
</body>
</html>"""
    
    for display_name in display_names:
        tag_slug = slugify_tag(display_name)
        
        # CRITICAL: Skip if display name == slug (this is the canonical URL)
        # We must NEVER overwrite canonical tag pages
        if display_name == tag_slug:
            continue
        
        # CRITICAL: Windows filesystems are case-insensitive!
        # Skip if display_name differs only in case from tag_slug
        if display_name.lower() == tag_slug.lower():
            log(f"  SKIP (case-insensitive match): /tags/{display_name}/ == /tags/{tag_slug}/")
            continue
        
        # Generate correct canonical URL
        canonical_url = f"{BASE_URL}/tags/{tag_slug}/"
        
        # CRITICAL: Only create redirect for the non-canonical display name
        # Never touch the canonical slug directory
        wrong_tag_dir = os.path.join(DEST, "tags", display_name)
        canonical_tag_dir = os.path.join(DEST, "tags", tag_slug)
        
        # Verify we're not about to overwrite the canonical page
        if wrong_tag_dir == canonical_tag_dir:
            log(f"  SKIP: Refusing to overwrite canonical page at /tags/{tag_slug}/")
            continue
        
        os.makedirs(wrong_tag_dir, exist_ok=True)
        
        redirect_file = os.path.join(wrong_tag_dir, "index.html")
        with open(redirect_file, "w", encoding="utf-8") as f:
            f.write(redirect_template.format(canonical_url=canonical_url))
        
        redirects_created += 1
        log(f"  Created redirect: /tags/{display_name}/ -> /tags/{tag_slug}/")
    
    # --- Phase 2: title-case shims for slugs missing a display-name shim ---
    # Many posts store tags already in slug form (e.g. "management-groups").
    # Google indexed the Title Case + spaces version from link text or
    # historical crawls.  The loop above only creates shims for tags whose
    # raw frontmatter string differs from the slug, so those Title Case
    # variants never got a shim.  Generate them here.
    all_slugs = set()
    for post in posts:
        for tag in post.get('tags', []):
            all_slugs.add(slugify_tag(tag))
    
    for tag_slug in sorted(all_slugs):
        # "azure-hybrid-benefit" → "Azure Hybrid Benefit"
        pretty_name = tag_slug.replace('-', ' ').title()
        
        # If pretty name equals the slug (single-word lowercase-only edge case), skip
        if pretty_name == tag_slug:
            continue
        
        # CRITICAL: Windows filesystems are case-insensitive!
        # Skip if pretty_name lowercased equals tag_slug (prevents overwriting on Windows)
        if pretty_name.lower() == tag_slug.lower():
            log(f"  SKIP (case-insensitive match): /tags/{pretty_name}/ == /tags/{tag_slug}/")
            continue
        
        # CRITICAL: Verify this is not the canonical slug directory
        shim_dir = os.path.join(DEST, "tags", pretty_name)
        canonical_dir = os.path.join(DEST, "tags", tag_slug)
        
        # Never overwrite canonical tag pages
        if shim_dir == canonical_dir:
            log(f"  SKIP (canonical): /tags/{pretty_name}/")
            continue
        
        # If a shim directory was already created in phase 1, skip
        if os.path.exists(os.path.join(shim_dir, "index.html")):
            log(f"  Skipping (already exists): /tags/{pretty_name}/")
            continue
        
        # Create the redirect shim
        canonical_url = f"{BASE_URL}/tags/{tag_slug}/"
        os.makedirs(shim_dir, exist_ok=True)
        
        redirect_file = os.path.join(shim_dir, "index.html")
        with open(redirect_file, "w", encoding="utf-8") as f:
            f.write(redirect_template.format(canonical_url=canonical_url))
        
        redirects_created += 1
        log(f"  Created redirect: /tags/{pretty_name}/ -> /tags/{tag_slug}/")
    
    log(f"✓ Generated {redirects_created} tag redirect shims (phase 1 + phase 2)")
    return redirects_created

def update_robots_txt():
    """
    Update robots.txt for the site.
    
    NOTE: We do NOT block redirect shim URLs here. Google needs to crawl them
    to discover the redirects. The redirect HTML pages have <meta name="robots" 
    content="noindex, follow"> which tells Google to follow the redirect but 
    not index the redirect page itself. This is the correct approach.
    """
    robots_content = """User-agent: *
Allow: /

# Don't index API endpoint
Disallow: /search.json

# AI crawlers - explicitly allowed for GEO/AEO visibility
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Bytespider
Allow: /

User-agent: CCBot
Allow: /

Sitemap: https://azure-noob.com/sitemap.xml"""
    
    robots_file = os.path.join(DEST, "robots.txt")
    with open(robots_file, "w", encoding="utf-8") as f:
        f.write(robots_content)
    
    log("✓ Updated robots.txt (redirect shims are crawlable)")

def normalize_generated_html_files():
    """Move extensionless HTML files into folders with `index.html`.
    GitHub Pages (and many static hosts) serve `index.html` inside a
    directory. Flask-Frozen sometimes writes files without a .html
    extension; this function converts those into `dir/index.html` so
    the site behaves as expected.
    """
    import io

    moved = 0
    for root, dirs, files in os.walk(DEST):
        for name in files:
            # Skip known special files
            if name.startswith('.') or name in ('CNAME', 'search.json', 'sitemap.xml'):
                continue

            src_path = os.path.join(root, name)
            # If file has an extension, skip
            if os.path.splitext(name)[1]:
                continue

            # Read a small prefix to check if it's HTML
            try:
                with open(src_path, 'r', encoding='utf-8') as f:
                    prefix = f.read(256)
            except Exception:
                continue

            if '<!doctype html' in prefix.lower() or '<html' in prefix.lower():
                dest_dir = os.path.join(root, name)
                dest_file = os.path.join(dest_dir, 'index.html')

                try:
                    # If a file exists at the target dir path, move it aside first
                    if os.path.exists(dest_dir) and os.path.isfile(dest_dir):
                        # Rename the existing file to a temporary path so we can create the directory
                        tmp_path = dest_dir + '.tmp'
                        try:
                            os.replace(dest_dir, tmp_path)
                        except Exception:
                            # If replace fails, skip this file
                            continue

                        # Now create the directory and move the temp file into index.html
                        try:
                            os.makedirs(dest_dir, exist_ok=True)
                            os.replace(tmp_path, dest_file)
                            moved += 1
                            # If the current src_path equals dest_dir (we just moved it), skip further handling
                            continue
                        except Exception:
                            # Attempt to recover by moving temp back
                            try:
                                if os.path.exists(tmp_path) and not os.path.exists(dest_dir):
                                    os.replace(tmp_path, dest_dir)
                            except Exception:
                                pass
                            continue

                    # Normal case: create directory and move the file into index.html
                    os.makedirs(dest_dir, exist_ok=True)
                    try:
                        shutil.move(src_path, dest_file)
                        moved += 1
                    except Exception:
                        # Fallback: copy+remove
                        try:
                            with open(src_path, 'rb') as fsrc, open(dest_file, 'wb') as fdst:
                                fdst.write(fsrc.read())
                            os.remove(src_path)
                            moved += 1
                        except Exception:
                            continue
                except Exception:
                    continue

    log(f"✓ Normalized {moved} extensionless HTML files into directories")

# ---- Entrypoint ----
if __name__ == "__main__":
    try:
        log("Preparing docs/…")
        prepare_dest()
        log("Freezing Flask routes…")
        freezer.freeze()
        log("Generating tag redirect shims…")
        generate_tag_redirects()
        log("Writing sitemap…")
        write_sitemap()
        log("Updating robots.txt…")
        update_robots_txt()
        log("Copying 404 page…")
        copy_404_page()
        log("Normalizing generated HTML files for static hosting…")
        normalize_generated_html_files()
        log("✓ Done! Site frozen to docs/")
        log(f"✓ All URLs standardized (WITH trailing slashes to match GitHub Pages)")
        log(f"✓ Redirect shims created for wrong tag URL patterns")
    except Exception:
        traceback.print_exc()
        sys.exit(1)
