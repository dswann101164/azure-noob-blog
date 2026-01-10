"""
Google Search Console URL Redirect Fixer
Analyzes GSC export data and generates redirect rules for app.py

USAGE:
1. Export the "Page with redirect" URLs from Google Search Console
2. Save as gsc-redirects.csv (URL column)
3. Run this script
4. It will generate redirect rules to add to app.py
"""

import csv
import re
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse

def extract_slug(url):
    """Extract the slug from a URL"""
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    
    # Extract last part of path
    if '/' in path:
        return path.split('/')[-1]
    return path

def is_date_prefixed(slug):
    """Check if slug has YYYY-MM-DD prefix"""
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}-', slug))

def remove_date_prefix(slug):
    """Remove YYYY-MM-DD- prefix"""
    return re.sub(r'^\d{4}-\d{2}-\d{2}-', '', slug)

def analyze_gsc_export(csv_file):
    """Analyze GSC export to identify redirect patterns"""
    redirects = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get('URL', row.get('url', '')).strip()
                if url:
                    redirects.append(url)
    except FileNotFoundError:
        print(f"❌ File not found: {csv_file}")
        print("\nTo use this tool:")
        print("1. Go to Google Search Console")
        print("2. Navigate to Indexing → Pages")
        print("3. Click 'Page with redirect' filter")
        print("4. Export the data")
        print("5. Save as 'gsc-redirects.csv' in the blog root")
        return None
    
    return redirects

def categorize_redirects(redirects):
    """Categorize redirects by pattern"""
    categories = {
        'date_prefixed': [],
        'http_to_https': [],
        'www_redirect': [],
        'trailing_slash': [],
        'other': []
    }
    
    for url in redirects:
        parsed = urlparse(url)
        path = parsed.path
        
        # HTTP vs HTTPS
        if parsed.scheme == 'http':
            categories['http_to_https'].append(url)
            continue
        
        # WWW redirect
        if parsed.hostname and parsed.hostname.startswith('www.'):
            categories['www_redirect'].append(url)
            continue
        
        # Date-prefixed URLs
        slug = extract_slug(url)
        if is_date_prefixed(slug):
            clean_slug = remove_date_prefix(slug)
            categories['date_prefixed'].append({
                'old': url,
                'old_slug': slug,
                'new_slug': clean_slug
            })
            continue
        
        # Trailing slash
        if not path.endswith('/') and '.' not in path.split('/')[-1]:
            categories['trailing_slash'].append(url)
            continue
        
        categories['other'].append(url)
    
    return categories

def generate_redirect_rules(categories):
    """Generate Python code for redirect rules"""
    print("\n" + "=" * 80)
    print("REDIRECT RULES TO ADD TO app.py")
    print("=" * 80)
    
    if categories['date_prefixed']:
        print("\n# Date-prefixed blog URL redirects")
        print("# These handle old URLs with YYYY-MM-DD- prefix\n")
        
        # Group by pattern
        for item in categories['date_prefixed'][:20]:  # Show first 20
            old_path = urlparse(item['old']).path
            new_path = old_path.replace(item['old_slug'], item['new_slug'])
            print(f"    '{old_path}': '{new_path}',")
        
        if len(categories['date_prefixed']) > 20:
            print(f"    # ... and {len(categories['date_prefixed']) - 20} more")
    
    if categories['http_to_https']:
        print(f"\n# HTTP to HTTPS redirects: {len(categories['http_to_https'])} URLs")
        print("# These are handled by the existing HTTPS redirect in app.py")
    
    if categories['www_redirect']:
        print(f"\n# WWW to non-WWW redirects: {len(categories['www_redirect'])} URLs")
        print("# These are handled by the existing WWW redirect in app.py")
    
    if categories['trailing_slash']:
        print(f"\n# Trailing slash redirects: {len(categories['trailing_slash'])} URLs")
        print("# These are handled by the existing trailing slash redirect in app.py")
    
    if categories['other']:
        print(f"\n# Other redirects: {len(categories['other'])} URLs")
        print("# Manual review needed:\n")
        for url in categories['other'][:10]:
            print(f"    # {url}")

def main():
    print("=" * 80)
    print("GSC REDIRECT ANALYZER")
    print("=" * 80)
    
    csv_file = 'gsc-redirects.csv'
    redirects = analyze_gsc_export(csv_file)
    
    if not redirects:
        return
    
    print(f"\n✓ Found {len(redirects)} redirected URLs")
    
    categories = categorize_redirects(redirects)
    
    print("\n" + "=" * 80)
    print("REDIRECT BREAKDOWN")
    print("=" * 80)
    print(f"\nDate-prefixed URLs:      {len(categories['date_prefixed'])}")
    print(f"HTTP → HTTPS:            {len(categories['http_to_https'])}")
    print(f"WWW → non-WWW:           {len(categories['www_redirect'])}")
    print(f"Missing trailing slash:  {len(categories['trailing_slash'])}")
    print(f"Other:                   {len(categories['other'])}")
    
    generate_redirect_rules(categories)
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("""
1. The date-prefixed redirects should already be handled by app.py
2. HTTP/HTTPS and WWW redirects are handled automatically
3. Trailing slash redirects are handled automatically

If you still see 212 redirects in GSC:
- These are likely OLD URLs that Google still has in its index
- They will gradually disappear as Google re-crawls
- You can speed this up by:
  a) Submitting updated sitemap to GSC
  b) Using GSC URL Inspection tool to request re-indexing
  c) Removing old URLs from GSC (if they no longer exist)

To remove old URLs from Google's index:
1. Go to GSC → Removals
2. Select "Temporarily remove URL"
3. Add the old date-prefixed URLs
4. Google will drop them from index
    """)

if __name__ == "__main__":
    main()
