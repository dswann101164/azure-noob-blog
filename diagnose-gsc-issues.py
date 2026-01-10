"""
Google Search Console Indexing Issues Diagnostic Tool
Analyzes the frozen site to identify causes of:
- Page with redirect (212 pages)
- Not found (404) (79 pages)
- Alternate page with proper canonical tag (50 pages)
- Crawled - currently not indexed (19 pages)
- Excluded by 'noindex' tag (86 pages)
"""

import os
from pathlib import Path
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from collections import defaultdict
import re

DOCS_DIR = Path("docs")
SITEMAP_PATH = DOCS_DIR / "sitemap.xml"

def load_sitemap_urls():
    """Extract all URLs from sitemap.xml"""
    urls = set()
    if SITEMAP_PATH.exists():
        tree = ET.parse(SITEMAP_PATH)
        root = tree.getroot()
        namespace = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for url in root.findall('.//sm:loc', namespace):
            urls.add(url.text)
    return urls

def find_html_files():
    """Find all HTML files in docs/"""
    html_files = []
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)
    return html_files

def check_meta_robots(html_content):
    """Check for noindex directives"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check meta robots tag
    meta_robots = soup.find('meta', attrs={'name': 'robots'})
    if meta_robots:
        content = meta_robots.get('content', '').lower()
        if 'noindex' in content:
            return True
    
    # Check X-Robots-Tag in comments (some frameworks do this)
    for comment in soup.find_all(string=lambda text: isinstance(text, str) and 'noindex' in text.lower()):
        return True
    
    return False

def check_canonical(html_content, file_path):
    """Check canonical tag"""
    soup = BeautifulSoup(html_content, 'html.parser')
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if canonical:
        return canonical.get('href')
    return None

def check_redirects(html_content):
    """Check for meta refresh redirects"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check meta refresh
    meta_refresh = soup.find('meta', attrs={'http-equiv': lambda x: x and x.lower() == 'refresh'})
    if meta_refresh:
        return meta_refresh.get('content')
    
    # Check for JavaScript redirects (common pattern)
    for script in soup.find_all('script'):
        if script.string and 'window.location' in script.string:
            return "JavaScript redirect detected"
    
    return None

def get_url_from_path(file_path):
    """Convert file path to expected URL"""
    rel_path = file_path.relative_to(DOCS_DIR)
    
    # Handle index.html files
    if rel_path.name == 'index.html':
        if rel_path.parent == Path('.'):
            return "https://azure-noob.com/"
        else:
            return f"https://azure-noob.com/{rel_path.parent}/"
    
    # Handle other HTML files
    path_str = str(rel_path).replace('\\', '/').replace('.html', '')
    return f"https://azure-noob.com/{path_str}/"

def analyze_site():
    """Main analysis function"""
    print("=" * 80)
    print("AZURE NOOB - GSC INDEXING ISSUES DIAGNOSTIC")
    print("=" * 80)
    print()
    
    # Load sitemap
    sitemap_urls = load_sitemap_urls()
    print(f"✓ Found {len(sitemap_urls)} URLs in sitemap.xml")
    print()
    
    # Find all HTML files
    html_files = find_html_files()
    print(f"✓ Found {len(html_files)} HTML files in docs/")
    print()
    
    # Analysis results
    issues = {
        'noindex': [],
        'redirects': [],
        'canonical_mismatch': [],
        'not_in_sitemap': [],
        'thin_content': []
    }
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            expected_url = get_url_from_path(html_file)
            
            # Check for noindex
            if check_meta_robots(content):
                issues['noindex'].append({
                    'file': str(html_file.relative_to(DOCS_DIR)),
                    'url': expected_url
                })
            
            # Check for redirects
            redirect = check_redirects(content)
            if redirect:
                issues['redirects'].append({
                    'file': str(html_file.relative_to(DOCS_DIR)),
                    'url': expected_url,
                    'redirect': redirect
                })
            
            # Check canonical
            canonical = check_canonical(content, html_file)
            if canonical and canonical != expected_url:
                # Remove trailing slash for comparison
                canonical_clean = canonical.rstrip('/')
                expected_clean = expected_url.rstrip('/')
                if canonical_clean != expected_clean:
                    issues['canonical_mismatch'].append({
                        'file': str(html_file.relative_to(DOCS_DIR)),
                        'expected': expected_url,
                        'canonical': canonical
                    })
            
            # Check if in sitemap
            if expected_url not in sitemap_urls:
                issues['not_in_sitemap'].append({
                    'file': str(html_file.relative_to(DOCS_DIR)),
                    'url': expected_url
                })
            
            # Check content length (thin content)
            soup = BeautifulSoup(content, 'html.parser')
            main_content = soup.find('main') or soup.find('article') or soup.body
            if main_content:
                text = main_content.get_text(strip=True)
                word_count = len(text.split())
                if word_count < 300:
                    issues['thin_content'].append({
                        'file': str(html_file.relative_to(DOCS_DIR)),
                        'url': expected_url,
                        'words': word_count
                    })
        
        except Exception as e:
            print(f"⚠ Error processing {html_file}: {e}")
    
    # Print results
    print("\n" + "=" * 80)
    print("ISSUE #1: NOINDEX TAGS (86 pages in GSC)")
    print("=" * 80)
    if issues['noindex']:
        print(f"Found {len(issues['noindex'])} pages with noindex:")
        for item in issues['noindex'][:10]:
            print(f"  • {item['file']}")
            print(f"    URL: {item['url']}")
        if len(issues['noindex']) > 10:
            print(f"  ... and {len(issues['noindex']) - 10} more")
    else:
        print("✓ No noindex tags found - this is good!")
    
    print("\n" + "=" * 80)
    print("ISSUE #2: REDIRECTS (212 pages in GSC)")
    print("=" * 80)
    if issues['redirects']:
        print(f"Found {len(issues['redirects'])} pages with redirects:")
        for item in issues['redirects'][:10]:
            print(f"  • {item['file']}")
            print(f"    Redirect: {item['redirect'][:80]}")
        if len(issues['redirects']) > 10:
            print(f"  ... and {len(issues['redirects']) - 10} more")
    else:
        print("✓ No meta refresh redirects found in HTML - this is good!")
        print("  (If GSC shows 212 redirects, they may be:")
        print("  - Server-level redirects (GitHub Pages)")
        print("  - Old URLs still in Google's index")
        print("  - External links pointing to old URLs")
    
    print("\n" + "=" * 80)
    print("ISSUE #3: CANONICAL MISMATCHES (50 pages in GSC)")
    print("=" * 80)
    if issues['canonical_mismatch']:
        print(f"Found {len(issues['canonical_mismatch'])} canonical mismatches:")
        for item in issues['canonical_mismatch'][:10]:
            print(f"  • {item['file']}")
            print(f"    Expected:  {item['expected']}")
            print(f"    Canonical: {item['canonical']}")
        if len(issues['canonical_mismatch']) > 10:
            print(f"  ... and {len(issues['canonical_mismatch']) - 10} more")
    else:
        print("✓ All canonical tags match expected URLs - this is good!")
    
    print("\n" + "=" * 80)
    print("ISSUE #4: PAGES NOT IN SITEMAP")
    print("=" * 80)
    if issues['not_in_sitemap']:
        print(f"Found {len(issues['not_in_sitemap'])} pages not in sitemap:")
        for item in issues['not_in_sitemap'][:10]:
            print(f"  • {item['url']}")
        if len(issues['not_in_sitemap']) > 10:
            print(f"  ... and {len(issues['not_in_sitemap']) - 10} more")
    else:
        print("✓ All HTML files are in sitemap - this is good!")
    
    print("\n" + "=" * 80)
    print("ISSUE #5: THIN CONTENT (<300 words)")
    print("=" * 80)
    if issues['thin_content']:
        print(f"Found {len(issues['thin_content'])} pages with thin content:")
        for item in sorted(issues['thin_content'], key=lambda x: x['words'])[:10]:
            print(f"  • {item['file']} ({item['words']} words)")
        if len(issues['thin_content']) > 10:
            print(f"  ... and {len(issues['thin_content']) - 10} more")
    else:
        print("✓ All pages have substantial content - this is good!")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    if issues['noindex']:
        print("\n1. NOINDEX TAGS:")
        print("   Remove noindex from posts you want indexed")
        print("   Keep noindex on thank-you pages, search pages, etc.")
    
    if not issues['redirects']:
        print("\n2. REDIRECTS (212 in GSC):")
        print("   No meta redirects found in HTML files.")
        print("   ACTION NEEDED:")
        print("   - Check Google Search Console for specific URLs")
        print("   - These are likely OLD URLs that changed")
        print("   - Update internal links to use new URLs")
        print("   - Submit updated sitemap to GSC")
    
    if issues['canonical_mismatch']:
        print("\n3. CANONICAL TAGS:")
        print("   Fix canonical mismatches in templates")
    
    if issues['not_in_sitemap']:
        print("\n4. SITEMAP:")
        print("   Add missing pages to sitemap.xml")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("""
1. Export the 404 list from Google Search Console
   - Go to GSC → Indexing → Pages
   - Filter by "Not found (404)"
   - Export the list

2. Export the redirect list from GSC
   - Filter by "Page with redirect"
   - Export the list

3. Create a mapping of old URLs → new URLs

4. Update app.py to add strategic redirects

5. Re-freeze the site and push to GitHub
    """)

if __name__ == "__main__":
    analyze_site()
