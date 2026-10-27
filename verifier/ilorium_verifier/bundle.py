# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Verification of an Evidence Bundle (Evidence Format 1.0, section 13)."""

from __future__ import annotations

import base64
import hashlib

from .canon import CanonError, canonicalize, parse_strict
from .common import FAIL, UNKNOWN, Checks, JsonlError, parse_time, split_jsonl, worst
from .schemas import validate
from .spore import SPORE_CHECKS, verify_spore
from .strata import LIMITATIONS, verify_strata
from .trust import Trust

MANIFEST = "bundle.json"
TRUST_FILE = "trust.json"
BUNDLE_CHECKS = (
    "bundle.parse", "bundle.schema", "bundle.files", "bundle.no_trust",
    "bundle.period", "bundle.identity", "bundle.spore_key",
)
BUNDLE_LIMITATIONS = [
    "The manifest is a list of checksums. It is not signed: it shows that the files are the ones listed, not who assembled the bundle.",
    "The Spore is what the organism says about itself; the bundle shows that it was published, not that it is true.",
]


def sha256_label(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def parse_manifest(files: dict[str, bytes]) -> tuple[dict | None, str, str, str]:
    """Return ``(manifest, check_id, verdict, reason)``; the last three describe the problem when there is no manifest."""
    data = files.get(MANIFEST)
    if data is None:
        return None, "bundle.parse", UNKNOWN, f"{MANIFEST} not provided"
    try:
        obj = parse_strict(data)
    except CanonError as exc:
        return None, "bundle.parse", FAIL, f"{MANIFEST}: {exc.code}"
    if data != canonicalize(obj) + b"\n":
        return None, "bundle.parse", FAIL, f"{MANIFEST}: not in canonical form"
    problem = validate("bundle", obj)
    if problem is None:
        try:
            start, end, created = (parse_time(obj["period"]["from"]), parse_time(obj["period"]["to"]),
                                   parse_time(obj["created_at"]))
            if not start <= end <= created:
                problem = "period must satisfy from <= to <= created_at"
        except ValueError as exc:
            problem = f"invalid time: {exc}"
    if problem is not None:
        return None, "bundle.schema", FAIL, f"{MANIFEST}: {problem}"
    return obj, "", "", ""


def check_listed_files(manifest: dict, files: dict[str, bytes], checks: Checks) -> None:
    for name, ref in manifest["files"].items():
        data = files.get(name)
        if data is None:
            checks.add("bundle.files", UNKNOWN, f"{name} is listed but was not provided")
            continue
        if sha256_label(data) != ref["sha256"]:
            checks.add("bundle.files", FAIL, f"{name}: sha256 does not match the manifest")
        elif len(data) != ref["bytes"]:
            checks.add("bundle.files", FAIL, f"{name}: size does not match the manifest")
        elif "entries" in ref and data.count(b"\n") != ref["entries"]:
            checks.add("bundle.files", FAIL, f"{name}: number of entries does not match the manifest")
    for name in sorted(files):
        if name != MANIFEST and name not in manifest["files"]:
            checks.add("bundle.files", FAIL, f"{name} is present but not listed")


def _record_times(data: bytes) -> list[float]:
    times: list[float] = []
    try:
        lines = split_jsonl(data)
    except JsonlError:
        return times
    for line in lines:
        try:
            value = parse_strict(line).get("recorded_at")
            if isinstance(value, str):
                times.append(parse_time(value))
        except (CanonError, ValueError):
            continue
    return times


def verify_bundle(files: dict[str, bytes], trust: Trust, now: str | None = None) -> dict:
    checks = Checks()
    checks.declare(*BUNDLE_CHECKS, *SPORE_CHECKS)
    manifest, problem_check, problem_verdict, reason = parse_manifest(files)

    if manifest is None:
        checks.add(problem_check, problem_verdict, reason)
        for cid in (*BUNDLE_CHECKS, *SPORE_CHECKS):
            if cid not in ("bundle.no_trust", problem_check):
                checks.add(cid, UNKNOWN, "not evaluated: manifest unavailable")
    else:
        check_listed_files(manifest, files, checks)
        spore_bytes = files.get("spore.json")
        if spore_bytes is not None:
            spore_report = verify_spore(spore_bytes)
            for item in spore_report["checks"]:
                checks.add(item["id"], item["verdict"], item["detail"])
        else:
            for cid in SPORE_CHECKS:
                checks.add(cid, UNKNOWN, "spore.json not provided")
        _identity_and_period(manifest, files, trust, checks)

    if TRUST_FILE in files:
        checks.add("bundle.no_trust", FAIL, f"the bundle carries {TRUST_FILE}; trust is brought by the verifier, never by the bundle")

    strata = verify_strata(
        records=files.get("records.jsonl"), checkpoints=files.get("checkpoints.jsonl"),
        pulses=files.get("pulses.jsonl"), trust=trust, now=now,
    )
    all_checks = checks.as_list() + strata["checks"]
    report = dict(strata)
    report["checks"] = all_checks
    report["verdict"] = worst([c["verdict"] for c in all_checks])
    report["limitations"] = LIMITATIONS + BUNDLE_LIMITATIONS
    report["bundle"] = None if manifest is None else {
        "manifest_sha256": sha256_label(files[MANIFEST]),
        "created_at": manifest["created_at"],
        "period": manifest["period"],
        "files": sorted(manifest["files"]),
    }
    return report


def _identity_and_period(manifest: dict, files: dict[str, bytes], trust: Trust, checks: Checks) -> None:
    if manifest["organism"] != trust.organism:
        checks.add("bundle.identity", FAIL, "manifest organism is not the configured organism")
    if manifest["origin"] != trust.origin:
        checks.add("bundle.identity", FAIL, "manifest origin is not the configured log origin")

    spore = None
    spore_bytes = files.get("spore.json")
    if spore_bytes is not None:
        try:
            candidate = parse_strict(spore_bytes)
            if validate("spore", candidate) is None:
                spore = candidate
        except CanonError:
            pass
    if spore is None:
        checks.add("bundle.identity", UNKNOWN, "the Spore is missing or invalid, so it cannot be compared with the manifest")
        checks.add("bundle.spore_key", UNKNOWN, "the Spore is missing or invalid")
    else:
        if spore["organism"] != manifest["organism"]:
            checks.add("bundle.identity", FAIL, "Spore organism differs from the manifest")
        if spore["domain"] != manifest["domain"]:
            checks.add("bundle.identity", FAIL, "Spore domain differs from the manifest")
        spore_key = spore.get("pulse_key")
        if spore_key is None or trust.pulse_key is None:
            checks.add("bundle.spore_key", UNKNOWN, "the Spore or the trust configuration has no pulse key to compare")
        elif base64.b64decode(spore_key.removeprefix("ed25519:")) != trust.pulse_key:
            checks.add("bundle.spore_key", FAIL, "the Spore's pulse key differs from the pulse key you trust")

    records = files.get("records.jsonl")
    if records is None:
        checks.add("bundle.period", UNKNOWN, "records not provided")
        return
    start, end = parse_time(manifest["period"]["from"]), parse_time(manifest["period"]["to"])
    for moment in _record_times(records):
        if not start <= moment <= end:
            checks.add("bundle.period", FAIL, "a record lies outside the declared period")
            break
