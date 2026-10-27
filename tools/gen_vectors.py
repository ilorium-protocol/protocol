#!/usr/bin/env python3
# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Generate the Ilorium conformity vectors (Evidence Format 1.0, section 15).

Independence rule: this script imports NOTHING from ``ilorium_verifier``. It builds
evidence with the ``rfc8785`` package, ``hashlib``, ``cryptography`` and its own
naive recursive RFC 6962 tree, and (for ML-DSA-44) the pure-Python ``dilithium-py``, a FIPS 204
implementation that shares nothing with the OpenSSL-backed verifier. The expected result of every case is written by
hand from the specification, never produced by running a verifier.

All keys are derived from public seeds. They are TEST KEYS: never use them.
ML-DSA-44 signatures are made in the deterministic mode of FIPS 204 (rnd = 0^32), so regenerating
reproduces every file byte for byte; tests/test_reproducible.py checks it.

Usage: python tools/gen_vectors.py [output-dir]
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import rfc8785
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519
from dilithium_py.ml_dsa import ML_DSA_44

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "vectors"
SPEC = "Evidence Format 1.0"


# ---------------------------------------------------------------- primitives
def canon(obj) -> bytes:
    return rfc8785.dumps(obj)


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def sha(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def seed(name: str) -> bytes:
    return sha(b"ilorium-test-vector-key/" + name.encode())


class Ed:
    def __init__(self, name: str):
        self.sk = ed25519.Ed25519PrivateKey.from_private_bytes(seed(name))
        self.pk = self.sk.public_key().public_bytes_raw()


def key_id(name: str, typ: int, pub: bytes) -> bytes:
    return sha(name.encode() + b"\n" + bytes([typ]) + pub)[:4]


def vkey(name: str, typ: int, pub: bytes, kid: bytes | None = None) -> str:
    kid = kid or key_id(name, typ, pub)
    return f"{name}+{kid.hex()}+{b64(bytes([typ]) + pub)}"


def tamper(text: str, old: str, new: str, count: int = 1) -> str:
    """str.replace that refuses to be a silent no-op (a tampered vector must differ from the original)."""
    assert old in text, f"tamper target not found: {old[:40]!r}"
    return text.replace(old, new, count)


# ---------------------------------------------------------------- merkle (naive, RFC 6962)
def lh(data: bytes) -> bytes:
    return sha(b"\x00" + data)


def nh(left: bytes, right: bytes) -> bytes:
    return sha(b"\x01" + left + right)


def split(n: int) -> int:
    return 1 << ((n - 1).bit_length() - 1)  # largest power of two strictly less than n


def mth(leaves: list[bytes]) -> bytes:
    n = len(leaves)
    if n == 0:
        return sha(b"")
    if n == 1:
        return leaves[0]
    k = split(n)
    return nh(mth(leaves[:k]), mth(leaves[k:]))


def inclusion_path(m: int, leaves: list[bytes]) -> list[bytes]:
    n = len(leaves)
    if n == 1:
        return []
    k = split(n)
    if m < k:
        return inclusion_path(m, leaves[:k]) + [mth(leaves[k:])]
    return inclusion_path(m - k, leaves[k:]) + [mth(leaves[:k])]


def consistency_proof(m: int, leaves: list[bytes]) -> list[bytes]:
    def sub(m: int, d: list[bytes], b: bool) -> list[bytes]:
        n = len(d)
        if m == n:
            return [] if b else [mth(d)]
        k = split(n)
        if m <= k:
            return sub(m, d[:k], b) + [mth(d[k:])]
        return sub(m - k, d[k:], False) + [mth(d[:k])]

    return sub(m, leaves, True)


# ---------------------------------------------------------------- time
T0 = datetime(2026, 11, 3, 14, 0, 0, tzinfo=timezone.utc)


def tiso(offset: int) -> str:
    return (T0 + timedelta(seconds=offset)).strftime("%Y-%m-%dT%H:%M:%SZ")


def tepoch(offset: int) -> int:
    return int((T0 + timedelta(seconds=offset)).timestamp())


# ---------------------------------------------------------------- identities
ORG = "organism-test"
ORIGIN = "ilorium.example/strata/organism-test"
LOG, WA, OTHER, PULSE_KEY = Ed("log"), Ed("witness-a"), Ed("other"), Ed("pulse")
WD = Ed("witness-d")  # a witness nobody configured
WB_PUB, WB = ML_DSA_44.key_derive(seed("witness-b"))  # (public key, secret key), from a 32-byte seed
_ck = ec.derive_private_key(int.from_bytes(seed("witness-c"), "big"), ec.SECP256R1())
WC_SPKI = _ck.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
NAME_A, NAME_B, NAME_C, NAME_D = (f"witness-{x}.example/w" for x in "abcd")

VK_LOG = vkey(ORIGIN, 0x01, LOG.pk)
VK_A = vkey(NAME_A, 0x04, WA.pk)
VK_B = vkey(NAME_B, 0x06, WB_PUB)
VK_C = vkey(NAME_C, 0x02, WC_SPKI, kid=sha(WC_SPKI)[:4])


def make_trust(*, quorum=2, witnesses=None, freshness=(900, 120), pulse=True, log_vkeys=None) -> dict:
    t = {
        "trust": "1.0",
        "organism": ORG,
        "log": {"origin": ORIGIN, "vkeys": log_vkeys or [VK_LOG]},
        "witnesses": {"quorum": quorum, "vkeys": witnesses if witnesses is not None else [VK_A, VK_B]},
    }
    if pulse:
        t["pulse_key"] = "ed25519:" + b64(PULSE_KEY.pk)
    if freshness:
        t["freshness"] = {"max_interval_s": freshness[0], "grace_s": freshness[1]}
    return t


# ---------------------------------------------------------------- notes
def sig_line(name: str, blob: bytes) -> str:
    return f"— {name} {b64(blob)}\n"


def log_sig(text: str, key: Ed = LOG, kid_key: Ed | None = None, flip: bool = False) -> str:
    sig = bytearray(key.sk.sign(text.encode()))
    if flip:
        sig[0] ^= 1
    kid = key_id(ORIGIN, 0x01, (kid_key or key).pk)
    return sig_line(ORIGIN, kid + bytes(sig))


def cosig_ed(name: str, key: Ed, origin: str, size: int, root: bytes, ts: int, ext=(), flip=False) -> str:
    msg = f"cosignature/v1\ntime {ts}\n{origin}\n{size}\n{b64(root)}\n" + "".join(f"{e}\n" for e in ext)
    sig = bytearray(key.sk.sign(msg.encode()))
    if flip:
        sig[0] ^= 1
    return sig_line(name, key_id(name, 0x04, key.pk) + ts.to_bytes(8, "big") + bytes(sig))


def cosig_ml(name: str, key, pub: bytes, origin: str, size: int, root: bytes, ts: int, flip=False) -> str:
    nb, ob = name.encode(), origin.encode()
    msg = (b"subtree/v1\n\x00" + bytes([len(nb)]) + nb + ts.to_bytes(8, "big")
           + bytes([len(ob)]) + ob + (0).to_bytes(8, "big") + size.to_bytes(8, "big") + root)
    sig = bytearray(ML_DSA_44.sign(key, msg, deterministic=True))
    if flip:
        sig[5] ^= 1
    return sig_line(name, key_id(name, 0x06, pub) + ts.to_bytes(8, "big") + bytes(sig))


def cosig_ecdsa_placeholder(name: str, ts: int) -> str:
    """A cosignature on an algorithm the verifier does not support; its bytes are never verified."""
    fake = (sha(b"placeholder" + name.encode()) * 3)[:64]
    return sig_line(name, sha(WC_SPKI)[:4] + ts.to_bytes(8, "big") + fake)


# ---------------------------------------------------------------- records
BASE_MS = tepoch(0) * 1000
CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def ulid(i: int) -> str:
    n = ((BASE_MS + i * 20000) << 80) | int.from_bytes(sha(b"ulid%d" % i)[:10], "big")
    out = []
    for _ in range(26):
        out.append(CROCKFORD[n & 31])
        n >>= 5
    return "".join(reversed(out))


def envelope(i: int, rtype: str, t: int, **extra) -> dict:
    rec = {
        "id": ulid(i), "type": rtype,
        "occurred_at": tiso(t - 2), "received_at": tiso(t - 1), "recorded_at": tiso(t),
        "protocol_release": "1.0", "probe_version": "0.1.0", "rules_version": "r1",
        "policy_version": "p1", "spore_version": "s1",
    }
    rec.update(extra)
    return rec


def obs(i: int, t: int, beat: int | None, *, source="github", kind="event", actor=("oz-architect[bot]", "agent"),
        action="push", obj="repo/main") -> dict:
    rec = envelope(
        i, "observation", t, source=source, source_event_id=f"evt-{i}", kind=kind,
        actor={"id": actor[0], "kind": actor[1]}, action=action, object=obj,
        fields={"ref": "refs/heads/main", "files": 3}, content_hash="sha256:" + sha(b"content%d" % i).hex(),
    )
    if beat is not None:
        rec["beat"] = beat
    return rec


def claim(i: int, t: int, about: str, cause="directive", ref="D-1") -> dict:
    return envelope(i, "claim", t, claimant={"id": "oz-architect", "kind": "agent"}, about=about,
                    cause={"type": cause, "ref": ref}, context={"duration_s": 60, "nature": "routine"})


def evaluation(i: int, t: int, inputs: list[str], **kw) -> dict:
    rec = envelope(i, "evaluation", t, evaluator={"name": "correlator", "version": "0.1.0"}, inputs=inputs,
                   function="operation", attribution="linked", crossing="directive", weight="low")
    rec.update(kw)
    return rec


def base_records(n: int = 12) -> list[dict]:
    recs: list[dict] = []
    beat = 0
    for i in range(n):
        t = i * 20
        phase = i % 4
        if phase in (0, 1):
            beat += 1
            recs.append(obs(i, t, beat, source="telegram" if phase == 1 else "github",
                            actor=("founder", "human") if phase == 1 else ("oz-architect[bot]", "agent"),
                            kind="outcome" if i == 5 else "event"))
        elif phase == 2:
            recs.append(claim(i, t, recs[i - 1]["id"]))
        else:
            recs.append(evaluation(i, t, [recs[i - 2]["id"], recs[i - 1]["id"]]))
    return recs


def gap_record(i: int, t: int) -> dict:
    return envelope(
        i, "observation", t, source="github", source_event_id=f"gap-{i}", kind="gap",
        actor={"id": "probe", "kind": "instrument"}, action="capture_gap", object="github",
        fields={"from": tiso(t - 60), "to": tiso(t - 5), "reason": "collector_down", "lost": 3},
    )


def jsonl(objs: list[dict]) -> str:
    return "".join(canon(o).decode() + "\n" for o in objs)


def leaf_hashes(recs: list[dict]) -> list[bytes]:
    return [lh(canon(r)) for r in recs]


def beat_at(recs: list[dict], size: int) -> int:
    return max([r.get("beat", 0) for r in recs[:size]] + [0])


# ---------------------------------------------------------------- checkpoints and pulses
PLAN_CPS = [(4, 100, "beats"), (8, 300, "beats"), (8, 1200, "interval"), (12, 1500, "beats")]
PLAN_PULSES = [(1, 110, "beats", 0), (2, 310, "beats", 1), (3, 1210, "interval", 2), (4, 1510, "beats", 3)]
NOW = tiso(1560)


def checkpoint_entry(size: int, root: bytes, t: int, beat: int, trigger: str, *, witnesses=("A", "B"),
                     origin: str = ORIGIN, ext=(), log_flip=False, log_kid_key=None, log_key=LOG,
                     skip_log=False, witness_ts_shift=0, flips=(), meta_key=LOG, meta_mut=None, extra_sigs="") -> dict:
    text = f"{origin}\n{size}\n{b64(root)}\n" + "".join(f"{e}\n" for e in ext)
    ts = tepoch(t) + 5 + witness_ts_shift
    sigs = "" if skip_log else log_sig(text, key=log_key, kid_key=log_kid_key, flip=log_flip)
    if "A" in witnesses:
        sigs += cosig_ed(NAME_A, WA, origin, size, root, ts, ext, flip="A" in flips)
    if "B" in witnesses:
        sigs += cosig_ml(NAME_B, WB, WB_PUB, origin, size, root, ts, flip="B" in flips)
    if "C" in witnesses:
        sigs += cosig_ecdsa_placeholder(NAME_C, ts)
    if "D" in witnesses:
        sigs += cosig_ed(NAME_D, WD, origin, size, root, ts, ext)
    sigs += extra_sigs
    note = text + "\n" + sigs
    meta = {"checkpoint_meta": "1.0", "origin": origin, "tree_size": size, "root": "sha256:" + root.hex(),
            "beat": beat, "translation_time": tiso(t), "trigger": trigger}
    if meta_mut:
        meta_mut(meta)
    meta["signature"] = b64(meta_key.sk.sign(b"ilorium.checkpoint-meta.v1\n" + canon(meta)))
    return {"note": note, "meta": meta}


def pulse_obj(seq: int, t: int, trigger: str, prev: str | None, beat: int, size: int, root: bytes, *,
              key: Ed = PULSE_KEY, mut=None, sign=True) -> dict:
    body = {
        "pulse": "1.0", "organism": ORG, "domain": "ilorium.example", "seq": seq, "beat": beat,
        "trigger": trigger, "prev_pulse": prev,
        "seen": [{"organism": "forge-north", "seq": 1290, "beat": 88102}],
        "checkpoint": {"tree_size": size, "root": "sha256:" + root.hex(), "witness_cosigned": True, "age_s": 30},
        "capture": {"github": "ok", "server": "ok"}, "state": "active", "recovery": "unknown",
        "challenge": None, "translation_time": tiso(t),
    }
    if trigger == "challenge":
        body["challenge"] = {"value": b64(sha(b"challenge")[:16]), "issued_at": tiso(t - 30), "deadline_s": 600}
    if mut:
        mut(body)
    if sign:
        body["signature"] = b64(key.sk.sign(b"ilorium.pulse.v1\n" + canon(body)))
    return body


def digest(obj: dict) -> str:
    return "sha256:" + sha(canon(obj)).hex()


def build(recs: list[dict] | None = None, *, file_recs: list[dict] | str | None = None, cps=PLAN_CPS,
          pulses_plan=PLAN_PULSES, with_cps=True, with_pulses=True, trust: dict | None = None, now: str | None = NOW,
          cp_kw=None, cp_hook=None, pulse_hook=None, pulse_kw=None, cp_raw=None, pulse_raw=None) -> dict:
    recs = recs if recs is not None else base_records()
    leaves = leaf_hashes(recs)
    inp: dict = {"trust": trust or make_trust()}
    if now:
        inp["now"] = now
    shown = recs if file_recs is None else file_recs
    inp["records_jsonl"] = shown if isinstance(shown, str) else jsonl(shown)
    entries = []
    if with_cps:
        for idx, (size, t, trig) in enumerate(cps):
            kw = (cp_kw or {}).get(idx, {})
            root = kw.pop("root", None) or mth(leaves[:size])
            entries.append(checkpoint_entry(size, root, t, beat_at(recs, size), trig, **kw))
        if cp_hook:
            cp_hook(entries)
        inp["checkpoints_jsonl"] = cp_raw if cp_raw is not None else jsonl(entries)
    if with_pulses:
        plist, prev = [], None
        for idx, (seq, t, trig, cpi) in enumerate(pulses_plan):
            size = cps[cpi][0]
            kw = (pulse_kw or {}).get(idx, {})
            p = pulse_obj(seq, t, trig, prev, beat_at(recs, size), size, mth(leaves[:size]), **kw)
            plist.append(p)
            prev = digest(p)
        if pulse_hook:
            pulse_hook(plist)
        inp["pulses_jsonl"] = pulse_raw if pulse_raw is not None else jsonl(plist)
    return inp


ALL_CHECKS = [
    "records.parse", "records.canonical", "records.schema", "records.ids", "records.refs", "records.order",
    "checkpoints.parse", "checkpoint.note", "checkpoint.log_signature", "checkpoint.witnesses", "checkpoint.meta",
    "checkpoint.monotonic", "checkpoint.interval", "checkpoint.witness_time", "log.root", "log.coverage",
    "pulses.parse", "pulse.schema", "pulse.signature", "pulse.chain", "pulse.order", "pulse.interval",
    "pulse.checkpoint_ref",
]


def exp(verdict: str, gaps=None, **checks) -> dict:
    out = {"verdict": verdict, "checks": {k.replace("__", "."): v for k, v in checks.items()}}
    if gaps is not None:
        out["gap_kinds"] = sorted(gaps)
    return out


def case(cid: str, description: str, inp: dict, expect: dict) -> dict:
    return {"id": cid, "description": description, "input": inp, "expect": expect}


def write(name: str, operation: str, spec: str, description: str, cases: list[dict]) -> None:
    doc = {"vector": "1.0", "operation": operation, "spec": f"{SPEC} {spec}", "description": description, "cases": cases}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    print(f"{name}: {len(cases)} cases")


# ================================================================= canonicalize
def vectors_canonical() -> None:
    cases = []

    def ok(cid, text, canonical, desc=""):
        # cross-check the hand-written expectation against the independent rfc8785 package
        assert rfc8785.dumps(json.loads(text)).decode() == canonical, cid
        cases.append(case(cid, desc, {"json": text}, {"verdict": "PASS", "canonical": canonical}))

    def bad(cid, text, code, desc="", hex_input=None):
        inp = {"json_hex": hex_input} if hex_input else {"json": text}
        cases.append(case(cid, desc, inp, {"verdict": "FAIL", "error": code}))

    ok("key-order", '{"b":1,"a":2}', '{"a":2,"b":1}', "members sorted by name")
    ok("whitespace-nesting", '{ "z" : [ 3 , 2 , 1 ] , "y" : { "b" : null , "a" : true } }',
       '{"y":{"a":true,"b":null},"z":[3,2,1]}', "whitespace removed, arrays keep order")
    ok("escapes", '{"s":"\\u0008\\u0009\\u000a\\u000c\\u000d\\"\\\\\\u001f\\u007f\\/"}',
       '{"s":"\\b\\t\\n\\f\\r\\"\\\\\\u001f\x7f/"}', "short escapes, lowercase \\u00xx for other controls, DEL and solidus literal")
    ok("utf16-key-order", '{"\\ue000":1,"\\ud83d\\ude00":2}', '{"\U0001F600":2,"":1}',
       "keys sort by UTF-16 code units: U+1F600 (D83D) before U+E000")
    ok("non-ascii-literal", '{"\\u00e9":"\\u65e5\\u672c"}', '{"é":"日本"}', "non-ASCII stays as UTF-8")
    ok("line-separator-literal", '{"a":"\\u2028"}', '{"a":" "}', "U+2028 is not escaped")
    ok("integers", '{"a":0,"b":-1,"c":9007199254740991,"d":-9007199254740991}',
       '{"a":0,"b":-1,"c":9007199254740991,"d":-9007199254740991}', "integers up to 2^53-1")
    ok("empty-containers", '{"a":{},"b":[]}', '{"a":{},"b":[]}')
    ok("sorted-by-unicode-not-locale", '{"b":1,"B":2,"a":3,"A":4}', '{"A":4,"B":2,"a":3,"b":1}')
    bad("float", '{"a":1.0}', "float_not_allowed", "no fractional numbers, even when integral")
    bad("float-fraction", '{"a":0.5}', "float_not_allowed")
    bad("float-exponent", '{"a":1e2}', "float_not_allowed")
    bad("negative-zero", '{"a":-0}', "negative_zero")
    bad("integer-too-large", '{"a":9007199254740992}', "integer_out_of_range")
    bad("integer-too-small", '{"a":-9007199254740992}', "integer_out_of_range")
    bad("duplicate-key", '{"a":1,"a":2}', "duplicate_key")
    bad("duplicate-key-escaped", '{"a":1,"\\u0061":2}', "duplicate_key", "same name after unescaping")
    bad("lone-surrogate-value", '{"a":"\\ud800"}', "lone_surrogate")
    bad("lone-surrogate-key", '{"\\udc00":1}', "lone_surrogate")
    bad("not-object-array", "[1]", "not_object")
    bad("not-object-string", '"x"', "not_object")
    bad("not-object-null", "null", "not_object")
    bad("syntax-missing-value", '{"a":}', "invalid_json")
    bad("trailing-data", '{"a":1} x', "invalid_json")
    bad("empty-input", "", "invalid_json")
    bad("single-quotes", "{'a':1}", "invalid_json")
    bad("nan", '{"a":NaN}', "invalid_json")
    bad("infinity", '{"a":Infinity}', "invalid_json")
    bad("leading-zero", '{"a":01}', "invalid_json")
    bad("byte-order-mark", "", "invalid_json", "UTF-8 byte order mark is rejected", hex_input="efbbbf7b7d")
    bad("invalid-utf8", "", "invalid_utf8", "0xff is not valid UTF-8", hex_input="7b2261223a22ff227d")
    bad("too-deep", '{"a":' + "[" * 70 + "]" * 70 + "}", "too_deep", "nesting deeper than 64")
    write("canonicalize.json", "canonicalize", "section 4",
          "Strict parsing and canonical serialization (RFC 8785 profile).", cases)


# ================================================================= merkle
CT_LEAVES = ["", "00", "10", "2021", "3031", "40414243", "5051525354555657", "606162636465666768696a6b6c6d6e6f"]
LEAVES = CT_LEAVES + [sha(b"leaf%d" % i)[: 1 + i % 7].hex() for i in range(8, 40)]


def vectors_merkle() -> None:
    raw = [bytes.fromhex(x) for x in LEAVES]
    hashes = [lh(x) for x in raw]
    cases = []
    for n in range(0, 18):
        cases.append(case(f"root-size-{n}", "RFC 6962 tree hash of the first n leaves",
                          {"leaves": LEAVES[:n]}, {"root": mth(hashes[:n]).hex()}))
    write("merkle-root.json", "merkle_root", "section 7",
          "Tree root over leaf data (leaf hash = SHA-256(0x00 || data)). The first eight leaves are the "
          "ones used in the Certificate Transparency reference tests.", cases)

    def inc(i, n, **over):
        leaf_hex = LEAVES[i]
        proof = [p.hex() for p in inclusion_path(i, hashes[:n])]
        d = {"leaf": leaf_hex, "index": i, "size": n, "proof": proof, "root": mth(hashes[:n]).hex()}
        d.update(over)
        return d

    cases = []
    for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 16, 17, 33):
        for i in sorted({0, n // 2, n - 1}):
            cases.append(case(f"valid-{i}-of-{n}", "", inc(i, n), {"verdict": "PASS"}))
    d = inc(3, 8)
    cases += [
        case("wrong-root", "", inc(3, 8, root=mth(hashes[:7]).hex()), {"verdict": "FAIL"}),
        case("wrong-index", "", inc(3, 8, index=4), {"verdict": "FAIL"}),
        case("wrong-leaf", "", inc(3, 8, leaf="ff"), {"verdict": "FAIL"}),
        case("proof-truncated", "", inc(3, 8, proof=d["proof"][:-1]), {"verdict": "FAIL"}),
        case("proof-extended", "", inc(3, 8, proof=d["proof"] + [sha(b"x").hex()]), {"verdict": "FAIL"}),
        case("proof-hash-flipped", "", inc(3, 8, proof=[d["proof"][0][:-1] + ("0" if d["proof"][0][-1] != "0" else "1")] + d["proof"][1:]), {"verdict": "FAIL"}),
        case("index-out-of-range", "", inc(3, 8, index=8), {"verdict": "FAIL"}),
        case("index-negative", "", inc(3, 8, index=-1), {"verdict": "FAIL"}),
        case("size-zero", "", inc(0, 1, size=0), {"verdict": "FAIL"}),
        case("single-leaf-nonempty-proof", "", inc(0, 1, proof=[sha(b"x").hex()]), {"verdict": "FAIL"}),
    ]
    write("merkle-inclusion.json", "verify_inclusion", "section 7", "Inclusion proofs (RFC 9162 section 2.1.3.2).", cases)

    def cons(m, n, **over):
        d = {"first_size": m, "second_size": n, "first_root": mth(hashes[:m]).hex(), "second_root": mth(hashes[:n]).hex(),
             "proof": [p.hex() for p in consistency_proof(m, hashes[:n])] if 0 < m < n else []}
        d.update(over)
        return d

    cases = []
    for n in range(1, 10):
        for m in range(1, n + 1):
            cases.append(case(f"valid-{m}-to-{n}", "", cons(m, n), {"verdict": "PASS"}))
    for m, n in ((1, 33), (16, 33), (17, 33), (31, 33), (32, 33)):
        cases.append(case(f"valid-{m}-to-{n}", "", cons(m, n), {"verdict": "PASS"}))
    cases.append(case("valid-from-empty", "the empty tree is a prefix of every tree",
                      {"first_size": 0, "second_size": 5, "first_root": mth([]).hex(), "second_root": mth(hashes[:5]).hex(), "proof": []},
                      {"verdict": "PASS"}))
    p = cons(3, 8)["proof"]
    cases += [
        case("wrong-first-root", "", cons(3, 8, first_root=mth(hashes[:4]).hex()), {"verdict": "FAIL"}),
        case("wrong-second-root", "", cons(3, 8, second_root=mth(hashes[:7]).hex()), {"verdict": "FAIL"}),
        case("proof-truncated", "", cons(3, 8, proof=p[:-1]), {"verdict": "FAIL"}),
        case("proof-extended", "", cons(3, 8, proof=p + [sha(b"x").hex()]), {"verdict": "FAIL"}),
        case("proof-hash-flipped", "", cons(3, 8, proof=[p[0][:-1] + ("0" if p[0][-1] != "0" else "1")] + p[1:]), {"verdict": "FAIL"}),
        case("first-larger-than-second", "", cons(5, 3, proof=[]), {"verdict": "FAIL"}),
        case("equal-sizes-different-roots", "", cons(4, 4, second_root=mth(hashes[:5]).hex()), {"verdict": "FAIL"}),
        case("equal-sizes-nonempty-proof", "", cons(4, 4, proof=[sha(b"x").hex()]), {"verdict": "FAIL"}),
        case("from-empty-nonempty-proof", "", {"first_size": 0, "second_size": 5, "first_root": mth([]).hex(),
                                                "second_root": mth(hashes[:5]).hex(), "proof": [sha(b"x").hex()]}, {"verdict": "FAIL"}),
        case("growing-tree-without-proof", "", cons(3, 8, proof=[]), {"verdict": "FAIL"}),
    ]
    write("merkle-consistency.json", "verify_consistency", "section 7", "Consistency proofs (RFC 9162 section 2.1.4.2).", cases)


# ================================================================= signed notes
C2SP_VKEY = "example.com/foo+530d903a+AekyeRrm56hApGFkyQR4ZCbV54Id2LKaANYcrnKv3U2k"
C2SP_NOTE = ("This is an example message.\n\n— example.com/foo "
             "Uw2QOkn8srV1yJGh2VYRlL1Tnagv1YEq6TfXppzi2ONncAlTgK7Ztg1ERYNZXsYjOBH3mFXmRKuwHjG1Yu72IneyaQM=\n")


def vectors_notes() -> None:
    cases = []
    root = mth(leaf_hashes(base_records())[:8])
    text = f"{ORIGIN}\n8\n{b64(root)}\n"
    ts = tepoch(300) + 5

    def n(cid, note, vkeys, verdict, verified=None, desc=""):
        e = {"verdict": verdict}
        if verified is not None:
            e["verified"] = verified
        cases.append(case(cid, desc, {"note": note, "vkeys": vkeys}, e))

    n("c2sp-example", C2SP_NOTE, [C2SP_VKEY], "PASS", ["example.com/foo"],
      "EXTERNAL: the example in c2sp.org/signed-note@v1.1.0, produced by another implementation")
    n("c2sp-example-text-tampered", tamper(C2SP_NOTE, "example", "exampl3"), [C2SP_VKEY], "FAIL")
    n("c2sp-example-signature-tampered", tamper(C2SP_NOTE, "nagv1YEq6", "nagv1YEq7"), [C2SP_VKEY], "FAIL")
    n("c2sp-example-unknown-key", C2SP_NOTE, [VK_LOG], "FAIL", None, "no configured key signed the note")
    n("c2sp-example-no-keys", C2SP_NOTE, [], "FAIL")
    note = text + "\n" + log_sig(text)
    n("ilorium-checkpoint-log-signature", note, [VK_LOG], "PASS", [ORIGIN])
    n("log-signature-flipped", text + "\n" + log_sig(text, flip=True), [VK_LOG], "FAIL")
    n("log-signature-other-key-same-name", text + "\n" + log_sig(text, key=OTHER, kid_key=OTHER), [VK_LOG], "FAIL",
      None, "key id differs, so the signature is from an unknown key")
    n("known-key-bad-plus-good", text + "\n" + log_sig(text, flip=True) + cosig_ed(NAME_A, WA, ORIGIN, 8, root, ts),
      [VK_LOG, VK_A], "FAIL", None, "a failing signature from a known key rejects the note even if another verifies")
    n("unknown-plus-known", text + "\n" + cosig_ed(NAME_D, WD, ORIGIN, 8, root, ts) + log_sig(text), [VK_LOG], "PASS", [ORIGIN],
      "signatures from unknown keys are ignored")
    n("ed25519-cosignature", text + "\n" + cosig_ed(NAME_A, WA, ORIGIN, 8, root, ts), [VK_A], "PASS", [NAME_A])
    n("ed25519-cosignature-wrong-size", tamper(text, "\n8\n", "\n9\n") + "\n" + cosig_ed(NAME_A, WA, ORIGIN, 8, root, ts),
      [VK_A], "FAIL", None, "the cosignature binds the tree size")
    n("ed25519-cosignature-flipped", text + "\n" + cosig_ed(NAME_A, WA, ORIGIN, 8, root, ts, flip=True), [VK_A], "FAIL")
    n("mldsa44-cosignature", text + "\n" + cosig_ml(NAME_B, WB, WB_PUB, ORIGIN, 8, root, ts), [VK_B], "PASS", [NAME_B],
      "ML-DSA-44; signed with dilithium-py in the deterministic mode of FIPS 204; verified by the OpenSSL-backed verifier, an independent implementation")
    n("mldsa44-cosignature-flipped", text + "\n" + cosig_ml(NAME_B, WB, WB_PUB, ORIGIN, 8, root, ts, flip=True), [VK_B], "FAIL")
    n("mldsa44-cosignature-wrong-root", tamper(text, b64(root), b64(sha(b"other"))) + "\n"
      + cosig_ml(NAME_B, WB, WB_PUB, ORIGIN, 8, root, ts), [VK_B], "FAIL")
    n("two-witnesses", text + "\n" + cosig_ed(NAME_A, WA, ORIGIN, 8, root, ts) + cosig_ml(NAME_B, WB, WB_PUB, ORIGIN, 8, root, ts),
      [VK_A, VK_B], "PASS", [NAME_A, NAME_B])
    n("unsupported-algorithm-only", text + "\n" + cosig_ecdsa_placeholder(NAME_C, ts), [VK_C], "UNKNOWN", [],
      "ECDSA (type 0x02) is not in the initial profile: UNKNOWN, never PASS and never silently dropped")
    n("unsupported-plus-verified", text + "\n" + cosig_ecdsa_placeholder(NAME_C, ts) + cosig_ed(NAME_A, WA, ORIGIN, 8, root, ts),
      [VK_A, VK_C], "PASS", [NAME_A])
    n("no-final-newline", note[:-1], [VK_LOG], "FAIL")
    n("no-signature-block", text, [VK_LOG], "FAIL")
    n("no-signatures", text + "\n", [VK_LOG], "FAIL")
    n("signature-line-without-em-dash", tamper(note, "\u2014", "-"), [VK_LOG], "FAIL")
    n("control-character", tamper(note, "8\n", "8\x07\n"), [VK_LOG], "FAIL")
    line = note.splitlines()[-1]
    n("non-canonical-base64", tamper(note, line, line[:-2] + "=="), [VK_LOG], "FAIL")
    write("signed-note.json", "verify_signed_note", "section 7",
          "C2SP signed notes and cosignatures under the Ilorium algorithm profile.", cases)


# ================================================================= records
def vectors_records() -> None:
    cases = []
    base = base_records()

    def r(cid, text_or_objs, checks, verdict=None, desc=""):
        text = text_or_objs if isinstance(text_or_objs, str) else jsonl(text_or_objs)
        if verdict is None:
            verdict = "PASS" if all(v == "PASS" for v in checks.values()) else (
                "FAIL" if "FAIL" in checks.values() else "UNKNOWN")
        cases.append(case(cid, desc, {"records_jsonl": text}, {"verdict": verdict, "checks": checks}))

    allpass = {k: "PASS" for k in ("records.parse", "records.canonical", "records.schema", "records.ids", "records.refs", "records.order")}

    def one(mut, check, desc="", cid=None, verdict="FAIL"):
        recs = copy.deepcopy(base)
        mut(recs)
        r(cid, recs, {check: verdict}, None, desc)

    r("valid-mixed", base, allpass, "PASS", "observations, claims and evaluations")
    gap_recs = copy.deepcopy(base)
    gap_recs[8] = gap_record(8, 160)
    r("valid-gap-record", gap_recs, allpass, "PASS", "the Probe declares an interval it could not capture")
    sup = copy.deepcopy(base) + [evaluation(12, 240, [base[0]["id"]], supersedes=base[3]["id"])]
    r("valid-supersedes", sup, allpass, "PASS", "a correction supersedes an earlier evaluation")
    cl = copy.deepcopy(base)
    cl[2]["about"] = "deploy"
    r("valid-claim-about-action", cl, allpass, "PASS", "`about` may be an action name")
    r("valid-empty-file", "", allpass, "PASS", "no records")

    def f(i, key, val):
        def m(recs):
            recs[i][key] = val
        return m

    def delete(i, key):
        def m(recs):
            del recs[i][key]
        return m

    one(f(0, "extra", 1), "records.schema", "unknown top-level field", "unknown-field")
    one(delete(0, "spore_version"), "records.schema", "missing envelope field", "missing-envelope-field")
    one(f(0, "id", ulid(0).lower()), "records.schema", "ULID must be uppercase Crockford", "bad-ulid")
    one(f(0, "type", "event"), "records.schema", "unknown record type", "bad-type")
    one(delete(0, "actor"), "records.schema", "observation without actor", "observation-missing-actor")
    one(f(0, "kind", "gap"), "records.schema", "gap without the required fields", "gap-without-fields")
    one(f(0, "recorded_at", "2026-13-03T14:00:00Z"), "records.schema", "month 13", "invalid-date")
    one(f(0, "recorded_at", "2026-11-03T14:00:00"), "records.schema", "time without Z", "time-without-zone")
    one(f(0, "content_hash", "sha256:abc"), "records.schema", "malformed digest", "bad-content-hash")
    one(f(0, "fields", {"n": -1}), "records.schema", "negative integer in fields", "fields-negative")
    one(f(0, "fields", {"n": {"x": 1}}), "records.schema", "nested object in fields", "fields-nested")
    one(f(0, "fields", {"Ref": "x"}), "records.schema", "uppercase field name", "fields-uppercase-name")
    one(f(2, "cause", {"type": "magic"}), "records.schema", "unknown cause", "claim-bad-cause")
    one(f(2, "context", {"mood": "x"}), "records.schema", "unknown context key", "claim-bad-context")
    one(f(3, "inputs", []), "records.schema", "evaluation needs inputs", "evaluation-empty-inputs")
    one(f(3, "weight", "huge"), "records.schema", "unknown weight", "evaluation-bad-weight")
    one(f(3, "crossing", "magic"), "records.schema", "unknown crossing", "evaluation-bad-crossing")
    g = copy.deepcopy(base); g[8] = gap_record(8, 160); g[8]["fields"]["from"], g[8]["fields"]["to"] = tiso(150), tiso(100)
    r("gap-starts-after-it-ends", g, {"records.schema": "FAIL"}, None, "")
    g = copy.deepcopy(base); g[8] = gap_record(8, 160); g[8]["fields"]["reason"] = "tired"
    r("gap-bad-reason", g, {"records.schema": "FAIL"})
    g = copy.deepcopy(base); g[8] = gap_record(8, 160); g[8]["actor"]["kind"] = "agent"
    r("gap-actor-not-instrument", g, {"records.schema": "FAIL"}, None, "only the Probe (an instrument) declares gaps")
    dup = copy.deepcopy(base); dup[5]["id"] = dup[4]["id"]
    r("duplicate-id", dup, {"records.ids": "FAIL"})
    one(f(3, "inputs", [ulid(99)]), "records.refs", "input is not in the log", "ref-unknown-input")
    one(f(3, "inputs", [ulid(7)]), "records.refs", "input is a later record", "ref-later-input")
    one(f(3, "supersedes", ulid(99)), "records.refs", "supersedes nothing", "ref-supersedes-unknown")
    one(f(3, "supersedes", base[0]["id"]), "records.refs", "supersedes an observation", "ref-supersedes-not-evaluation")
    one(f(2, "about", ulid(99)), "records.refs", "claim about a missing record", "ref-claim-about-missing")
    one(f(5, "beat", 1), "records.order", "beat does not increase", "beat-not-increasing")
    one(f(5, "recorded_at", tiso(10)), "records.order", "clock went backwards: cannot tell tampering from skew",
        "clock-regression", verdict="UNKNOWN")
    text = jsonl(base)
    lines = text.splitlines(keepends=True)
    r("float-in-fields", tamper(text, '"files":3', '"files":3.5'), {"records.parse": "FAIL"})
    r("duplicate-member", tamper(text, '"files":3', '"files":3,"files":4'), {"records.parse": "FAIL"})
    r("no-final-newline", text[:-1], {"records.parse": "FAIL"})
    r("blank-line", lines[0] + "\n" + "".join(lines[1:]), {"records.parse": "FAIL"})
    r("crlf", tamper(text, "\n", "\r\n", -1), {"records.parse": "FAIL"})
    loose = json.dumps(base[1])  # same object, not canonical: spaces and original key order
    r("not-canonical-spaces", lines[0] + loose + "\n" + "".join(lines[2:]), {"records.canonical": "FAIL", "records.schema": "PASS"})
    shuffled = json.dumps(dict(reversed(list(base[1].items()))), separators=(",", ":"))
    r("not-canonical-key-order", lines[0] + shuffled + "\n" + "".join(lines[2:]), {"records.canonical": "FAIL", "records.schema": "PASS"})
    write("records.json", "verify_records", "section 5", "Record schema, canonical form and referential checks.", cases)


# ================================================================= strata
def vectors_strata() -> None:
    base = base_records()

    def all_pass(extra_gaps=None, pulses=True):
        names = [c for c in ALL_CHECKS if pulses or not c.startswith("pulse")]
        return exp("PASS", gaps=extra_gaps or [], **{c.replace(".", "__"): "PASS" for c in names})

    # ---------------- checkpoints
    cases = []
    cases.append(case("healthy", "records, four checkpoints (one idle), two witnesses, four pulses", build(), all_pass()))

    def cp(cid, desc, expect, **kw):
        cases.append(case(cid, desc, build(**kw), expect))

    def kwall(**k):
        return {i: dict(k) for i in range(4)}

    cp("log-signature-missing", "no log signature on the notes", exp("FAIL", checkpoint__log_signature="FAIL"), cp_kw=kwall(skip_log=True))
    cp("log-signature-wrong-key", "signed by another key that claims the log's name", exp("FAIL", checkpoint__log_signature="FAIL"),
       cp_kw=kwall(log_key=OTHER, log_kid_key=OTHER))
    cp("log-signature-flipped", "log signature does not verify", exp("FAIL", checkpoint__log_signature="FAIL"), cp_kw=kwall(log_flip=True))
    cp("witness-quorum-short", "one of two required witnesses", exp("UNKNOWN", checkpoint__witnesses="UNKNOWN"),
       cp_kw=kwall(witnesses=("A",)))
    cp("witness-quorum-one", "quorum 1 with one witness", all_pass(), cp_kw=kwall(witnesses=("A",)), trust=make_trust(quorum=1))
    cp("witness-none", "log signature only", exp("UNKNOWN", checkpoint__witnesses="UNKNOWN", checkpoint__log_signature="PASS"),
       cp_kw=kwall(witnesses=()))
    cp("witness-ed25519-tampered", "a witness cosignature does not verify", exp("FAIL", checkpoint__witnesses="FAIL"),
       cp_kw={3: {"flips": ("A",)}})
    cp("witness-mldsa-tampered", "an ML-DSA-44 cosignature does not verify", exp("FAIL", checkpoint__witnesses="FAIL"),
       cp_kw={3: {"flips": ("B",)}})
    cp("witness-unsupported-algorithm", "ECDSA witness + one verified, quorum 2: UNKNOWN",
       exp("UNKNOWN", checkpoint__witnesses="UNKNOWN"), cp_kw=kwall(witnesses=("A", "C")),
       trust=make_trust(quorum=2, witnesses=[VK_A, VK_C]))
    cp("witness-unsupported-quorum-met", "the unsupported witness is not needed", all_pass(), cp_kw=kwall(witnesses=("A", "C")),
       trust=make_trust(quorum=1, witnesses=[VK_A, VK_C]))
    cp("witness-unknown-ignored", "a cosignature from a witness nobody configured is ignored", all_pass(),
       cp_kw=kwall(witnesses=("A", "B", "D")))
    cp("witness-timestamp-in-future", "witness timestamps after the current time do not count",
       exp("UNKNOWN", checkpoint__witness_time="UNKNOWN", checkpoint__witnesses="UNKNOWN"), now=tiso(1502), with_pulses=False)
    cp("witness-timestamp-skewed", "witness time far from the checkpoint time", exp("UNKNOWN", checkpoint__witness_time="UNKNOWN",
       checkpoint__witnesses="PASS"), cp_kw={1: {"witness_ts_shift": 500}})
    cp("meta-beat-tampered", "sidecar changed after signing", exp("FAIL", checkpoint__meta="FAIL"),
       cp_hook=lambda e: e[1]["meta"].__setitem__("beat", e[1]["meta"]["beat"] + 1))
    cp("meta-root-mismatch", "validly signed sidecar that disagrees with the note", exp("FAIL", checkpoint__meta="FAIL"),
       cp_kw={1: {"meta_mut": lambda m: m.__setitem__("root", "sha256:" + sha(b"x").hex())}})
    cp("meta-size-mismatch", "sidecar tree size differs from the note", exp("FAIL", checkpoint__meta="FAIL"),
       cp_kw={1: {"meta_mut": lambda m: m.__setitem__("tree_size", 9)}})
    cp("meta-wrong-key", "sidecar signed by another key", exp("FAIL", checkpoint__meta="FAIL"), cp_kw=kwall(meta_key=OTHER))
    cp("meta-missing-field", "sidecar without a beat", exp("FAIL", checkpoint__meta="FAIL"),
       cp_kw={0: {"meta_mut": lambda m: m.pop("beat")}})
    cp("extension-lines", "extension lines are not allowed in Ilorium checkpoints", exp("FAIL", checkpoint__note="FAIL"),
       cp_kw={2: {"ext": ("extra",)}})
    cp("wrong-origin", "checkpoint of another log", exp("FAIL", checkpoint__note="FAIL"), cp_kw={2: {"origin": "other.example/log"}})

    def hook_no_blank(entries):
        entries[1]["note"] = tamper(entries[1]["note"], "\n\n", "\n")

    cp("note-without-blank-line", "signatures not separated from the text", exp("FAIL", checkpoint__note="FAIL"), cp_hook=hook_no_blank)
    cp("fork-same-size", "same tree size, different root, both validly signed", exp("FAIL", checkpoint__monotonic="FAIL", log__root="FAIL"),
       cp_kw={2: {"root": sha(b"forked")}})
    cp("size-shrinks", "tree size goes down", exp("FAIL", checkpoint__monotonic="FAIL"),
       cps=[(4, 100, "beats"), (8, 300, "beats"), (12, 500, "beats"), (8, 700, "interval")], with_pulses=False)
    cp("time-backwards", "translation time goes backwards", exp("FAIL", checkpoint__monotonic="FAIL"),
       cps=[(4, 300, "beats"), (8, 100, "beats"), (12, 500, "beats")], with_pulses=False)
    cp("beat-backwards", "beat goes backwards", exp("FAIL", checkpoint__monotonic="FAIL"),
       cp_kw={2: {"meta_mut": lambda m: m.__setitem__("beat", 0)}}, with_pulses=False)
    cp("file-not-provided", "no checkpoints", exp("UNKNOWN", checkpoint__note="UNKNOWN", log__root="UNKNOWN"), with_cps=False, with_pulses=False)
    cp("file-empty", "empty checkpoints file", exp("UNKNOWN", checkpoint__note="UNKNOWN"), cp_raw="", with_pulses=False)
    cp("line-not-canonical", "a checkpoint line with spaces", exp("FAIL", checkpoints__parse="FAIL"),
       cp_hook=lambda e: None, with_pulses=False, cp_raw="__LOOSE__")
    cp("blank-line", "blank line in the checkpoints file", exp("FAIL", checkpoints__parse="FAIL"), cp_raw="__BLANK__", with_pulses=False)
    cp("not-an-object", "line is not a JSON object", exp("FAIL", checkpoints__parse="FAIL"), cp_raw="[1]\n", with_pulses=False)
    cp("missing-meta", "line has only a note", exp("FAIL", checkpoints__parse="FAIL"), cp_raw="__NOMETA__", with_pulses=False)
    # raw-text cases are rewritten below from the healthy build
    healthy = build()
    entries = [json.loads(line) for line in healthy["checkpoints_jsonl"].splitlines()]
    for c in cases:
        raw = c["input"].get("checkpoints_jsonl")
        if raw == "__LOOSE__":
            c["input"]["checkpoints_jsonl"] = json.dumps(entries[0]) + "\n" + "".join(canon(e).decode() + "\n" for e in entries[1:])
        elif raw == "__BLANK__":
            c["input"]["checkpoints_jsonl"] = canon(entries[0]).decode() + "\n\n" + "".join(canon(e).decode() + "\n" for e in entries[1:])
        elif raw == "__NOMETA__":
            c["input"]["checkpoints_jsonl"] = canon({"note": entries[0]["note"]}).decode() + "\n"
    write("strata-checkpoints.json", "verify_strata", "sections 7 and 9",
          "Checkpoint notes, log and witness signatures, algorithm profile, sidecars and checkpoint sequence.", cases)

    # ---------------- log
    cases = []

    def lg(cid, desc, expect, **kw):
        cases.append(case(cid, desc, build(**kw), expect))

    altered = copy.deepcopy(base); altered[6]["claimant"]["id"] = "someone-else"
    lg("record-altered", "a record changed after it was checkpointed", exp("FAIL", log__root="FAIL"), file_recs=altered, with_pulses=False)
    lg("record-deleted", "a record removed", exp("FAIL", log__root="FAIL"), file_recs=base[:5] + base[6:], with_pulses=False)
    lg("records-reordered", "two records swapped", exp("FAIL", log__root="FAIL", records__order="FAIL"),
       file_recs=base[:8] + [base[9], base[8]] + base[10:], with_pulses=False)
    lg("records-truncated", "fewer records than the checkpoints cover", exp("UNKNOWN", log__root="UNKNOWN"), file_recs=base[:6], with_pulses=False)
    tail = base + [obs(12, 240, 7), obs(13, 260, 8)]
    lg("uncheckpointed-tail", "records after the latest checkpoint are not covered", exp("UNKNOWN", log__root="PASS", log__coverage="UNKNOWN"),
       recs=tail, cps=PLAN_CPS, with_pulses=False)
    loose = copy.deepcopy(base)
    lines = jsonl(base).splitlines(keepends=True)
    lines[3] = json.dumps(base[3]) + "\n"
    lg("record-not-canonical", "the leaf is the canonical form, so the tree still matches", exp("FAIL", records__canonical="FAIL", log__root="PASS"),
       file_recs="".join(lines), with_pulses=False)
    dup = copy.deepcopy(base); dup[5]["id"] = dup[4]["id"]
    lg("duplicate-id-signed", "a tree over records with a duplicate id", exp("FAIL", records__ids="FAIL", log__root="PASS"), recs=dup, with_pulses=False)
    lg("no-trailing-newline", "records file without a final newline", exp("FAIL", records__parse="FAIL"),
       file_recs=jsonl(base)[:-1], with_pulses=False)
    lg("records-file-empty", "no records, checkpoints that cover some", exp("UNKNOWN", log__root="UNKNOWN"), file_recs="", with_pulses=False)
    empty_cp = build(recs=[], cps=[(0, 100, "interval"), (0, 700, "interval")], with_pulses=False)
    cases.append(case("empty-log-idle-checkpoints", "an organism with no records yet proves it is alive with idle checkpoints",
                      empty_cp, exp("PASS", gaps=[], log__root="PASS", log__coverage="PASS", checkpoint__interval="PASS")))
    write("strata-log.json", "verify_strata", "sections 5 and 7", "Tampering with records against signed checkpoints.", cases)

    # ---------------- pulses
    cases = []

    def pl(cid, desc, expect, **kw):
        cases.append(case(cid, desc, build(**kw), expect))

    pl("signature-tampered", "pulse changed after signing", exp("FAIL", pulse__signature="FAIL"),
       pulse_hook=lambda p: p[1].__setitem__("state", "dormant"))
    pl("wrong-key", "pulse signed by another key", exp("FAIL", pulse__signature="FAIL"), pulse_kw={2: {"key": OTHER}})
    pl("no-pulse-key-configured", "cannot verify without a key", exp("UNKNOWN", pulse__signature="UNKNOWN"), trust=make_trust(pulse=False))

    pl("chain-broken", "prev_pulse does not match, validly signed", exp("FAIL", pulse__chain="FAIL"),
       pulse_kw={2: {"mut": lambda b: b.__setitem__("prev_pulse", "sha256:" + sha(b"wrong").hex())}})
    pl("first-pulse-with-predecessor", "seq 1 must have prev_pulse null", exp("FAIL", pulse__chain="FAIL"),
       pulse_kw={0: {"mut": lambda b: b.__setitem__("prev_pulse", "sha256:" + sha(b"wrong").hex())}})
    sub = build()
    plist = [json.loads(x) for x in sub["pulses_jsonl"].splitlines()]
    cases.append(case("export-starts-mid-chain", "an export may start after seq 1; its first predecessor is simply not checked",
                      {**sub, "pulses_jsonl": jsonl(plist[2:])}, exp("PASS", pulse__chain="PASS", pulse__signature="PASS")))
    cases.append(case("sequence-gap", "pulse 3 is missing, which also leaves 1200 s without a pulse", {**sub, "pulses_jsonl": jsonl([plist[0], plist[1], plist[3]])},
                      exp("UNKNOWN", gaps=["pulse_seq", "pulse_interval"], pulse__chain="UNKNOWN", pulse__interval="UNKNOWN", pulse__signature="PASS")))
    cases.append(case("sequence-repeats", "the same seq twice", {**sub, "pulses_jsonl": jsonl([plist[0], plist[1], plist[1]])},
                      exp("FAIL", pulse__chain="FAIL")))
    pl("beat-backwards", "beat goes down", exp("FAIL", pulse__order="FAIL"),
       pulse_kw={2: {"mut": lambda b: b.__setitem__("beat", 1)}})
    pl("time-backwards", "translation time goes down", exp("FAIL", pulse__order="FAIL"),
       pulses_plan=[(1, 110, "beats", 0), (2, 310, "beats", 1), (3, 200, "interval", 2), (4, 1510, "beats", 3)])
    pl("interval-gap-pulses", "a long silence between pulses", exp("UNKNOWN", pulse__interval="UNKNOWN"),
       pulses_plan=[(1, 110, "beats", 0), (2, 310, "beats", 1), (3, 1210, "interval", 2), (4, 3000, "beats", 3)], now=None)
    pl("checkpoint-ref-wrong-root", "the pulse points at a root the records do not produce", exp("FAIL", pulse__checkpoint_ref="FAIL"),
       pulse_kw={1: {"mut": lambda b: b["checkpoint"].__setitem__("root", "sha256:" + sha(b"x").hex())}})
    pl("checkpoint-ref-beyond-records", "the pulse refers to a tree larger than the records provided",
       exp("UNKNOWN", pulse__checkpoint_ref="UNKNOWN"),
       pulse_kw={1: {"mut": lambda b: b["checkpoint"].__setitem__("tree_size", 99)}})
    pl("organism-mismatch", "pulse of another organism", exp("FAIL", pulse__schema="FAIL"),
       pulse_kw={1: {"mut": lambda b: b.__setitem__("organism", "someone-else")}})
    pl("unknown-field", "unknown member", exp("FAIL", pulse__schema="FAIL"), pulse_kw={1: {"mut": lambda b: b.__setitem__("extra", 1)}})
    pl("challenge-trigger-without-challenge", "trigger challenge needs the challenge", exp("FAIL", pulse__schema="FAIL"),
       pulse_kw={1: {"mut": lambda b: b.__setitem__("trigger", "challenge")}})
    pl("answer-to-challenge", "a valid pulse answering a challenge", all_pass(),
       pulses_plan=[(1, 110, "beats", 0), (2, 310, "beats", 1), (3, 1210, "interval", 2), (4, 1510, "challenge", 3)])
    pl("bad-state", "unknown state of being", exp("FAIL", pulse__schema="FAIL"), pulse_kw={1: {"mut": lambda b: b.__setitem__("state", "dead")}})
    healthy_pulses = jsonl(plist)
    first = healthy_pulses.splitlines(keepends=True)
    cases.append(case("line-not-canonical", "pulse written with spaces", {**sub, "pulses_jsonl": json.dumps(plist[0]) + "\n" + "".join(first[1:])},
                      exp("FAIL", pulses__parse="FAIL")))
    cases.append(case("file-empty", "empty pulses file", {**sub, "pulses_jsonl": ""}, exp("UNKNOWN", pulse__chain="UNKNOWN")))
    write("strata-pulses.json", "verify_strata", "sections 6 and 8", "Pulse signatures, chain, order and references to the log.", cases)

    # ---------------- gaps and freshness
    cases = []

    def gp(cid, desc, expect, **kw):
        cases.append(case(cid, desc, build(**kw), expect))

    gp("checkpoint-interval-exceeded", "no checkpoint for 1700 s with a limit of 1020",
       exp("UNKNOWN", gaps=["checkpoint_interval"], checkpoint__interval="UNKNOWN"),
       cps=[(4, 100, "beats"), (8, 300, "beats"), (8, 2000, "interval"), (12, 2300, "beats")], with_pulses=False, now=tiso(2350))
    gp("checkpoint-stale", "the latest checkpoint is far older than the limit",
       exp("UNKNOWN", gaps=["stale"], checkpoint__interval="UNKNOWN"), with_pulses=False, now=tiso(5000))
    gp("both-stale", "checkpoints and pulses both stale", exp("UNKNOWN", gaps=["stale", "stale_pulse"],
       checkpoint__interval="UNKNOWN", pulse__interval="UNKNOWN"), now=tiso(5000))
    gp("exactly-at-limit", "a delta equal to limit plus grace (1020 s) is not a gap",
       all_pass(pulses=False), cps=[(4, 100, "beats"), (8, 1120, "beats"), (12, 1500, "beats")], with_pulses=False)
    gp("no-freshness-configuration", "without limits the intervals cannot be judged",
       exp("UNKNOWN", checkpoint__interval="UNKNOWN", checkpoint__witness_time="UNKNOWN", pulse__interval="UNKNOWN"),
       trust=make_trust(freshness=None))
    declared = copy.deepcopy(base); declared[8] = gap_record(8, 160)
    gp("declared-gap", "the Probe declared an interval it could not capture: listed, and the evidence stays PASS",
       all_pass(extra_gaps=["declared"]), recs=declared)
    gp("no-now-no-staleness", "without a current time freshness is not evaluated", all_pass(), now=None)
    write("strata-gaps.json", "verify_strata", "sections 9 and 10", "Evidence gaps: declared, detected and stale.", cases)


# ================================================================= spore
def vectors_spore() -> None:
    def holder(i: int, kind="human") -> dict:
        return {"kind": kind, "id": f"holder-{i}", "name": f"Holder {i}", "contact": f"holder{i}@example.org",
                "credential": f"https://example.org/credentials/{i}"}

    def spore(**over) -> dict:
        doc = {"spore": "1.0", "ilorium": "1.0", "organism": "organism-zero", "domain": "example.org",
               "stop_key_holders": [holder(1)]}
        doc.update(over)
        return doc

    def sp(obj, *, raw: str | None = None) -> dict:
        return {"spore_json": raw if raw is not None else json.dumps(obj, indent=1, ensure_ascii=False)}

    def ok(**checks):
        return exp("PASS", **checks)

    full = spore(
        genome="1.0", probe="1.0", membrane=["github.com/example"], responsible="Example Founder",
        threshold={"platform": "github", "group": "example/core", "sentinel": "example/sentinel", "commands": ["/stop"]},
        agents={"oz-architect": ["oz-architect[bot]"]},
        pulse_key="ed25519:" + b64(bytes(32)),
        pulse={"every_beats": 100, "max_interval_s": 3600, "challenge_deadline_s": 300},
        checkpoints={"url": "https://example.org/checkpoints", "every_beats": 100, "max_interval_s": 3600},
        witnesses=["witness-a"], humans=[{"id": "founder", "role": "founder", "accounts": ["github:founder"]}],
        stop_key_holders=[holder(1), holder(2, "institution")], announce=True)
    cases = [
        case("minimal", "the smallest valid Spore: one human stop key holder", sp(spore()), ok(spore__schema="PASS", spore__holders="PASS")),
        case("full", "every optional field, two holders (a human and an institution)", sp(full), ok()),
        case("wardens", "three holders: anyone can stop, so any number is valid", sp(spore(stop_key_holders=[holder(1, "institution"), holder(2, "institution"), holder(3)])), ok()),
        case("old-singular-field", "the draft singular stop_key_holder is not accepted", sp(None, raw=json.dumps({k: v for k, v in spore().items() if k != "stop_key_holders"} | {"stop_key_holder": holder(1)})), exp("FAIL", spore__schema="FAIL")),
        case("no-holders-field", "stop_key_holders is required", sp(None, raw=json.dumps({k: v for k, v in spore().items() if k != "stop_key_holders"})), exp("FAIL", spore__schema="FAIL")),
        case("empty-holders", "at least one holder", sp(spore(stop_key_holders=[])), exp("FAIL", spore__schema="FAIL")),
        case("holder-kind-organism", "a holder is never an organism", sp(spore(stop_key_holders=[holder(1, "organism")])), exp("FAIL", spore__schema="FAIL")),
        case("holder-missing-contact", "every holder needs a contact", sp(spore(stop_key_holders=[{k: v for k, v in holder(1).items() if k != "contact"}])), exp("FAIL", spore__schema="FAIL")),
        case("holder-missing-credential", "every holder needs a credential", sp(spore(stop_key_holders=[{k: v for k, v in holder(1).items() if k != "credential"}])), exp("FAIL", spore__schema="FAIL")),
        case("holder-extra-field", "holders are closed objects", sp(spore(stop_key_holders=[holder(1) | {"extra": "x"}])), exp("FAIL", spore__schema="FAIL")),
        case("duplicate-holder-id", "holder ids are unique", sp(spore(stop_key_holders=[holder(1), holder(1)])), exp("FAIL", spore__holders="FAIL")),
        case("unknown-field", "the Spore is a closed object", sp(spore(surprise=1)), exp("FAIL", spore__schema="FAIL")),
        case("wrong-version", "spore must be 1.0", sp(spore(spore="2.0")), exp("FAIL", spore__schema="FAIL")),
        case("duplicate-key", "duplicate member names are rejected", sp(None, raw='{"spore":"1.0","spore":"1.0"}'), exp("FAIL", spore__parse="FAIL")),
        case("float", "numbers are integers", sp(spore(pulse={"every_beats": 1.5, "max_interval_s": 1, "challenge_deadline_s": 1})), exp("FAIL", spore__parse="FAIL")),
        case("not-an-object", "a Spore is an object", sp(None, raw="[]"), exp("FAIL", spore__parse="FAIL")),
        case("bad-pulse-key", "pulse_key is an Ed25519 key", sp(spore(pulse_key="ed25519:short")), exp("FAIL", spore__schema="FAIL")),
        case("http-checkpoints", "checkpoint url must be https", sp(spore(checkpoints={"url": "http://example.org/c", "every_beats": 1, "max_interval_s": 1})), exp("FAIL", spore__schema="FAIL")),
    ]
    write("spore.json", "verify_spore", "section 12", "Spore documents: the stop_key_holders list and the closed schema.", cases)


# ================================================================= bundle and Vital Signs
BUNDLE_DOMAIN = "ilorium.example"
BUNDLE_CHECKS = ["bundle.parse", "bundle.schema", "bundle.files", "bundle.no_trust", "bundle.period", "bundle.identity",
                 "bundle.spore_key", "spore.parse", "spore.schema", "spore.holders"]
HOLDER = {"kind": "human", "id": "founder", "name": "Example Founder", "contact": "founder@example.org",
          "credential": "https://example.org/credentials/founder"}


def spore_dict(**over) -> dict:
    doc = {"spore": "1.0", "ilorium": "1.0", "organism": ORG, "domain": BUNDLE_DOMAIN,
           "pulse_key": "ed25519:" + b64(PULSE_KEY.pk), "stop_key_holders": [HOLDER]}
    doc.update(over)
    return doc


def file_ref(text: str, jsonl: bool) -> dict:
    data = text.encode("utf-8")
    ref = {"sha256": "sha256:" + sha(data).hex(), "bytes": len(data)}
    if jsonl:
        ref["entries"] = text.count("\n")
    return ref


def make_bundle(*, strata: dict | None = None, spore: dict | str | None = None, drop=(), manifest_mut=None,
                period=(-60, 1500), created=1555, extra_files=None, tamper_after=None) -> dict:
    """Return the bundle's files as {name: text}. The manifest is computed from the files as given, before ``tamper_after``."""
    strata = strata if strata is not None else build()
    spore_text = spore if isinstance(spore, str) else json.dumps(spore or spore_dict(), indent=1)
    files = {"records.jsonl": strata["records_jsonl"], "spore.json": spore_text}
    if "checkpoints_jsonl" in strata:
        files["checkpoints.jsonl"] = strata["checkpoints_jsonl"]
    if "pulses_jsonl" in strata:
        files["pulses.jsonl"] = strata["pulses_jsonl"]
    manifest = {
        "bundle": "1.0", "ilorium": "1.0", "organism": ORG, "domain": BUNDLE_DOMAIN, "origin": ORIGIN,
        "created_at": tiso(created), "period": {"from": tiso(period[0]), "to": tiso(period[1])},
        "files": {name: file_ref(text, name.endswith(".jsonl")) for name, text in files.items()},
    }
    if manifest_mut:
        manifest_mut(manifest)
    for name in drop:
        files.pop(name, None)
    if tamper_after:
        tamper_after(files)
    files.update(extra_files or {})
    files["bundle.json"] = canon(manifest).decode("utf-8") + "\n"
    return files


def manifest_hash(files: dict) -> str:
    return "sha256:" + sha(files["bundle.json"].encode("utf-8")).hex()


def vectors_bundle() -> None:
    trust = make_trust()
    all_ok = {c.replace(".", "__"): "PASS" for c in BUNDLE_CHECKS + ALL_CHECKS}

    def bc(cid, desc, files, expect, *, t=None, now=NOW):
        inp = {"files": files, "trust": t or trust}
        if now:
            inp["now"] = now
        cases.append(case(cid, desc, inp, expect))

    cases: list[dict] = []
    healthy = make_bundle()
    ok = exp("PASS", gaps=[], **all_ok)
    ok["manifest_sha256"] = manifest_hash(healthy)
    bc("healthy", "records, checkpoints, pulses and the Spore, with a manifest that matches", healthy, ok)
    bc("no-pulses", "pulses are optional", make_bundle(strata=build(with_pulses=False)),
       exp("PASS", gaps=[], **{k: v for k, v in all_ok.items() if not k.startswith("pulse")}))
    bc("no-checkpoints", "without checkpoints the records are not protected", make_bundle(strata=build(with_cps=False, with_pulses=False)),
       exp("UNKNOWN", log__root="UNKNOWN", bundle__files="PASS"))

    # --- the manifest
    bc("manifest-missing", "no bundle.json: not a bundle, and never PASS", {k: v for k, v in healthy.items() if k != "bundle.json"},
       exp("UNKNOWN", bundle__parse="UNKNOWN", bundle__files="UNKNOWN", spore__parse="UNKNOWN", spore__schema="UNKNOWN", spore__holders="UNKNOWN"))
    pretty = dict(healthy)
    pretty["bundle.json"] = json.dumps(json.loads(healthy["bundle.json"]), indent=1) + "\n"
    bc("manifest-not-canonical", "the manifest is Ilorium JSON, one canonical line", pretty, exp("FAIL", bundle__parse="FAIL"))
    nolf = dict(healthy)
    nolf["bundle.json"] = healthy["bundle.json"].rstrip("\n")
    bc("manifest-no-final-newline", "the manifest ends in a single line feed", nolf, exp("FAIL", bundle__parse="FAIL"))
    bc("manifest-duplicate-key", "duplicate member names are rejected", dict(healthy, **{"bundle.json": '{"bundle":"1.0","bundle":"1.0"}\n'}),
       exp("FAIL", bundle__parse="FAIL"))
    bc("manifest-unknown-field", "the manifest is a closed object", make_bundle(manifest_mut=lambda m: m.__setitem__("note", "x")),
       exp("FAIL", bundle__schema="FAIL"))
    bc("manifest-carries-keys", "a bundle never carries trust: no field for keys exists", make_bundle(manifest_mut=lambda m: m.__setitem__("trust", {"pulse_key": "x"})),
       exp("FAIL", bundle__schema="FAIL"))
    bc("manifest-requires-records", "records.jsonl must be listed", make_bundle(manifest_mut=lambda m: m["files"].pop("records.jsonl")),
       exp("FAIL", bundle__schema="FAIL"))
    bc("manifest-requires-spore", "spore.json must be listed", make_bundle(manifest_mut=lambda m: m["files"].pop("spore.json")),
       exp("FAIL", bundle__schema="FAIL"))
    bc("period-reversed", "from must not be after to", make_bundle(period=(1500, -60)), exp("FAIL", bundle__schema="FAIL"))
    bc("created-before-period-end", "a bundle cannot be created before the period it covers ends", make_bundle(created=1000),
       exp("FAIL", bundle__schema="FAIL"))
    bc("unknown-file-name", "only the four named files are listed", make_bundle(manifest_mut=lambda m: m["files"].__setitem__("notes.txt", {"sha256": "sha256:" + "0" * 64, "bytes": 0})),
       exp("FAIL", bundle__schema="FAIL"))

    # --- files against the manifest
    def alter_records(files):
        files["records.jsonl"] = files["records.jsonl"].replace("repo/main", "repo/maim", 1)

    bc("record-altered-after-manifest", "one record changed (same length): the checksum and the log root both fail", make_bundle(tamper_after=alter_records),
       exp("FAIL", bundle__files="FAIL", log__root="FAIL"))
    bc("manifest-wrong-hash", "the manifest lists another hash for the records", make_bundle(manifest_mut=lambda m: m["files"]["records.jsonl"].__setitem__("sha256", "sha256:" + "0" * 64)),
       exp("FAIL", bundle__files="FAIL", log__root="PASS"))
    bc("manifest-wrong-size", "bytes differ", make_bundle(manifest_mut=lambda m: m["files"]["pulses.jsonl"].__setitem__("bytes", m["files"]["pulses.jsonl"]["bytes"] + 1)),
       exp("FAIL", bundle__files="FAIL"))
    bc("manifest-wrong-entries", "entries differ", make_bundle(manifest_mut=lambda m: m["files"]["records.jsonl"].__setitem__("entries", 11)),
       exp("FAIL", bundle__files="FAIL"))
    bc("listed-file-missing", "a listed file was not provided: not proven, never PASS", make_bundle(drop=("checkpoints.jsonl",)),
       exp("UNKNOWN", bundle__files="UNKNOWN"))
    bc("records-missing", "the records are what everything rests on", make_bundle(drop=("records.jsonl",)),
       exp("UNKNOWN", bundle__files="UNKNOWN", records__parse="UNKNOWN"))
    bc("spore-missing", "a listed Spore was not provided", make_bundle(drop=("spore.json",)),
       exp("UNKNOWN", bundle__files="UNKNOWN", spore__parse="UNKNOWN", bundle__identity="UNKNOWN", bundle__spore_key="UNKNOWN"))
    bc("unlisted-file", "a file the manifest does not list", make_bundle(extra_files={"notes.txt": "hello\n"}), exp("FAIL", bundle__files="FAIL"))
    bc("trust-file-inside", "a bundle never carries trust configuration", make_bundle(extra_files={"trust.json": json.dumps(trust)}),
       exp("FAIL", bundle__no_trust="FAIL", bundle__files="FAIL"))

    # --- identity and period
    bc("organism-mismatch", "the manifest names another organism than the one configured",
       make_bundle(manifest_mut=lambda m: m.__setitem__("organism", "other-organism"), spore=spore_dict(organism="other-organism")),
       exp("FAIL", bundle__identity="FAIL"))
    bc("origin-mismatch", "the manifest names another log origin than the one configured",
       make_bundle(manifest_mut=lambda m: m.__setitem__("origin", "other.example/log")), exp("FAIL", bundle__identity="FAIL"))
    bc("spore-organism-differs", "the Spore names another organism than the manifest", make_bundle(spore=spore_dict(organism="other-organism")),
       exp("FAIL", bundle__identity="FAIL"))
    bc("spore-domain-differs", "the Spore names another domain than the manifest", make_bundle(spore=spore_dict(domain="other.example")),
       exp("FAIL", bundle__identity="FAIL"))
    bc("record-outside-period", "a record was written after the period ends", make_bundle(period=(-60, 100)), exp("FAIL", bundle__period="FAIL"))
    bc("record-before-period", "a record was written before the period starts", make_bundle(period=(100, 1500)), exp("FAIL", bundle__period="FAIL"))

    # --- the Spore inside the bundle
    other = Ed("other-pulse")
    bc("spore-key-differs", "the Spore's pulse key is not the one the verifier trusts", make_bundle(spore=spore_dict(pulse_key="ed25519:" + b64(other.pk))),
       exp("FAIL", bundle__spore_key="FAIL"))
    no_key = spore_dict()
    no_key.pop("pulse_key")
    bc("spore-without-pulse-key", "nothing to compare with the trusted key", make_bundle(spore=no_key), exp("UNKNOWN", bundle__spore_key="UNKNOWN"))
    bc("spore-invalid", "a Spore that breaks its schema", make_bundle(spore=spore_dict(surprise=1)),
       exp("FAIL", spore__schema="FAIL", bundle__identity="UNKNOWN", bundle__spore_key="UNKNOWN"))
    old = spore_dict()
    old.pop("stop_key_holders")
    old["stop_key_holder"] = HOLDER
    bc("spore-singular-holder", "the draft singular field is not accepted", make_bundle(spore=old), exp("FAIL", spore__schema="FAIL"))
    bc("spore-duplicate-holders", "holder ids are unique", make_bundle(spore=spore_dict(stop_key_holders=[HOLDER, HOLDER])),
       exp("FAIL", spore__holders="FAIL"))
    bc("spore-not-json", "the Spore must parse", make_bundle(spore="not json"), exp("FAIL", spore__parse="FAIL"))

    # --- a strata problem still shows through the bundle
    bc("strata-checks-included", "checkpoint and pulse checks appear in the bundle report", make_bundle(strata=build(cp_kw={1: {"flips": ("A",)}})),
       exp("FAIL", bundle__files="PASS", checkpoint__witnesses="FAIL"))
    write("bundle.json", "verify_bundle", "section 13", "Evidence Bundles: the manifest, the files, identity and the Spore.", cases)


def vital_dict(files: dict, **over) -> dict:
    pulses = [json.loads(line) for line in files["pulses.jsonl"].splitlines()]
    last = pulses[-1]
    dim = lambda status, newest, measures, lims: {"status": status, "newest_evidence": newest, "measures": measures, "limitations": lims}
    doc = {
        "vitalsigns": "1.0", "ilorium": "1.0", "organism": ORG, "domain": BUNDLE_DOMAIN, "generated_at": tiso(1600),
        "period": {"from": tiso(-60), "to": tiso(1500)},
        "bundle": {"url": "https://ilorium.example/bundles/organism-test/latest", "manifest_sha256": manifest_hash(files)},
        "web_status": "observed",
        "latest_pulse": {"seq": last["seq"], "beat": last["beat"], "translation_time": last["translation_time"],
                         "state": last["state"], "recovery": last["recovery"]},
        "dimensions": {
            "autonomy": dim("observed", tiso(1400), [{"id": "executed-by-agents", "count": 6, "of": 8}],
                            ["Only actions with attribution linked or better are counted."]),
            "coverage": dim("observed", tiso(1500), [{"id": "capture-available", "count": 2, "of": 2}],
                            ["Coverage is measured on the sources the Probe was configured for."]),
            "reliability": dim("not_observed", None, [], ["The organism has declared no work units yet."]),
            "control": dim("stale", tiso(300), [{"id": "drills-passed", "count": 1, "of": 1}],
                           ["The latest drill is older than the freshness window."]),
            "human_dependency": dim("no_activity", None, [], ["No work units were delivered in the period."]),
            "provenance": dim("observed", tiso(-60), [], ["Provenance is declared at birth and not independently attested."]),
        },
        "conformity": [{"law": n, "status": "conforms" if n < 5 else "not_observed"} for n in range(1, 8)],
        "provenance": {"birth": "founded", "succession": "founded", "generation": 0, "parents": []},
        "stop_key_holders": [HOLDER],
        "limitations": ["This is a presentation of evidence; it establishes the integrity of the evidence and nothing more."],
    }
    doc.update(over)
    return doc


def vectors_vitalsigns() -> None:
    files = make_bundle()
    base = vital_dict(files)
    cases: list[dict] = []

    def vc(cid, desc, doc, expect, *, bundle=files, raw=None):
        inp = {"vitalsigns_json": raw if raw is not None else json.dumps(doc, indent=1, ensure_ascii=False), "bundle": bundle}
        cases.append(case(cid, desc, inp, expect))

    def mutated(fn):
        doc = copy.deepcopy(base)
        fn(doc)
        return doc

    allv = {k: "PASS" for k in ("vitals__parse", "vitals__schema", "vitals__words", "vitals__bundle", "vitals__identity",
                                  "vitals__pulse", "vitals__stop_key_holders")}
    vc("healthy", "Vital Signs that match their bundle; one dimension is not_observed, one stale, one no_activity, at equal weight", base, exp("PASS", **allv))
    vc("bundle-unreachable", "the bundle cannot be reached: UNKNOWN, never PASS", base, exp("UNKNOWN", vitals__schema="PASS", vitals__bundle="UNKNOWN"), bundle=None)
    vc("manifest-missing", "the bundle has no manifest", base, exp("UNKNOWN", vitals__bundle="UNKNOWN"),
       bundle={k: v for k, v in files.items() if k != "bundle.json"})
    vc("manifest-hash-differs", "computed from another bundle", mutated(lambda d: d["bundle"].__setitem__("manifest_sha256", "sha256:" + "0" * 64)),
       exp("FAIL", vitals__bundle="FAIL"))

    def alter(f):
        f = dict(f)
        f["records.jsonl"] = f["records.jsonl"].replace("repo/main", "repo/maim", 1)
        return f

    vc("bundle-file-altered", "a file of the bundle no longer matches its manifest", base, exp("FAIL", vitals__bundle="FAIL"), bundle=alter(files))
    vc("bundle-file-missing", "a listed file is missing", base, exp("UNKNOWN", vitals__bundle="UNKNOWN", vitals__pulse="PASS"),
       bundle={k: v for k, v in files.items() if k != "checkpoints.jsonl"})
    vc("organism-differs", "another organism than the manifest's", mutated(lambda d: d.__setitem__("organism", "other-organism")), exp("FAIL", vitals__identity="FAIL"))
    vc("domain-differs", "another domain than the manifest's", mutated(lambda d: d.__setitem__("domain", "other.example")), exp("FAIL", vitals__identity="FAIL"))
    vc("period-differs", "another period than the manifest's", mutated(lambda d: d["period"].__setitem__("from", tiso(-30))), exp("FAIL", vitals__identity="FAIL"))
    vc("pulse-seq-differs", "not the last pulse of the bundle", mutated(lambda d: d["latest_pulse"].__setitem__("seq", 3)), exp("FAIL", vitals__pulse="FAIL"))
    vc("pulse-state-differs", "state of being differs from the last pulse", mutated(lambda d: d["latest_pulse"].__setitem__("state", "dormant")), exp("FAIL", vitals__pulse="FAIL"))
    vc("pulse-recovery-differs", "recovery differs from the last pulse", mutated(lambda d: d["latest_pulse"].__setitem__("recovery", "proven")), exp("FAIL", vitals__pulse="FAIL"))
    vc("pulse-null-but-pulses-exist", "a pulse exists, so latest_pulse cannot be null", mutated(lambda d: d.__setitem__("latest_pulse", None)), exp("FAIL", vitals__pulse="FAIL"))
    nop = make_bundle(strata=build(with_pulses=False))
    vc("pulses-not-in-bundle", "no pulses in the bundle: the latest pulse cannot be checked", mutated(lambda d: d["bundle"].__setitem__("manifest_sha256", manifest_hash(nop))),
       exp("UNKNOWN", vitals__pulse="UNKNOWN", vitals__bundle="PASS"), bundle=nop)
    vc("holders-differ", "stop key holders differ from the Spore", mutated(lambda d: d["stop_key_holders"].append(dict(HOLDER, id="other"))),
       exp("FAIL", vitals__stop_key_holders="FAIL"))
    vc("holder-name-differs", "the list is compared as published", mutated(lambda d: d["stop_key_holders"].__setitem__(0, dict(HOLDER, name="Another Name"))),
       exp("FAIL", vitals__stop_key_holders="FAIL"))

    # --- no seal words
    vc("word-certified", "never 'certified'", mutated(lambda d: d["limitations"].append("Certified by the index.")), exp("FAIL", vitals__words="FAIL"))
    vc("word-trusted-in-dimension", "never 'trusted', in any case, in a dimension", mutated(lambda d: d["dimensions"]["control"]["limitations"].append("A TRUSTED organism.")),
       exp("FAIL", vitals__words="FAIL"))
    vc("word-approved", "never 'approved'", mutated(lambda d: d["limitations"].append("Approved for delegation.")), exp("FAIL", vitals__words="FAIL"))
    vc("word-trusted-after-untrusted", "a whole word elsewhere in the sentence still fails", mutated(lambda d: d["limitations"].append("Nothing here is untrusted or trusted by the index by default.")),
       exp("FAIL", vitals__words="FAIL"))
    vc("word-in-longer-word-is-fine", "'distrusted' is not 'trusted'", mutated(lambda d: d["limitations"].append("Keys are never distrusted automatically.")),
       exp("PASS", vitals__words="PASS"))

    # --- the schema: no score, no rank, all six dimensions
    def put(key, value):
        return lambda d: d.__setitem__(key, value)

    vc("field-score", "there is no score field", mutated(put("score", 87)), exp("FAIL", vitals__schema="FAIL"))
    vc("field-rank", "there is no rank field", mutated(put("rank", 1)), exp("FAIL", vitals__schema="FAIL"))
    vc("field-seal", "there is no seal field", mutated(put("seal", "certified")), exp("FAIL", vitals__schema="FAIL"))
    vc("dimension-missing", "all six dimensions appear, observed or not", mutated(lambda d: d["dimensions"].pop("control")), exp("FAIL", vitals__schema="FAIL"))
    vc("dimension-extra", "an extra dimension is a composite by another name", mutated(lambda d: d["dimensions"].__setitem__("overall", copy.deepcopy(d["dimensions"]["control"]))),
       exp("FAIL", vitals__schema="FAIL"))
    vc("dimension-no-limitations", "every dimension states its limitations", mutated(lambda d: d["dimensions"]["autonomy"].__setitem__("limitations", [])),
       exp("FAIL", vitals__schema="FAIL"))
    vc("not-observed-with-evidence", "not_observed has no evidence", mutated(lambda d: d["dimensions"]["reliability"].__setitem__("newest_evidence", tiso(100))),
       exp("FAIL", vitals__schema="FAIL"))
    vc("not-observed-with-measures", "not_observed has no measures", mutated(lambda d: d["dimensions"]["reliability"].__setitem__("measures", [{"id": "x", "count": 0, "of": None}])),
       exp("FAIL", vitals__schema="FAIL"))
    vc("observed-without-evidence", "observed needs evidence", mutated(lambda d: d["dimensions"]["autonomy"].__setitem__("newest_evidence", None)), exp("FAIL", vitals__schema="FAIL"))
    vc("stale-without-evidence", "stale needs evidence", mutated(lambda d: d["dimensions"]["control"].__setitem__("newest_evidence", None)), exp("FAIL", vitals__schema="FAIL"))
    vc("evidence-after-period", "evidence cannot be newer than the period it is shown for", mutated(lambda d: d["dimensions"]["autonomy"].__setitem__("newest_evidence", tiso(1550))),
       exp("FAIL", vitals__schema="FAIL"))
    vc("period-reversed", "from must not be after to", mutated(lambda d: d.__setitem__("period", {"from": tiso(1500), "to": tiso(-60)})), exp("FAIL", vitals__schema="FAIL"))
    vc("generated-before-period-end", "generated_at is not before the end of the period", mutated(put("generated_at", tiso(1000))), exp("FAIL", vitals__schema="FAIL"))
    vc("status-certified", "web_status is one of four values", mutated(put("web_status", "certified")), exp("FAIL", vitals__schema="FAIL"))
    vc("conformity-law-twice", "a law is listed once", mutated(lambda d: d["conformity"].append({"law": 1, "status": "conforms"})), exp("FAIL", vitals__schema="FAIL"))
    vc("conformity-unknown-status", "conformity statuses are three", mutated(lambda d: d["conformity"][0].__setitem__("status", "excellent")), exp("FAIL", vitals__schema="FAIL"))
    vc("bundle-url-http", "the bundle link is https", mutated(lambda d: d["bundle"].__setitem__("url", "http://ilorium.example/b")), exp("FAIL", vitals__schema="FAIL"))
    vc("holders-empty", "at least one holder", mutated(put("stop_key_holders", [])), exp("FAIL", vitals__schema="FAIL"))
    vc("no-limitations", "limitations are part of every presentation", mutated(put("limitations", [])), exp("FAIL", vitals__schema="FAIL"))

    # --- parse
    vc("duplicate-key", "duplicate member names are rejected", None, exp("FAIL", vitals__parse="FAIL"), raw='{"vitalsigns":"1.0","vitalsigns":"1.0"}')
    vc("float-measure", "numbers are integers", None, exp("FAIL", vitals__parse="FAIL"),
       raw=json.dumps(base).replace('"count": 6', '"count": 6.5'))
    write("vitalsigns.json", "check_vitalsigns", "section 14", "Vital Signs against their Evidence Bundle.", cases)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    vectors_canonical()
    vectors_merkle()
    vectors_notes()
    vectors_records()
    vectors_strata()
    vectors_spore()
    vectors_bundle()
    vectors_vitalsigns()
    index = {"vector_index": "1.0", "protocol_release": "1.0", "note": "TEST KEYS ONLY. See Evidence Format 1.0, section 15.", "files": {}}
    total = 0
    for path in sorted(OUT.glob("*.json")):
        if path.name == "index.json":
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        index["files"][path.name] = {"operation": doc["operation"], "cases": len(doc["cases"]),
                                     "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        total += len(doc["cases"])
    index["total_cases"] = total
    (OUT / "index.json").write_text(json.dumps(index, indent=1) + "\n", encoding="utf-8")
    print(f"total cases: {total}")


if __name__ == "__main__":
    main()
