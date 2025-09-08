# freeze.py
from flask_frozen import Freezer
from app import app, POSTS

# Where to put the static build
app.config["FREEZER_DESTINATION"] = "build"
# Absolute URL for links inside the build
app.config["FREEZER_BASE_URL"] = "https://azure-noob.com/"
app.config["SERVER_NAME"] = "azure-noob.com"

freezer = Freezer(app)

# Dynamic routes to pre-render
@freezer.register_generator
def blog_post():
    for p in POSTS:
        yield {"slug": p["slug"]}

@freezer.register_generator
def rss_xml():
    yield {}

@freezer.register_generator
def sitemap_xml():
    yield {}

@freezer.register_generator
def robots_txt():
    yield {}

if __name__ == "__main__":
    freezer.freeze()

    # Optional: write CNAME for GitHub Pages custom domain
    with open("build/CNAME", "w", encoding="utf-8") as f:
        f.write("azure-noob.com\nwww.azure-noob.com\n")
