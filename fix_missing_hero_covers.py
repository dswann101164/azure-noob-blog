#!/usr/bin/env python
"""
Fix cover paths that point to missing .svg heroes when a .png exists.

For each post:
  - read YAML front matter
  - if cover: /static/images/hero/<name>.svg
    and static/images/hero/<name>.png exists,
    rewrite cover to .png
"""

import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("This script requires PyYAML. Install with: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
HERO_DIR = ROOT / "static" / "images" / "hero"

def split_front_matter(content: str):
    if not content.lstrip().startswith("---"):
        return None, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content
    _, fm, body = parts
    return fm.strip(), body.lstrip("\n")

def main():
    # build set of actual hero filenames (.png)
    hero_pngs = {p.name for p in HERO_DIR.glob("*.png")}
    print(f"Found {len(hero_pngs)} PNG heroes in {HERO_DIR}")

    rewritten = 0

    for md_path in POSTS_DIR.glob("*.md"):
        text = md_path.read_text(encoding="utf-8")
        fm_text, body = split_front_matter(text)
        if fm_text is None:
            continue

        try:
            fm = yaml.safe_load(fm_text) or {}
        except Exception as e:
            print(f"[WARN] Skipping {md_path.name}: bad YAML ({e})")
            continue

        cover = fm.get("cover")
        if not isinstance(cover, str):
            continue

        m = re.match(r"^/static/images/hero/(.+)\.svg$", cover)
        if not m:
            continue

        base = m.group(1)
        png_name = base + ".png"

        if png_name in hero_pngs:
            new_cover = f"/static/images/hero/{png_name}"
            print(f"[UPDATE] {md_path.name}: {cover} -> {new_cover}")
            fm["cover"] = new_cover

            # dump back
            new_fm = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip() + "\n"
            new_text = "---\n" + new_fm + "---\n" + body
            md_path.write_text(new_text, encoding="utf-8")
            rewritten += 1
        else:
            print(f"[WARN] No PNG hero for {cover} (expected {png_name})")

    print(f"\nDone. Updated {rewritten} post(s).")

if __name__ == "__main__":
    main()
