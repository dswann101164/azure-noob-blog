#!/usr/bin/env python
"""
Update YAML front matter for KQL-related posts:
- Standardize summary
- Normalize tags

Does NOT touch 'cover' so hero images remain intact.
"""

import sys
from pathlib import Path

import yaml  # pip install pyyaml

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"

KQL_POSTS = {
    "kql-cheat-sheet-complete": {
        "summary": "A complete KQL cheat sheet for Azure admins: joins, summarize, extend, project, and real-world query patterns for Azure Resource Graph and Log Analytics.",
        "tags": ["Azure", "KQL", "Resource Graph", "Log Analytics", "Cheat Sheet"],
    },
    "azure-vm-inventory-kql": {
        "summary": "Production-grade KQL queries for Azure Resource Graph that build a reliable VM inventory across subscriptions, tenants, and environments.",
        "tags": ["Azure", "KQL", "Resource Graph", "Inventory", "VM Management"],
    },
    "kql-query-library-git": {
        "summary": "How to treat your KQL queries like code: organize them in Git, reuse patterns, and build a shared query library for your Azure team.",
        "tags": ["Azure", "KQL", "Git", "Automation", "Resource Graph"],
    },
    "kql-multiple-systems": {
        "summary": "Patterns for writing KQL that works across multiple systems and tables—ARG, Log Analytics, and workbooks—without losing your mind.",
        "tags": ["Azure", "KQL", "Log Analytics", "Resource Graph", "Dashboards"],
    },
    "azure-debugging-ai-rule": {
        "summary": "Using KQL to debug AI-driven alerts, complex rules, and noisy signals in Azure Monitor so your dashboards stop lying to you.",
        "tags": ["Azure", "KQL", "Monitoring", "Azure Monitor", "Debugging"],
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
    matches.sort(key=lambda p: p.name)
    return matches[0]


def main():
    updated = 0
    for slug, meta in KQL_POSTS.items():
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

    print(f"\nDone. Updated {updated} KQL post(s).")


if __name__ == "__main__":
    sys.exit(main())
