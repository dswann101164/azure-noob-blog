# Test what build_tags() returns
import sys
sys.path.insert(0, '.')

from app import build_tags

tags = build_tags()
print(f"Total tags: {len(tags)}")
print("\nFirst 10 tag keys:")
for i, key in enumerate(list(tags.keys())[:10]):
    print(f"  {i+1}. '{key}'")

# Check for specific duplicates
problem_tags = ['Active Directory', 'active-directory', 'Azure AD', 'azure-ad']
print("\nChecking for problem tags:")
for tag in problem_tags:
    if tag in tags:
        print(f"  ✓ Found: '{tag}' ({len(tags[tag])} posts)")
