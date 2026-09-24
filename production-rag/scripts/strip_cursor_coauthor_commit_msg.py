"""Remove Cursor Co-authored-by lines from a commit message file (commit-msg hook)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_CURSOR_COAUTHOR = re.compile(
    r"^Co-authored-by:\s*Cursor\s*<cursoragent@cursor\.com>\s*$",
    re.IGNORECASE,
)


def strip_message(text: str) -> str:
    lines = text.splitlines(keepends=True)
    filtered = [line for line in lines if not _CURSOR_COAUTHOR.match(line.rstrip("\r\n"))]
    while filtered and filtered[-1].strip() == "":
        filtered.pop()
    body = "".join(filtered)
    if body and not body.endswith("\n"):
        body += "\n"
    return body


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: strip_cursor_coauthor_commit_msg.py <commit-msg-file>")
    path = Path(sys.argv[1])
    path.write_text(strip_message(path.read_text(encoding="utf-8")), encoding="utf-8")


if __name__ == "__main__":
    main()
