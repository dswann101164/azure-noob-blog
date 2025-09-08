# freeze.py
import os
import shutil
from flask_frozen import Freezer
from app import app, POSTS   # imports your Flask app and the POSTS list

# Where to put the static build
DEST = "build"
app.config["FREEZER_DESTINATION"] = DEST

# Absolute URL used for links inside the build
app.config["FREEZER_BASE_URL"] = os.environ.get("SITE_URL", "https://azure-noob.com/")

# Map mimetypes to file extensions so URLs without an explicit extension
# become real files (avoids 'build/blog' conflict).
app.config["FREEZER_DEFAULT_MIMETYPE"] = "text/html"
app.config["FREEZER_DEFAULT_MIMETYPE_EXTENSIONS"] = {
    "text/html": "html",
    "application/xml": "xml",
    "application/rss+xml": "xml",
    "application/json": "json",
    "text/plain": "txt",
}

# Optional: silence the mimetype warnings we were seeing
app.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True

freezer = Freezer(app)

# Clean build dir before freezing
shutil.rmtree(DEST, ignore_errors=True)
os.makedirs(DEST, exist_ok=True)

# Dynamic routes to pre-render
@freezer.register_generator
def blog_post():
    for p in POSTS:
        yield {"slug": p["slug"]}

@freezer.register_generator
def rss_xml():
    yield {}

if __name__ == "__main__":
    freezer.freeze()
