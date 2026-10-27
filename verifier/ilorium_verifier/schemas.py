# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Loading and applying the Evidence Format JSON Schemas."""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import best_match
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


def schemas_dir() -> Path:
    candidates: list[Path] = []
    if os.environ.get("ILORIUM_SCHEMAS"):
        candidates.append(Path(os.environ["ILORIUM_SCHEMAS"]))
    here = Path(__file__).resolve()
    candidates += [here.parent / "schemas", here.parents[2] / "schemas"]
    for candidate in candidates:
        if (candidate / "common.schema.json").is_file():
            return candidate
    raise FileNotFoundError("Ilorium schemas not found; set ILORIUM_SCHEMAS")


@lru_cache(maxsize=1)
def _load() -> tuple[Registry, dict[str, dict]]:
    registry = Registry()
    documents: dict[str, dict] = {}
    for path in sorted(schemas_dir().glob("*.schema.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        registry = registry.with_resource(
            document["$id"], Resource.from_contents(document, default_specification=DRAFT202012)
        )
        documents[path.name.removesuffix(".schema.json")] = document
    return registry, documents


@lru_cache(maxsize=None)
def _validator(name: str) -> Draft202012Validator:
    registry, documents = _load()
    return Draft202012Validator(documents[name], registry=registry)


def validate(name: str, instance: Any) -> str | None:
    """Return a short description of the most relevant schema error, or None if valid."""
    error = best_match(_validator(name).iter_errors(instance))
    if error is None:
        return None
    where = "/".join(str(part) for part in error.absolute_path) or "(root)"
    return f"{where}: {error.message}"[:240]
