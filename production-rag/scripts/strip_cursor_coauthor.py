"""Strip Cursor Co-authored-by trailer lines from git commit messages (msg-filter)."""

from __future__ import annotations

import re
import sys

_CURSOR_COAUTHOR = re.compile(
    r"^Co-authored-by:\s*Cursor\s*<cursoragent@cursor\.com>\s*$",
    re.IGNORECASE,
)


def main() -> None:
    raw = sys.stdin.read()
    lines = raw.splitlines(keepends=True)
    filtered = [line for line in lines if not _CURSOR_COAUTHOR.match(line.rstrip("\r\n"))]
    while filtered and filtered[-1].strip() == "":
        filtered.pop()
    if filtered and not filtered[-1].endswith("\n"):
        filtered[-1] = filtered[-1].rstrip("\r\n") + "\n"
    sys.stdout.write("".join(filtered))


if __name__ == "__main__":
    main()
