# freeze.py
import os, shutil, sys, traceback
from datetime import datetime
from flask_frozen import Freezer
from app import app, load_posts, build_tags   # make sure build_tags is exported in app.py

DEST = "docs"
BASE_URL = os.environ.get("SITE_URL", "https://azure-noob.com").rstrip("/")

# ---- Freezer config ----
app.config["FREEZER_DESTINATION"] = DEST
app.config["FREEZER_BASE_URL"] = BASE_URL
app.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True
app.config["FREEZER_REMOVE_EXTRA_FILES"] = False
app.config["FREEZER_RELATIVE_URLS"] = True

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
def home():
    yield {}

@freezer.register_generator
def blog():
    yield {}

@freezer.register_generator
def about():
    yield {}

# SEARCH (page + JSON)
# These names must match your @app.route handlers in app.py
@freezer.register_generator
def search():            # /search/
    yield {}

@freezer.register_generator
def search_json():       # /search.json
    yield {}

# Blog posts
@freezer.register_generator
def blog_post():
    for p in load_posts():           # reload at freeze time
        yield {"slug": p["slug"]}

# Tags index and each tag page
@freezer.register_generator
def tags_index():
    yield {}

@freezer.register_generator
def tag_page():
    posts = load_posts()
    tags = build_tags(posts)
    for tag in tags.keys():
        yield {"tag": tag}

# ---- Sitemap & robots.txt ----
def _fmt_lastmod(dt):
    try:
        if isinstance(dt, datetime):
            return dt.date().isoformat()
        return datetime.fromisoformat(str(dt)).date().isoformat()
    except Exception:
        return None

def write_sitemap_and_robots():
    base = BASE_URL
    urls = [
        {"loc": f"{base}/", "changefreq": "weekly", "priority": "1.0"},
        {"loc": f"{base}/blog/", "changefreq": "weekly", "priority": "0.8"},
        {"loc": f"{base}/about/", "changefreq": "monthly", "priority": "0.5"},
        {"loc": f"{base}/tags/", "changefreq": "monthly", "priority": "0.4"},
        {"loc": f"{base}/search/", "changefreq": "monthly", "priority": "0.3"},
    ]

    posts = load_posts()
    tags = build_tags(posts)

    for t in tags.keys():
        urls.append({"loc": f"{base}/tags/{t}/", "changefreq": "monthly", "priority": "0.4"})

    for p in posts:
        urls.append({
            "loc": f"{base}/blog/{p['slug'].strip('/')}/",
            "lastmod": _fmt_lastmod(p.get("date")),
            "changefreq": "monthly",
            "priority": "0.6",
        })

    with open(os.path.join(DEST, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write("  <url>\n")
            f.write(f"    <loc>{u['loc']}</loc>\n")
            if u.get("lastmod"): f.write(f"    <lastmod>{u['lastmod']}</lastmod>\n")
            f.write(f"    <changefreq>{u['changefreq']}</changefreq>\n")
            f.write(f"    <priority>{u['priority']}</priority>\n")
            f.write("  </url>\n")
        f.write("</urlset>\n")

    with open(os.path.join(DEST, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n")

# ---- Entrypoint ----
if __name__ == "__main__":
    try:
        log("Preparing docs/…")
        prepare_dest()
        log("Freezing Flask routes…")
        freezer.freeze()
        log("Writing sitemap & robots…")
        write_sitemap_and_robots()
        log("Done.")
    except Exception:
        traceback.print_exc()
        sys.exit(1)
