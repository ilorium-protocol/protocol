# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""The verifier's tree and proofs against a naive recursive RFC 6962 implementation written here."""

import hashlib

from ilorium_verifier.merkle import (
    EMPTY_ROOT, IncrementalTree, leaf_hash, node_hash, root_from_leaf_hashes,
    verify_consistency, verify_inclusion,
)


def split(n):
    return 1 << ((n - 1).bit_length() - 1)


def mth(leaves):
    if not leaves:
        return hashlib.sha256(b"").digest()
    if len(leaves) == 1:
        return leaves[0]
    k = split(len(leaves))
    return node_hash(mth(leaves[:k]), mth(leaves[k:]))


def path(m, leaves):
    if len(leaves) == 1:
        return []
    k = split(len(leaves))
    if m < k:
        return path(m, leaves[:k]) + [mth(leaves[k:])]
    return path(m - k, leaves[k:]) + [mth(leaves[:k])]


def subproof(m, leaves, b):
    n = len(leaves)
    if m == n:
        return [] if b else [mth(leaves)]
    k = split(n)
    if m <= k:
        return subproof(m, leaves[:k], b) + [mth(leaves[k:])]
    return subproof(m - k, leaves[k:], False) + [mth(leaves[:k])]


HASHES = [leaf_hash(bytes([i % 251]) * (1 + i % 5)) for i in range(70)]


def test_empty_root_is_sha256_of_nothing():
    assert EMPTY_ROOT == hashlib.sha256(b"").digest()
    assert root_from_leaf_hashes([]) == EMPTY_ROOT


def test_known_leaf_hash():
    # SHA-256(0x00): the leaf hash of the empty entry in the Certificate Transparency reference tests
    assert leaf_hash(b"").hex() == "6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d"


def test_incremental_root_matches_naive_for_every_prefix():
    tree = IncrementalTree()
    assert tree.root() == mth([])
    for n, item in enumerate(HASHES, start=1):
        tree.append(item)
        assert tree.root() == mth(HASHES[:n]), n


def test_every_inclusion_proof_verifies_and_no_neighbor_does():
    for n in range(1, 41):
        leaves, root = HASHES[:n], mth(HASHES[:n])
        for i in range(n):
            proof = path(i, leaves)
            assert verify_inclusion(leaves[i], i, n, proof, root), (i, n)
            if n > 1:
                other = (i + 1) % n
                assert not verify_inclusion(leaves[i], other, n, proof, root) or other == i


def test_every_consistency_proof_verifies():
    for n in range(1, 41):
        for m in range(1, n + 1):
            proof = subproof(m, HASHES[:n], True)
            assert verify_consistency(m, n, mth(HASHES[:m]), mth(HASHES[:n]), proof), (m, n)


def test_any_flipped_proof_bit_is_rejected():
    n, m = 23, 9
    proof = subproof(m, HASHES[:n], True)
    for index in range(len(proof)):
        for bit in (0, 100, 255):
            broken = list(proof)
            value = bytearray(broken[index])
            value[bit // 8] ^= 1 << (bit % 8)
            broken[index] = bytes(value)
            assert not verify_consistency(m, n, mth(HASHES[:m]), mth(HASHES[:n]), broken)
    ipath = path(11, HASHES[:n])
    for index in range(len(ipath)):
        broken = list(ipath)
        broken[index] = bytes([broken[index][0] ^ 1]) + broken[index][1:]
        assert not verify_inclusion(HASHES[11], 11, n, broken, mth(HASHES[:n]))


def test_consistency_rejects_a_different_history():
    """A tree that rewrote one early leaf is not an extension of the original."""
    n, m = 20, 10
    forked = list(HASHES[:n])
    forked[3] = leaf_hash(b"rewritten")
    proof = subproof(m, forked, True)
    assert not verify_consistency(m, n, mth(HASHES[:m]), mth(forked), proof)
