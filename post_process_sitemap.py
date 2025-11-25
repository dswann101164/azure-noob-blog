import re
import sys

# Read sitemap
with open('docs/sitemap.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove trailing slashes from ALL URLs except root
# Pattern: <loc>https://azure-noob.com/ANYTHING/</loc>
# Replace with: <loc>https://azure-noob.com/ANYTHING</loc>
content = re.sub(
    r'<loc>(https://azure-noob\.com/[^<]+)/</loc>',
    r'<loc>\1</loc>',
    content
)

# Write back
with open('docs/sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Sitemap URLs cleaned (removed trailing slashes)")
