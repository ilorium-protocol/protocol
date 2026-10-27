# ilorium-verifier

The isolated verifier for Ilorium evidence. It checks a Strata export (records, checkpoints, pulses), an Evidence Bundle,
a Spore and Vital Signs against the Ilorium Evidence Format and prints a report with a verdict per check: **PASS**, **FAIL** or **UNKNOWN**.

The format it implements is defined in `specs/evidence-format-v1.md` (draft, release 1.0). This README does not
repeat it.

```
pip install -e ".[dev]"
ilorium-verifier conformity ../vectors                       # run the conformity vectors
ilorium-verifier strata EXPORT_DIR --trust trust.json --now 2026-11-03T14:30:00Z
ilorium-verifier bundle BUNDLE_DIR --trust trust.json --now 2026-11-03T14:30:00Z
ilorium-verifier vitalsigns vitalsigns.json --bundle BUNDLE_DIR   # without --bundle: UNKNOWN
ilorium-verifier spore spore.json
ilorium-verifier canon file.json                             # print the canonical form
```

Exit status: 0 PASS, 1 FAIL, 2 UNKNOWN, 64 usage error.

**ML-DSA-44.** Witness cosignatures with ML-DSA-44 need `cryptography` 48 or later (OpenSSL 3.5 or later). Without it the
verifier reports those cosignatures as unsupported, which gives UNKNOWN, never an error; the report says
`ml_dsa_44: false`.

**Isolation.** This package never imports the Probe or any other part of the reference implementation. It depends
on `cryptography` and `jsonschema` only; `tests/test_isolation.py` enforces it.

**Licenses.** Code, schemas and test vectors: Apache-2.0 (see `LICENSE`). Specification text: CC BY 4.0.
