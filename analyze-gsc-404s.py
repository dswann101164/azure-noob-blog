"""
404 Error Analyzer and Auto-Fixer
Analyzes 404 URLs from GSC and suggests fixes

USAGE:
1. Export 404 errors from Google Search Console
2. Save as gsc-404s.csv
3. Run this script
"""

import csv
import re
from pathlib import Path
from difflib import SequenceMatcher
from urllib.parse import urlparse, unquote

def load_live_urls():
    """Load all live URLs from sitemap"""
    import xml.etree.ElementTree as ET
    
    urls = set()
    sitemap_path = Path('docs') / 'sitemap.xml'
    
    if sitemap_path.exists():
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        namespace = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for url in root.findall('.//sm:loc', namespace):
            urls.add(url.text.lower())
    
    return urls

def find_similar_url(broken_url, live_urls, threshold=0.7):
    """Find similar live URLs using fuzzy matching"""
    broken_path = urlparse(broken_url).path.lower()
    
    best_match = None
    best_ratio = 0
    
    for live_url in live_urls:
        live_path = urlparse(live_url).path.lower()
        ratio = SequenceMatcher(None, broken_path, live_path).ratio()
        
        if ratio > best_ratio and ratio >= threshold:
            best_ratio = ratio
            best_match = live_url
    
    return best_match, best_ratio

def categorize_404(url, live_urls):
    """Categorize the 404 error"""
    parsed = urlparse(url)
    path = parsed.path.lower()
    
    # Common 404 patterns
    if '.xml' in path or '.txt' in path:
        return 'config_file', None
    
    if '/feed' in path or '/rss' in path:
        return 'feed', None
    
    if 'wp-content' in path or 'wordpress' in path:
        return 'wordpress_artifact', None
    
    if 'index.php' in path or '.php' in path:
        return 'php_file', None
    
    # Check for similar URLs (typos, old slugs)
    similar, ratio = find_similar_url(url, live_urls)
    if similar and ratio > 0.8:
        return 'likely_redirect', similar
    elif similar and ratio > 0.6:
        return 'possible_redirect', similar
    
    return 'unknown', None

def analyze_404s(csv_file):
    """Analyze 404 URLs from GSC export"""
    broken_urls = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get('URL', row.get('url', '')).strip()
                if url:
                    broken_urls.append(url)
    except FileNotFoundError:
        print(f"❌ File not found: {csv_file}")
        print("\nTo use this tool:")
        print("1. Go to Google Search Console")
        print("2. Navigate to Indexing → Pages")
        print("3. Click 'Not found (404)' filter")
        print("4. Export the data")
        print("5. Save as 'gsc-404s.csv' in the blog root")
        return None
    
    return broken_urls

def main():
    print("=" * 80)
    print("404 ERROR ANALYZER")
    print("=" * 80)
    
    csv_file = 'gsc-404s.csv'
    broken_urls = analyze_404s(csv_file)
    
    if not broken_urls:
        return
    
    print(f"\n✓ Found {len(broken_urls)} 404 URLs")
    print("\nLoading live URLs from sitemap...")
    live_urls = load_live_urls()
    print(f"✓ Found {len(live_urls)} live URLs")
    
    # Categorize each 404
    results = {
        'likely_redirect': [],
        'possible_redirect': [],
        'wordpress_artifact': [],
        'config_file': [],
        'feed': [],
        'php_file': [],
        'unknown': []
    }
    
    for url in broken_urls:
        category, suggestion = categorize_404(url, live_urls)
        results[category].append({
            'url': url,
            'suggestion': suggestion
        })
    
    # Print results
    print("\n" + "=" * 80)
    print("404 ANALYSIS RESULTS")
    print("=" * 80)
    
    if results['likely_redirect']:
        print(f"\n🎯 LIKELY REDIRECTS ({len(results['likely_redirect'])} URLs)")
        print("These are probably typos or old URLs that should redirect:")
        for item in results['likely_redirect'][:10]:
            print(f"\n  FROM: {item['url']}")
            print(f"  TO:   {item['suggestion']}")
        if len(results['likely_redirect']) > 10:
            print(f"\n  ... and {len(results['likely_redirect']) - 10} more")
    
    if results['possible_redirect']:
        print(f"\n⚠️  POSSIBLE REDIRECTS ({len(results['possible_redirect'])} URLs)")
        print("These might be old URLs - review manually:")
        for item in results['possible_redirect'][:5]:
            print(f"\n  FROM: {item['url']}")
            print(f"  TO:   {item['suggestion']} (similarity: ~70%)")
        if len(results['possible_redirect']) > 5:
            print(f"\n  ... and {len(results['possible_redirect']) - 5} more")
    
    if results['wordpress_artifact']:
        print(f"\n🗑️  WORDPRESS ARTIFACTS ({len(results['wordpress_artifact'])} URLs)")
        print("These are leftover WordPress URLs - safe to ignore:")
        for item in results['wordpress_artifact'][:5]:
            print(f"  • {item['url']}")
    
    if results['config_file']:
        print(f"\n📄 CONFIG FILES ({len(results['config_file'])} URLs)")
        print("These are config files that don't exist - safe to ignore:")
        for item in results['config_file'][:5]:
            print(f"  • {item['url']}")
    
    if results['feed']:
        print(f"\n📡 FEED URLS ({len(results['feed'])} URLs)")
        print("These are feed URLs - check if feed.xml exists:")
        for item in results['feed'][:5]:
            print(f"  • {item['url']}")
    
    if results['unknown']:
        print(f"\n❓ UNKNOWN ({len(results['unknown'])} URLs)")
        print("These need manual review:")
        for item in results['unknown'][:10]:
            print(f"  • {item['url']}")
    
    # Generate redirect rules
    if results['likely_redirect']:
        print("\n" + "=" * 80)
        print("SUGGESTED REDIRECT RULES FOR app.py")
        print("=" * 80)
        print("\nAdd these to the strategic_redirects dictionary:\n")
        
        for item in results['likely_redirect']:
            from_path = urlparse(item['url']).path
            to_path = urlparse(item['suggestion']).path
            print(f"    '{from_path}': '{to_path}',")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("""
1. Review the LIKELY REDIRECTS and add them to app.py
2. For POSSIBLE REDIRECTS, manually verify they're correct
3. Ignore WordPress artifacts and config files
4. After adding redirects:
   a) Run freeze.py
   b) Push to GitHub
   c) Wait 24-48 hours
   d) Use GSC to request removal of old URLs

To remove 404s from Google:
1. Go to GSC → Removals
2. New Request → Remove URL
3. Add each 404 URL
4. Google will remove from search results
    """)

if __name__ == "__main__":
    main()
