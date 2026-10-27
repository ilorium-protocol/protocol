#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright The Ilorium Authors
"""Scan files that agents read for hidden-instruction patterns.

The rule (README, Lighthouse): what an agent reads is what a human reads. A
file that hides text from humans while showing it to agents fails this check.

Files scanned: llms.txt, *.txt and *.json under any .well-known/ directory,
and every .md file (documents are agent-readable). Standard library only.

Patterns:
  - zero-width and invisible Unicode characters (U+200B..U+200F, U+2028..U+202E,
    U+2060..U+2064, U+FEFF inside the text, U+00AD, Unicode tag characters
    U+E0000..U+E007F);
  - HTML comments containing imperative text aimed at an agent;
  - "ignore previous/prior/above instructions" and variants;
  - base64-looking blobs of 120+ characters;
  - HTML spans or divs hidden by style (display:none, visibility:hidden,
    font-size:0, color matching background, opacity:0) or by the `hidden` attribute.

Exit 1 on any hit. Use --quiet to print only hits.

Usage:
    python3 tools/check_agent_readable.py [ROOT] [--quiet]
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

INVISIBLE = re.compile("[​-‏ -‮⁠-⁤­﻿\U000e0000-\U000e007f]")
IMPERATIVE_WORDS = r"(ignore|disregard|forget|override|you must|you should|do not tell|don't tell|execute|run |print |send |exfiltrate|reveal|system prompt|assistant|as an ai)"
HTML_COMMENT = re.compile(r"<!--(.*?)-->", re.S | re.I)
IGNORE_PREVIOUS = re.compile(r"ignore\s+(all\s+)?(the\s+)?(previous|prior|above|earlier|preceding)\s+(instructions?|prompts?|rules?|messages?)", re.I)
BASE64_BLOB = re.compile(r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{120,}={0,2}(?![A-Za-z0-9+/=])")
HIDDEN_STYLE = re.compile(
    r"<(span|div|p|section|a)\b[^>]*(style\s*=\s*\"[^\"]*(display\s*:\s*none|visibility\s*:\s*hidden|font-size\s*:\s*0|opacity\s*:\s*0|color\s*:\s*(#fff|#ffffff|white|transparent))[^\"]*\"|\bhidden\b)[^>]*>",
    re.I,
)

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__"}


def is_agent_readable(path: Path) -> bool:
    name = path.name
    parts = set(path.parts)
    if name == "llms.txt":
        return True
    if ".well-known" in parts and path.suffix in {".txt", ".json"}:
        return True
    return path.suffix == ".md"


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            p = Path(dirpath) / name
            if is_agent_readable(p.relative_to(root)):
                yield p


def scan(path: Path, text: str) -> list[str]:
    hits: list[str] = []
    for m in INVISIBLE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        hits.append(f"{path}:{line}: invisible character U+{ord(m.group()):04X}")
        if len(hits) > 20:
            break
    for m in HTML_COMMENT.finditer(text):
        body = m.group(1)
        if re.search(IMPERATIVE_WORDS, body, re.I):
            line = text.count("\n", 0, m.start()) + 1
            hits.append(f"{path}:{line}: HTML comment with imperative text: {body.strip()[:80]!r}")
    for m in IGNORE_PREVIOUS.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        hits.append(f"{path}:{line}: 'ignore previous instructions' pattern")
    for m in BASE64_BLOB.finditer(text):
        blob = m.group()
        # A long hex string (hash) is not base64 in the sense that matters here.
        if re.fullmatch(r"[0-9a-fA-F]+", blob):
            continue
        line = text.count("\n", 0, m.start()) + 1
        hits.append(f"{path}:{line}: base64-looking blob of {len(blob)} characters")
    for m in HIDDEN_STYLE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        hits.append(f"{path}:{line}: hidden HTML element: {m.group()[:80]!r}")
    return hits


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    quiet = "--quiet" in argv
    root = Path(args[0]) if args else Path(".")
    total = 0
    hits: list[str] = []
    for path in iter_files(root):
        total += 1
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            hits.append(f"{path}: not UTF-8")
            continue
        hits.extend(scan(path, text))
    for h in hits:
        print(f"hit: {h}")
    if not quiet or hits:
        print(f"check_agent_readable: {total} file(s) scanned, {len(hits)} hit(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
