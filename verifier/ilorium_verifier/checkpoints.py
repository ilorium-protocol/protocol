# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Checks on the checkpoints file of a Strata export (Evidence Format 1.0, section 7)."""

from __future__ import annotations

from dataclasses import dataclass, field

from .canon import CanonError, canonicalize, parse_strict
from .common import FAIL, UNKNOWN, Checks, JsonlError, parse_time, split_jsonl
from .note import NoteError, Checkpoint, parse_checkpoint, parse_note, verify_note_signatures
from .schemas import validate
from .sigjson import LABEL_CHECKPOINT_META, verify_json_signature
from .trust import Trust

CHECKPOINT_CHECKS = [
    "checkpoints.parse", "checkpoint.note", "checkpoint.log_signature", "checkpoint.witnesses",
    "checkpoint.meta", "checkpoint.monotonic", "checkpoint.interval", "checkpoint.witness_time",
]


@dataclass
class CheckpointsResult:
    caps: list[Checkpoint] = field(default_factory=list)  # checkpoints whose note parsed
    gaps: list[dict] = field(default_factory=list)
    latest: dict | None = None


def _iso(seconds: float) -> str:
    from datetime import datetime, timezone

    return datetime.fromtimestamp(seconds, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def analyze_checkpoints(
    data: bytes | None, trust: Trust, now: str | None, checks: Checks
) -> CheckpointsResult:
    checks.declare(*CHECKPOINT_CHECKS)
    result = CheckpointsResult()
    if data is None:
        for cid in CHECKPOINT_CHECKS:
            checks.add(cid, UNKNOWN, "checkpoints file not provided")
        return result
    try:
        lines = split_jsonl(data)
    except JsonlError as exc:
        checks.add("checkpoints.parse", FAIL, f"checkpoints file: {exc.code}")
        for cid in CHECKPOINT_CHECKS[1:]:
            checks.add(cid, UNKNOWN, "not evaluated: checkpoints file malformed")
        return result
    if not lines:
        for cid in CHECKPOINT_CHECKS:
            checks.add(cid, UNKNOWN, "no checkpoints in the export")
        return result

    log_ids = {(k.name, k.key_id) for k in trust.log_keys}
    witness_ids = {(k.name, k.key_id) for k in trust.witness_keys} - log_ids
    all_keys = trust.log_keys + trust.witness_keys
    now_ts = parse_time(now) if now else None
    window = (trust.max_interval_s or 0) + (trust.grace_s or 0)

    prev_cp: Checkpoint | None = None
    prev_time: float | None = None
    prev_beat: int | None = None
    last_meta: dict | None = None
    last_time: float | None = None

    for number, line in enumerate(lines, start=1):
        label = f"checkpoint {number}"
        try:
            obj = parse_strict(line)
        except CanonError as exc:
            checks.add("checkpoints.parse", FAIL, f"{label}: {exc.code}")
            continue
        if canonicalize(obj) != line:
            checks.add("checkpoints.parse", FAIL, f"{label}: not in canonical form")
        if set(obj) != {"note", "meta"} or not isinstance(obj["note"], str):
            checks.add("checkpoints.parse", FAIL, f"{label}: expected exactly note and meta")
            continue
        try:
            parsed = parse_note(obj["note"])
            cp = parse_checkpoint(parsed.text)
        except NoteError as exc:
            checks.add("checkpoint.note", FAIL, f"{label}: {exc}")
            continue
        if cp.origin != trust.origin:
            checks.add("checkpoint.note", FAIL, f"{label}: origin is not the configured log origin")
            continue
        if cp.extensions:
            checks.add("checkpoint.note", FAIL, f"{label}: extension lines are not allowed")
        result.caps.append(cp)

        sigs = verify_note_signatures(parsed, cp, all_keys)
        log_sigs = [s for s in sigs if (s.name, s.key_id) in log_ids]
        witness_sigs = [s for s in sigs if (s.name, s.key_id) in witness_ids]

        # --- log signature ---
        if any(s.status == "failed" for s in log_sigs):
            checks.add("checkpoint.log_signature", FAIL, f"{label}: log signature does not verify")
        elif not any(s.status == "verified" for s in log_sigs):
            if any(s.status == "unsupported" for s in log_sigs):
                checks.add("checkpoint.log_signature", UNKNOWN, f"{label}: log key uses an unsupported algorithm")
            else:
                checks.add("checkpoint.log_signature", FAIL, f"{label}: not signed by a configured log key")

        # --- sidecar ---
        meta, meta_time = obj["meta"], None
        problem = validate("checkpoint-meta", meta)
        if problem is None:
            try:
                meta_time = parse_time(meta["translation_time"])
            except ValueError as exc:
                problem = f"invalid time: {exc}"
        if problem is None and (
            meta["origin"] != cp.origin
            or meta["tree_size"] != cp.size
            or meta["root"] != "sha256:" + cp.root.hex()
        ):
            problem = "does not match the checkpoint note"
        if problem is not None:
            checks.add("checkpoint.meta", FAIL, f"{label}: {problem}")
        elif trust.meta_key is None:
            checks.add("checkpoint.meta", UNKNOWN, f"{label}: no Ed25519 log key to verify the sidecar")
        elif not verify_json_signature(meta, LABEL_CHECKPOINT_META, trust.meta_key):
            checks.add("checkpoint.meta", FAIL, f"{label}: sidecar signature does not verify")
        if problem is None:
            last_meta, last_time = meta, meta_time

        # --- witnesses ---
        failed = [s for s in witness_sigs if s.status == "failed"]
        verified = [s for s in witness_sigs if s.status == "verified"]
        future = [s for s in verified if now_ts is not None and s.timestamp is not None and s.timestamp > now_ts]
        counted = {s.name for s in verified if s not in future}
        unsupported = {s.name for s in witness_sigs if s.status == "unsupported"}
        if failed:
            checks.add("checkpoint.witnesses", FAIL, f"{label}: a witness cosignature does not verify")
        elif len(counted) < trust.quorum:
            checks.add("checkpoint.witnesses", UNKNOWN,
                       f"{label}: {len(counted)} verified of {trust.quorum} required"
                       + (f"; {len(unsupported)} on unsupported algorithms" if unsupported else ""))
        if future:
            checks.add("checkpoint.witness_time", UNKNOWN, f"{label}: a witness timestamp is in the future")

        # --- sequence ---
        if prev_cp is not None:
            if cp.size < prev_cp.size:
                checks.add("checkpoint.monotonic", FAIL, f"{label}: tree size shrinks")
            elif cp.size == prev_cp.size and cp.root != prev_cp.root:
                checks.add("checkpoint.monotonic", FAIL, f"{label}: same size, different root")
        if problem is None:
            if prev_beat is not None and meta["beat"] < prev_beat:
                checks.add("checkpoint.monotonic", FAIL, f"{label}: beat goes backwards")
            if prev_time is not None and meta_time < prev_time:
                checks.add("checkpoint.monotonic", FAIL, f"{label}: translation time goes backwards")
            if trust.has_freshness:
                if prev_time is not None and meta_time - prev_time > window:
                    result.gaps.append({"kind": "checkpoint_interval", "from": _iso(prev_time),
                                        "to": meta["translation_time"], "seconds": int(meta_time - prev_time)})
                    checks.add("checkpoint.interval", UNKNOWN,
                               f"{label}: {int(meta_time - prev_time)} s since the previous checkpoint")
                for s in verified:
                    if s.timestamp is not None and abs(s.timestamp - meta_time) > (trust.grace_s or 0):
                        checks.add("checkpoint.witness_time", UNKNOWN,
                                   f"{label}: witness {s.name} timestamp differs from checkpoint time")
            prev_beat, prev_time = meta["beat"], meta_time
        prev_cp = cp

    if not trust.has_freshness:
        checks.add("checkpoint.interval", UNKNOWN, "no freshness configuration")
        checks.add("checkpoint.witness_time", UNKNOWN, "no freshness configuration")
    elif now_ts is not None and last_time is not None and now_ts - last_time > window:
        result.gaps.append({"kind": "stale", "from": last_meta["translation_time"], "to": _iso(now_ts),
                            "seconds": int(now_ts - last_time)})
        checks.add("checkpoint.interval", UNKNOWN, f"latest checkpoint is {int(now_ts - last_time)} s old")
    if prev_cp is not None and last_meta is not None and last_time is not None:
        result.latest = {"tree_size": prev_cp.size, "root": "sha256:" + prev_cp.root.hex(),
                         "beat": last_meta["beat"], "translation_time": last_meta["translation_time"]}
        if now_ts is not None:
            result.latest["age_s"] = int(now_ts - last_time)
    return result
