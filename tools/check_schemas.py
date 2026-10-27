#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright The Ilorium Authors
"""Check that every JSON file under schemas/ is strict JSON and a valid JSON Schema.

Needs the `jsonschema` package only when at least one schema exists; with an
empty schemas/ directory it prints a notice and exits 0, so CI can run it
before the M0 archive is in place.

Usage:
    python3 tools/check_schemas.py [SCHEMAS_DIR]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path("schemas")
    files = sorted(p for p in root.rglob("*.json") if p.is_file()) if root.is_dir() else []
    if not files:
        print(f"check_schemas: no JSON files under {root}; skipped (schemas/ is populated from the M0 archive before the first release)")
        return 0
    try:
        import jsonschema  # type: ignore
        from jsonschema import validators  # type: ignore
    except ImportError:
        print("check_schemas: the jsonschema package is required when schemas exist (pip install jsonschema==4.26.0)", file=sys.stderr)
        return 1

    errors = 0
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            print(f"error: {path}: not strict JSON: {exc}")
            errors += 1
            continue
        try:
            cls = validators.validator_for(data)
            cls.check_schema(data)
        except jsonschema.exceptions.SchemaError as exc:
            print(f"error: {path}: not a valid JSON Schema: {exc.message}")
            errors += 1
            continue
        print(f"ok: {path}")
    print(f"check_schemas: {len(files)} file(s), {errors} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
