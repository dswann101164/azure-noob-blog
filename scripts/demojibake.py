"""Find/fix double-encoded UTF-8 (UTF-8 bytes misread as cp1252).

Usage:
  python demojibake.py report <dir>      # per-file count of affected lines
  python demojibake.py fix <file>        # rewrite file in place (UTF-8, newlines preserved)
  python demojibake.py check <dir>       # exit 1 if any post has mojibake, a BOM, or invalid UTF-8
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
    elif mode == "check":
        problems = []
        for p in sorted(target.glob("*.md")):
            raw = p.read_bytes()
            if raw.startswith(b"\xef\xbb\xbf"):
                problems.append(f"{p.name}: UTF-8 BOM (breaks front matter parsing)")
            try:
                lines = affected_lines(raw.decode("utf-8"))
            except UnicodeDecodeError as e:
                problems.append(f"{p.name}: not valid UTF-8 at byte {e.start}")
                continue
            if lines:
                shown = ", ".join(map(str, lines[:10])) + (" ..." if len(lines) > 10 else "")
                problems.append(f"{p.name}: mojibake on {len(lines)} line(s): {shown}")
        for line in problems:
            print(line)
        print(f"encoding check: {len(problems)} problem(s) in {target}")
        sys.exit(1 if problems else 0)
