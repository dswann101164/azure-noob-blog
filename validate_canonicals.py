# validate_canonicals.py
"""
Validates that all generated HTML files have proper canonical tags
and that there are no duplicate URL patterns in the frozen site.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

DOCS_DIR = "docs"
SITE_URL = "https://azure-noob.com"

def find_all_html_files():
    """Find all HTML files in docs/"""
    html_files = []
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                html_files.append(full_path)
    return html_files

def extract_canonical(html_path):
    """Extract canonical URL from HTML file"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read(5000)  # Only read first 5000 chars (head section)
            
        # Look for canonical tag
        match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](https?://[^"\']+)["\']', content)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Error reading {html_path}: {e}")
    
    return None

def url_from_filepath(filepath):
    """Convert file path to URL"""
    # Remove docs/ prefix
    rel_path = filepath.replace(DOCS_DIR, '').replace('\\', '/')
    
    # Remove index.html
    rel_path = rel_path.replace('/index.html', '')
    
    # Remove .html extension
    rel_path = rel_path.replace('.html', '')
    
    # Ensure starts with /
    if not rel_path.startswith('/'):
        rel_path = '/' + rel_path
    
    # Root becomes just /
    if rel_path == '/':
        return f"{SITE_URL}/"
    
    # Everything else has NO trailing slash
    return f"{SITE_URL}{rel_path.rstrip('/')}"

def find_duplicate_urls():
    """Find HTML files that represent the same logical URL"""
    url_to_files = defaultdict(list)
    
    html_files = find_all_html_files()
    
    for filepath in html_files:
        url = url_from_filepath(filepath)
        url_to_files[url].append(filepath)
    
    # Find duplicates
    duplicates = {url: files for url, files in url_to_files.items() if len(files) > 1}
    
    return duplicates

def validate_canonical_tags():
    """Check all HTML files have correct canonical tags"""
    issues = []
    html_files = find_all_html_files()
    
    print(f"\nValidating {len(html_files)} HTML files...")
    
    for filepath in html_files:
        # Skip validation for static HTML files (they have noindex anyway)
        if '\\static\\' in filepath or '/static/' in filepath:
            continue
            
        expected_url = url_from_filepath(filepath)
        canonical = extract_canonical(filepath)
        
        if not canonical:
            issues.append({
                'type': 'missing_canonical',
                'file': filepath,
                'expected': expected_url
            })
        elif canonical != expected_url:
            # Check if it's just a trailing slash difference
            if canonical.rstrip('/') != expected_url.rstrip('/'):
                # Also ignore case-only differences (for tags)
                if canonical.lower().rstrip('/') != expected_url.lower().rstrip('/'):
                    issues.append({
                        'type': 'wrong_canonical',
                        'file': filepath,
                        'found': canonical,
                        'expected': expected_url
                    })
    
    return issues

def main():
    print("="*80)
    print("CANONICAL URL VALIDATOR")
    print("="*80)
    
    # Check for duplicate URLs
    print("\n1. Checking for duplicate URL patterns...")
    duplicates = find_duplicate_urls()
    
    if duplicates:
        print(f"\n❌ Found {len(duplicates)} duplicate URLs:")
        for url, files in duplicates.items():
            print(f"\n  URL: {url}")
            for f in files:
                print(f"    - {f}")
    else:
        print("✓ No duplicate URLs found")
    
    # Check canonical tags
    print("\n2. Validating canonical tags...")
    issues = validate_canonical_tags()
    
    if issues:
        print(f"\n❌ Found {len(issues)} canonical tag issues:\n")
        
        missing = [i for i in issues if i['type'] == 'missing_canonical']
        wrong = [i for i in issues if i['type'] == 'wrong_canonical']
        
        if missing:
            print(f"\nMissing canonical tags ({len(missing)}):")
            for issue in missing[:10]:  # Show first 10
                print(f"  {issue['file']}")
                print(f"    Expected: {issue['expected']}")
        
        if wrong:
            print(f"\nWrong canonical tags ({len(wrong)}):")
            for issue in wrong[:10]:  # Show first 10
                print(f"  {issue['file']}")
                print(f"    Found:    {issue['found']}")
                print(f"    Expected: {issue['expected']}")
    else:
        print("✓ All canonical tags are correct")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Duplicate URLs: {len(duplicates)}")
    print(f"Canonical issues: {len(issues)}")
    
    if duplicates or issues:
        print("\n❌ VALIDATION FAILED")
        return 1
    else:
        print("\n✓ VALIDATION PASSED")
        return 0

if __name__ == '__main__':
    exit(main())
