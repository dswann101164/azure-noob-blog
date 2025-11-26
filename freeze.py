# freeze.py
import os, shutil, sys, traceback
from datetime import datetime
from flask_frozen import Freezer
from app import app, load_posts, build_tags
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
    print(msg, flush=True)

def prepare_dest():
    # Clean output dir and prep essentials
    shutil.rmtree(DEST, ignore_errors=True)
    os.makedirs(DEST, exist_ok=True)
    # No Jekyll so Pages serves JSON etc. verbatim
    open(os.path.join(DEST, ".nojekyll"), "w").close()
    # Custom domain
    with open(os.path.join(DEST, "CNAME"), "w", encoding="utf-8") as f:
        f.write("azure-noob.com")

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
    for tag in tags.keys():
        yield {"tag": tag}

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

# ---- Sitemap generation (NO trailing slashes) ----
def _fmt_lastmod(dt):
    try:
        if isinstance(dt, datetime):
            return dt.date().isoformat()
        return datetime.fromisoformat(str(dt)).date().isoformat()
    except Exception:
        return None

def write_sitemap():
    """Generate sitemap.xml with NO trailing slashes"""
    base = BASE_URL
    urls = [
        {"loc": f"{base}/", "changefreq": "weekly", "priority": "1.0"},
        {"loc": f"{base}/blog", "changefreq": "weekly", "priority": "0.9"},
        {"loc": f"{base}/hubs", "changefreq": "weekly", "priority": "0.9"},
        {"loc": f"{base}/tags", "changefreq": "monthly", "priority": "0.8"},
        {"loc": f"{base}/about", "changefreq": "monthly", "priority": "0.5"},
        {"loc": f"{base}/start-here", "changefreq": "monthly", "priority": "0.7"},
        {"loc": f"{base}/search", "changefreq": "monthly", "priority": "0.3"},
    ]

    posts = load_posts()
    tags = build_tags()
    hubs = get_all_hubs()

    # Tag pages (NO trailing slashes)
    for t in tags.keys():
        urls.append({"loc": f"{base}/tags/{t}", "changefreq": "monthly", "priority": "0.6"})
    
    # Hub pages (NO trailing slashes)
    for hub_slug in hubs.keys():
        urls.append({"loc": f"{base}/hub/{hub_slug}", "changefreq": "weekly", "priority": "0.9"})

    # Blog posts (NO trailing slashes)
    for p in posts:
        urls.append({
            "loc": f"{base}/blog/{p['slug']}",
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

    log(f"✓ Sitemap written with {len(urls)} URLs (NO trailing slashes)")

def remove_trailing_slashes_from_sitemap():
    """Post-process sitemap to remove ALL trailing slashes except root"""
    import re
    
    sitemap_path = os.path.join(DEST, "sitemap.xml")
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove trailing slashes: <loc>https://azure-noob.com/PATH/</loc> -> <loc>https://azure-noob.com/PATH</loc>
    original_count = content.count('</loc>')
    content = re.sub(
        r'<loc>(https://azure-noob\.com/[^<]+)/</loc>',
        r'<loc>\1</loc>',
        content
    )
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log(f"✓ Removed trailing slashes from sitemap ({original_count} URLs processed)")

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
        log("Writing sitemap…")
        write_sitemap()
        log("Cleaning trailing slashes from sitemap…")
        remove_trailing_slashes_from_sitemap()
        log("Normalizing generated HTML files for static hosting…")
        normalize_generated_html_files()
        log("✓ Done! Site frozen to docs/")
        log(f"✓ All URLs standardized (NO trailing slashes)")
    except Exception:
        traceback.print_exc()
        sys.exit(1)
