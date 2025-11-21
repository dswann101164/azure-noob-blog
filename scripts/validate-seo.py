"""
SEO Validator for Azure Noob Blog
Checks posts for SEO issues before publishing
No API calls - pure validation logic
"""

from pathlib import Path
import re
import yaml
import sys

def validate_post_seo(filepath: Path) -> list:
    """Returns list of SEO issues found"""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"❌ {filepath.name}: Could not read file - {e}"]
    
    # Extract frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return [f"❌ {filepath.name}: No YAML frontmatter found"]
    
    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return [f"❌ {filepath.name}: Invalid YAML frontmatter - {e}"]
    
    # Check title
    title = fm.get('title', '')
    if not title:
        issues.append(f"❌ {filepath.name}: Missing title")
    elif len(title) > 60:
        issues.append(f"⚠️  {filepath.name}: Title is {len(title)} chars (recommend max 60 for SEO)")
    
    # Check summary (your current field)
    summary = fm.get('summary', '')
    if not summary:
        issues.append(f"⚠️  {filepath.name}: Missing summary field")
    elif len(summary) > 160:
        issues.append(f"⚠️  {filepath.name}: Summary is {len(summary)} chars (recommend 150-160 for SEO)")
    
    # Check meta_description (optional enhanced field)
    meta_desc = fm.get('meta_description', '')
    if meta_desc and len(meta_desc) > 160:
        issues.append(f"⚠️  {filepath.name}: Meta description too long ({len(meta_desc)} chars)")
    
    # Check tags
    tags = fm.get('tags', [])
    if not tags:
        issues.append(f"⚠️  {filepath.name}: No tags defined")
    elif len(tags) < 3:
        issues.append(f"⚠️  {filepath.name}: Only {len(tags)} tag(s) - recommend 5-7 for better discovery")
    
    # Check date format
    date = fm.get('date', '')
    if not date:
        issues.append(f"⚠️  {filepath.name}: Missing date field")
    elif not re.match(r'^\d{4}-\d{2}-\d{2}$', str(date)):
        issues.append(f"⚠️  {filepath.name}: Date should be YYYY-MM-DD format")
    
    # Check cover image
    cover = fm.get('cover', '')
    if not cover:
        issues.append(f"⚠️  {filepath.name}: Missing cover image")
    
    if not issues:
        print(f"✓ {filepath.name}")
    
    return issues


def main():
    posts_dir = Path("posts")
    
    if not posts_dir.exists():
        print("❌ posts/ directory not found")
        sys.exit(1)
    
    posts = list(posts_dir.glob("*.md"))
    if not posts:
        print("❌ No markdown posts found in posts/")
        sys.exit(1)
    
    print(f"Validating {len(posts)} posts...\n")
    
    all_issues = []
    for post in sorted(posts):
        issues = validate_post_seo(post)
        all_issues.extend(issues)
    
    if all_issues:
        print("\n" + "="*60)
        print("SEO ISSUES FOUND")
        print("="*60)
        for issue in all_issues:
            print(issue)
        print("\n💡 Fix these issues in your markdown files before publishing.")
        print("   Focus on: title length, summary/meta_description, and tags.")
        sys.exit(1)  # Exit with error code to stop publish workflow
    else:
        print("\n" + "="*60)
        print("✓ ALL POSTS HAVE SOLID SEO!")
        print("="*60)
        sys.exit(0)


if __name__ == "__main__":
    main()
