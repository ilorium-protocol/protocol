# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Checks a Spore document (Evidence Format 1.0, section 12)."""

from __future__ import annotations

from .canon import CanonError, parse_strict
from .common import FAIL, UNKNOWN, Checks
from .schemas import validate

SPORE_CHECKS = ("spore.parse", "spore.schema", "spore.holders")


def verify_spore(data: bytes) -> dict:
    """Return ``{"verdict", "checks"}``. The schema is closed; holder ids must be unique."""
    checks = Checks()
    checks.declare(*SPORE_CHECKS)
    try:
        obj = parse_strict(data)
    except CanonError as exc:
        checks.add("spore.parse", FAIL, exc.code)
        for cid in SPORE_CHECKS[1:]:
            checks.add(cid, UNKNOWN, "not evaluated: the Spore did not parse")
        return {"verdict": checks.overall(), "checks": checks.as_list()}
    problem = validate("spore", obj)
    if problem is not None:
        checks.add("spore.schema", FAIL, problem)
        checks.add("spore.holders", UNKNOWN, "not evaluated: the Spore does not match its schema")
        return {"verdict": checks.overall(), "checks": checks.as_list()}
    ids = [holder["id"] for holder in obj["stop_key_holders"]]
    for holder_id in sorted({i for i in ids if ids.count(i) > 1}):
        checks.add("spore.holders", FAIL, f"duplicate stop key holder id {holder_id}")
    return {"verdict": checks.overall(), "checks": checks.as_list()}
