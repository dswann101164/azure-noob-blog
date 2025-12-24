# fix_static_html_noindex.py
"""
Add noindex meta tags to static HTML files that shouldn't be indexed.
"""

import os
import re

STATIC_HTML_FILES = [
    "docs/static/azure-icons-table.html",
    "docs/static/downloads/azure-command-finder.html", 
    "docs/static/images/hero/azure-ai-copilot-temp.html",
    "docs/static/images/hero/azure-cost-optimization-complete.html",
    "docs/static/images/hero/azure-cost-optimization-facade.html"
]

def add_noindex_tag(filepath):
    """Add noindex meta tag to HTML file if it doesn't exist"""
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has noindex
        if 'noindex' in content:
            print(f"✓ Already has noindex: {filepath}")
            return False
        
        # Add noindex tag after <head>
        noindex_tag = '<meta name="robots" content="noindex, nofollow">'
        
        if '<head>' in content:
            content = content.replace('<head>', f'<head>\n  {noindex_tag}')
        elif '<HEAD>' in content:
            content = content.replace('<HEAD>', f'<HEAD>\n  {noindex_tag}')
        else:
            print(f"⚠️  No <head> tag found: {filepath}")
            return False
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Added noindex: {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    print("Adding noindex tags to static HTML files...")
    print("="*80)
    
    modified = 0
    for filepath in STATIC_HTML_FILES:
        if add_noindex_tag(filepath):
            modified += 1
    
    print("="*80)
    print(f"Modified {modified} files")

if __name__ == '__main__':
    main()
