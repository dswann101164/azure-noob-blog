# freeze.py
import os
import shutil
from datetime import datetime
from flask_frozen import Freezer
from app import app, POSTS  # your Flask app and POSTS list (with 'slug' and optionally 'date')

# --- Build destination for GitHub Pages ---
DEST = "docs"  # Pages -> Settings -> Source: main / (docs)
app.config["FREEZER_DESTINATION"] = DEST

# Absolute site URL (used in generated links)
BASE_URL = os.environ.get("SITE_URL", "https://azure-noob.com/").rstrip("/") + "/"
app.config["FREEZER_BASE_URL"] = BASE_URL

# Map default extensions so extensionless routes become real files
app.config["FREEZER_DEFAULT_MIMETYPE"] = "text/html"
app.config["FREEZER_DEFAULT_MIMETYPE_EXTENSIONS"] = {
    "text/html": "html",
    "application/xml": "xml",
    "application/rss+xml": "xml",
    "application/json": "json",
    "text/plain": "txt",
}

# Optional: quiet mime warnings
app.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True

freezer = Freezer(app)

# Clean the build folder each run
shutil.rmtree(DEST, ignore_errors=True)
os.makedirs(DEST, exist_ok=True)

# Ensure GitHub Pages doesn't try to Jekyll-process the folder
open(os.path.join(DEST, ".nojekyll"), "w").close()

# --------- Dynamic routes to generate ---------
@freezer.register_generator
def blog_post():
    for p in POSTS:
        yield {"slug": p["slug"]}

@freezer.register_generator
def rss_xml():
    yield {}

@freezer.register_generator
def static_pages():
    # Make sure these endpoints exist in app.py (@app.route("/"), "/blog/", "/about/")
    yield "home", {}
    yield "blog", {}
    yield "about", {}
# ---------------------------------------------

def _fmt_lastmod(dt):
    """Return W3C Datetime format (yyyy-mm-dd) for <lastmod> if dt provided, else None."""
    try:
        if isinstance(dt, datetime):
            return dt.date().isoformat()
        # if dt is string like '2025-01-01'
        return datetime.fromisoformat(str(dt)).date().isoformat()
    except Exception:
        return None

def write_sitemap_and_robots():
    """Generate sitemap.xml from static sections + POSTS, and robots.txt."""
    urls = []

    # Core sections (trailing slashes)
    urls.append({"loc": BASE_URL, "changefreq": "weekly", "priority": "1.0"})
    urls.append({"loc": BASE_URL + "blog/", "changefreq": "weekly", "priority": "0.8"})
    urls.append({"loc": BASE_URL + "about/", "changefreq": "monthly", "priority": "0.5"})

    # Blog posts
    for p in POSTS:
        slug = p["slug"].strip("/")
        lastmod = _fmt_lastmod(p.get("date"))
        urls.append({
            "loc": f"{BASE_URL}blog/{slug}/",
            "changefreq": "monthly",
            "priority": "0.6",
            "lastmod": lastmod
        })

    # Build sitemap.xml
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{u['loc']}</loc>")
        if u.get("lastmod"):
            lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        lines.append(f"    <priority>{u['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>\n")

    with open(os.path.join(DEST, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # robots.txt (points to sitemap)
    robots = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}sitemap.xml
"""
    with open(os.path.join(DEST, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

if __name__ == "__main__":
    freezer.freeze()
    # After freezing pages/assets, drop fresh sitemap & robots in docs/
    write_sitemap_and_robots()
