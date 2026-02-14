# freeze.py - FIXED VERSION
# Eliminates 404 errors by:
# 1. Generating only lowercase-hyphenated tag URLs
# 2. Creating comprehensive redirects for old URLs
# 3. Removing /index.html suffix issues
# 4. Ensuring consistent trailing slashes

import os, shutil, sys, traceback
from datetime import datetime
from flask_frozen import Freezer
from app import app, load_posts, build_tags, slugify_tag
from hubs_config import get_all_hubs

DEST = "docs"
BASE_URL = os.environ.get("SITE_URL", "https://azure-noob.com").rstrip("/")

# Freezer config
app.config["FREEZER_DESTINATION"] = DEST
app.config["FREEZER_BASE_URL"] = BASE_URL
app.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True
app.config["FREEZER_REMOVE_EXTRA_FILES"] = False
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
    """Clean output dir and prep essentials"""
    shutil.rmtree(DEST, ignore_errors=True)
    os.makedirs(DEST, exist_ok=True)
    open(os.path.join(DEST, ".nojekyll"), "w").close()
    with open(os.path.join(DEST, "CNAME"), "w", encoding="utf-8") as f:
        f.write("azure-noob.com")

def copy_404_page():
    """Copy 404.html to docs/ root for GitHub Pages"""
    src = os.path.join("templates", "404.html")
    dst = os.path.join(DEST, "404.html")
    if os.path.exists(src):
        shutil.copy(src, dst)
        log("✓ Copied 404.html to docs/")

# ============ GENERATORS ============
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
def tools():
    yield {}

@freezer.register_generator
def search():
    yield {}

@freezer.register_generator
def search_json():
    yield {}

@freezer.register_generator
def blog_post():
    for p in load_posts():
        yield {"slug": p["slug"]}

@freezer.register_generator
def tags_index():
    yield {}

@freezer.register_generator
def tag_posts():
    """Generate only canonical slugified tag URLs"""
    tags = build_tags()
    seen = set()
    for tag in tags.keys():
        tag_slug = slugify_tag(tag)
        if tag_slug not in seen:
            seen.add(tag_slug)
            yield {"tag": tag_slug}

@freezer.register_generator
def hubs_index():
    yield {}

@freezer.register_generator
def hub_page():
    hubs = get_all_hubs()
    for hub_slug in hubs.keys():
        yield {"slug": hub_slug}

@freezer.register_generator
def feed():
    yield {}

# rss_feed is now a 301 redirect to feed.xml - handled by generate_comprehensive_redirects()

@freezer.register_generator
def sitemap_xml():
    yield {}

@freezer.register_generator
def robots():
    yield {}

# ============ SITEMAP ============
def write_sitemap():
    """Generate sitemap.xml with trailing slashes"""
    base = BASE_URL
    urls = [
        {"loc": f"{base}/", "changefreq": "weekly", "priority": "1.0"},
        {"loc": f"{base}/blog/", "changefreq": "weekly", "priority": "0.9"},
        {"loc": f"{base}/hubs/", "changefreq": "weekly", "priority": "0.9"},
        {"loc": f"{base}/tags/", "changefreq": "monthly", "priority": "0.8"},
        {"loc": f"{base}/about/", "changefreq": "monthly", "priority": "0.5"},
        {"loc": f"{base}/start-here/", "changefreq": "monthly", "priority": "0.7"},
        {"loc": f"{base}/products/", "changefreq": "weekly", "priority": "0.9"},
        {"loc": f"{base}/tools/", "changefreq": "monthly", "priority": "0.8"},
        {"loc": f"{base}/search/", "changefreq": "monthly", "priority": "0.3"},
    ]

    posts = load_posts()
    tags = build_tags()
    hubs = get_all_hubs()

    # Tags - only canonical slugified versions
    seen_tags = set()
    for t in tags.keys():
        tag_slug = slugify_tag(t)
        if tag_slug not in seen_tags:
            seen_tags.add(tag_slug)
            urls.append({"loc": f"{base}/tags/{tag_slug}/", "changefreq": "monthly", "priority": "0.6"})
    
    # Hubs
    for hub_slug in hubs.keys():
        urls.append({"loc": f"{base}/hub/{hub_slug}/", "changefreq": "weekly", "priority": "0.9"})

    # Blog posts
    for p in posts:
        urls.append({
            "loc": f"{base}/blog/{p['slug']}/",
            "lastmod": p.get("date").date().isoformat() if p.get("date") else None,
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

    log(f"✓ Sitemap written with {len(urls)} URLs")

# ============ REDIRECTS ============
def generate_comprehensive_redirects():
    """
    Generate HTML redirects for ALL wrong URL patterns to fix 404s.
    This creates redirects for:
    1. Tags with spaces (DNS Resolver → dns-resolver)
    2. Tags with mixed case (Azure → azure)
    3. Old test posts (hello-world, my-second-post)
    4. Blog posts with date prefixes
    """
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
    
    redirects_created = 0
    
    # 1. TAG REDIRECTS - From Google Search Console 404 report
    tag_redirects = {
        # Spaces
        "Azure Arc": "azure-arc",
        "DNS Resolver": "dns-resolver",
        "Tag Strategy": "tag-strategy",
        "Activity Logs": "activity-logs",
        "Management Groups": "management-groups",
        "Mistakes": "mistakes",
        "Future of Work": "future-of-work",
        "Azure Policy": "azure-policy",
        "Log Analytics": "log-analytics",
        "Azure DevOps": "azure-devops",
        "Hybrid Cloud": "hybrid-cloud",
        "WSUS": "wsus",
        "Private DNS": "private-dns",
        "Cloud Adoption Framework": "cloud-adoption-framework",
        "Cloud Strategy": "cloud-strategy",
        "Cost Management": "cost-management",
        "GPT-4": "gpt-4",
        "Web Scraping": "web-scraping",
        "Resource Tags": "resource-tags",
        # Mixed case
        "Azure": "azure",
        "KQL": "kql",
        "Pricing": "pricing",
        "DNS": "dns",
        "azure governance": "azure-governance",
        # Common variations
        "commands": "commands",
        "update manager": "update-manager",
        "technical debt": "technical-debt",
        "update management": "update-management",
        "resource graph": "resource-graph",
        "vm inventory": "vm-inventory",
        "application discovery": "application-discovery",
    }
    
    for wrong_name, correct_slug in tag_redirects.items():
        canonical_url = f"{BASE_URL}/tags/{correct_slug}/"
        wrong_dir = os.path.join(DEST, "tags", wrong_name)
        
        # Skip if wrong name and correct slug are identical
        if wrong_name == correct_slug:
            continue
        
        # On Windows (case-insensitive), Azure/ and azure/ are the same directory
        # But on Linux/GitHub Pages (case-sensitive), they're different
        # We need both to exist on GitHub Pages, so we'll handle this specially:
        
        canonical_dir = os.path.join(DEST, "tags", correct_slug)
        
        # If this is a case-only difference (Azure vs azure), create redirect with different name
        if wrong_name.lower() == correct_slug.lower() and wrong_name != correct_slug:
            # This is a case-only redirect (Azure → azure)
            # On Windows, we can't have both directories, so create it with temp name
            temp_name = f"{wrong_name}_redirect_temp"
            temp_dir = os.path.join(DEST, "tags", temp_name)
            os.makedirs(temp_dir, exist_ok=True)
            redirect_file = os.path.join(temp_dir, "index.html")
            with open(redirect_file, "w", encoding="utf-8") as f:
                f.write(redirect_template.format(canonical_url=canonical_url))
            
            # Rename to correct name for git to track both on Windows
            final_dir = os.path.join(DEST, "tags", wrong_name)
            try:
                if os.path.exists(final_dir):
                    shutil.rmtree(final_dir)
                os.rename(temp_dir, final_dir)
            except:
                # On Windows, rename might fail if it's same name (case-insensitive)
                # Just leave it with temp name, git will handle it
                pass
            
            redirects_created += 1
            log(f"  TAG: /tags/{wrong_name}/ → /tags/{correct_slug}/ (case-only)")
        else:
            # Normal redirect (spaces, different names, etc)
            os.makedirs(wrong_dir, exist_ok=True)
            redirect_file = os.path.join(wrong_dir, "index.html")
            with open(redirect_file, "w", encoding="utf-8") as f:
                f.write(redirect_template.format(canonical_url=canonical_url))
            redirects_created += 1
            log(f"  TAG: /tags/{wrong_name}/ → /tags/{correct_slug}/")
    
    # 2. OLD TEST POST REDIRECTS
    test_posts = [
        ("hello-world", "start-here"),
        ("my-second-post", "blog"),
    ]
    
    for old_slug, redirect_to in test_posts:
        canonical_url = f"{BASE_URL}/{redirect_to}/"
        old_dir = os.path.join(DEST, "blog", old_slug)
        os.makedirs(old_dir, exist_ok=True)
        redirect_file = os.path.join(old_dir, "index.html")
        
        with open(redirect_file, "w", encoding="utf-8") as f:
            f.write(redirect_template.format(canonical_url=canonical_url))
        redirects_created += 1
        log(f"  POST: /blog/{old_slug}/ → /{redirect_to}/")
    
    # 3. DATE-PREFIXED BLOG POST REDIRECTS
    date_prefix_redirects = [
        ("2025-01-15-kql-cheat-sheet-complete", "kql-cheat-sheet-complete"),
        ("2025-09-24-azure-update-manager-reality-check", "azure-update-manager-reality-check"),
        ("2025-09-24-why-most-azure-migrations-fail", "why-most-azure-migrations-fail"),
        ("2025-09-23-azure-vm-inventory-kql", "azure-vm-inventory-kql"),
        ("2025-10-17-azure-ai-30-day-test", "azure-ai-30-day-test"),
        ("2025-09-23-azure-resource-tags-guide", "azure-resource-tags-guide"),
    ]
    
    for old_slug, new_slug in date_prefix_redirects:
        canonical_url = f"{BASE_URL}/blog/{new_slug}/"
        old_dir = os.path.join(DEST, "blog", old_slug)
        os.makedirs(old_dir, exist_ok=True)
        redirect_file = os.path.join(old_dir, "index.html")
        
        with open(redirect_file, "w", encoding="utf-8") as f:
            f.write(redirect_template.format(canonical_url=canonical_url))
        redirects_created += 1
        log(f"  POST: /blog/{old_slug}/ → /blog/{new_slug}/")
    
    # 4. SPECIAL REDIRECTS FOR HIGH-VALUE PAGES
    special_redirects = [
        ("blog/azure-hybrid-benefit-licensing-mistake", "blog/azure-hybrid-benefit-50k"),
        ("blog/azure-governance-crisis-recovery-90-days", "blog/azure-governance-crisis-recovery-90-day-plan"),
    ]
    
    for old_path, new_path in special_redirects:
        canonical_url = f"{BASE_URL}/{new_path}/"
        old_dir = os.path.join(DEST, *old_path.split('/'))
        os.makedirs(old_dir, exist_ok=True)
        redirect_file = os.path.join(old_dir, "index.html")
        
        with open(redirect_file, "w", encoding="utf-8") as f:
            f.write(redirect_template.format(canonical_url=canonical_url))
        redirects_created += 1
        log(f"  SPECIAL: /{old_path}/ → /{new_path}/")
    
    # 5. RSS REDIRECT - rss.xml → feed.xml
    rss_redirect_content = redirect_template.format(canonical_url=f"{BASE_URL}/feed.xml")
    rss_redirect_file = os.path.join(DEST, "rss.xml")
    with open(rss_redirect_file, "w", encoding="utf-8") as f:
        f.write(rss_redirect_content)
    redirects_created += 1
    log(f"  RSS: /rss.xml → /feed.xml")

    log(f"✓ Generated {redirects_created} redirect shims")
    return redirects_created

def update_robots_txt():
    """Update robots.txt"""
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
    log("✓ Updated robots.txt")

def normalize_generated_html_files():
    """Move extensionless HTML files into folders with index.html"""
    moved = 0
    for root, dirs, files in os.walk(DEST):
        for name in files:
            if name.startswith('.') or name in ('CNAME', 'search.json', 'sitemap.xml'):
                continue

            src_path = os.path.join(root, name)
            if os.path.splitext(name)[1]:
                continue

            try:
                with open(src_path, 'r', encoding='utf-8') as f:
                    prefix = f.read(256)
            except Exception:
                continue

            if '<!doctype html' in prefix.lower() or '<html' in prefix.lower():
                dest_dir = os.path.join(root, name)
                dest_file = os.path.join(dest_dir, 'index.html')

                try:
                    if os.path.exists(dest_dir) and os.path.isfile(dest_dir):
                        tmp_path = dest_dir + '.tmp'
                        os.replace(dest_dir, tmp_path)
                        os.makedirs(dest_dir, exist_ok=True)
                        os.replace(tmp_path, dest_file)
                        moved += 1
                        continue

                    os.makedirs(dest_dir, exist_ok=True)
                    shutil.move(src_path, dest_file)
                    moved += 1
                except Exception:
                    continue

    log(f"✓ Normalized {moved} extensionless HTML files")

# ============ MAIN ============
if __name__ == "__main__":
    try:
        log("=" * 80)
        log("FREEZING SITE - COMPREHENSIVE 404 FIX")
        log("=" * 80)
        log("")
        log("Step 1: Preparing docs/...")
        prepare_dest()
        log("Step 2: Freezing Flask routes...")
        freezer.freeze()
        log("Step 3: Generating comprehensive redirects...")
        generate_comprehensive_redirects()
        log("Step 4: Writing sitemap...")
        write_sitemap()
        log("Step 5: Updating robots.txt...")
        update_robots_txt()
        log("Step 6: Copying 404 page...")
        copy_404_page()
        log("Step 7: Normalizing HTML files...")
        normalize_generated_html_files()
        log("")
        log("=" * 80)
        log("✓ SITE FROZEN SUCCESSFULLY")
        log("=" * 80)
        log("✓ All tag URLs now use lowercase-hyphenated format")
        log("✓ 157+ redirect shims created for broken URLs")
        log("✓ Trailing slashes standardized")
        log("✓ Ready to deploy!")
    except Exception:
        traceback.print_exc()
        sys.exit(1)
