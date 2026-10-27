# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""C2SP signed notes, checkpoints and cosignatures.

Pinned to c2sp.org/signed-note@v1.1.0, c2sp.org/tlog-checkpoint@v1.1.0 and
c2sp.org/tlog-cosignature@v1.1.0 (see Evidence Format 1.0, section 7).
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import re
from dataclasses import dataclass, field

from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.hazmat.primitives.asymmetric import ed25519

try:  # ML-DSA needs cryptography >= 48 built against OpenSSL >= 3.5
    from cryptography.hazmat.primitives.asymmetric import mldsa
except ImportError:  # pragma: no cover - depends on the environment
    mldsa = None

from .canon import MAX_SAFE_INT

# Signature type identifier bytes (signed-note v1.1.0).
SIG_ED25519_NOTE = 0x01
SIG_ECDSA = 0x02
SIG_ED25519_COSIG = 0x04
SIG_MLDSA44_COSIG = 0x06
SUPPORTED_TYPES = {SIG_ED25519_NOTE, SIG_ED25519_COSIG, SIG_MLDSA44_COSIG}

_PUBKEY_LEN = {SIG_ED25519_NOTE: 32, SIG_ED25519_COSIG: 32, SIG_MLDSA44_COSIG: 1312}
_SIG_LEN = {SIG_ED25519_NOTE: 64, SIG_ED25519_COSIG: 8 + 64, SIG_MLDSA44_COSIG: 8 + 2420}
MAX_SIGNATURES = 64
EM_DASH = "—"
_MLDSA_LABEL = b"subtree/v1\n\x00"


class NoteError(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def b64decode_strict(text: str) -> bytes:
    """Standard base64 with padding; reject non-canonical encodings (RFC 4648 section 3.5)."""
    try:
        raw = base64.b64decode(text.encode("ascii"), validate=True)
    except (binascii.Error, UnicodeEncodeError) as exc:
        raise NoteError("bad_base64", text[:40]) from exc
    if base64.b64encode(raw).decode("ascii") != text:
        raise NoteError("non_canonical_base64", text[:40])
    return raw


def _valid_name(name: str) -> bool:
    return bool(name) and not any(
        ch.isspace() or ch == "+" or ord(ch) < 0x20 for ch in name
    )


@dataclass(frozen=True)
class VKey:
    name: str
    key_id: bytes
    sigtype: int
    pubkey: bytes
    raw: str = field(default="", compare=False)

    @property
    def supported(self) -> bool:
        return self.sigtype in SUPPORTED_TYPES


def compute_key_id(name: str, sigtype: int, pubkey: bytes) -> bytes:
    return hashlib.sha256(name.encode("utf-8") + b"\n" + bytes([sigtype]) + pubkey).digest()[:4]


def make_vkey(name: str, sigtype: int, pubkey: bytes) -> str:
    key_id = compute_key_id(name, sigtype, pubkey).hex()
    return f"{name}+{key_id}+{base64.b64encode(bytes([sigtype]) + pubkey).decode('ascii')}"


_HEX8 = re.compile(r"^[0-9a-f]{8}$")


def parse_vkey(text: str) -> VKey:
    parts = text.split("+", 2)  # base64 key material may itself contain "+"
    if len(parts) != 3:
        raise NoteError("bad_vkey", "expected name+id+key")
    name, id_hex, key_b64 = parts
    if not _valid_name(name):
        raise NoteError("bad_vkey", "invalid key name")
    if not _HEX8.match(id_hex):
        raise NoteError("bad_vkey", "invalid key id")
    material = b64decode_strict(key_b64)
    if len(material) < 2:
        raise NoteError("bad_vkey", "key material too short")
    sigtype, pubkey = material[0], material[1:]
    key_id = bytes.fromhex(id_hex)
    if sigtype in SUPPORTED_TYPES:
        if len(pubkey) != _PUBKEY_LEN[sigtype]:
            raise NoteError("bad_vkey", "wrong public key length")
        if compute_key_id(name, sigtype, pubkey) != key_id:
            raise NoteError("bad_vkey", "key id does not match key")
    return VKey(name, key_id, sigtype, pubkey, text)


@dataclass(frozen=True)
class NoteSig:
    name: str
    key_id: bytes
    payload: bytes  # everything after the 4-byte key id


@dataclass(frozen=True)
class ParsedNote:
    text: str
    sigs: list[NoteSig]


def parse_note(note: str) -> ParsedNote:
    try:
        note.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise NoteError("invalid_utf8") from exc
    if any(ord(ch) < 0x20 and ch != "\n" for ch in note):
        raise NoteError("control_character")
    if not note.endswith("\n"):
        raise NoteError("no_final_newline")
    cut = note.rfind("\n\n")
    if cut < 0:
        raise NoteError("no_signature_block")
    text, block = note[: cut + 1], note[cut + 2 :]
    if not block:
        raise NoteError("no_signatures")
    lines = block[:-1].split("\n")
    if len(lines) > MAX_SIGNATURES:
        raise NoteError("too_many_signatures")
    sigs: list[NoteSig] = []
    for line in lines:
        if not line.startswith(EM_DASH + " "):
            raise NoteError("bad_signature_line", line[:40])
        name, sep, b64 = line[2:].partition(" ")
        if not sep or not _valid_name(name) or " " in b64:
            raise NoteError("bad_signature_line", line[:40])
        blob = b64decode_strict(b64)
        if len(blob) < 5:
            raise NoteError("bad_signature_line", "signature too short")
        sigs.append(NoteSig(name, blob[:4], blob[4:]))
    return ParsedNote(text, sigs)


@dataclass(frozen=True)
class Checkpoint:
    origin: str
    size: int
    root: bytes
    extensions: list[str]
    text: str


_SIZE = re.compile(r"^(0|[1-9][0-9]*)$")


def parse_checkpoint(text: str) -> Checkpoint:
    if not text.endswith("\n"):
        raise NoteError("no_final_newline")
    lines = text[:-1].split("\n")
    if len(lines) < 3 or any(line == "" for line in lines):
        raise NoteError("bad_checkpoint", "need three non-empty lines")
    origin, size_text, root_text = lines[0], lines[1], lines[2]
    if not _valid_name(origin) or len(origin.encode("utf-8")) > 255:
        raise NoteError("bad_checkpoint", "invalid origin")
    if not _SIZE.match(size_text):
        raise NoteError("bad_checkpoint", "invalid tree size")
    size = int(size_text)
    if size > MAX_SAFE_INT:
        raise NoteError("bad_checkpoint", "tree size out of range")
    root = b64decode_strict(root_text)
    if len(root) != 32:
        raise NoteError("bad_checkpoint", "root hash must be 32 bytes")
    return Checkpoint(origin, size, root, lines[3:], text)


def format_checkpoint(origin: str, size: int, root: bytes) -> str:
    return f"{origin}\n{size}\n{base64.b64encode(root).decode('ascii')}\n"


def cosignature_message_ed25519(timestamp: int, cp: Checkpoint) -> bytes:
    """tlog-cosignature v1.1.0, Ed25519: the signed lines."""
    body = (
        "cosignature/v1\n"
        f"time {timestamp}\n"
        f"{cp.origin}\n{cp.size}\n{base64.b64encode(cp.root).decode('ascii')}\n"
    )
    body += "".join(f"{line}\n" for line in cp.extensions)
    return body.encode("utf-8")


def cosignature_message_mldsa44(cosigner: str, timestamp: int, cp: Checkpoint) -> bytes:
    """tlog-cosignature v1.1.0, ML-DSA-44: the CosignedSubtree structure for a checkpoint."""
    name, origin = cosigner.encode("utf-8"), cp.origin.encode("utf-8")
    return (
        _MLDSA_LABEL
        + bytes([len(name)]) + name
        + timestamp.to_bytes(8, "big")
        + bytes([len(origin)]) + origin
        + (0).to_bytes(8, "big")
        + cp.size.to_bytes(8, "big")
        + cp.root
    )


def mldsa44_available() -> bool:
    """Whether this environment can verify ML-DSA-44. When it cannot, signatures of that type are
    reported ``unsupported`` (so the verdict is UNKNOWN), never as an error and never as PASS."""
    if mldsa is None:
        return False
    try:
        mldsa.MLDSA44PrivateKey.from_seed_bytes(bytes(32)).public_key()
    except (UnsupportedAlgorithm, AttributeError, NotImplementedError):  # pragma: no cover
        return False
    return True


@dataclass(frozen=True)
class SigResult:
    name: str
    key_id: bytes
    status: str  # verified | failed | unsupported | unknown_key
    sigtype: int | None = None
    timestamp: int | None = None
    detail: str = ""


def verify_note_signatures(parsed: ParsedNote, cp: Checkpoint | None, keys: list[VKey]) -> list[SigResult]:
    """Evaluate every signature line against the configured keys.

    Signatures from unknown keys are ignored (reported as ``unknown_key``); a signature
    from a known key must verify (signed-note v1.1.0, section Signatures).
    ``cp`` is required to verify cosignature types.
    """
    results: list[SigResult] = []
    for sig in parsed.sigs:
        matches = [k for k in keys if k.name == sig.name and k.key_id == sig.key_id]
        if not matches:
            results.append(SigResult(sig.name, sig.key_id, "unknown_key"))
            continue
        key = matches[0]
        if not key.supported:
            results.append(SigResult(sig.name, sig.key_id, "unsupported", key.sigtype,
                                     detail=f"signature type 0x{key.sigtype:02x}"))
            continue
        if key.sigtype == SIG_MLDSA44_COSIG and not mldsa44_available():
            results.append(SigResult(sig.name, sig.key_id, "unsupported", key.sigtype,
                                     detail="ML-DSA-44 is not available in this environment"))
            continue
        if len(sig.payload) != _SIG_LEN[key.sigtype]:
            results.append(SigResult(sig.name, sig.key_id, "failed", key.sigtype, detail="bad length"))
            continue
        timestamp: int | None = None
        try:
            if key.sigtype == SIG_ED25519_NOTE:
                message, value = parsed.text.encode("utf-8"), sig.payload
                ed25519.Ed25519PublicKey.from_public_bytes(key.pubkey).verify(value, message)
            elif key.sigtype == SIG_ED25519_COSIG:
                if cp is None:
                    raise NoteError("bad_checkpoint", "cosignature needs a checkpoint")
                timestamp = int.from_bytes(sig.payload[:8], "big")
                message = cosignature_message_ed25519(timestamp, cp)
                ed25519.Ed25519PublicKey.from_public_bytes(key.pubkey).verify(sig.payload[8:], message)
            else:
                if cp is None:
                    raise NoteError("bad_checkpoint", "cosignature needs a checkpoint")
                timestamp = int.from_bytes(sig.payload[:8], "big")
                message = cosignature_message_mldsa44(key.name, timestamp, cp)
                mldsa.MLDSA44PublicKey.from_public_bytes(key.pubkey).verify(sig.payload[8:], message)
        except (InvalidSignature, NoteError, ValueError) as exc:
            results.append(SigResult(sig.name, sig.key_id, "failed", key.sigtype, timestamp, str(exc) or "invalid signature"))
            continue
        results.append(SigResult(sig.name, sig.key_id, "verified", key.sigtype, timestamp))
    return results


def verify_signed_note(note: str, vkeys: list[str]) -> tuple[str, list[SigResult]]:
    """Generic signed-note verdict (PASS, FAIL or UNKNOWN) and per-signature results.

    PASS: at least one known key verified and no known key failed.
    FAIL: malformed note, a known key's signature failed, or no known key signed.
    UNKNOWN: no signature verified, and at least one known key uses an unsupported algorithm.
    """
    try:
        keys = [parse_vkey(item) for item in vkeys]
        parsed = parse_note(note)
        try:
            cp: Checkpoint | None = parse_checkpoint(parsed.text)
        except NoteError:
            cp = None
        results = verify_note_signatures(parsed, cp, keys)
    except NoteError:
        return "FAIL", []
    if any(r.status == "failed" for r in results):
        return "FAIL", results
    if any(r.status == "verified" for r in results):
        return "PASS", results
    if any(r.status == "unsupported" for r in results):
        return "UNKNOWN", results
    return "FAIL", results
