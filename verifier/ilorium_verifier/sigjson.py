# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Ed25519 signatures over Ilorium JSON objects (Evidence Format 1.0, section 6)."""

from __future__ import annotations

import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed25519

from .canon import canonicalize
from .note import NoteError, b64decode_strict

LABEL_PULSE = "ilorium.pulse.v1"
LABEL_CHECKPOINT_META = "ilorium.checkpoint-meta.v1"


def signing_input(label: str, obj: dict) -> bytes:
    """Domain label, a newline, then the canonical form of the object without ``signature``."""
    body = {key: value for key, value in obj.items() if key != "signature"}
    return label.encode("ascii") + b"\n" + canonicalize(body)


def verify_json_signature(obj: dict, label: str, pubkey: bytes) -> bool:
    try:
        signature = b64decode_strict(obj["signature"])
        if len(signature) != 64:
            return False
        ed25519.Ed25519PublicKey.from_public_bytes(pubkey).verify(signature, signing_input(label, obj))
    except (InvalidSignature, NoteError, KeyError, TypeError, ValueError):
        return False
    return True


def object_digest(obj: dict) -> str:
    """``sha256:`` digest of the full canonical object, signature included (used by ``prev_pulse``)."""
    return "sha256:" + hashlib.sha256(canonicalize(obj)).hexdigest()
