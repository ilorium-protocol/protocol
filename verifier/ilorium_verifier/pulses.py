# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Checks on the pulses file of a Strata export (Evidence Format 1.0, section 8)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from .canon import CanonError, canonicalize, parse_strict
from .common import FAIL, UNKNOWN, Checks, JsonlError, parse_time, split_jsonl
from .schemas import validate
from .sigjson import LABEL_PULSE, object_digest, verify_json_signature
from .trust import Trust

PULSE_CHECKS = [
    "pulses.parse", "pulse.schema", "pulse.signature", "pulse.chain",
    "pulse.order", "pulse.interval", "pulse.checkpoint_ref",
]


@dataclass
class PulsesResult:
    count: int = 0
    first_seq: int | None = None
    last_seq: int | None = None
    gaps: list[dict] = field(default_factory=list)


def analyze_pulses(
    data: bytes,
    trust: Trust,
    now: str | None,
    root_at: Callable[[int], bytes | None],
    checks: Checks,
) -> PulsesResult:
    checks.declare(*PULSE_CHECKS)
    result = PulsesResult()
    try:
        lines = split_jsonl(data)
    except JsonlError as exc:
        checks.add("pulses.parse", FAIL, f"pulses file: {exc.code}")
        for cid in PULSE_CHECKS[1:]:
            checks.add(cid, UNKNOWN, "not evaluated: pulses file malformed")
        return result
    if not lines:
        for cid in PULSE_CHECKS:
            checks.add(cid, UNKNOWN, "no pulses in the export")
        return result

    window = (trust.max_interval_s or 0) + (trust.grace_s or 0)
    prev: dict | None = None
    prev_digest: str | None = None
    prev_time: float | None = None
    for number, line in enumerate(lines, start=1):
        label = f"pulse {number}"
        try:
            pulse = parse_strict(line)
        except CanonError as exc:
            checks.add("pulses.parse", FAIL, f"{label}: {exc.code}")
            prev = None
            continue
        if canonicalize(pulse) != line:
            checks.add("pulses.parse", FAIL, f"{label}: not in canonical form")
        problem = validate("pulse", pulse)
        pulse_time = None
        if problem is None:
            try:
                pulse_time = parse_time(pulse["translation_time"])
                if pulse["challenge"] is not None:
                    parse_time(pulse["challenge"]["issued_at"])
            except ValueError as exc:
                problem = f"invalid time: {exc}"
        if problem is None and pulse["organism"] != trust.organism:
            problem = "organism is not the configured organism"
        if problem is not None:
            checks.add("pulse.schema", FAIL, f"{label}: {problem}")
            prev = None
            continue
        result.count += 1
        result.first_seq = pulse["seq"] if result.first_seq is None else result.first_seq
        result.last_seq = pulse["seq"]

        if trust.pulse_key is None:
            checks.add("pulse.signature", UNKNOWN, "no pulse key configured")
        elif not verify_json_signature(pulse, LABEL_PULSE, trust.pulse_key):
            checks.add("pulse.signature", FAIL, f"{label}: signature does not verify")

        if prev is None:
            if pulse["seq"] == 1 and pulse["prev_pulse"] is not None:
                checks.add("pulse.chain", FAIL, f"{label}: first pulse must have prev_pulse null")
        else:
            if pulse["seq"] == prev["seq"] + 1:
                if pulse["prev_pulse"] != prev_digest:
                    checks.add("pulse.chain", FAIL, f"{label}: prev_pulse does not match the previous pulse")
            elif pulse["seq"] > prev["seq"] + 1:
                result.gaps.append({"kind": "pulse_seq", "after_seq": prev["seq"], "before_seq": pulse["seq"]})
                checks.add("pulse.chain", UNKNOWN, f"{label}: pulses {prev['seq'] + 1} to {pulse['seq'] - 1} missing")
            else:
                checks.add("pulse.chain", FAIL, f"{label}: seq does not increase")
            if pulse["beat"] < prev["beat"]:
                checks.add("pulse.order", FAIL, f"{label}: beat goes backwards")
            if pulse_time < prev_time:
                checks.add("pulse.order", FAIL, f"{label}: translation time goes backwards")
            if trust.has_freshness and pulse_time - prev_time > window:
                result.gaps.append({"kind": "pulse_interval", "from": prev["translation_time"],
                                    "to": pulse["translation_time"], "seconds": int(pulse_time - prev_time)})
                checks.add("pulse.interval", UNKNOWN, f"{label}: {int(pulse_time - prev_time)} s since the previous pulse")

        reference = pulse["checkpoint"]
        expected = root_at(reference["tree_size"])
        if expected is None:
            checks.add("pulse.checkpoint_ref", UNKNOWN, f"{label}: tree size {reference['tree_size']} not covered by the records provided")
        elif "sha256:" + expected.hex() != reference["root"]:
            checks.add("pulse.checkpoint_ref", FAIL, f"{label}: root does not match the records")

        prev, prev_digest, prev_time = pulse, object_digest(pulse), pulse_time

    if not trust.has_freshness:
        checks.add("pulse.interval", UNKNOWN, "no freshness configuration")
    elif now is not None and prev is not None and prev_time is not None:
        now_ts = parse_time(now)
        if now_ts - prev_time > window:
            result.gaps.append({"kind": "stale_pulse", "from": prev["translation_time"], "to": now,
                                "seconds": int(now_ts - prev_time)})
            checks.add("pulse.interval", UNKNOWN, f"latest pulse is {int(now_ts - prev_time)} s old")
    return result
