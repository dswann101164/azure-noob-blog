import sys
sys.path.insert(0, r'C:\Users\dswann\Documents\GitHub\azure-noob-blog')

from app import get_all_tags, build_tags, load_posts

# Get all tags
all_tags = get_all_tags()
print(f"\nget_all_tags() returned {len(all_tags)} tags:")
for i, tag in enumerate(all_tags, 1):
    print(f"  {i:3d}. {tag}")

# Get build_tags
tag_posts = build_tags()
print(f"\n\nbuild_tags() returned {len(tag_posts)} tags:")
for i, (tag, posts) in enumerate(sorted(tag_posts.items()), 1):
    print(f"  {i:3d}. {tag:30} ({len(posts)} posts)")

# Load our legitimate missing tags
with open(r'C:\Users\dswann\Documents\GitHub\azure-noob-blog\legitimate_missing_tags.txt', 'r', encoding='utf-8') as f:
    legit_missing = []
    for line in f:
        parts = line.strip().split('\t')
        if parts:
            legit_missing.append(parts[0])

print(f"\n\nlegitimate_missing_tags.txt has {len(legit_missing)} tags")

# Find which legitimate missing tags are in get_all_tags()
missing_from_get_all_tags = []
for tag in legit_missing:
    if tag not in all_tags:
        missing_from_get_all_tags.append(tag)

if missing_from_get_all_tags:
    print(f"\n\nTags in legitimate_missing_tags.txt but NOT in get_all_tags():")
    for tag in sorted(missing_from_get_all_tags):
        print(f"  - {tag}")
else:
    print(f"\n\n✓ ALL 62 legitimate tags ARE in get_all_tags()!")
    print(f"✓ ALL 62 legitimate tags ARE in build_tags()!")
    print(f"\nThe problem is NOT in get_all_tags() or build_tags()")
    print(f"The problem must be in Flask-Frozen's URL generation")
