from app import get_all_tags, build_tags

print("=== get_all_tags() ===")
all_tags = get_all_tags()
print(f"Total tags: {len(all_tags)}")
print(f"First 20 tags: {all_tags[:20]}")

print("\n=== build_tags() ===")
tags_dict = build_tags()
print(f"Total tag keys: {len(tags_dict.keys())}")
print(f"First 20 keys: {list(tags_dict.keys())[:20]}")

# Check specific tags
test_tags = ['ai', 'azure', 'architecture', 'governance', 'finops']
print(f"\n=== Checking test tags ===")
for tag in test_tags:
    if tag in tags_dict:
        print(f"  {tag}: {len(tags_dict[tag])} posts")
    else:
        print(f"  {tag}: NOT FOUND")
