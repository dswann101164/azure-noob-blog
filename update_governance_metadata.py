#!/usr/bin/env python
"""
Update YAML front matter for Governance-related posts:
- Standardize summary
- Normalize tags

Does NOT touch 'cover' so hero images you just fixed remain intact.
"""

import sys
from pathlib import Path

import yaml  # pip install pyyaml

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"

GOV_POSTS = {
    "azure-resource-tags-guide": {
        "summary": "A practical, enterprise-focused guide to Azure resource tags: which tags matter, how to design a tag taxonomy that business owners actually use, and how to keep 31,000+ resources from turning into an ungoverned mess.",
        "tags": ["Azure", "Governance", "Tags", "FinOps", "Policy"],
    },
    "azure-tag-governance-policy": {
        "summary": "How to turn Azure tags from 'nice to have' into enforceable governance using Azure Policy, deny/modify effects, and remediation so teams can’t slip around your standards.",
        "tags": ["Azure", "Governance", "Tags", "Azure Policy", "Compliance"],
    },
    "azure-chargeback-tags-model": {
        "summary": "A chargeback/showback model built on tags that finance, app owners, and cloud teams can all live with—without 47 competing cost spreadsheets.",
        "tags": ["Azure", "Governance", "Chargeback", "Tags", "FinOps"],
    },
    "resource-tags-100k-problem": {
        "summary": "What happens when an enterprise ends up with 100,000+ tag variations, why it happens in the real world, and how to systematically clean it up without breaking production.",
        "tags": ["Azure", "Governance", "Tags", "Technical Debt", "FinOps"],
    },
    "tag-governance-247-variations": {
        "summary": "A post-mortem on 247 variations of the same tag key in a regulated environment—and the governance patterns that finally stopped the bleeding.",
        "tags": ["Azure", "Governance", "Tags", "Azure Policy", "Standards"],
    },
    "azure-update-manager-reality-check": {
        "summary": "Azure Update Manager vs SCCM/WSUS/Intune in a real enterprise: what actually works, what breaks, and the governance traps nobody mentions in the docs.",
        "tags": ["Azure", "Governance", "Patching", "Azure Update Manager", "Operations"],
    },
    "azure-support-ticket-reality": {
        "summary": "A governance and process look at Azure support tickets: SLAs, ownership, escalation, and why leaving it to 'open a ticket with Microsoft' is not a strategy.",
        "tags": ["Azure", "Governance", "Support", "Operations", "Process"],
    },
    "azure-audit-gap-nobody-talks-about": {
        "summary": "The hidden audit gap between what Azure logs, what auditors expect, and what your governance model actually covers—plus concrete steps to close it.",
        "tags": ["Azure", "Governance", "Audit", "Compliance", "Logging"],
    },
    "pull-meta-from-arm": {
        "summary": "A reusable pattern for pulling metadata from ARM at scale to feed CMDBs, reports, and governance dashboards when Azure alone isn’t enough.",
        "tags": ["Azure", "Governance", "Automation", "ARM", "CMDB"],
    },
    "service-inventory-tool": {
        "summary": "A practical service inventory pattern for Azure: map resources to real business services, owners, and environments so governance and audits stop being guesswork.",
        "tags": ["Azure", "Governance", "Inventory", "CMDB", "Operations"],
    },
    "azure-arc-ghost-registrations": {
        "summary": "How Azure Arc ghost registrations happen, why they wreck governance reporting, and how to detect and clean them up at scale.",
        "tags": ["Azure", "Governance", "Azure Arc", "Hybrid", "Inventory"],
    },
    "azure-arc-private-lab": {
        "summary": "A private Azure Arc lab design that lets you learn governance patterns, vCenter onboarding, and policy testing without touching production.",
        "tags": ["Azure", "Governance", "Azure Arc", "Lab", "Hybrid"],
    },
    "azure-arc-vcenter-implementation-guide": {
        "summary": "End-to-end implementation guide for connecting VMware vCenter to Azure Arc with governance in mind: tags, policy, RBAC, and reporting from day one.",
        "tags": ["Azure", "Governance", "Azure Arc", "VMware", "Hybrid"],
    },
}


def split_front_matter(content: str):
    content = content.lstrip()
    if not content.startswith("---"):
        return None, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content
    _, fm, body = parts
    return fm.strip(), body.lstrip("\n")


def find_md_for_slug(slug: str) -> Path | None:
    matches = list(POSTS_DIR.glob(f"*{slug}*.md"))
    if not matches:
        return None
    # Prefer dated filename if multiple
    matches.sort(key=lambda p: p.name)
    return matches[0]


def main():
    updated = 0
    for slug, meta in GOV_POSTS.items():
        md_path = find_md_for_slug(slug)
        if not md_path:
            print(f"[WARN] No markdown file found for slug '{slug}'")
            continue

        text = md_path.read_text(encoding="utf-8")
        fm_text, body = split_front_matter(text)
        if fm_text is None:
            print(f"[WARN] {md_path.name}: no front matter, skipping")
            continue

        try:
            fm = yaml.safe_load(fm_text) or {}
        except Exception as e:
            print(f"[WARN] {md_path.name}: bad YAML ({e}), skipping")
            continue

        changed = False

        # Update summary
        summary = meta.get("summary")
        if summary and fm.get("summary") != summary:
            fm["summary"] = summary
            changed = True

        # Merge/override tags
        new_tags = meta.get("tags")
        if new_tags:
            existing = fm.get("tags") or []
            if isinstance(existing, str):
                existing = [existing]
            merged = sorted(set(existing) | set(new_tags))
            if merged != existing:
                fm["tags"] = merged
                changed = True

        if not changed:
            print(f"[SKIP] {md_path.name} ({slug}) – already up to date")
            continue

        new_fm = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip() + "\n"
        new_text = "---\n" + new_fm + "---\n" + body
        md_path.write_text(new_text, encoding="utf-8")
        updated += 1
        print(f"[UPDATED] {md_path.name} ({slug})")

    print(f"\nDone. Updated {updated} Governance post(s).")


if __name__ == "__main__":
    sys.exit(main())
