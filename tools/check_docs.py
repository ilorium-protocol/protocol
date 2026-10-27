#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright The Ilorium Authors
"""Lint the Markdown documents of the protocol repository. Standard library only.

Checks, for every tracked .md file under the given root:
  - decodes as UTF-8, no byte order mark;
  - no tab characters;
  - no trailing whitespace at end of line (warning only);
  - ends with exactly one newline;
  - every protocol document <name>.md has a <name>.es.md counterpart, and the reverse
    (repository-only files such as CONTRIBUTING.md and files under excluded
    directories are exempt; see EXEMPT and EXCLUDED_DIRS).

Exit 1 on any error. Warnings do not fail.

Usage:
    python3 tools/check_docs.py [ROOT]
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Repository files that have no Spanish counterpart by design.
EXEMPT = {
    "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "GOVERNANCE.md",
    "docs/README.md", "schemas/README.md", "vectors/README.md", "verifier/README.md",
    "tools/README.md", "iips/README.md", "iips/TEMPLATE.md",
    "governance/README.md", "governance/custodians/README.md", "governance/security/README.md",
    ".github/PULL_REQUEST_TEMPLATE.md", "verifier/CHANGELOG.md",
}
# Directories whose files never need a counterpart.
EXCLUDED_DIRS = {".git", ".github", "governance", "iips", "verifier", "vectors", "schemas", "tools", "docs", "node_modules", ".venv", "dist", "build"}


def iter_md(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root)
        top = rel_dir.parts[0] if rel_dir.parts else ""
        if top in EXCLUDED_DIRS:
            dirnames[:] = []
            continue
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIRS and not d.startswith("."))
        for name in sorted(filenames):
            if name.endswith(".md"):
                yield Path(dirpath) / name


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(".")
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()

    for path in iter_md(root):
        rel = path.relative_to(root).as_posix()
        seen.add(rel)
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            errors.append(f"{rel}: byte order mark")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{rel}: not UTF-8 ({exc})")
            continue
        if "\t" in text:
            n = text.count("\t")
            errors.append(f"{rel}: {n} tab character(s)")
        if "\r" in text:
            errors.append(f"{rel}: carriage return")
        if text and not text.endswith("\n"):
            errors.append(f"{rel}: no newline at end of file")
        if text.endswith("\n\n"):
            warnings.append(f"{rel}: more than one newline at end of file")
        for i, line in enumerate(text.split("\n"), 1):
            if line.rstrip() != line and not line.endswith("  "):
                warnings.append(f"{rel}:{i}: trailing whitespace")

    # Counterparts.
    for rel in sorted(seen):
        if rel in EXEMPT:
            continue
        if rel.endswith(".es.md"):
            other = rel[: -len(".es.md")] + ".md"
        else:
            other = rel[: -len(".md")] + ".es.md"
        if other not in seen and other not in EXEMPT:
            errors.append(f"{rel}: counterpart {other} is absent")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"check_docs: {len(seen)} file(s), {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
