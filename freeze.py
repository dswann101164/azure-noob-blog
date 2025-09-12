# freeze.py
import os, shutil
from datetime import datetime
from flask_frozen import Freezer
from app import app, load_posts  # use the loader at freeze time

DEST = "docs"

# ---- Flask-Frozen config ----
app.config.update(
    FREEZER_DESTINATION=DEST,
    FREEZER_BASE_URL=os.environ.get("SITE_URL", "https://azure-noob.com").rstrip("/"),
    FREEZER_IGNORE_MIMETYPE_WARNINGS=True,
    FREEZER_REMOVE_EXTRA_FILES=False,
)

# Include /static files automatically
freezer = Freezer(app, with_static_files=True)

# Clean output & ensure .nojekyll so GitHub Pages serves raw paths
shutil.rmtree(DEST, ignore_errors=True)
os.makedirs(DEST, exist_ok=True)
open(os.path.join(DEST, ".nojekyll"), "w").close()

# ---------- Route generators (dynamic URLs) ----------
@freezer.register_generator
def home():
    yield {}

@freezer.register_generator
def blog():
    yield {}

@freezer.register_generator
def about():
    yield {}

@freezer.register_generator
def blog_post():
    for p in load_posts():
        yield {"slug": p["slug"]}

# Tags index + each tag page
@freezer.register_generator
def tags_index():
    yield {}

@freezer.register_generator
def by_tag():
    seen = set()
    for p in load_posts():
        for t in p.get("tags", []) or []:
            if not t:
                continue
            key = t.lower()
            if key in seen:
                continue
            seen.add(key)
            yield {"tag": t}

# Search page + JSON index
@freezer.register_generator
def search_page():
    yield {}

@freezer.register_generator
def search_json():
    # freezer will hit the endpoint and write docs/search.json
    yield {}

# Optional: export these XML/health endpoints as static files, too
@freezer.register_generator
def sitemap_xml():
    yield {}

@freezer.register_generator
def rss_xml():
    yield {}

# ---------- Helpers for sitemap/robots/CNAME ----------
def _fmt_lastmod(dt):
    try:
        return (dt if isinstance(dt, datetime) else datetime.fromisoformat(str(dt))).date().isoformat()
    except Exception:
        return None

def write_sitemap_and_robots():
    base = app.config["FREEZER_BASE_URL"].rstrip("/")
    # We also write static XML files to be safe (even though the frozen endpoints exist)
    urls = [
        {"loc": f"{base}/", "changefreq": "weekly", "priority": "1.0"},
        {"loc": f"{base}/blog/", "changefreq": "weekly", "priority": "0.8"},
        {"loc": f"{base}/about/", "changefreq": "monthly", "priority": "0.5"},
        {"loc": f"{base}/tags/", "changefreq": "weekly", "priority": "0.6"},
        {"loc": f"{base}/search/", "changefreq": "weekly", "priority": "0.3"},
    ]
    seen = set()
    for p in load_posts():
        urls.append({
            "loc": f"{base}/blog/{p['slug'].strip('/')}/",
            "lastmod": _fmt_lastmod(p.get("date")),
            "changefreq": "monthly",
            "priority": "0.7",
        })
        for t in p.get("tags", []) or []:
            key = t.lower()
            if key in seen: 
                continue
            seen.add(key)
            urls.append({"loc": f"{base}/tags/{t}/", "changefreq": "weekly", "priority": "0.5"})

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

if __name__ == "__main__":
    freezer.freeze()
    # Ensure CNAME for your custom domain
    with open(os.path.join(DEST, "CNAME"), "w", encoding="utf-8") as f:
        f.write("azure-noob.com")
    write_sitemap_and_robots()
