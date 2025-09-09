from flask import Flask, render_template, abort, Response, url_for, request
from datetime import datetime
from pathlib import Path
from email.utils import format_datetime
import os
import re
import markdown
import yaml

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True  # show real errors in browser when debug=True

# ---- Site identity ----
SITE_NAME = "Azure Noob"
SITE_TAGLINE = "Practical Cloud Guides"
SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:5000")  # set to https://azure-noob.com in prod

# ---- Content paths ----
ROOT_DIR = Path(__file__).parent
POSTS_DIR = ROOT_DIR / "posts"

# ---- Markdown setup ----
MD_EXTENSIONS = ["fenced_code", "tables", "codehilite", "attr_list"]
MD_EXTENSION_CONFIGS = {
    "codehilite": {"guess_lang": False, "linenums": False, "noclasses": False}
}

# ---- Template helpers ----
@app.template_filter("ymd")
def _fmt_ymd(dt):
    try:
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return str(dt)

# ---- Front matter helpers ----
def parse_front_matter(text: str):
    """Return (meta_dict, body_str). If no front matter, meta_dict = {}.

    Robust to UTF-8 BOM and leading blank lines/whitespace.
    """
    # Strip UTF-8 BOM if present, then any leading whitespace/newlines
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")
    s = text.lstrip()

    if s.startswith("---"):
        parts = s.split("---", 2)
        if len(parts) >= 3:
            _, fm, body = parts
            try:
                meta = yaml.safe_load(fm) or {}
            except Exception:
                meta = {}
            return meta, body.lstrip()
    return {}, text

def coerce_date(value, default_dt: datetime):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                pass
        try:
            return datetime.fromisoformat(value)
        except Exception:
            pass
    return default_dt

def load_posts():
    """
    Scan ./posts/*.md. Supported FM keys: slug, title, date, summary, tags (list), cover
    Returns list of dicts (newest first).
    """
    posts = []
    for md_file in POSTS_DIR.glob("*.md"):
        raw = md_file.read_text(encoding="utf-8")
        meta, body = parse_front_matter(raw)

        slug = (meta.get("slug") or md_file.stem).strip()
        title = (meta.get("title") or "").strip()
        if not title:
            m = re.search(r"^\s*#\s+(.+)$", body, flags=re.MULTILINE)
            title = m.group(1).strip() if m else slug.replace("-", " ").title()

        default_dt = datetime.fromtimestamp(md_file.stat().st_mtime)
        date = coerce_date(meta.get("date"), default_dt)

        summary = (meta.get("summary") or "").strip()
        tags = meta.get("tags") or []
        cover = (meta.get("cover") or "").strip() or None

        posts.append({
            "slug": slug,
            "title": title,
            "date": date,
            "summary": summary,
            "tags": tags,
            "cover": cover,
            "md_path": md_file,
        })

    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts

# ---- Cached posts ----
POSTS = load_posts()
POSTS_BY_SLUG = {p["slug"]: p for p in POSTS}

# ---- Auto-reload posts in debug so new/edited files appear without restart ----
def _refresh_posts_cache():
    global POSTS, POSTS_BY_SLUG
    POSTS = load_posts()
    POSTS_BY_SLUG = {p["slug"]: p for p in POSTS}

@app.before_request
def _reload_posts_in_debug():
    if app.debug:
        _refresh_posts_cache()

# ---- Health checks ----
@app.route("/ping")
def ping():
    return "pong", 200

@app.route("/healthz")
def healthz():
    return {"ok": True, "posts": len(POSTS)}, 200

# ---- Routes ----
@app.route("/")
def home():
    return render_template("index.html", posts=POSTS, site_name=SITE_NAME, site_tagline=SITE_TAGLINE)

@app.route("/about/")  # trailing slash for directory-style output
def about():
    return render_template("about.html", site_name=SITE_NAME, site_tagline=SITE_TAGLINE)

@app.route("/blog/")  # trailing slash for directory-style output
def blog():
    return render_template("blog_index.html", posts=POSTS, site_name=SITE_NAME, site_tagline=SITE_TAGLINE)

@app.route("/blog/<slug>/")  # trailing slash for directory-style output
def blog_post(slug: str):
    post = POSTS_BY_SLUG.get(slug)
    if not post:
        abort(404)

    raw = post["md_path"].read_text(encoding="utf-8")
    meta, body = parse_front_matter(raw)

    html = markdown.markdown(
        body,
        extensions=MD_EXTENSIONS,
        extension_configs=MD_EXTENSION_CONFIGS,
        output_format="html5",
    )

    # Reading time
    words = len(re.findall(r"\w+", body))
    reading_min = max(1, round(words / 200))

    idx = next((i for i, p in enumerate(POSTS) if p["slug"] == slug), None)
    prev_post = POSTS[idx + 1] if idx is not None and idx + 1 < len(POSTS) else None
    next_post = POSTS[idx - 1] if idx is not None and idx - 1 >= 0 else None
    to_obj = (lambda d: type("P", (), d) if d else None)

    return render_template(
        "blog_post.html",
        post=post,
        content=html,            # template uses {{ content|safe }}
        reading_min=reading_min,
        cover=(meta.get("cover") or post.get("cover")),
        prev_post=to_obj(prev_post),
        next_post=to_obj(next_post),
        site_name=SITE_NAME,
        site_tagline=SITE_TAGLINE,
    )

# ---- Robots / Sitemap / RSS ----
def _absurl(endpoint, **values) -> str:
    base = SITE_URL.rstrip("/") if SITE_URL else request.url_root.rstrip("/")
    return f"{base}{url_for(endpoint, **values)}"

@app.route("/robots.txt")
def robots_txt():
    lines = ["User-agent: *", "Allow: /", f"Sitemap: {SITE_URL.rstrip('/')}/sitemap.xml", ""]
    return Response("\n".join(lines), mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap_xml():
    urls = [{"loc": _absurl("home")}, {"loc": _absurl("blog")}, {"loc": _absurl("about")}]
    for p in POSTS:
        urls.append({"loc": _absurl("blog_post", slug=p["slug"]), "lastmod": p["date"].date().isoformat()})

    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml += ["<url>", f"<loc>{u['loc']}</loc>"]
        if "lastmod" in u: xml.append(f"<lastmod>{u['lastmod']}</lastmod>")
        xml.append("</url>")
    xml.append("</urlset>")
    return Response("\n".join(xml), mimetype="application/xml")

@app.route("/rss.xml")
def rss_xml():
    last_build = POSTS[0]["date"] if POSTS else datetime.utcnow()
    items = []
    for p in POSTS[:20]:
        link = _absurl("blog_post", slug=p["slug"])
        title = (p["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        description = ((p["summary"] or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        pub = format_datetime(p["date"])
        items.append(f"""  <item>
    <title>{title}</title>
    <link>{link}</link>
    <guid isPermaLink="true">{link}</guid>
    <pubDate>{pub}</pubDate>
    <description>{description}</description>
  </item>""")
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>{SITE_NAME} — {SITE_TAGLINE}</title>
  <link>{SITE_URL}</link>
  <description>Latest posts from {SITE_NAME}</description>
  <lastBuildDate>{format_datetime(last_build)}</lastBuildDate>
  <ttl>120</ttl>
{chr(10).join(items)}
</channel>
</rss>"""
    return Response(rss, mimetype="application/rss+xml")

# ---- Friendly errors ----
@app.errorhandler(404)
def not_found(e):
    try:
        return render_template("404.html"), 404
    except Exception:
        return "404 Not Found", 404

@app.errorhandler(500)
def server_error(e):
    try:
        return render_template("500.html"), 500
    except Exception:
        return "500 Internal Server Error", 500

if __name__ == "__main__":
    app.run(debug=True)
