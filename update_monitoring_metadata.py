#!/usr/bin/env python
"""
Update YAML front matter for Monitoring-related posts:
- Standardize summary
- Normalize tags (merge existing + hub-defined)

Does NOT touch 'cover' so hero images remain intact.

Usage:
    python update_monitoring_metadata.py
    python update_monitoring_metadata.py --dry-run
"""

import sys
from pathlib import Path

import yaml  # pip install pyyaml if needed

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"

# Map post slug -> desired summary + core tags
MONITORING_POSTS = {
    "azure-dashboards-cloud-noc": {
        "summary": (
            "How to design Azure dashboards for a Cloud NOC team that actually "
            "answer questions instead of dumping metrics on a big screen."
        ),
        "tags": ["Azure", "Monitoring", "Dashboards", "Operations", "Cloud NOC"],
    },
    "chris-bowman-dashboard": {
        "summary": (
            "Reverse-engineering and modernizing the legendary Chris Bowman Azure "
            "dashboard model for real-world enterprise environments."
        ),
        "tags": ["Azure", "Monitoring", "Dashboards", "Architecture", "Executive"],
    },
    "mcp-vs-powerbi-ai-what-actually-creates-dashboards": {
        "summary": (
            "A practical comparison of MCP vs Power BI AI: what actually reads data, "
            "what actually builds visuals, and how Azure admins should think about both."
        ),
        "tags": ["Azure", "Monitoring", "Power BI", "AI", "Dashboards"],
    },
    "modernizing-azure-workbooks": {
        "summary": (
            "How to modernize Azure Monitor workbooks with better UX, KQL patterns, "
            "and business context so teams actually use them."
        ),
        "tags": ["Azure", "Monitoring", "Workbooks", "KQL", "Dashboards"],
    },
    "workbook-app-tool": {
        "summary": (
            "An Azure Monitor workbook-driven app concept: turn your dashboards into "
            "lightweight tools for operators instead of static reports."
        ),
        "tags": ["Azure", "Monitoring", "Workbooks", "Tools", "Operations"],
    },
    "azure-dashboard-rebranding-tool": {
        "summary": (
            "A dark-mode rebranding tool for Azure dashboards and Excel exports so "
            "your reports look as modern as your cloud environment."
        ),
        "tags": ["Azure", "Monitoring", "Dashboards", "Branding", "Tools"],
    },
    "azure-ipam-tool": {
        "summary": (
            "An Azure IPAM workbook and process for tracking IP address usage across "
            "subscriptions, VNets, and environments without losing your mind."
        ),
        "tags": ["Azure", "Monitoring", "IPAM", "Networking", "Workbooks"],
    },
    "azure-update-manager-reality-check": {
        "summary": (
            "What Azure Update Manager really looks like in an enterprise: agent "
            "confusion, SCCM overlap, and how to make patching governance work."
        ),
        "tags": ["Azure", "Monitoring", "Update Management", "Patching", "Governance"],
    },
}


def split_front_matter(content: str):
    """Return (front_matter_text, body_text) or (None, content) if no FM."""
    content = content.lstrip()
    if not content.startswith("---"):
        return None, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content
    _, fm, body = parts
    return fm.strip(), body.lstrip("\n")


def find_md_for_slug(slug: str) -> Path | None:
    """
    Find the markdown file for a given slug.

    Prefer files like: YYYY-MM-DD-slug.md
    Fallback to any *slug*.md if needed.
    """
    # Preferred pattern: date-slug.md
    primary = sorted(POSTS_DIR.glob(f"*-{slug}.md"), key=lambda p: p.name)
    if primary:
        return primary[0]

    # Fallback: anything containing the slug
    fallback = sorted(POSTS_DIR.glob(f"*{slug}*.md"), key=lambda p: p.name)
    if fallback:
        return fallback[0]

    return None


def main():
    DRY_RUN = "--dry-run" in sys.argv
    updated = 0

    for slug, meta in MONITORING_POSTS.items():
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

        # -------- summary --------
        summary = meta.get("summary")
        if summary and fm.get("summary") != summary:
            fm["summary"] = summary
            changed = True

        # -------- tags --------
        new_tags = meta.get("tags")
        if new_tags:
            existing = fm.get("tags") or []
            if isinstance(existing, str):
                existing = [existing]
            elif not isinstance(existing, list):
                existing = []

            merged = sorted(set(existing) | set(new_tags))
            if merged != existing:
                fm["tags"] = merged
                changed = True

        if not changed:
            print(f"[SKIP] {md_path.name} ({slug}) – already up to date")
            continue

        new_fm = yaml.safe_dump(
            fm,
            sort_keys=False,
            allow_unicode=True,
        ).strip() + "\n"
        new_text = "---\n" + new_fm + "---\n" + body

        if DRY_RUN:
            print(f"[DRY RUN] Would update {md_path.name} ({slug})")
        else:
            md_path.write_text(new_text, encoding="utf-8")
            updated += 1
            print(f"[UPDATED] {md_path.name} ({slug})")

    suffix = " (dry run)" if DRY_RUN else ""
    print(f"\nDone. Updated {updated} Monitoring post(s){suffix}.")


if __name__ == "__main__":
    sys.exit(main())
