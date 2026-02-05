#!/usr/bin/env python3
"""
Fix all tags in all blog posts to use lowercase-hyphenated format.
This eliminates 404 errors from mixed case and spaces in tag URLs.
"""
import os
import re
import sys
from pathlib import Path

def slugify_tag(tag):
    """Convert tag to URL-safe slug: lowercase with hyphens."""
    return tag.lower().replace(' ', '-').replace(',', '').strip()

def fix_post_tags(filepath):
    """
    Read a post, fix all tags to lowercase-hyphenated format, write back.
    Returns (original_tags, fixed_tags, changed) tuple.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract YAML frontmatter
    if not content.startswith('---'):
        return ([], [], False)
    
    # Find tags line
    tags_match = re.search(r'^tags:\s*\[(.*?)\]\s*$', content, re.MULTILINE)
    if not tags_match:
        return ([], [], False)
    
    tags_line = tags_match.group(0)
    tags_content = tags_match.group(1)
    
    # Parse tags
    original_tags = [t.strip().strip('"').strip("'") for t in tags_content.split(',')]
    
    # Slugify tags
    fixed_tags = [slugify_tag(tag) for tag in original_tags]
    
    # Check if any changes needed
    if original_tags == fixed_tags:
        return (original_tags, fixed_tags, False)
    
    # Build new tags line
    fixed_tags_str = ', '.join([f'"{tag}"' for tag in fixed_tags])
    new_tags_line = f'tags: [{fixed_tags_str}]'
    
    # Replace in content
    new_content = content.replace(tags_line, new_tags_line)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return (original_tags, fixed_tags, True)

def main():
    posts_dir = Path('posts')
    
    if not posts_dir.exists():
        print(f"ERROR: {posts_dir} directory not found!")
        sys.exit(1)
    
    print("=" * 80)
    print("FIXING ALL TAGS IN ALL POSTS")
    print("=" * 80)
    
    total_files = 0
    changed_files = 0
    skipped_files = 0
    all_original_tags = set()
    all_fixed_tags = set()
    
    # Process all markdown files
    for md_file in sorted(posts_dir.glob('*.md')):
        total_files += 1
        
        original, fixed, changed = fix_post_tags(md_file)
        
        all_original_tags.update(original)
        all_fixed_tags.update(fixed)
        
        if changed:
            changed_files += 1
            print(f"\n✓ {md_file.name}")
            print(f"  BEFORE: {original}")
            print(f"  AFTER:  {fixed}")
        else:
            skipped_files += 1
            if original:
                print(f"  SKIP: {md_file.name} (already correct)")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files processed: {total_files}")
    print(f"Files changed: {changed_files}")
    print(f"Files skipped (already correct): {skipped_files}")
    print(f"\nUnique original tags: {len(all_original_tags)}")
    print(f"Unique fixed tags: {len(all_fixed_tags)}")
    
    # Show problematic original tags
    problematic = sorted([t for t in all_original_tags if ' ' in t or t != t.lower()])
    if problematic:
        print(f"\n✓ FIXED {len(problematic)} problematic tags:")
        for tag in problematic:
            print(f"  '{tag}' → '{slugify_tag(tag)}'")
    else:
        print("\n✓ No problematic tags found!")
    
    print("\n" + "=" * 80)
    print("✓ TAG FIX COMPLETE - Ready to freeze site")
    print("=" * 80)

if __name__ == '__main__':
    main()
