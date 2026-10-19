"""Find/fix double-encoded UTF-8 (UTF-8 bytes misread as cp1252).

Usage:
  python demojibake.py report <dir>      # per-file count of affected lines
  python demojibake.py fix <file>        # rewrite file in place (UTF-8, newlines preserved)
"""
import re, sys, pathlib

# Map each cp1252 byte 0x80-0xFF to the character it decodes to.
# 0x81, 0x8D, 0x8F, 0x90, 0x9D are undefined in cp1252; Windows passes them
# through as the matching C1 control character (U+0081 etc.), so map those too.
def cp(b):
    try:
        return bytes([b]).decode("cp1252")
    except UnicodeDecodeError:
        return chr(b)

TO_BYTE = {cp(b): b for b in range(0x80, 0x100)}

def to_bytes(s):
    return bytes(TO_BYTE[c] if c in TO_BYTE else ord(c) for c in s)

def cls(lo, hi):
    return "".join(re.escape(cp(b)) for b in range(lo, hi + 1))

CONT = f"[{cls(0x80, 0xBF)}]"
PATTERN = re.compile(
    f"[{cls(0xC2, 0xDF)}]{CONT}"
    f"|[{cls(0xE0, 0xEF)}]{CONT}{{2}}"
    f"|[{cls(0xF0, 0xF4)}]{CONT}{{3}}"
)

def repair(m):
    s = m.group(0)
    try:
        return to_bytes(s).decode("utf-8")
    except UnicodeError:
        return s  # not a real mojibake sequence; leave it

def fix_text(text):
    return PATTERN.sub(repair, text)

def affected_lines(text):
    return [i for i, line in enumerate(text.split("\n"), 1) if fix_text(line) != line]

def read(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()

if __name__ == "__main__":
    mode, target = sys.argv[1], pathlib.Path(sys.argv[2])
    if mode == "report":
        total = 0
        for p in sorted(target.glob("*.md")):
            n = len(affected_lines(read(p)))
            if n:
                total += 1
                print(f"{n:5}  {p.name}")
        print(f"files affected: {total}")
    elif mode == "fix":
        before = read(target)
        after = fix_text(before)
        print(f"lines changed: {len(affected_lines(before))}")
        with open(target, "w", encoding="utf-8", newline="") as f:
            f.write(after)
