"""
Generate HTML redirect pages for 404 tag URLs.

This creates meta-refresh redirect pages for tag URLs with spaces/capitals
that Google has cached, redirecting them to the correct slugified versions.
"""

import os
from pathlib import Path

# Map of bad tag names (from 404 report) to correct slugified versions
TAG_REDIRECTS = {
    # Spaces
    "Management Groups": "management-groups",
    "azure governance": "azure-governance",
    "Cloud Adoption Framework": "cloud-adoption-framework",
    "Private DNS": "private-dns",
    "Resource Tags": "azure-tags",  # Using your existing tag
    "Hybrid Cloud": "hybrid-cloud",
    "application discovery": "application-mapping",  # Using your existing tag
    "update manager": "azure-update-manager",  # Using your existing tag  
    "technical debt": "technical-debt",
    "update management": "update-management",
    "resource graph": "resource-graph",
    "vm inventory": "vm-inventory",
    "DNS Resolver": "dns-resolver",
    "Cloud Strategy": "cloud-strategy",
    
    # Capitals
    "GPT-4": "gpt-4",
    "WSUS": "wsus",
    "DNS": "private-dns",  # Assuming this should map to private-dns
}

# HTML template for redirect pages
REDIRECT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=/tags/{correct_slug}/">
    <link rel="canonical" href="https://azure-noob.com/tags/{correct_slug}/">
    <title>Redirecting...</title>
    <script>
        window.location.href = "/tags/{correct_slug}/";
    </script>
</head>
<body>
    <p>Redirecting to <a href="/tags/{correct_slug}/">/tags/{correct_slug}/</a>...</p>
</body>
</html>
"""

def create_redirect_page(bad_tag: str, correct_slug: str, docs_dir: str = "docs/tags"):
    """Create a redirect HTML page for a bad tag URL."""
    
    # Create directory for bad tag (with spaces/capitals as-is)
    tag_dir = Path(docs_dir) / bad_tag
    tag_dir.mkdir(parents=True, exist_ok=True)
    
    # Create index.html with redirect
    index_file = tag_dir / "index.html"
    html_content = REDIRECT_TEMPLATE.format(correct_slug=correct_slug)
    
    index_file.write_text(html_content, encoding='utf-8')
    print(f"✅ Created redirect: /tags/{bad_tag}/ → /tags/{correct_slug}/")

def main():
    """Generate all redirect pages."""
    
    # Auto-detect docs/tags directory
    docs_dir = Path("docs/tags")
    
    if not docs_dir.exists():
        print(f"❌ Error: Directory '{docs_dir}' does not exist")
        print(f"   Current directory: {os.getcwd()}")
        return
    
    print(f"\n🔧 Creating {len(TAG_REDIRECTS)} redirect pages...\n")
    
    for bad_tag, correct_slug in TAG_REDIRECTS.items():
        create_redirect_page(bad_tag, correct_slug, str(docs_dir))
    
    print(f"\n✅ Done! Created {len(TAG_REDIRECTS)} redirect pages")
    print(f"\n📝 Next steps:")
    print(f"   1. Review the created directories in docs/tags/")
    print(f"   2. Commit and push to GitHub")
    print(f"   3. Wait for Google to recrawl (or submit via Search Console)")
    print(f"\n   git add docs/tags")
    print(f"   git commit -m \"Add redirect pages for 404 tag URLs\"")
    print(f"   git push")

if __name__ == "__main__":
    main()
