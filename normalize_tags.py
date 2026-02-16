#!/usr/bin/env python3
"""
Normalize all tags in blog post frontmatter to slugified format.
"App Service" -> "app-service"
"Machine Learning" -> "machine-learning"  
"CCO Dashboard" -> "cco-dashboard"
etc.

Run from the blog root: python normalize_tags.py
"""
import os
import re
import sys

def slugify_tag(tag):
    """Convert tag to URL-safe slug."""
    return tag.lower().replace(' ', '-').replace(',', '').strip()

def normalize_post_tags(filepath):
    """Read a post, normalize its tags, write it back. Returns (changed, old_tags, new_tags)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the YAML front matter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return False, [], []
    
    frontmatter = match.group(1)
    rest_of_content = content[match.end():]
    
    # === Handle MULTI-LINE tags format ===
    # tags:
    #   - Azure
    #   - IP Management
    multi_match = re.search(r'^(tags:\s*\n)((?:\s*-\s+.*\n?)+)', frontmatter, re.MULTILINE)
    if multi_match:
        tag_block = multi_match.group(0)
        lines = multi_match.group(2).strip().split('\n')
        old_tags = []
        for line in lines:
            t = re.sub(r'^\s*-\s+', '', line).strip().strip('"').strip("'")
            if t:
                old_tags.append(t)
        
        new_tags = [slugify_tag(t) for t in old_tags]
        
        # Remove duplicates while preserving order
        seen = set()
        deduped = []
        for t in new_tags:
            if t not in seen:
                seen.add(t)
                deduped.append(t)
        new_tags = deduped
        
        if old_tags == new_tags and len(old_tags) == len(deduped):
            return False, old_tags, new_tags
        
        # Convert to single-line format
        new_tags_line = 'tags: [' + ', '.join(f'"{t}"' for t in new_tags) + ']'
        new_frontmatter = frontmatter.replace(tag_block.rstrip('\n'), new_tags_line)
        
        new_content = f'---\n{new_frontmatter}\n---\n{rest_of_content}'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, old_tags, new_tags
    
    # === Handle SINGLE-LINE tags format ===
    # tags: ["Azure", "KQL", "FinOps"]
    inline_match = re.search(r'^tags:\s*\[([^\]]*)\]\s*$', frontmatter, re.MULTILINE)
    if not inline_match:
        return False, [], []
    
    raw_tags_str = inline_match.group(1)
    # Extract individual tags - handle quoted and unquoted
    old_tags = re.findall(r'"([^"]+)"|\'([^\']+)\'', raw_tags_str)
    old_tags = [t[0] or t[1] for t in old_tags]
    old_tags = [t.strip() for t in old_tags if t.strip()]
    
    if not old_tags:
        # Try unquoted
        old_tags = [t.strip() for t in raw_tags_str.split(',') if t.strip()]
    
    new_tags = [slugify_tag(t) for t in old_tags]
    
    # Remove duplicates
    seen = set()
    deduped = []
    for t in new_tags:
        if t not in seen:
            seen.add(t)
            deduped.append(t)
    new_tags = deduped
    
    if old_tags == new_tags and len(old_tags) == len(deduped):
        return False, old_tags, new_tags
    
    # Build new tags line
    new_tags_line = 'tags: [' + ', '.join(f'"{t}"' for t in new_tags) + ']'
    old_tags_line = inline_match.group(0).strip()
    
    new_content = content.replace(old_tags_line, new_tags_line, 1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, old_tags, new_tags

def main():
    posts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'posts')
    if not os.path.exists(posts_dir):
        print(f"ERROR: posts directory not found at {posts_dir}")
        sys.exit(1)
    
    changed_count = 0
    unchanged_count = 0
    all_tag_changes = []
    
    for filename in sorted(os.listdir(posts_dir)):
        if not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(posts_dir, filename)
        if os.path.isdir(filepath):
            continue
            
        changed, old_tags, new_tags = normalize_post_tags(filepath)
        
        if changed:
            changed_count += 1
            print(f"  FIXED: {filename}")
            for old, new in zip(old_tags, new_tags):
                if old != new:
                    print(f"         {old} -> {new}")
                    all_tag_changes.append((old, new))
        else:
            unchanged_count += 1
    
    # Also check pages/ subdirectory
    pages_dir = os.path.join(posts_dir, 'pages')
    if os.path.exists(pages_dir):
        for filename in sorted(os.listdir(pages_dir)):
            if not filename.endswith('.md'):
                continue
            filepath = os.path.join(pages_dir, filename)
            if os.path.isdir(filepath):
                continue
            changed, old_tags, new_tags = normalize_post_tags(filepath)
            if changed:
                changed_count += 1
                print(f"  FIXED: pages/{filename}")
                for old, new in zip(old_tags, new_tags):
                    if old != new:
                        print(f"         {old} -> {new}")
    
    print(f"\n{'='*60}")
    print(f"RESULTS: {changed_count} posts updated, {unchanged_count} already clean")
    
    if all_tag_changes:
        unique_changes = sorted(set(all_tag_changes))
        print(f"\nUnique tag normalizations ({len(unique_changes)}):")
        for old, new in unique_changes:
            print(f"  '{old}' -> '{new}'")

if __name__ == '__main__':
    main()
