# freeze.py
import os, shutil
from datetime import datetime
from flask_frozen import Freezer
from app import app, load_posts   # import the loader, not the cached POSTS

DEST = "docs"
app.config["FREEZER_DESTINATION"] = DEST
app.config["FREEZER_BASE_URL"] = os.environ.get("SITE_URL", "https://azure-noob.com").rstrip("/")
app.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True
app.config["FREEZER_REMOVE_EXTRA_FILES"] = False

freezer = Freezer(app)

# Clean output & ensure nojekyll so GitHub Pages serves our raw files
shutil.rmtree(DEST, ignore_errors=True)
os.makedirs(DEST, exist_ok=True)
open(os.path.join(DEST, ".nojekyll"), "w").close()

@freezer.register_generator
def blog_post():
    # Always reload posts at freeze time (avoid stale cache)
    for p in load_posts():
        print("FREEZE POST:", p["slug"])
        yield {"slug": p["slug"]}

@freezer.register_generator
def home():
    yield {}

@freezer.register_generator
def blog():
    yield {}

@freezer.register_generator
def about():
    yield {}

def _fmt_lastmod(dt):
    try:
        return (dt if isinstance(dt, datetime) else datetime.fromisoformat(str(dt))).date().isoformat()
    except Exception:
        return None

def write_sitemap_and_robots():
    base = app.config["FREEZER_BASE_URL"].rstrip("/")
    urls = [
        {"loc": f"{base}/", "changefreq": "weekly", "priority": "1.0"},
        {"loc": f"{base}/blog/", "changefreq": "weekly", "priority": "0.8"},
        {"loc": f"{base}/about/", "changefreq": "monthly", "priority": "0.5"},
    ]
    for p in load_posts():  # reload fresh
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

if __name__ == "__main__":
    freezer.freeze()
    # Ensure CNAME is present in output for custom domain
    with open(os.path.join(DEST, "CNAME"), "w", encoding="utf-8") as f:
        f.write("azure-noob.com")
    write_sitemap_and_robots()
