# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Merkle tree hashes and proofs (RFC 6962 section 2.1; same construction as RFC 9162 with SHA-256)."""

from __future__ import annotations

import hashlib

EMPTY_ROOT = hashlib.sha256(b"").digest()


def leaf_hash(data: bytes) -> bytes:
    return hashlib.sha256(b"\x00" + data).digest()


def node_hash(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(b"\x01" + left + right).digest()


class IncrementalTree:
    """Append-only tree that can report the root at the current size in O(log n)."""

    def __init__(self) -> None:
        self._stack: list[tuple[bytes, int]] = []
        self.size = 0

    def append(self, leaf: bytes) -> None:
        """Append a leaf *hash* (already prefixed and hashed)."""
        node, width = leaf, 1
        while self._stack and self._stack[-1][1] == width:
            left, _ = self._stack.pop()
            node = node_hash(left, node)
            width *= 2
        self._stack.append((node, width))
        self.size += 1

    def root(self) -> bytes:
        if not self._stack:
            return EMPTY_ROOT
        node = self._stack[-1][0]
        for left, _ in reversed(self._stack[:-1]):
            node = node_hash(left, node)
        return node


def root_from_leaf_hashes(hashes: list[bytes]) -> bytes:
    tree = IncrementalTree()
    for item in hashes:
        tree.append(item)
    return tree.root()


def verify_inclusion(
    leaf: bytes, index: int, size: int, proof: list[bytes], root: bytes
) -> bool:
    """Verify an inclusion proof for a leaf hash (RFC 9162 section 2.1.3.2)."""
    if index < 0 or size <= 0 or index >= size:
        return False
    fn, sn = index, size - 1
    current = leaf
    for sibling in proof:
        if sn == 0:
            return False
        if fn & 1 or fn == sn:
            current = node_hash(sibling, current)
            if not fn & 1:
                while not fn & 1 and fn != 0:
                    fn >>= 1
                    sn >>= 1
        else:
            current = node_hash(current, sibling)
        fn >>= 1
        sn >>= 1
    return sn == 0 and current == root


def verify_consistency(
    first: int, second: int, first_root: bytes, second_root: bytes, proof: list[bytes]
) -> bool:
    """Verify that the tree of size ``first`` is a prefix of the tree of size ``second``
    (RFC 9162 section 2.1.4.2)."""
    if first < 0 or second < first:
        return False
    if first == 0:
        return not proof
    if first == second:
        return not proof and first_root == second_root
    if not proof:
        return False
    path = list(proof)
    if first & (first - 1) == 0:
        path.insert(0, first_root)
    fn, sn = first - 1, second - 1
    while fn & 1:
        fn >>= 1
        sn >>= 1
    fr = sr = path[0]
    for step in path[1:]:
        if sn == 0:
            return False
        if fn & 1 or fn == sn:
            fr = node_hash(step, fr)
            sr = node_hash(step, sr)
            while not fn & 1 and fn != 0:
                fn >>= 1
                sn >>= 1
        else:
            sr = node_hash(sr, step)
        fn >>= 1
        sn >>= 1
    return sn == 0 and fr == first_root and sr == second_root
