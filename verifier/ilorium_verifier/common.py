# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Verdicts, check bookkeeping, time parsing and JSON Lines splitting."""

from __future__ import annotations

from datetime import datetime, timezone

PASS, FAIL, UNKNOWN = "PASS", "FAIL", "UNKNOWN"
_RANK = {PASS: 0, UNKNOWN: 1, FAIL: 2}


def worst(verdicts: list[str]) -> str:
    """FAIL outranks UNKNOWN, which outranks PASS."""
    return max(verdicts, key=_RANK.__getitem__, default=PASS)


class Checks:
    """Worst verdict and first details per check id, in declaration order."""

    MAX_DETAILS = 5

    def __init__(self) -> None:
        self._items: dict[str, dict] = {}

    def declare(self, *check_ids: str) -> None:
        for cid in check_ids:
            self._items.setdefault(cid, {"verdict": PASS, "details": []})

    def add(self, cid: str, verdict: str, detail: str = "") -> None:
        self.declare(cid)
        item = self._items[cid]
        item["verdict"] = worst([item["verdict"], verdict])
        if verdict != PASS and detail and len(item["details"]) < self.MAX_DETAILS:
            item["details"].append(detail)

    def verdict(self, cid: str) -> str:
        return self._items[cid]["verdict"]

    def overall(self) -> str:
        return worst([item["verdict"] for item in self._items.values()])

    def as_list(self) -> list[dict]:
        return [
            {"id": cid, "verdict": item["verdict"], "detail": "; ".join(item["details"])}
            for cid, item in self._items.items()
        ]

    def as_map(self) -> dict[str, str]:
        return {cid: item["verdict"] for cid, item in self._items.items()}


def parse_time(text: str) -> float:
    """Seconds since the epoch for an Evidence Format time string; ValueError if invalid."""
    moment = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if moment.tzinfo is None:
        raise ValueError("time must be UTC")
    return moment.astimezone(timezone.utc).timestamp()


class JsonlError(ValueError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def split_jsonl(data: bytes) -> list[bytes]:
    """Split a JSON Lines file: LF-terminated, no blank lines, no CR."""
    if data == b"":
        return []
    if b"\r" in data:
        raise JsonlError("carriage_return")
    if not data.endswith(b"\n"):
        raise JsonlError("no_final_newline")
    lines = data[:-1].split(b"\n")
    if any(line == b"" for line in lines):
        raise JsonlError("blank_line")
    return lines
