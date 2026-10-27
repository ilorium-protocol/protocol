# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""The verifier's canonicalizer against the independent ``rfc8785`` package."""

import random

import pytest
import rfc8785

from ilorium_verifier.canon import MAX_SAFE_INT, CanonError, canonicalize, parse_strict

ALPHABET = (
    [chr(c) for c in range(0x20, 0x7F)]
    + ["\x00", "\x08", "\x09", "\x0a", "\x0c", "\x0d", "\x1f", "\x7f", "é", "日", " ", "", "\U0001F600", "\U00010000"]
)


def _text(rng: random.Random) -> str:
    return "".join(rng.choice(ALPHABET) for _ in range(rng.randint(0, 8)))


def _value(rng: random.Random, depth: int = 0):
    kind = rng.randint(0, 6 if depth < 4 else 4)
    if kind == 0:
        return None
    if kind == 1:
        return rng.choice([True, False])
    if kind == 2:
        return rng.choice([0, 1, -1, 42, MAX_SAFE_INT, -MAX_SAFE_INT, rng.randint(-10**9, 10**9)])
    if kind in (3, 4):
        return _text(rng)
    if kind == 5:
        return [_value(rng, depth + 1) for _ in range(rng.randint(0, 4))]
    return {_text(rng): _value(rng, depth + 1) for _ in range(rng.randint(0, 4))}


def test_matches_rfc8785_on_random_documents():
    rng = random.Random(8785)
    for _ in range(2000):
        document = {_text(rng): _value(rng) for _ in range(rng.randint(0, 5))}
        assert canonicalize(document) == rfc8785.dumps(document)


def test_parse_then_canonicalize_is_idempotent():
    rng = random.Random(1)
    for _ in range(500):
        document = {_text(rng): _value(rng) for _ in range(rng.randint(1, 4))}
        once = canonicalize(document)
        assert canonicalize(parse_strict(once)) == once


@pytest.mark.parametrize(
    "text,code",
    [
        ('{"a":1.0}', "float_not_allowed"),
        ('{"a":1E5}', "float_not_allowed"),
        ('{"a":-0}', "negative_zero"),
        ('{"a":1,"a":1}', "duplicate_key"),
        ('{"a":[{"b":1,"b":2}]}', "duplicate_key"),
        ('{"a":"\\udfff"}', "lone_surrogate"),
        ("[]", "not_object"),
        ("{", "invalid_json"),
        ('{"a":1}\n{"a":2}', "invalid_json"),
    ],
)
def test_rejections(text, code):
    with pytest.raises(CanonError) as info:
        parse_strict(text)
    assert info.value.code == code


def test_programmatic_floats_and_big_ints_rejected():
    with pytest.raises(CanonError):
        canonicalize({"a": 1.5})
    with pytest.raises(CanonError):
        canonicalize({"a": MAX_SAFE_INT + 1})
    with pytest.raises(CanonError):
        canonicalize({1: "non-string key"})
