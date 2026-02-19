import os, re, glob, sys

def slugify_tag(tag):
    t = tag.lower().strip()
    t = re.sub(r'[^a-z0-9\s-]', '-', t)
    t = re.sub(r'[\s]+', '-', t)
    t = re.sub(r'-+', '-', t)
    t = t.strip('-')
    return t

posts_dir = r"C:\Users\dswann\Documents\GitHub\azure-noob-blog\posts"
files = [f for f in glob.glob(os.path.join(posts_dir, "*.md"))
         if not f.endswith(".bak") and not f.endswith(".backup")]

changed = 0
tag_changes = {}

for fpath in sorted(files):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_tags(m):
        raw = m.group(1)
        tags = re.findall(r'"([^"]+)"|\'([^\']+)\'', raw)
        tags = [a or b for a, b in tags]
        if not tags:
            tags = [t.strip() for t in raw.strip('[]').split(',') if t.strip()]

        new_tags = [slugify_tag(t) for t in tags]
        new_tags = list(dict.fromkeys(new_tags))

        if tags != new_tags:
            fname = os.path.basename(fpath)
            tag_changes[fname] = list(zip(tags, new_tags))

        quoted = ', '.join(f'"{t}"' for t in new_tags)
        return f'tags: [{quoted}]'

    new_content = re.sub(r'tags:\s*\[([^\]]*)\]', replace_tags, content)

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        changed += 1

with open(r"C:\Users\dswann\Documents\GitHub\azure-noob-blog\normalize_tags_output.txt", 'w', encoding='utf-8') as out:
    out.write(f"Modified {changed} files\n\n")
    for fname, changes in sorted(tag_changes.items()):
        diffs = [(a, b) for a, b in changes if a != b]
        if diffs:
            out.write(f"{fname}:\n")
            for old, new in diffs:
                out.write(f"  {repr(old)} -> {repr(new)}\n")
            out.write("\n")

print(f"Done. Modified {changed} files. See normalize_tags_output.txt for details.")
