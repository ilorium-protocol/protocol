# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Verification of a Strata export and the report it produces (Evidence Format 1.0, sections 9 and 10)."""

from __future__ import annotations

from . import __version__
from .note import mldsa44_available
from .checkpoints import analyze_checkpoints
from .common import FAIL, UNKNOWN, Checks
from .merkle import EMPTY_ROOT, IncrementalTree
from .pulses import analyze_pulses
from .records import analyze_records
from .trust import Trust

PROTOCOL_RELEASE = "1.0"
LIMITATIONS = [
    "A signature shows who signed, not that the content is true.",
    "Only the records, checkpoints and pulses provided were checked; this cannot show that every relevant event was recorded.",
    "Records after the latest checkpoint are not protected by it.",
    "Keys come from the trust configuration supplied to the verifier; anchoring them in the birth act is not implemented yet.",
    "This verifier checks evidence integrity only; it does not evaluate the Genome's laws or Proof of Life.",
]


def _prefix_roots(leaves: list[bytes]) -> list[bytes]:
    """Root at every prefix size 0..len(leaves)."""
    tree = IncrementalTree()
    roots = [EMPTY_ROOT]
    for leaf in leaves:
        tree.append(leaf)
        roots.append(tree.root())
    return roots


def verify_strata(
    *,
    records: bytes | None,
    checkpoints: bytes | None,
    pulses: bytes | None,
    trust: Trust,
    now: str | None = None,
) -> dict:
    checks = Checks()
    rec = analyze_records(records, checks)
    cps = analyze_checkpoints(checkpoints, trust, now, checks)

    checks.declare("log.root", "log.coverage")
    prefix: list[bytes] | None = None
    if rec.usable:
        prefix = _prefix_roots(rec.leaves)
    else:
        checks.add("log.root", UNKNOWN, "records unavailable or malformed")
        checks.add("log.coverage", UNKNOWN, "records unavailable or malformed")

    def root_at(size: int) -> bytes | None:
        if prefix is None or size >= len(prefix):
            return None
        return prefix[size]

    if prefix is not None:
        total = len(rec.leaves)
        if not cps.caps:
            checks.add("log.root", UNKNOWN, "no checkpoint to compare the records with")
            checks.add("log.coverage", UNKNOWN, "no checkpoints")
        else:
            for cp in cps.caps:
                expected = root_at(cp.size)
                if expected is None:
                    checks.add("log.root", UNKNOWN,
                               f"checkpoint covers {cp.size} records but only {total} were provided")
                elif expected != cp.root:
                    checks.add("log.root", FAIL, f"records do not produce the root of the checkpoint of size {cp.size}")
            covered = max(cp.size for cp in cps.caps)
            if covered < total:
                checks.add("log.coverage", UNKNOWN, f"{total - covered} records come after the latest checkpoint")

    pulse_result = analyze_pulses(pulses, trust, now, root_at, checks) if pulses is not None else None

    gaps = list(rec.gaps) + cps.gaps + (pulse_result.gaps if pulse_result else [])
    covered_size = max((cp.size for cp in cps.caps), default=0)
    summary = {
        "records": len(rec.leaves) if rec.usable else None,
        "checkpoints": len(cps.caps),
        "pulses": pulse_result.count if pulse_result else None,
        "uncovered_records": (len(rec.leaves) - covered_size) if rec.usable and cps.caps else None,
        "latest_checkpoint": cps.latest,
    }
    return {
        "report": "1.0",
        "verifier": {"name": "ilorium-verifier", "version": __version__, "ml_dsa_44": mldsa44_available()},
        "protocol_release": PROTOCOL_RELEASE,
        "organism": trust.organism,
        "origin": trust.origin,
        "verdict": checks.overall(),
        "summary": summary,
        "checks": checks.as_list(),
        "gaps": gaps,
        "limitations": LIMITATIONS,
    }
