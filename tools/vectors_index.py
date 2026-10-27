#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright The Ilorium Authors
"""Check or rewrite vectors/index.json, the index of the conformity vectors.

The index is the one `tools/gen_vectors.py` writes (Evidence Format 1.0, section 15):

    {
      "vector_index": "1.0",
      "protocol_release": "1.0",
      "note": "...",
      "files": {"<file>.json": {"operation": "...", "cases": N, "sha256": "..."}, ...},
      "total_cases": N
    }

`--check` (the default) recomputes the SHA-256 and the case count of every listed file,
verifies that every vector file in the directory is listed and that `total_cases` adds up.
It prints one line per file and exits 1 on any mismatch. `--write` rewrites the sha256,
cases and total_cases fields in place, keeping every other field, after the generator ran.
With an empty vectors directory, `--check` prints a notice and exits 0.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def count_cases(path: Path) -> int | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if isinstance(data, dict):
        for key in ("cases", "vectors", "tests"):
            if isinstance(data.get(key), list):
                return len(data[key])
    if isinstance(data, list):
        return len(data)
    return None


def vector_files(vectors: Path) -> list[Path]:
    return sorted(p for p in vectors.glob("*.json") if p.name != "index.json")


def check(vectors: Path) -> int:
    index_path = vectors / "index.json"
    files = vector_files(vectors)
    if not files and not index_path.exists():
        print("::notice title=vectors::vectors/ is empty; nothing to check.")
        return 0
    if not index_path.exists():
        print(f"error: {index_path} is missing; run `python3 tools/vectors_index.py --write`")
        return 1
    index = json.loads(index_path.read_text(encoding="utf-8"))
    listed = index.get("files", {})
    errors = 0
    for p in files:
        entry = listed.get(p.name)
        digest = sha256_of(p)
        cases = count_cases(p)
        if entry is None:
            print(f"MISSING  {p.name}: not listed in index.json")
            errors += 1
            continue
        ok = entry.get("sha256") == digest and (cases is None or entry.get("cases") == cases)
        print(f"{'ok      ' if ok else 'MISMATCH'} {p.name}  cases={entry.get('cases')}  sha256={digest[:16]}…")
        if not ok:
            errors += 1
    for name in listed:
        if not (vectors / name).exists():
            print(f"ABSENT   {name}: listed in index.json but not in {vectors}/")
            errors += 1
    total = sum(int(e.get("cases", 0)) for e in listed.values())
    if index.get("total_cases") != total:
        print(f"MISMATCH total_cases={index.get('total_cases')} but the files add up to {total}")
        errors += 1
    print(f"{len(files)} file(s), {total} cases, {errors} problem(s)")
    return 1 if errors else 0


def write(vectors: Path) -> int:
    index_path = vectors / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8")) if index_path.exists() else {
        "vector_index": "1.0", "protocol_release": "1.0", "note": "TEST KEYS ONLY. See Evidence Format 1.0, section 15.", "files": {}}
    files = index.setdefault("files", {})
    for p in vector_files(vectors):
        entry = files.setdefault(p.name, {"operation": "unknown"})
        entry["sha256"] = sha256_of(p)
        cases = count_cases(p)
        if cases is not None:
            entry["cases"] = cases
    for name in list(files):
        if not (vectors / name).exists():
            del files[name]
    index["files"] = dict(sorted(files.items()))
    index["total_cases"] = sum(int(e.get("cases", 0)) for e in files.values())
    index_path.write_text(json.dumps(index, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {index_path}: {len(files)} file(s), {index['total_cases']} cases")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--vectors", default="vectors", help="vectors directory (default: vectors)")
    ap.add_argument("--write", action="store_true", help="rewrite sha256/cases/total_cases in index.json")
    ap.add_argument("--check", action="store_true", help="check index.json against the files (default)")
    args = ap.parse_args(argv)
    vectors = Path(args.vectors)
    if args.write:
        return write(vectors)
    return check(vectors)


if __name__ == "__main__":
    sys.exit(main())
