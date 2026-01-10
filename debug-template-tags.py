# Debug what tags_index() is actually passing to the template
import sys
sys.path.insert(0, '.')

from app import app, get_all_tags, load_posts, slugify_tag

with app.test_request_context():
    all_tags = get_all_tags()
    posts = load_posts()
    
    tag_posts = {}
    tags_with_counts = []
    
    for tag_slug in all_tags:
        tag_posts[tag_slug] = [p for p in posts if any(slugify_tag(t) == tag_slug for t in p['tags'])]
        tags_with_counts.append((tag_slug, len(tag_posts[tag_slug])))
    
    print(f"Total tags being passed to template: {len(tags_with_counts)}")
    print("\nFirst 20 tags (what template receives):")
    for i, (tag, count) in enumerate(tags_with_counts[:20]):
        print(f"  {i+1}. '{tag}' ({count} posts)")
    
    # Check for problem tags
    print("\nLooking for problem tags:")
    problem_tags = ['Active Directory', 'active-directory', 'Azure AD', 'azure-ad', 'Hybrid Cloud', 'hybrid-cloud']
    for tag in problem_tags:
        found = any(t == tag for t, c in tags_with_counts)
        if found:
            print(f"  ✗ FOUND: '{tag}'")
        else:
            print(f"  ✓ Not found: '{tag}'")
