# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Checks on the records file of a Strata export (Evidence Format 1.0, section 5)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .canon import CanonError, canonicalize, parse_strict
from .common import FAIL, UNKNOWN, Checks, JsonlError, parse_time, split_jsonl
from .merkle import leaf_hash
from .schemas import validate

RECORD_CHECKS = [
    "records.parse", "records.canonical", "records.schema",
    "records.ids", "records.refs", "records.order",
]
_ULID = re.compile(r"^[0-7][0-9A-HJKMNP-TV-Z]{25}$")
_TIME_FIELDS = ("occurred_at", "received_at", "recorded_at")


@dataclass
class RecordsResult:
    records: list[dict] = field(default_factory=list)
    leaves: list[bytes] = field(default_factory=list)  # leaf hashes over canonical bytes
    usable: bool = False  # every line parsed, so the tree can be computed
    gaps: list[dict] = field(default_factory=list)  # gaps the Probe declared in the log


def analyze_records(data: bytes | None, checks: Checks) -> RecordsResult:
    checks.declare(*RECORD_CHECKS)
    result = RecordsResult()
    if data is None:
        for cid in RECORD_CHECKS:
            checks.add(cid, UNKNOWN, "records file not provided")
        return result
    try:
        lines = split_jsonl(data)
    except JsonlError as exc:
        checks.add("records.parse", FAIL, f"records file: {exc.code}")
        for cid in RECORD_CHECKS[1:]:
            checks.add(cid, UNKNOWN, "not evaluated: records file malformed")
        return result

    parsed_ok = True
    schema_ok: list[bool] = []
    for number, line in enumerate(lines, start=1):
        try:
            obj = parse_strict(line)
        except CanonError as exc:
            checks.add("records.parse", FAIL, f"line {number}: {exc.code}")
            parsed_ok = False
            schema_ok.append(False)
            result.records.append({})
            continue
        canonical = canonicalize(obj)
        if canonical != line:
            checks.add("records.canonical", FAIL, f"line {number}: not in canonical form")
        problem = validate("record", obj)
        if problem is None:
            try:
                for name in _TIME_FIELDS:
                    parse_time(obj[name])
                if obj["type"] == "observation" and obj["kind"] == "gap":
                    if parse_time(obj["fields"]["from"]) > parse_time(obj["fields"]["to"]):
                        problem = "fields/from: gap starts after it ends"
            except ValueError as exc:
                problem = f"invalid time: {exc}"
        if problem is not None:
            checks.add("records.schema", FAIL, f"line {number}: {problem}")
        schema_ok.append(problem is None)
        result.records.append(obj)
        result.leaves.append(leaf_hash(canonical))
    result.usable = parsed_ok

    _check_ids_refs_order(result.records, schema_ok, checks)
    for obj, ok in zip(result.records, schema_ok):
        if ok and obj["type"] == "observation" and obj["kind"] == "gap":
            gap = {"kind": "declared", "record": obj["id"], "source": obj["source"],
                   "from": obj["fields"]["from"], "to": obj["fields"]["to"],
                   "reason": obj["fields"]["reason"]}
            if "lost" in obj["fields"]:
                gap["lost"] = obj["fields"]["lost"]
            result.gaps.append(gap)
    return result


def _check_ids_refs_order(records: list[dict], schema_ok: list[bool], checks: Checks) -> None:
    seen: dict[str, str] = {}  # id -> record type, for earlier records
    last_recorded: float | None = None
    last_beat: int | None = None
    for number, (obj, ok) in enumerate(zip(records, schema_ok), start=1):
        if not ok:
            continue
        rid = obj["id"]
        if rid in seen:
            checks.add("records.ids", FAIL, f"line {number}: duplicate id {rid}")
        if obj["type"] == "evaluation":
            for ref in obj["inputs"]:
                if ref not in seen:
                    checks.add("records.refs", FAIL, f"line {number}: input {ref} is not an earlier record")
            sup = obj.get("supersedes")
            if sup is not None and seen.get(sup) != "evaluation":
                checks.add("records.refs", FAIL, f"line {number}: supersedes {sup}, not an earlier evaluation")
        elif obj["type"] == "claim" and _ULID.match(obj["about"]) and obj["about"] not in seen:
            checks.add("records.refs", FAIL, f"line {number}: about {obj['about']} is not an earlier record")
        seen.setdefault(rid, obj["type"])
        recorded = parse_time(obj["recorded_at"])
        if last_recorded is not None and recorded < last_recorded:
            checks.add("records.order", UNKNOWN, f"line {number}: recorded_at goes backwards (clock regression?)")
        last_recorded = recorded if last_recorded is None else max(last_recorded, recorded)
        if "beat" in obj:
            if last_beat is not None and obj["beat"] <= last_beat:
                checks.add("records.order", FAIL, f"line {number}: beat {obj['beat']} does not increase")
            last_beat = obj["beat"]
