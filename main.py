#!/usr/bin/env python3
"""Patch-notes entry: one changelog line about calling the teacher 'mom'.

When the grader runs this program it writes the line to entry.txt. The
line is measured against the competition's 160-character ceiling before
anything is written, so an oversize line fails here loudly instead of
shipping an entry the judge would reject.
"""

import os
import sys

PATCH_LINE = "v1.3.9: fixed a bug where the mouth called the teacher 'mom' in front of the class; the name resolver now checks the room first."
CHARACTER_LIMIT = 160


def sanitise(line):
    """Check the patch line and hand back the exact text to ship."""
    stripped = line.strip()
    if not stripped:
        raise SystemExit("patch line is empty")
    if len(stripped) > CHARACTER_LIMIT:
        raise SystemExit(
            "patch line is %d chars, limit is %d" % (len(stripped), CHARACTER_LIMIT)
        )
    if "\n" in stripped or "\r" in stripped:
        raise SystemExit("patch line must be a single line")
    for ch in stripped:
        if ord(ch) < 32:
            raise SystemExit(
                "patch line holds a control character (U+%04X)" % ord(ch)
            )
    return stripped


def publish(line):
    """Drop the checked line into the grader's output folder."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line)
    with open(path, encoding="utf-8") as handle:
        if handle.read() != line:
            raise SystemExit("entry.txt does not match the checked line")
    return path


def main():
    line = sanitise(PATCH_LINE)
    publish(line)
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
