#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright The Ilorium Authors
"""Check that a change to a protocol document comes with its translation and a changelog entry.

Rules (CONTRIBUTING.md, "Rules for every pull request"):
  - WARN  if a document <name>.md changed and <name>.es.md did not (or the reverse).
  - FAIL  if any protocol document changed and CHANGELOG.md did not.

"Protocol document" means a .md file at the repository root or under genome/,
specs/, engineering/, research/ or brand/, except the changelogs themselves.
Repository files (CONTRIBUTING.md, GOVERNANCE.md, governance/, iips/, .github/
and so on) are not documents for this purpose.

Reads the list of changed files from stdin (one path per line, as printed by
`git diff --name-only BASE...HEAD`) or from --files. Standard library only.

Usage:
    git diff --name-only BASE...HEAD | python3 tools/check_translation_changelog.py
    python3 tools/check_translation_changelog.py --files a.md b.es.md
"""

from __future__ import annotations

import sys

DOC_DIRS = ("genome/", "specs/", "engineering/", "research/", "brand/")
CHANGELOGS = {"CHANGELOG.md", "CHANGELOG.es.md"}


def is_document(path: str) -> bool:
    if not path.endswith(".md") or path in CHANGELOGS:
        return False
    if "/" not in path:
        return True
    return path.startswith(DOC_DIRS)


def counterpart(path: str) -> str:
    if path.endswith(".es.md"):
        return path[: -len(".es.md")] + ".md"
    return path[: -len(".md")] + ".es.md"


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0
    if "--files" in argv:
        changed = argv[argv.index("--files") + 1:]
    elif sys.stdin.isatty():
        print("check_translation_changelog: pipe `git diff --name-only BASE...HEAD` to stdin or pass --files", file=sys.stderr)
        return 2
    else:
        changed = [line.strip() for line in sys.stdin if line.strip()]
    changed_set = set(changed)
    docs = sorted(p for p in changed if is_document(p))

    warnings: list[str] = []
    errors: list[str] = []
    for p in docs:
        other = counterpart(p)
        if other not in changed_set:
            warnings.append(f"{p} changed but {other} did not (add the translation, or label needs-translation)")
    if docs and "CHANGELOG.md" not in changed_set:
        errors.append("a document changed but CHANGELOG.md did not (every change gets a changelog entry)")
    if docs and "CHANGELOG.md" in changed_set and "CHANGELOG.es.md" not in changed_set:
        warnings.append("CHANGELOG.md changed but CHANGELOG.es.md did not")

    for w in warnings:
        print(f"::warning::{w}")
        print(f"warning: {w}")
    for e in errors:
        print(f"::error::{e}")
        print(f"error: {e}")
    print(f"check_translation_changelog: {len(docs)} document(s) changed, {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
