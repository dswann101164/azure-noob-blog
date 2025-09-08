# freeze.py
import os
import shutil
from flask_frozen import Freezer
from app import app, POSTS  # your Flask app + POSTS list

# --- Build destination for GitHub Pages ---
DEST = "docs"  # Pages -> Settings -> Source: main / (docs)
app.config["FREEZER_DESTINATION"] = DEST

# Absolute site URL (used in generated links)
app.config["FREEZER_BASE_URL"] = os.environ.get("SITE_URL", "https://azure-noob.com/")

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

# If your Flask endpoints are named home/blog/about, include them explicitly.
@freezer.register_generator
def static_pages():
    yield "home", {}
    yield "blog", {}
    yield "about", {}
# ----------------------------------------------

if __name__ == "__main__":
    freezer.freeze()
