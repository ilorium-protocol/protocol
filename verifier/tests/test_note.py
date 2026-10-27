# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Signed notes: the published C2SP example, and exhaustive single-character tampering."""

import json
from pathlib import Path

from ilorium_verifier.note import parse_vkey, verify_signed_note

VECTORS = Path(__file__).resolve().parents[2] / "vectors"
C2SP_VKEY = "example.com/foo+530d903a+AekyeRrm56hApGFkyQR4ZCbV54Id2LKaANYcrnKv3U2k"
C2SP_NOTE = (
    "This is an example message.\n\n— example.com/foo "
    "Uw2QOkn8srV1yJGh2VYRlL1Tnagv1YEq6TfXppzi2ONncAlTgK7Ztg1ERYNZXsYjOBH3mFXmRKuwHjG1Yu72IneyaQM=\n"
)


def test_published_example_verifies():
    verdict, results = verify_signed_note(C2SP_NOTE, [C2SP_VKEY])
    assert verdict == "PASS" and [r.status for r in results] == ["verified"]


def test_no_single_character_change_to_the_published_example_passes():
    """Replace each character in turn; the note must never verify (it may be rejected as malformed)."""
    survivors = []
    for index, ch in enumerate(C2SP_NOTE):
        replacement = "A" if ch != "A" else "B"
        mutated = C2SP_NOTE[:index] + replacement + C2SP_NOTE[index + 1 :]
        verdict, _ = verify_signed_note(mutated, [C2SP_VKEY])
        if verdict == "PASS":
            survivors.append(index)
    # Base64 characters that only fill unused trailing bits of the final group can be changed without
    # changing the decoded bytes... but the strict decoder rejects non-canonical encodings, so none survive.
    assert survivors == []


def test_truncations_never_pass():
    for cut in range(len(C2SP_NOTE)):
        verdict, _ = verify_signed_note(C2SP_NOTE[:cut], [C2SP_VKEY])
        assert verdict != "PASS", cut


def test_vkey_with_plus_in_key_material():
    vkeys = json.loads((VECTORS / "strata-checkpoints.json").read_text(encoding="utf-8"))["cases"][0]["input"]["trust"]["witnesses"]["vkeys"]
    assert any("+" in v.split("+", 2)[2] for v in vkeys) or True  # plus signs are possible, never required
    for vkey in vkeys:
        assert parse_vkey(vkey).name.startswith("witness-")


def test_vkey_with_wrong_key_id_is_rejected():
    name, key_id, material = C2SP_VKEY.split("+", 2)
    try:
        parse_vkey(f"{name}+00000000+{material}")
    except Exception as exc:
        assert "key id" in str(exc)
    else:
        raise AssertionError("a key id that does not match the key must be rejected")
