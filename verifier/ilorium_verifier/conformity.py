# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Runs language-neutral conformity vectors (Evidence Format 1.0, section 15)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .canon import CanonError, canonicalize, parse_strict
from .common import Checks
from .merkle import leaf_hash, root_from_leaf_hashes, verify_consistency, verify_inclusion
from .note import verify_signed_note
from .records import analyze_records
from .bundle import verify_bundle
from .spore import verify_spore
from .vitalsigns import verify_vitalsigns
from .strata import verify_strata
from .trust import load_trust


@dataclass
class VectorResult:
    vector_id: str
    ok: bool
    message: str = ""


def _hex_list(items: list[str]) -> list[bytes]:
    return [bytes.fromhex(item) for item in items]


def _op_canonicalize(inp: dict) -> dict:
    data: bytes | str = bytes.fromhex(inp["json_hex"]) if "json_hex" in inp else inp["json"]
    try:
        value = parse_strict(data)
    except CanonError as exc:
        return {"verdict": "FAIL", "error": exc.code}
    return {"verdict": "PASS", "canonical": canonicalize(value).decode("utf-8")}


def _op_merkle_root(inp: dict) -> dict:
    hashes = [leaf_hash(bytes.fromhex(item)) for item in inp["leaves"]]
    return {"root": root_from_leaf_hashes(hashes).hex(), "leaf_hashes": [h.hex() for h in hashes]}


def _op_verify_inclusion(inp: dict) -> dict:
    ok = verify_inclusion(
        leaf_hash(bytes.fromhex(inp["leaf"])), inp["index"], inp["size"],
        _hex_list(inp["proof"]), bytes.fromhex(inp["root"]),
    )
    return {"verdict": "PASS" if ok else "FAIL"}


def _op_verify_consistency(inp: dict) -> dict:
    ok = verify_consistency(
        inp["first_size"], inp["second_size"], bytes.fromhex(inp["first_root"]),
        bytes.fromhex(inp["second_root"]), _hex_list(inp["proof"]),
    )
    return {"verdict": "PASS" if ok else "FAIL"}


def _op_verify_signed_note(inp: dict) -> dict:
    verdict, results = verify_signed_note(inp["note"], inp["vkeys"])
    return {"verdict": verdict, "verified": sorted(r.name for r in results if r.status == "verified")}


def _op_verify_records(inp: dict) -> dict:
    checks = Checks()
    analyze_records(inp["records_jsonl"].encode("utf-8"), checks)
    return {"verdict": checks.overall(), "checks": checks.as_map()}


def _op_verify_strata(inp: dict) -> dict:
    def blob(key: str) -> bytes | None:
        return inp[key].encode("utf-8") if key in inp else None

    report = verify_strata(
        records=blob("records_jsonl"), checkpoints=blob("checkpoints_jsonl"),
        pulses=blob("pulses_jsonl"), trust=load_trust(inp["trust"]), now=inp.get("now"),
    )
    return {
        "verdict": report["verdict"],
        "checks": {c["id"]: c["verdict"] for c in report["checks"]},
        "gap_kinds": sorted(g["kind"] for g in report["gaps"]),
    }


def _op_verify_spore(inp: dict) -> dict:
    report = verify_spore(inp["spore_json"].encode("utf-8"))
    return {"verdict": report["verdict"], "checks": {c["id"]: c["verdict"] for c in report["checks"]}}


def _files(raw: dict[str, str]) -> dict[str, bytes]:
    return {name: text.encode("utf-8") for name, text in raw.items()}


def _op_verify_bundle(inp: dict) -> dict:
    report = verify_bundle(_files(inp["files"]), load_trust(inp["trust"]), inp.get("now"))
    return {
        "verdict": report["verdict"],
        "checks": {c["id"]: c["verdict"] for c in report["checks"]},
        "gap_kinds": sorted(g["kind"] for g in report["gaps"]),
        "manifest_sha256": (report["bundle"] or {}).get("manifest_sha256"),
    }


def _op_check_vitalsigns(inp: dict) -> dict:
    bundle = inp.get("bundle")
    report = verify_vitalsigns(inp["vitalsigns_json"].encode("utf-8"), None if bundle is None else _files(bundle))
    return {"verdict": report["verdict"], "checks": {c["id"]: c["verdict"] for c in report["checks"]}}


OPERATIONS = {
    "canonicalize": _op_canonicalize,
    "merkle_root": _op_merkle_root,
    "verify_inclusion": _op_verify_inclusion,
    "verify_consistency": _op_verify_consistency,
    "verify_signed_note": _op_verify_signed_note,
    "verify_records": _op_verify_records,
    "verify_strata": _op_verify_strata,
    "verify_spore": _op_verify_spore,
    "verify_bundle": _op_verify_bundle,
    "check_vitalsigns": _op_check_vitalsigns,
}


def _matches(expected: Any, actual: Any, path: str = "") -> str | None:
    """Every key listed in ``expected`` must equal the actual value; ``checks`` is a subset match."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return f"{path or 'result'}: expected an object"
        for key, value in expected.items():
            if key not in actual:
                return f"{path}/{key}: missing"
            problem = _matches(value, actual[key], f"{path}/{key}")
            if problem:
                return problem
        return None
    if expected != actual:
        return f"{path or 'result'}: expected {expected!r}, got {actual!r}"
    return None


def run_case(operation_name: str, case: dict) -> VectorResult:
    case_id = case.get("id", "?")
    operation = OPERATIONS.get(operation_name)
    if operation is None:
        return VectorResult(case_id, False, f"unknown operation {operation_name!r}")
    try:
        actual = operation(case["input"])
    except Exception as exc:  # a conforming verifier reports, never crashes, on vector input
        return VectorResult(case_id, False, f"raised {type(exc).__name__}: {exc}")
    problem = _matches(case["expect"], actual)
    return VectorResult(case_id, problem is None, problem or "")


def run_directory(directory: Path) -> list[VectorResult]:
    """Run every vector file under ``directory`` (each file: one operation, many cases)."""
    results: list[VectorResult] = []
    for path in sorted(directory.rglob("*.json")):
        if path.name == "index.json":
            continue
        document = json.loads(path.read_text(encoding="utf-8"))
        for case in document["cases"]:
            result = run_case(document["operation"], case)
            result.vector_id = f"{path.relative_to(directory).as_posix()}::{result.vector_id}"
            results.append(result)
    return results
