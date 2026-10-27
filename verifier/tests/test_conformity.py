# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
import hashlib
import json
from pathlib import Path

from ilorium_verifier.conformity import run_directory

VECTORS = Path(__file__).resolve().parents[2] / "vectors"


def test_all_vectors_pass():
    results = run_directory(VECTORS)
    assert len(results) > 200
    failed = [f"{r.vector_id}: {r.message}" for r in results if not r.ok]
    assert not failed, "\n".join(failed)


def test_index_matches_files():
    """Vectors are generated, never edited by hand: the index pins every file."""
    index = json.loads((VECTORS / "index.json").read_text(encoding="utf-8"))
    names = sorted(p.name for p in VECTORS.glob("*.json") if p.name != "index.json")
    assert names == sorted(index["files"])
    total = 0
    for name, entry in index["files"].items():
        data = (VECTORS / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == entry["sha256"], name
        assert len(json.loads(data)["cases"]) == entry["cases"], name
        total += entry["cases"]
    assert total == index["total_cases"]


def test_case_ids_are_unique_per_file():
    for path in VECTORS.glob("*.json"):
        if path.name == "index.json":
            continue
        ids = [c["id"] for c in json.loads(path.read_text(encoding="utf-8"))["cases"]]
        assert len(ids) == len(set(ids)), path.name
