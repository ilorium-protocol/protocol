# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Strict parsing and canonical serialization of Ilorium JSON.

Evidence Format 1.0, section 4: RFC 8785 (JCS) restricted to a profile in
which numbers are integers in the I-JSON safe range, objects have no
duplicate member names and strings are well-formed Unicode.
"""

from __future__ import annotations

import json
from typing import Any

MAX_SAFE_INT = 2**53 - 1
MAX_DEPTH = 64


class CanonError(ValueError):
    """A violation of the canonical JSON profile, with a stable error code."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise CanonError("duplicate_key", key)
        obj[key] = value
    return obj


def _parse_int(text: str) -> int:
    if text == "-0":
        raise CanonError("negative_zero")
    value = int(text)
    if abs(value) > MAX_SAFE_INT:
        raise CanonError("integer_out_of_range", text)
    return value


def _parse_float(text: str) -> Any:
    raise CanonError("float_not_allowed", text)


def _parse_constant(text: str) -> Any:
    raise CanonError("invalid_json", text)


def parse_strict(data: bytes | str, *, require_object: bool = True) -> Any:
    """Parse JSON text under the Ilorium profile; raise CanonError on any violation."""
    if isinstance(data, bytes):
        if data.startswith(b"\xef\xbb\xbf"):
            raise CanonError("invalid_json", "byte order mark")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise CanonError("invalid_utf8", str(exc)) from exc
    else:
        text = data
        if text.startswith("﻿"):
            raise CanonError("invalid_json", "byte order mark")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_object_pairs,
            parse_int=_parse_int,
            parse_float=_parse_float,
            parse_constant=_parse_constant,
        )
    except CanonError:
        raise
    except RecursionError as exc:
        raise CanonError("too_deep") from exc
    except json.JSONDecodeError as exc:
        raise CanonError("invalid_json", str(exc)) from exc
    if require_object and not isinstance(value, dict):
        raise CanonError("not_object")
    # Serializing validates strings (lone surrogates) and nesting depth.
    canonicalize(value)
    return value


_ESCAPES = {
    0x22: '\\"',
    0x5C: "\\\\",
    0x08: "\\b",
    0x09: "\\t",
    0x0A: "\\n",
    0x0C: "\\f",
    0x0D: "\\r",
}


def _quote(text: str) -> str:
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise CanonError("lone_surrogate") from exc
    out = ['"']
    for ch in text:
        code = ord(ch)
        if code in _ESCAPES:
            out.append(_ESCAPES[code])
        elif code < 0x20:
            out.append(f"\\u{code:04x}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _serialize(value: Any, depth: int, out: list[str]) -> None:
    if depth > MAX_DEPTH:
        raise CanonError("too_deep")
    if value is None:
        out.append("null")
    elif value is True:
        out.append("true")
    elif value is False:
        out.append("false")
    elif isinstance(value, int):
        if abs(value) > MAX_SAFE_INT:
            raise CanonError("integer_out_of_range", str(value))
        out.append(str(value))
    elif isinstance(value, str):
        out.append(_quote(value))
    elif isinstance(value, (list, tuple)):
        out.append("[")
        for index, item in enumerate(value):
            if index:
                out.append(",")
            _serialize(item, depth + 1, out)
        out.append("]")
    elif isinstance(value, dict):
        out.append("{")
        # RFC 8785 section 3.2.3: sort by UTF-16 code units.
        for key in value:
            if not isinstance(key, str):
                raise CanonError("unsupported_type", type(key).__name__)
        for index, key in enumerate(sorted(value, key=_utf16_key)):
            if index:
                out.append(",")
            out.append(_quote(key))
            out.append(":")
            _serialize(value[key], depth + 1, out)
        out.append("}")
    elif isinstance(value, float):
        raise CanonError("float_not_allowed", repr(value))
    else:
        raise CanonError("unsupported_type", type(value).__name__)


def _utf16_key(key: str) -> bytes:
    try:
        return key.encode("utf-16-be")
    except UnicodeEncodeError as exc:
        raise CanonError("lone_surrogate") from exc


def canonicalize(value: Any) -> bytes:
    """Return the canonical UTF-8 bytes of a value (RFC 8785 under the Ilorium profile)."""
    out: list[str] = []
    _serialize(value, 0, out)
    return "".join(out).encode("utf-8")
