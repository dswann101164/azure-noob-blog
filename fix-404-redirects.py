#!/usr/bin/env python3
"""
Generate HTML redirect files for date-prefixed blog URLs
Run this after freeze.py to create redirect files in docs/
"""

import os
import re

# Map of old date-prefixed URLs to new clean URLs
REDIRECTS = {
    '/blog/2025-01-15-kql-cheat-sheet-complete/': '/blog/kql-cheat-sheet-complete/',
    '/blog/2025-01-15-kql-cheat-sheet-complete': '/blog/kql-cheat-sheet-complete/',
    '/blog/2025-09-24-azure-update-manager-reality-check/': '/blog/azure-update-manager-reality-check/',
    '/blog/2025-09-24-why-most-azure-migrations-fail/': '/blog/why-most-azure-migrations-fail/',
    '/blog/2025-09-24-why-most-azure-migrations-fail': '/blog/why-most-azure-migrations-fail/',
    '/blog/2025-09-23-azure-vm-inventory-kql/': '/blog/azure-vm-inventory-kql/',
    '/blog/2025-09-23-azure-resource-tags-guide/': '/blog/azure-resource-tags-guide/',
    '/blog/2025-10-17-azure-ai-30-day-test': '/blog/azure-ai-30-day-test/',
}

REDIRECT_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url={new_url}">
    <link rel="canonical" href="https://azure-noob.com{new_url}" />
    <title>Redirecting...</title>
    <script>window.location.href="{new_url}";</script>
</head>
<body>
    <p>Redirecting to <a href="{new_url}">{new_url}</a>...</p>
</body>
</html>
'''

def create_redirect(old_path, new_url, base_dir='docs'):
    """Create an HTML redirect file"""
    # Remove leading slash and convert to file path
    file_path = old_path.lstrip('/')
    
    # Handle both with and without trailing slash
    if file_path.endswith('/'):
        file_path = os.path.join(file_path, 'index.html')
    elif not file_path.endswith('.html'):
        # Create directory structure for extensionless URLs
        os.makedirs(os.path.join(base_dir, file_path), exist_ok=True)
        file_path = os.path.join(file_path, 'index.html')
    
    full_path = os.path.join(base_dir, file_path)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Write redirect HTML
    with open(full_path, 'w') as f:
        f.write(REDIRECT_HTML.format(new_url=new_url))
    
    print(f"✅ Created redirect: {old_path} → {new_url}")

def main():
    print("Creating HTML redirect files for 404 URLs...\n")
    
    for old_path, new_url in REDIRECTS.items():
        create_redirect(old_path, new_url)
    
    print(f"\n✅ Created {len(REDIRECTS)} redirect files in docs/")
    print("Run 'git add docs' and 'git commit' to deploy them.")

if __name__ == '__main__':
    main()
