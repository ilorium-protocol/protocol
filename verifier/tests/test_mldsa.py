# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""ML-DSA-44: a second implementation agrees, and a missing capability gives UNKNOWN, never an error."""

import json
from pathlib import Path

import pytest

from ilorium_verifier import note
from ilorium_verifier.strata import verify_strata
from ilorium_verifier.trust import load_trust

VECTORS = Path(__file__).resolve().parents[2] / "vectors"


def _case(file, case_id):
    return next(c for c in json.loads((VECTORS / file).read_text(encoding="utf-8"))["cases"] if c["id"] == case_id)


def test_independent_implementation_agrees_with_openssl():
    """dilithium-py (pure Python, FIPS 204) and the OpenSSL-backed verifier accept each other's output."""
    ml = pytest.importorskip("dilithium_py.ml_dsa")
    from cryptography.hazmat.primitives.asymmetric import mldsa
    seed = bytes(range(32))
    pk, sk = ml.ML_DSA_44.key_derive(seed)
    key = mldsa.MLDSA44PrivateKey.from_seed_bytes(seed)
    assert key.public_key().public_bytes_raw() == pk
    for message in (b"", b"abc", bytes(range(256)) * 3):
        deterministic = ml.ML_DSA_44.sign(sk, message, deterministic=True)
        assert deterministic == ml.ML_DSA_44.sign(sk, message, deterministic=True)
        key.public_key().verify(deterministic, message)
        assert ml.ML_DSA_44.verify(pk, message, key.sign(message))


def test_published_ml_dsa_vector_verifies_here():
    case = _case("signed-note.json", "mldsa44-cosignature")
    verdict, results = note.verify_signed_note(case["input"]["note"], case["input"]["vkeys"])
    assert verdict == "PASS" if note.mldsa44_available() else verdict == "UNKNOWN"


def test_without_ml_dsa_the_verdict_is_unknown_not_an_error(monkeypatch):
    monkeypatch.setattr(note, "mldsa44_available", lambda: False)
    case = _case("signed-note.json", "mldsa44-cosignature")
    verdict, results = note.verify_signed_note(case["input"]["note"], case["input"]["vkeys"])
    assert verdict == "UNKNOWN"
    assert [r.status for r in results] == ["unsupported"]
    assert "not available" in results[0].detail


def test_without_ml_dsa_a_tampered_ml_dsa_signature_is_not_failed_either(monkeypatch):
    """Unable to check is not the same as invalid: the verifier says it does not know."""
    monkeypatch.setattr(note, "mldsa44_available", lambda: False)
    case = _case("signed-note.json", "mldsa44-cosignature-flipped")
    verdict, _ = note.verify_signed_note(case["input"]["note"], case["input"]["vkeys"])
    assert verdict == "UNKNOWN"


def test_strata_without_ml_dsa_reports_unknown_and_says_so(monkeypatch):
    case = _case("strata-checkpoints.json", "healthy")
    inp = case["input"]
    monkeypatch.setattr(note, "mldsa44_available", lambda: False)
    report = verify_strata(
        records=inp["records_jsonl"].encode(), checkpoints=inp["checkpoints_jsonl"].encode(),
        pulses=inp["pulses_jsonl"].encode(), trust=load_trust(inp["trust"]), now=inp.get("now"))
    assert report["verdict"] in ("UNKNOWN", "PASS")  # PASS only if quorum is met without the ML-DSA witness
    if report["verdict"] == "UNKNOWN":
        assert any(c["id"] == "checkpoint.witnesses" and c["verdict"] == "UNKNOWN" for c in report["checks"])
