# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""The trust configuration a verifier is run with (Evidence Format 1.0, section 10)."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any

from .note import NoteError, SIG_ED25519_NOTE, VKey, parse_vkey
from .schemas import validate


class TrustError(ValueError):
    pass


@dataclass(frozen=True)
class Trust:
    organism: str
    origin: str
    log_keys: list[VKey]
    witness_keys: list[VKey]
    quorum: int
    pulse_key: bytes | None
    max_interval_s: int | None
    grace_s: int | None

    @property
    def meta_key(self) -> bytes | None:
        """The log's Ed25519 key, used to verify checkpoint sidecars."""
        for key in self.log_keys:
            if key.sigtype == SIG_ED25519_NOTE:
                return key.pubkey
        return None

    @property
    def has_freshness(self) -> bool:
        return self.max_interval_s is not None and self.grace_s is not None


def load_trust(document: Any) -> Trust:
    error = validate("trust", document)
    if error:
        raise TrustError(f"trust configuration invalid: {error}")
    try:
        log_keys = [parse_vkey(item) for item in document["log"]["vkeys"]]
        witness_keys = [parse_vkey(item) for item in document["witnesses"]["vkeys"]]
    except NoteError as exc:
        raise TrustError(f"trust configuration invalid: {exc}") from exc
    pulse_key = None
    if "pulse_key" in document:
        pulse_key = base64.b64decode(document["pulse_key"].removeprefix("ed25519:"))
    freshness = document.get("freshness")
    return Trust(
        organism=document["organism"],
        origin=document["log"]["origin"],
        log_keys=log_keys,
        witness_keys=witness_keys,
        quorum=document["witnesses"]["quorum"],
        pulse_key=pulse_key,
        max_interval_s=freshness["max_interval_s"] if freshness else None,
        grace_s=freshness["grace_s"] if freshness else None,
    )
