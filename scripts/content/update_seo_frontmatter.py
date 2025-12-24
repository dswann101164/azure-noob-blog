#!/usr/bin/env python3
"""
SEO Frontmatter Updater for Azure Noob Blog
Updates YAML frontmatter in posts to improve Google Search Console CTR
"""

import os
import re
from pathlib import Path

# Mapping of search queries to optimized frontmatter
SEO_UPDATES = {
    "kql": {
        "title": "Azure KQL Cheat Sheet | Log Analytics Query Language Examples + Free PDF",
        "summary": "Complete KQL cheat sheet for Azure Resource Graph. Query VMs, NICs, disks, NSGs with copy-paste examples. Free PDF download for Azure admins and architects.",
        "tags": ["Azure", "KQL", "Log Analytics", "Resource Graph", "Cheat Sheet"],
        "keywords": ["kql cheat sheet", "azure log analytics", "resource graph queries"]
    },
    "migration": {
        "title": "Common Azure Migration Mistakes | Enterprise Cloud Migration Failures to Avoid",
        "summary": "Real Azure migration mistakes from enterprise projects. Why lift-and-shift fails, how to avoid cost overruns, and what Microsoft doesn't tell you about cloud migration.",
        "tags": ["Azure", "Migration", "Cloud Strategy", "Enterprise"],
        "keywords": ["azure migration mistakes", "cloud migration failures", "azure migration best practices"]
    },
    "tagging": {
        "title": "Azure Resource Tagging Best Practices | Cost Allocation & FinOps Strategy",
        "summary": "Enterprise Azure tagging strategy for cost allocation, RBAC, and compliance. Why basic tagging fails and how to implement tags that actually work at scale.",
        "tags": ["Azure", "FinOps", "Cost Management", "Tagging", "Best Practices"],
        "keywords": ["azure resource tagging", "azure tagging best practices", "azure cost allocation"]
    },
    "raci": {
        "title": "Azure RACI Matrix | Cloud Responsibility Assignment for Enterprise IT",
        "summary": "RACI matrix template for Azure operations. Define responsibilities across security, networking, compute, and cost management. Free downloadable template for enterprise teams.",
        "tags": ["Azure", "Governance", "RACI", "Enterprise", "Operations"],
        "keywords": ["azure raci matrix", "cloud responsibility matrix", "azure governance"]
    },
    "cmdb": {
        "title": "Building an Azure CMDB | Resource Inventory with Azure Resource Graph and KQL",
        "summary": "How to build a Configuration Management Database for Azure using Resource Graph, KQL queries, and automation. Track 31,000+ resources across 44 subscriptions.",
        "tags": ["Azure", "CMDB", "Resource Graph", "KQL", "Inventory"],
        "keywords": ["cmdb azure", "azure resource inventory", "azure configuration management"]
    },
    "ipam": {
        "title": "Azure IPAM Solution | IP Address Management for Enterprise Networks",
        "summary": "Custom Azure IPAM tool for managing IP addresses across multiple subscriptions and VNets. Track subnets, prevent conflicts, and maintain network documentation.",
        "tags": ["Azure", "IPAM", "Networking", "IP Management", "Tools"],
        "keywords": ["azure ipam", "azure ip management", "azure network management"]
    },
    "icons": {
        "title": "Azure Icons Reference | Complete Microsoft Azure Architecture Icons Library",
        "summary": "Complete Azure icons reference with download links. Official Microsoft Azure architecture icons for Visio, PowerPoint, and diagrams. Updated for 2025.",
        "tags": ["Azure", "Icons", "Architecture", "Diagrams", "Reference"],
        "keywords": ["azure icons", "microsoft azure icons", "azure architecture icons"]
    },
    "private-dns": {
        "title": "Azure Private DNS Resolver | Complete Setup Guide for Hybrid DNS Resolution",
        "summary": "Step-by-step Azure Private DNS Resolver setup for hybrid cloud environments. Connect on-premises DNS with Azure Private DNS zones securely.",
        "tags": ["Azure", "DNS", "Private DNS", "Networking", "Hybrid Cloud"],
        "keywords": ["azure private dns resolver", "azure private dns", "hybrid dns azure"]
    }
}


def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content"""
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return None, content


def update_frontmatter_field(frontmatter, field, value):
    """Update or add a field in YAML frontmatter"""
    pattern = f'^{field}:.*$'
    
    if isinstance(value, list):
        # Handle list values (tags, keywords)
        new_value = f'{field}: {value}'
        if re.search(pattern, frontmatter, re.MULTILINE):
            frontmatter = re.sub(pattern, new_value, frontmatter, flags=re.MULTILINE)
        else:
            frontmatter += f'\n{field}: {value}'
    else:
        # Handle string values (title, summary)
        new_value = f'{field}: "{value}"'
        if re.search(pattern, frontmatter, re.MULTILINE):
            frontmatter = re.sub(pattern, new_value, frontmatter, flags=re.MULTILINE)
        else:
            frontmatter += f'\n{field}: "{value}"'
    
    return frontmatter


def detect_post_type(filename, content):
    """Detect which SEO update to apply based on filename and content"""
    filename_lower = filename.lower()
    content_lower = content.lower()
    
    for key, updates in SEO_UPDATES.items():
        if key in filename_lower or key in content_lower:
            return key, updates
    
    return None, None


def update_post(filepath):
    """Update a single post with optimized frontmatter"""
    print(f"\nProcessing: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    frontmatter, body = extract_frontmatter(content)
    if not frontmatter:
        print(f"  ⚠ No frontmatter found, skipping")
        return False
    
    # Detect which update to apply
    post_type, updates = detect_post_type(filepath.name, content)
    
    if not post_type:
        print(f"  ℹ No SEO update needed")
        return False
    
    print(f"  ✓ Detected as '{post_type}' post")
    print(f"  → Updating title: {updates['title'][:60]}...")
    
    # Update frontmatter fields
    new_frontmatter = frontmatter
    new_frontmatter = update_frontmatter_field(new_frontmatter, 'title', updates['title'])
    new_frontmatter = update_frontmatter_field(new_frontmatter, 'summary', updates['summary'])
    
    # Update tags if provided
    if 'tags' in updates:
        new_frontmatter = update_frontmatter_field(new_frontmatter, 'tags', updates['tags'])
    
    # Add keywords field if provided (for future SEO)
    if 'keywords' in updates:
        new_frontmatter = update_frontmatter_field(new_frontmatter, 'keywords', updates['keywords'])
    
    # Reconstruct the file
    new_content = f"---\n{new_frontmatter.strip()}\n---\n{body}"
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✅ Updated successfully")
    return True


def main():
    """Main function to update all posts"""
    posts_dir = Path('posts')
    
    if not posts_dir.exists():
        print("❌ Error: 'posts' directory not found!")
        print("   Make sure you're running this script from your blog root directory")
        return
    
    print("🔍 Azure Noob Blog - SEO Frontmatter Updater")
    print("=" * 60)
    
    updated_count = 0
    total_count = 0
    
    for post_file in sorted(posts_dir.glob('*.md')):
        total_count += 1
        if update_post(post_file):
            updated_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Complete: Updated {updated_count} of {total_count} posts")
    print("\nNext steps:")
    print("1. Review the changes: git diff posts/")
    print("2. Freeze the site: python freeze.py")
    print("3. Commit and push: git add posts docs && git commit -m 'SEO: Optimize post titles and meta descriptions' && git push")


if __name__ == '__main__':
    main()
