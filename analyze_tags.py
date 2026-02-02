import os
import re
from collections import Counter

posts_dir = r"C:\Users\dswann\Documents\GitHub\azure-noob-blog\posts"
all_tags = []

for filename in os.listdir(posts_dir):
    if not filename.endswith('.md'):
        continue
    
    filepath = os.path.join(posts_dir, filename)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue
    
    # Extract frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        continue
    
    frontmatter = match.group(1)
    
    # Extract tags array
    tags_match = re.search(r'tags:\s*\[(.*?)\]', frontmatter, re.DOTALL)
    if not tags_match:
        continue
    
    tags_str = tags_match.group(1)
    
    # Parse tags (handle quotes and commas)
    tags = re.findall(r'["\']([^"\']+)["\']', tags_str)
    all_tags.extend(tags)

# Count tag usage
tag_counts = Counter(all_tags)

print(f"Total tags found: {len(all_tags)}")
print(f"Unique tags: {len(tag_counts)}")
print()

# Save all unique tags
with open('all_tags_from_posts.txt', 'w', encoding='utf-8') as f:
    for tag in sorted(tag_counts.keys()):
        f.write(f"{tag}\n")

# Save tag counts
with open('tag_usage_counts.txt', 'w', encoding='utf-8') as f:
    for tag, count in sorted(tag_counts.items(), key=lambda x: (-x[1], x[0])):
        f.write(f"{count:3d} {tag}\n")

print("Created all_tags_from_posts.txt")
print("Created tag_usage_counts.txt")
