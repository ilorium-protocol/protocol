# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Checks that Vital Signs match the Evidence Bundle they link to (Evidence Format 1.0, section 14)."""

from __future__ import annotations

import re

from .bundle import check_listed_files, parse_manifest, sha256_label, MANIFEST
from .canon import CanonError, parse_strict
from .common import FAIL, UNKNOWN, Checks, JsonlError, parse_time, split_jsonl
from .schemas import validate

VITALS_CHECKS = (
    "vitals.parse", "vitals.schema", "vitals.words", "vitals.bundle",
    "vitals.identity", "vitals.pulse", "vitals.stop_key_holders",
)
FORBIDDEN_WORDS = ("certified", "trusted", "approved")
_WORDS = re.compile(r"\b(" + "|".join(FORBIDDEN_WORDS) + r")\b", re.IGNORECASE)


def _times_ok(vital: dict) -> str | None:
    try:
        start, end, generated = (parse_time(vital["period"]["from"]), parse_time(vital["period"]["to"]),
                                 parse_time(vital["generated_at"]))
        if not start <= end <= generated:
            return "period must satisfy from <= to <= generated_at"
        if vital["latest_pulse"] is not None:
            parse_time(vital["latest_pulse"]["translation_time"])
        for name, dim in vital["dimensions"].items():
            if dim["newest_evidence"] is not None and parse_time(dim["newest_evidence"]) > end:
                return f"dimensions/{name}: newest_evidence is after the end of the period"
    except ValueError as exc:
        return f"invalid time: {exc}"
    laws = [item["law"] for item in vital["conformity"]]
    if len(laws) != len(set(laws)):
        return "conformity lists a law twice"
    return None


def _texts(vital: dict) -> list[str]:
    out = list(vital["limitations"])
    for dim in vital["dimensions"].values():
        out += dim["limitations"]
    return out


def verify_vitalsigns(data: bytes, bundle_files: dict[str, bytes] | None) -> dict:
    """``bundle_files`` is None when the bundle could not be reached: the verdict is then UNKNOWN, never PASS."""
    checks = Checks()
    checks.declare(*VITALS_CHECKS)
    try:
        vital = parse_strict(data)
    except CanonError as exc:
        checks.add("vitals.parse", FAIL, exc.code)
        for cid in VITALS_CHECKS[1:]:
            checks.add(cid, UNKNOWN, "not evaluated: the Vital Signs did not parse")
        return {"verdict": checks.overall(), "checks": checks.as_list()}
    problem = validate("vitalsigns", vital)
    if problem is None:
        problem = _times_ok(vital)
    if problem is not None:
        checks.add("vitals.schema", FAIL, problem)
        for cid in VITALS_CHECKS[2:]:
            checks.add(cid, UNKNOWN, "not evaluated: the Vital Signs do not match their schema")
        return {"verdict": checks.overall(), "checks": checks.as_list()}

    for text in _texts(vital):
        match = _WORDS.search(text)
        if match:
            checks.add("vitals.words", FAIL, f"the word {match.group(0)!r} is not allowed in Vital Signs")

    rest = [c for c in VITALS_CHECKS[3:]]
    if bundle_files is None:
        for cid in rest:
            checks.add(cid, UNKNOWN, "the Evidence Bundle could not be reached")
        return {"verdict": checks.overall(), "checks": checks.as_list()}

    manifest, _check, problem_verdict, reason = parse_manifest(bundle_files)
    if manifest is None:
        checks.add("vitals.bundle", problem_verdict, reason)
        for cid in rest[1:]:
            checks.add(cid, UNKNOWN, "not evaluated: manifest unavailable")
        return {"verdict": checks.overall(), "checks": checks.as_list()}

    if sha256_label(bundle_files[MANIFEST]) != vital["bundle"]["manifest_sha256"]:
        checks.add("vitals.bundle", FAIL, "the bundle's manifest is not the one these Vital Signs were computed from")
    file_checks = Checks()
    file_checks.declare("bundle.files")
    check_listed_files(manifest, bundle_files, file_checks)
    listed = file_checks.as_list()[0]
    if listed["verdict"] != "PASS":
        checks.add("vitals.bundle", listed["verdict"], listed["detail"])

    if (vital["organism"], vital["domain"], vital["period"]) != (manifest["organism"], manifest["domain"], manifest["period"]):
        checks.add("vitals.identity", FAIL, "organism, domain or period differ from the bundle's manifest")

    pulses = bundle_files.get("pulses.jsonl")
    if pulses is None:
        checks.add("vitals.pulse", UNKNOWN, "pulses.jsonl is not in the bundle")
    else:
        try:
            lines = split_jsonl(pulses)
            last = parse_strict(lines[-1]) if lines else None
        except (JsonlError, CanonError):
            checks.add("vitals.pulse", UNKNOWN, "the bundle's pulses cannot be read")
        else:
            expected = None if last is None else {
                "seq": last.get("seq"), "beat": last.get("beat"), "translation_time": last.get("translation_time"),
                "state": last.get("state"), "recovery": last.get("recovery"),
            }
            if vital["latest_pulse"] != expected:
                checks.add("vitals.pulse", FAIL, "latest_pulse is not the last pulse in the bundle")

    spore_bytes = bundle_files.get("spore.json")
    try:
        spore = parse_strict(spore_bytes) if spore_bytes is not None else None
    except CanonError:
        spore = None
    if spore is None or "stop_key_holders" not in spore:
        checks.add("vitals.stop_key_holders", UNKNOWN, "the bundle's Spore cannot be read")
    elif vital["stop_key_holders"] != spore["stop_key_holders"]:
        checks.add("vitals.stop_key_holders", FAIL, "stop_key_holders differ from the Spore in the bundle")

    return {"verdict": checks.overall(), "checks": checks.as_list()}
