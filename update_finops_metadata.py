#!/usr/bin/env python
"""
Update front-matter for FinOps posts based on a metadata map.

- Derives slug from filename (YYYY-MM-DD-slug.md -> slug)
- If slug is in FINOPS_METADATA, updates:
    title, summary, tags, cover, slug, hub
- Preserves any other existing front-matter fields.
"""

import os
import re
import sys

try:
    import yaml
except ImportError:
    print("This script requires PyYAML. Install with: pip install pyyaml")
    sys.exit(1)

POSTS_DIR = "posts"

# ---------------------------------------------------------------------
# FinOps metadata map (slug -> front-matter fields)
# ---------------------------------------------------------------------

FINOPS_METADATA = {
    "azure-cost-reports-business-reality": {
        "title": "Why Your Azure Cost Reports Don’t Match Business Reality",
        "summary": "Azure Cost Management often conflicts with how businesses track spend. Here's why your cost reports never align and how to fix it at scale.",
        "tags": ["Azure", "FinOps", "Cost Management", "Governance", "Reporting"],
        "cover": "/static/images/hero/azure-finops-business-reality.png",
        "hub": "finops",
    },
    "azure-costs-apps-not-subscriptions": {
        "title": "Azure Costs Follow Applications, Not Subscriptions",
        "summary": "Azure bills at the subscription level—but the business thinks in terms of applications. Here's how to realign cost models for reality.",
        "tags": ["Azure", "FinOps", "Cost Allocation", "Application Mapping", "Governance"],
        "cover": "/static/images/hero/azure-finops-apps-vs-subscriptions.png",
        "hub": "finops",
    },
    "azure-cost-management-is-confusing-but-you-can-tame-it": {
        "title": "Azure Cost Management Is Confusing—But You Can Tame It",
        "summary": "Azure Cost Management has too many blades, scopes, and exports. Learn the core workflows you actually need to make FinOps sustainable.",
        "tags": ["Azure", "FinOps", "Cost Management", "Billing", "Optimization"],
        "cover": "/static/images/hero/azure-cost-management-tame.png",
        "hub": "finops",
    },
    "azure-cost-optimization-facade": {
        "title": "The Azure Cost Optimization Facade",
        "summary": "Most Azure optimization advice is surface-level. Reserved instances aren’t FinOps. Here’s what meaningful cost reduction really takes.",
        "tags": ["Azure", "FinOps", "Cost Optimization", "Advisor", "Governance"],
        "cover": "/static/images/hero/azure-cost-optimization-facade.png",
        "hub": "finops",
    },
    "azure-cost-optimization-complete-guide": {
        "title": "Azure Cost Optimization: A Complete Practical Guide",
        "summary": "A real-world guide to optimizing Azure costs using rightsizing, automation, cleanup, governance, tags, and financial accountability.",
        "tags": ["Azure", "FinOps", "Cost Optimization", "Automation", "Governance"],
        "cover": "/static/images/hero/azure-cost-optimization-guide.png",
        "hub": "finops",
    },
    "azure-resource-tags-guide": {
        "title": "Azure Resource Tagging: The Guide Microsoft Should Have Written",
        "summary": "Tags are the backbone of FinOps—but most enterprises misuse them. Learn how to design, enforce, and automate a tag strategy that works.",
        "tags": ["Azure", "Tags", "FinOps", "Governance", "Automation"],
        "cover": "/static/images/hero/azure-tags-guide.png",
        "hub": "finops",
    },
    "azure-chargeback-tags-model": {
        "title": "Designing an Azure Chargeback Model with Tags",
        "summary": "A practical tag-driven model for allocating Azure costs to applications, teams, and cost centers. No EA contract needed.",
        "tags": ["Azure", "FinOps", "Chargeback", "Showback", "Tags"],
        "cover": "/static/images/hero/azure-chargeback-model.png",
        "hub": "finops",
    },
    "azure-tag-governance-policy": {
        "title": "Azure Tag Governance: Policy Patterns That Actually Work",
        "summary": "Deny, append, and remediation policies that enforce tag governance without breaking deployments. Real patterns from production Azure.",
        "tags": ["Azure", "Tags", "Governance", "Azure Policy", "FinOps"],
        "cover": "/static/images/hero/azure-tag-governance.png",
        "hub": "finops",
    },
    "resource-tags-100k-problem": {
        "title": "The 100,000 Tag Problem in Enterprise Azure",
        "summary": "Large Azure estates accumulate tens of thousands of tag variations. Here’s how to audit, normalize, and govern tags at massive scale.",
        "tags": ["Azure", "Tags", "FinOps", "Governance", "Compliance"],
        "cover": "/static/images/hero/azure-tags-100k.png",
        "hub": "finops",
    },
    "tag-governance-247-variations": {
        "title": "Tag Governance: The 24/7 Reality Nobody Talks About",
        "summary": "Tag governance doesn’t fail in meetings—it fails during real deployments. Why operational drift destroys tag rules and how to fix it.",
        "tags": ["Azure", "Tags", "Governance", "FinOps", "Operations"],
        "cover": "/static/images/hero/azure-tag-governance-reality.png",
        "hub": "finops",
    },
    "azure-cost-reporting-boardroom": {
        "title": "How to Present Azure Costs in the Boardroom",
        "summary": "Executives don’t care about vCores or storage accounts. Learn how to translate Azure costs into a business narrative leaders actually understand.",
        "tags": ["Azure", "FinOps", "Reporting", "Executive", "Cost Management"],
        "cover": "/static/images/hero/azure-cost-boardroom.png",
        "hub": "finops",
    },
    "azure-openai-pricing-real-costs": {
        "title": "Azure OpenAI Pricing: The Real Costs Nobody Shows You",
        "summary": "Azure OpenAI usage looks cheap—until it doesn't. A real breakdown of hidden costs and how to prevent runaway AI spending in Azure.",
        "tags": ["Azure", "FinOps", "AI", "OpenAI", "Cost Management"],
        "cover": "/static/images/hero/azure-openai-costs.png",
        "hub": "finops",
    },
}


def slug_from_filename(filename: str) -> str:
    """Extract slug from filename like 2025-09-24-azure-cost-...md -> azure-cost-..."""
    base = os.path.splitext(filename)[0]
    m = re.match(r"^\d{4}-\d{2}-\d{2}-(.+)$", base)
    return m.group(1) if m else base


def split_front_matter(content: str):
    """
    Split a markdown file into (front_matter_text, body_text).
    Returns (None, content) if no YAML front-matter is found.
    """
    if not content.lstrip().startswith("---"):
        return None, content

    # Find first two occurrences of '---' at line start
    lines = content.splitlines(True)  # keep line endings
    if not lines:
        return None, content

    if not lines[0].strip().startswith("---"):
        return None, content

    fm_lines = []
    body_lines = []
    in_fm = True
    # start from line 1, we've already consumed the opening ---
    for line in lines[1:]:
        if in_fm and line.strip().startswith("---"):
            in_fm = False
            continue
        if in_fm:
            fm_lines.append(line)
        else:
            body_lines.append(line)

    if not fm_lines:
        return None, content

    fm_text = "".join(fm_lines)
    body_text = "".join(body_lines)
    return fm_text, body_text


def process_post(path: str):
    filename = os.path.basename(path)
    slug = slug_from_filename(filename)

    if slug not in FINOPS_METADATA:
        return False  # not a FinOps post we care about

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    fm_text, body = split_front_matter(content)
    if fm_text is None:
        print(f"[WARN] No front-matter found in {filename}, skipping.")
        return False

    try:
        fm = yaml.safe_load(fm_text) or {}
    except Exception as e:
        print(f"[ERROR] Failed to parse YAML in {filename}: {e}")
        return False

    meta = FINOPS_METADATA[slug]

    # Update front-matter fields
    fm["title"] = meta["title"]
    fm["summary"] = meta["summary"]
    fm["tags"] = meta["tags"]
    fm["cover"] = meta["cover"]
    fm["slug"] = slug  # ensure slug matches
    fm["hub"] = meta["hub"]

    # Dump YAML back, preserving key order if possible
    new_fm_text = yaml.safe_dump(
        fm, sort_keys=False, allow_unicode=True
    ).strip() + "\n"

    new_content = "---\n" + new_fm_text + "---\n" + body

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[UPDATED] {filename} ({slug})")
    return True


def main():
    posts_path = POSTS_DIR
    if not os.path.isdir(posts_path):
        print(f"Posts directory not found: {posts_path}")
        sys.exit(1)

    updated_count = 0
    for filename in os.listdir(posts_path):
        if not filename.endswith(".md"):
            continue
        full_path = os.path.join(posts_path, filename)
        if process_post(full_path):
            updated_count += 1

    print(f"\nDone. Updated {updated_count} FinOps post(s).")


if __name__ == "__main__":
    main()
