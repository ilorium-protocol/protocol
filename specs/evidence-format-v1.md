# Ilorium Evidence Format v1.0

Version 1.0 · 2026-10-20 · Draft

How evidence is written, signed, exported and checked.

> **Evidence is only worth what a stranger can check without trusting the one who wrote it.**

## 1. Purpose and scope

The Probe (see the Probe specification) records what an organization does. The Pulse (see the Pulse specification) shows that it is present. This document defines the **bytes**: the shape of every record, how records become a verifiable log, which checkpoint format is used and how it is witnessed, how pulses are signed, how a Strata is exported, what a Spore, an Evidence Bundle and Vital Signs contain, and what a verifier must report.

It is the contract between the **protocol** and any **implementation**. The Probe's code (Go, from M1), the isolated verifier (Python, M0) and any verifier written by anyone else read this document and the shared test vectors. They do not read each other's code.

**What this document does.** Defines formats and the behavior of a verifier. It states what is checked and, as important, what is not.

**What it does not do.** It does not say what a good organism is (Genome), how beats are counted (Pulse), which events are collected or how they are classified (Probe), or how a score is computed (Proof of Life). A verifier following this document checks **integrity of evidence**, nothing more (section 16).

Facts, hypotheses and vision are kept apart. Sections 4 to 15 are normative. Section 16 lists limits that are facts about this release. Section 17 lists what is not defined yet.

## 2. Conventions

- The words MUST, MUST NOT, SHOULD and MAY are used as in RFC 2119.
- **Release** `1.0` is the protocol release. This document, the JSON Schemas and the vectors move together with it.
- Text is UTF-8. A file never starts with a byte order mark.
- Times are UTC strings `YYYY-MM-DDTHH:MM:SS[.fff]Z`, with at most three fractional digits. Offsets other than `Z` are invalid.
- Hashes are written `sha256:` followed by 64 lowercase hex digits. Ed25519 public keys are written `ed25519:` followed by standard base64 of the 32 key bytes. Ed25519 signatures in JSON are standard base64 of the 64 bytes (88 characters, padded).
- Identifiers of records are ULIDs (26 characters, Crockford base32, uppercase).
- **Machine-readable definitions** are the JSON Schemas (draft 2020-12) under `schemas/`: `common`, `record`, `pulse`, `checkpoint-meta`, `trust`, `spore`, `bundle` and `vitalsigns`. Where this text and a schema disagree, that is a defect: the conformity vectors decide, and the defect is fixed in the next edit.
- Every object in the schemas is closed (`unevaluatedProperties: false` or `additionalProperties: false`). An unknown field is a rejection, not something to ignore.

## 3. Two encodings

Two different text formats appear in Ilorium evidence. They are never mixed.

| Used for | Encoding | Defined by |
| --- | --- | --- |
| Records, pulses, checkpoint sidecars, trust configuration, the verifier's report | **Ilorium JSON**: JSON canonicalized with RFC 8785, restricted by section 4 | This document |
| The bundle manifest | **Ilorium JSON**, canonical, one line | Section 13 |
| The Spore and Vital Signs | JSON under the restrictions of section 4 (strict parsing, integers only, no duplicate names); not required to be canonical on the wire | Sections 12 and 14 |
| Checkpoints and their witness cosignatures | **C2SP signed note**: a text note with signature lines | C2SP `signed-note`, `tlog-checkpoint`, `tlog-cosignature`, pinned in section 7 |

A checkpoint is **not** a JSON document and is **never** canonicalized with RFC 8785. Beat number and translation time, which the Pulse needs and a C2SP checkpoint cannot carry, travel in a separate signed JSON object, the sidecar (section 7.3).

## 4. Ilorium JSON

Ilorium JSON is RFC 8785 (JSON Canonicalization Scheme) applied to a restricted set of JSON values. The restrictions remove everything on which independent implementations tend to disagree.

A verifier MUST reject, with the code in the right-hand column:

| Rule | Code |
| --- | --- |
| Top-level value is not an object | `not_object` |
| Not valid JSON, or trailing content after the value | `invalid_json` |
| A number with a fraction or an exponent (`1.0`, `1E5`) | `float_not_allowed` |
| An integer outside ±(2^53 − 1) | `integer_out_of_range` |
| `-0` | `negative_zero` |
| A duplicate key in any object | `duplicate_key` |
| A lone UTF-16 surrogate in a string or key | `lone_surrogate` |
| Nesting deeper than 64 levels | `too_deep` |
| A byte order mark | `invalid_json` |

Consequences: no floating-point number ever enters evidence (a ratio is two integers or a string), and canonicalization needs no number formatting algorithm. Keys are sorted by UTF-16 code units, as RFC 8785 requires.

**Canonical form on disk.** Every line of `records.jsonl`, `checkpoints.jsonl` and `pulses.jsonl` MUST already be the canonical form of its object. A line that parses but is not canonical is a failure (`records.canonical`, `checkpoints.parse`, `pulses.parse`). There is one byte string per object, so there is one hash per object.

**Signatures over JSON** use a domain label so that a signature made for one purpose cannot be replayed for another:

```
signing input = label || 0x0A || canonical(object without its "signature" field)
signature     = Ed25519(signing input)
```

| Object | Label (ASCII) |
| --- | --- |
| Pulse | `ilorium.pulse.v1` |
| Checkpoint sidecar | `ilorium.checkpoint-meta.v1` |

## 5. Records

A **record** is one line of the Strata: an observation, a claim or an evaluation (see the Probe specification for what they mean). Section 5 defines their fields; `schemas/record.schema.json` is the machine form.

### 5.1 Envelope

| Field | Meaning |
| --- | --- |
| `id` | ULID, unique in the log |
| `type` | `observation`, `claim` or `evaluation` |
| `occurred_at` | When the event happened according to its source |
| `received_at` | When the Probe received it |
| `recorded_at` | When the Probe wrote it to the log |
| `beat` | The organism's beat count, if the record is a material event (optional) |
| `protocol_release`, `probe_version`, `rules_version`, `policy_version`, `spore_version` | Versions in force when the record was written |

The three times are kept apart on purpose: a source can be late, and a clock can be wrong. They are never merged.

### 5.2 Observation

What the instrument saw, without interpretation: `source`, `source_event_id`, `kind` (`event`, `outcome` or `gap`), `actor` (`id` and `kind`: `agent`, `human`, `unknown` or `instrument`), `action`, `object`, optional `fields` (up to 64 scalar values; strings up to 1024 characters; no nested objects) and optional `content_hash`.

Content itself is never stored in a record, only its hash.

### 5.3 Gap observations

An absence of evidence is evidence, if it is written down. When the Probe knows it did not capture something, it MUST write an observation with `kind: "gap"`. Its `actor.kind` MUST be `instrument` (the Probe itself reports, not an agent). Its `fields` MUST contain:

| Field | Meaning |
| --- | --- |
| `from`, `to` | The span, in UTC |
| `reason` | `collector_down`, `queue_overflow`, `source_retention`, `probe_down`, `clock_unreliable` or `other` |
| `lost` | Number of events known to be lost, if known (optional) |

A declared gap appears in the verifier's report as a gap of kind `declared`. A verifier never turns a gap into a failure by itself: the Probe told the truth about what it missed.

### 5.4 Claim

A statement made by someone about an event: `claimant` (`id`, `kind` of `agent` or `human`), `about` (a record `id` or a name), `cause.type` (`autonomous`, `environment`, `directive` or `approval`, with an optional `ref`), optional `policy` and `context`. A claim is never presented as a fact.

### 5.5 Evaluation

A conclusion drawn by an instrument from earlier records: `evaluator` (`name`, `version`), `inputs` (one or more record ids), `function` (`operation`, `resources`, `resolution`, `development`, `growth` or `unclassified`), `attribution` (`declared`, `linked`, `corroborated`, `unknown` or `disputed`), `crossing` (`none`, `unknown`, `operational`, `directive`, `approval`, `emergency`, `governance` or `test`), optional `work_unit`, `weight` (`low`, `medium` or `high`) and optional `supersedes`. An evaluation never edits what it evaluates: a correction is a new evaluation that supersedes the earlier one.

### 5.6 What a verifier checks about records

| Check ID | Fails or is unknown when |
| --- | --- |
| `records.parse` | A line is not Ilorium JSON, or the file has a blank line, a missing final newline or a carriage return |
| `records.canonical` | A line is not in canonical form |
| `records.schema` | A record does not match the schema |
| `records.ids` | Two records share an `id` |
| `records.refs` | An evaluation `inputs` entry or `supersedes`, or a claim `about` that is an id, does not point to an **earlier** record (of type evaluation for `supersedes`) |
| `records.order` | `beat` does not strictly increase (FAIL); `recorded_at` goes backwards (UNKNOWN: it may be a clock regression, not tampering) |

## 6. The log

The Strata is an append-only Merkle tree following RFC 6962 section 2.1 (the construction RFC 9162 keeps for SHA-256 logs).

- **Leaf**: `SHA-256(0x00 || canonical record bytes)`, where the record bytes are the line without its newline.
- **Node**: `SHA-256(0x01 || left || right)`.
- **Empty tree**: `SHA-256("")`.
- The tree splits at the largest power of two smaller than the size.
- **Inclusion proofs** and **consistency proofs** are those of RFC 6962 sections 2.1.1 and 2.1.2, verified as in RFC 9162 sections 2.1.3.2 and 2.1.4.2.

A verifier given the records recomputes the root at every checkpoint size itself. It does not need a proof from the Probe to do so, and it never takes a root from the Probe's word.

| Check ID | Fails or is unknown when |
| --- | --- |
| `log.root` | The records do not produce the root at a checkpoint's size (FAIL); the checkpoint covers more records than were provided (UNKNOWN) |
| `log.coverage` | Records come after the latest checkpoint (UNKNOWN: they are not yet protected) |

## 7. Checkpoints and witnesses

### 7.1 Format: C2SP, pinned

Checkpoints are **C2SP tlog-checkpoints** in **signed-note** format. Ilorium does not invent a checkpoint format. The versions are pinned:

| Specification | Pinned version |
| --- | --- |
| `signed-note` | C2SP v1.1.0 |
| `tlog-checkpoint` | C2SP v1.1.0 |
| `tlog-cosignature` | C2SP v1.1.0 |
| `tlog-witness` | C2SP v1.1.0 |

Changing a pin is a change to this document, with a changelog entry and new vectors.

A checkpoint body has three lines: the **origin** (the log's identity, configured in the trust file), the tree size in decimal, and the root hash in standard base64. **Extension lines are not allowed in Ilorium 1.0**: a checkpoint with a fourth line fails (`checkpoint.note`).

A verification key ("vkey") is written as in C2SP: `name+hex(keyid)+base64(type || public key)`, where `keyid = SHA-256(name || 0x0A || type || public key)[:4]`. Because the base64 part can contain `+`, a vkey is split at the first two `+` only. A vkey whose key ID does not match its key is invalid.

### 7.2 Algorithm profile and unsupported signatures

| Role | Signature type byte | Algorithm | Status in 1.0 |
| --- | --- | --- | --- |
| Log signature | `0x01` | Ed25519 over the note text | Required |
| Witness cosignature | `0x04` | Ed25519 (`cosignature/v1`, with timestamp) | Supported |
| Witness cosignature | `0x06` | ML-DSA-44 (`subtree/v1` structure, with timestamp) | Supported |
| Any other type, including `0x02` (ECDSA) | — | — | **Not supported** |

The initial profile is not "everything is Ed25519". Witnesses that sign with ML-DSA-44, which C2SP recommends, are accepted next to Ed25519 witnesses.

**What happens to a signature the verifier cannot check.** It never counts as verified and it never counts as invalid:

- A cosignature on an unsupported algorithm is reported as `unsupported`. It does not count toward the witness quorum. If the quorum is not reached and at least one such signature exists, the result is **UNKNOWN** with the reason stated, not FAIL: the verifier does not know that the witness was wrong, only that it cannot tell.
- A signature that is supported and does not verify is **FAIL**.
- A log signature on an unsupported algorithm, with no other valid log signature, is **UNKNOWN**. A checkpoint with no log signature from a configured key is **FAIL**.
- A signature line from a key not in the trust file is ignored.

**ML-DSA-44 depends on the platform.** A verifier needs a cryptographic library that provides it (the reference verifier requires `cryptography` 48 or later, which uses OpenSSL 3.5 or later). A verifier that does not have it MUST report ML-DSA-44 cosignatures as `unsupported`, which gives UNKNOWN as above, never an error, and MUST say so in the report (`verifier.ml_dsa_44` is `false`).

A new algorithm enters the profile only through a change to this document and new vectors.

### 7.3 The sidecar

A C2SP checkpoint carries no beat number and no translation time. The Pulse needs both (two clocks). Each checkpoint therefore travels with a **sidecar**, a signed Ilorium JSON object (`schemas/checkpoint-meta.schema.json`):

| Field | Meaning |
| --- | --- |
| `checkpoint_meta` | `"1.0"` |
| `origin`, `tree_size`, `root` | Must match the note exactly |
| `beat` | The organism's beat count when the checkpoint was made |
| `translation_time` | UTC time the log signed it |
| `trigger` | `beats` or `interval` |
| `signature` | Ed25519 by the log's key (the one of the `0x01` log signature), label `ilorium.checkpoint-meta.v1` |

The sidecar is the organism's claim about its own beat and time. Witnesses cosign the note, not the sidecar. The witness **timestamp** in a `0x04` or `0x06` cosignature is the independent time reference: a verifier compares it with the sidecar's `translation_time` (section 7.4).

### 7.4 What a verifier checks about checkpoints

A line of `checkpoints.jsonl` is an Ilorium JSON object with exactly two fields: `note` (the signed note, as a string) and `meta` (the sidecar).

| Check ID | Fails or is unknown when |
| --- | --- |
| `checkpoints.parse` | The file is malformed, a line is not canonical or does not have exactly `note` and `meta` |
| `checkpoint.note` | The note is malformed, the origin is not the configured one, or it has extension lines |
| `checkpoint.log_signature` | No valid log signature (FAIL); only an unsupported one (UNKNOWN) |
| `checkpoint.witnesses` | A supported cosignature does not verify (FAIL); fewer verified cosignatures than the quorum (UNKNOWN) |
| `checkpoint.meta` | The sidecar is invalid, does not match the note, or its signature fails (FAIL); there is no key to check it (UNKNOWN) |
| `checkpoint.monotonic` | Tree size shrinks, the same size has a different root, or beat or time goes backwards (FAIL). That a larger tree extends a smaller one is checked by `log.root`, which recomputes every checkpoint root from the records |
| `checkpoint.interval` | More than `max_interval_s + grace_s` between checkpoints (UNKNOWN; a gap of kind `checkpoint_interval`); no freshness configuration (UNKNOWN) |
| `checkpoint.witness_time` | A witness timestamp differs from the sidecar time by more than `grace_s`, or is in the future (UNKNOWN) |

Tree size growing while the beat does not, or the reverse, is not an error by itself; going backwards is.

### 7.5 Public witnesses: what is and is not claimed

Using the C2SP format makes Ilorium **compatible** with public witnesses. It does not give access to them: each witness operator configures the logs and keys it accepts, and may refuse an unknown origin.

**Public-witness integration is not available in this release.** It will be declared available only after both: (1) an interoperability test of an Ilorium log against a real witness, and (2) an agreement with a witness operator. Until then, witnesses are those the organization configures and runs or arranges itself, and the verifier checks whatever cosignatures it is given.

## 8. Pulses

A pulse is the object defined in the Pulse specification, section 4; `schemas/pulse.schema.json` is the machine form. This section adds only the evidence rules.

- `signature` is Ed25519 with the key in the Spore (`pulse_key`) under the label `ilorium.pulse.v1` (section 4).
- `prev_pulse` is `sha256:` of the **canonical previous pulse including its signature**. The first pulse has `prev_pulse: null`.
- `seq` starts at 1 and increases by one.
- `checkpoint` names a tree size and root; the root must be the one the records produce at that size.

| Check ID | Fails or is unknown when |
| --- | --- |
| `pulses.parse` | The file is malformed or a line is not canonical |
| `pulse.schema` | A pulse does not match the schema |
| `pulse.signature` | The signature does not verify (FAIL); no pulse key configured (UNKNOWN) |
| `pulse.chain` | `prev_pulse` does not match, the first pulse has a predecessor, or `seq` does not increase (FAIL); pulses are missing between two (UNKNOWN; a gap of kind `pulse_seq`) |
| `pulse.order` | `beat` or `translation_time` goes backwards (FAIL) |
| `pulse.interval` | More than `max_interval_s + grace_s` between pulses (UNKNOWN; a gap of kind `pulse_interval`), or the latest pulse is older than that at the moment of verification (UNKNOWN; a gap of kind `stale_pulse`) |
| `pulse.checkpoint_ref` | The root does not match the records (FAIL); the tree size is not covered by the records provided (UNKNOWN) |

## 9. The Strata export

An export is a directory:

| File | Content |
| --- | --- |
| `records.jsonl` | Every record, in log order, one canonical line each, each ending in a single line feed |
| `checkpoints.jsonl` | The checkpoints (section 7.4), oldest first |
| `pulses.jsonl` | The pulses, oldest first |

`checkpoints.jsonl` and `pulses.jsonl` may be absent; that is reported as UNKNOWN, not as FAIL. `records.jsonl` is required.

**The export does not contain the keys that verify it.** Keys are supplied separately in `trust.json` (section 10). An export that carried its own keys would only prove that it agrees with itself.

An empty file is a valid file of zero entries. Lines end in a single line feed; carriage returns, blank lines and a missing final line feed are rejected.

## 10. Trust configuration

`trust.json` (`schemas/trust.schema.json`) is what the **person verifying** brings:

| Field | Meaning |
| --- | --- |
| `trust` | `"1.0"` |
| `organism` | The organism's label |
| `log.origin`, `log.vkeys` | The log's origin and its verification keys (1 to 8) |
| `witnesses.quorum`, `witnesses.vkeys` | How many distinct witnesses must have cosigned, and their keys |
| `pulse_key` | The Ed25519 pulse key |
| `freshness.max_interval_s`, `freshness.grace_s` | Maximum seconds between checkpoints and pulses, and the tolerated delay |

Distinct witnesses are counted by **witness name**: the same witness signing twice counts once. A cosignature whose timestamp is later than the verification time does not count toward the quorum.

In release 1.0 the trust file is supplied by hand. Anchoring the keys in the organism's birth act, so that a verifier can start from the Spore, is not implemented yet (section 17).

## 11. Verdicts and the report

Every check ends in one of three results. There is no fourth.

| Verdict | Meaning |
| --- | --- |
| **PASS** | The check ran and what it examined is consistent |
| **FAIL** | The evidence is inconsistent, forged or altered |
| **UNKNOWN** | The verifier could not decide: evidence is missing, stale, or uses something it does not support |

The overall verdict is the worst of all checks: FAIL, then UNKNOWN, then PASS. A missing file or an absent configuration is UNKNOWN, **never PASS**. UNKNOWN is not a softer FAIL; it is an honest "not proven", and the report says why.

**Gaps.** The report lists every gap, declared or detected:

| Kind | Source |
| --- | --- |
| `declared` | A gap observation written by the Probe (section 5.3) |
| `checkpoint_interval` | Too long between two checkpoints |
| `stale` | The latest checkpoint is older than allowed at verification time |
| `pulse_interval` | Too long between two pulses |
| `pulse_seq` | Pulse numbers missing |
| `stale_pulse` | The latest pulse is older than allowed at verification time |

Freshness (`stale`, `stale_pulse`) needs a verification time. The verifier takes it from `--now`; without it, those two checks are UNKNOWN. The verifier never reads the system clock by itself, so the same input gives the same report.

**Report.** An Ilorium JSON object with `report: "1.0"`, `verifier` (name, version and whether ML-DSA-44 is available), `protocol_release`, `organism`, `origin`, `verdict`, `summary` (counts of records, checkpoints and pulses, records after the last checkpoint, the latest checkpoint), `checks` (id, verdict and a reason for each), `gaps` and `limitations`. A report on a bundle (section 13) adds `bundle`.

**Limitations are part of every report.** A report that omitted them could be mistaken for more than it is. The reference verifier prints the five of section 16 every time, with PASS as well.

**Exit status** of the command line verifier: 0 PASS, 1 FAIL, 2 UNKNOWN, 64 usage error.

## 12. The Spore

The Spore is the document an organism serves at `https://<domain>/.well-known/ilorium.json` (Discovery and Growth specification). `schemas/spore.schema.json` is its machine form. This release defines the fields the schema lists; they are a draft and may change before a Spore specification exists (section 17).

Required fields: `spore` (`"1.0"`), `ilorium` (the release), `organism`, `domain` and `stop_key_holders`. Optional: `genome`, `probe`, `membrane`, `threshold`, `agents`, `work_units`, `pulse_key`, `pulse`, `checkpoints`, `witnesses`, `humans`, `responsible`, `kin`, `partners`, `announce` and `signatures`. The object is closed.

**`stop_key_holders`** is a list of one to 64 holders. Each is `{kind, id, name, contact, credential}`:

| Field | Meaning |
| --- | --- |
| `kind` | `human` or `institution`. There is no value for an organism: an organism never holds a stop key |
| `id` | A stable identifier, unique in the list |
| `name`, `contact` | Who the holder is and how to reach them, in public |
| `credential` | A reference to what identifies the holder. Its content is not defined in this release (section 17) |

**Anyone on the list can stop the organism.** A lineage with no human founders lists its Wardens, at least two, independent of the organism, its lineage and each other. That requirement belongs to the Genome and is checked against the succession record; the schema does not check it, and this release does not define the succession record.

| Check ID | Fails or is unknown when |
| --- | --- |
| `spore.parse` | The document is not valid Ilorium JSON (FAIL) |
| `spore.schema` | The document does not match the schema (FAIL) |
| `spore.holders` | Two holders share an `id` (FAIL) |

A check that could not run because an earlier one failed is UNKNOWN. These checks do not show that a holder is who the Spore says, that the credential is valid, that the contact works or that the `signatures` verify; none of that is verified in this release.

## 13. The Evidence Bundle

An Evidence Bundle is the evidence behind an organism's Vital Signs (section 14), downloadable and checkable without trusting Ilorium or the organism. It is a Strata export (section 9), the Spore as it stood, and a manifest over both. `schemas/bundle.schema.json` is the machine form of the manifest.

A bundle is a flat directory. How it is packaged for download is not defined in this release; a verifier is given the files by name.

| File | Content | Required |
| --- | --- | --- |
| `bundle.json` | The manifest | Yes |
| `spore.json` | The Spore, as the organism served it | Yes |
| `records.jsonl` | As in section 9 | Yes |
| `checkpoints.jsonl` | As in section 9 | No |
| `pulses.jsonl` | As in section 9 | No |

The Proof of Life evaluations and claims that Vital Signs rest on are records (sections 5.4 and 5.5) inside `records.jsonl`; there is no separate file for them. The bundle always starts at the first record of the log. A bundle for part of the log is not defined (section 17).

**A bundle never contains the keys that verify it.** There is no trust file in a bundle, and no field in the manifest for keys. The Spore may carry the organism's `pulse_key`; that is the organism's claim, to be compared with the key the verifier trusts (`bundle.spore_key`), never a root of trust.

**The manifest** is an Ilorium JSON object, canonical, on one line ending in a single line feed:

| Field | Meaning |
| --- | --- |
| `bundle` | `"1.0"` |
| `ilorium` | The protocol release |
| `organism`, `domain`, `origin` | The organism's label, its domain, and its log's origin |
| `created_at` | When the bundle was assembled |
| `period` | `from` and `to`: every record's `recorded_at` lies between them, and `to` is not after `created_at` |
| `files` | For each file other than the manifest: `sha256` of its bytes, `bytes`, and, for `.jsonl` files, `entries` (the number of lines) |

The hash of the manifest file, `sha256:` followed by the SHA-256 of its bytes, is how Vital Signs point to the bundle they were computed from.

| Check ID | Fails or is unknown when |
| --- | --- |
| `bundle.parse` | The manifest is malformed or not canonical (FAIL); it was not provided (UNKNOWN) |
| `bundle.schema` | The manifest does not match the schema, or its period is not `from <= to <= created_at` (FAIL) |
| `bundle.files` | A file's hash, size or number of entries differs from the manifest, or a file is present and not listed (FAIL); a listed file was not provided (UNKNOWN) |
| `bundle.no_trust` | The bundle contains `trust.json` (FAIL) |
| `bundle.period` | A record's `recorded_at` lies outside the period (FAIL) |
| `bundle.identity` | The manifest's organism or origin is not the configured one, or the Spore's organism or domain differs from the manifest's (FAIL); the Spore cannot be read to compare (UNKNOWN) |
| `bundle.spore_key` | The Spore's `pulse_key` differs from the pulse key the verifier trusts (FAIL); either is absent (UNKNOWN) |

A verifier also runs the Spore checks (section 12) on `spore.json` and every check of section 9 on the Strata files. A bundle's verdict is the worst of all of them. A missing manifest is UNKNOWN, never PASS.

The report is the report of section 11, with the bundle's checks first, a `bundle` object (`manifest_sha256`, `created_at`, `period`, `files`) and two more limitations: the manifest is a list of checksums that is not signed, so it shows that the files are the ones listed and not who assembled them; and the Spore is what the organism says about itself.

Consulting and downloading a bundle is free and needs no account. Nothing in a bundle is a seal, a certificate or a score.

## 14. Vital Signs

Vital Signs are the current state of an organism in a form a person or an agent reads in seconds (Discovery and Growth specification). `schemas/vitalsigns.schema.json` is the machine form of the JSON served at a stable address. **They present evidence; they establish nothing by themselves.** Their link to the evidence is the bundle (section 13).

| Field | Meaning |
| --- | --- |
| `vitalsigns` | `"1.0"` |
| `ilorium`, `organism`, `domain` | Release, organism label and domain |
| `generated_at`, `period` | When they were computed, and the period they cover (`from <= to <= generated_at`) |
| `bundle` | `url` (https) and `manifest_sha256`: the Evidence Bundle they were computed from |
| `web_status` | `sighting`, `in_gestation`, `observed` or `verified` (Ecosystem specification) |
| `latest_pulse` | `seq`, `beat`, `translation_time`, `state` and `recovery` of the newest pulse, or `null` |
| `dimensions` | The six Proof of Life dimensions: `autonomy`, `coverage`, `reliability`, `control`, `human_dependency`, `provenance`. All six are always present |
| `conformity` | One entry per law of the Genome: `law` and `status` (`conforms`, `does_not_conform` or `not_observed`) |
| `provenance` | `birth`, `succession`, `generation` and `parents` (Ecosystem specification) |
| `stop_key_holders` | As in the Spore (section 12) |
| `limitations` | At least one |

Each dimension has the same fields whatever its status: `status`, `newest_evidence`, `measures` and `limitations` (at least one). `status` is `observed`, `not_observed`, `no_activity` or `stale`. `observed` and `stale` need `newest_evidence`; `not_observed` has none and no measures; `no_activity` may have either. **"Not observed" has the same fields, and therefore the same weight, as "observed".** A measure is `{id, count, of}`: integers, with `of` null for a plain count and the denominator for a share, so that no floating-point number appears. The calculation of each measure belongs to Proof of Life and is not defined here (section 17); measure identifiers are not yet registered.

**There is no field for a score, a rank, a seal or a badge, and the object is closed**: adding one needs a new release. Organisms are never ranked.

| Check ID | Fails or is unknown when |
| --- | --- |
| `vitals.parse` | The document is not valid Ilorium JSON (FAIL) |
| `vitals.schema` | The document does not match the schema; the period is out of order; `newest_evidence` is after the end of the period; a law is listed twice (FAIL) |
| `vitals.words` | A `limitations` text contains the word "certified", "trusted" or "approved", in any case, as a whole word (FAIL) |
| `vitals.bundle` | The manifest is not the one `manifest_sha256` names, or a file of the bundle no longer matches it (FAIL); the bundle cannot be reached, or a listed file is missing (UNKNOWN) |
| `vitals.identity` | Organism, domain or period differ from the manifest's (FAIL) |
| `vitals.pulse` | `latest_pulse` is not the last pulse of the bundle (FAIL); the bundle has no pulses file (UNKNOWN) |
| `vitals.stop_key_holders` | They differ from the bundle's Spore (FAIL); the Spore cannot be read (UNKNOWN) |

**Vital Signs whose bundle cannot be reached are UNKNOWN**, never PASS. The word check is a mechanical minimum for text written by whoever presents the Vital Signs; it does not guarantee that nothing misleading is said. These checks show that Vital Signs agree with their bundle in what can be compared mechanically. They do not recompute the dimensions, the web status, the conformity or the provenance (section 16).

## 15. Conformity vectors

The vectors under `vectors/` are the other half of this specification: the same inputs and expected results for every implementation, in any language.

- A vector file has `vector`, `operation`, `spec` (the section it tests), `description` and `cases`. Each case has an `id`, an `input` and the `expect`ed result (a subset match: the implementation may return more, never less or different).
- Operations: `canonicalize`, `merkle_root`, `verify_inclusion`, `verify_consistency`, `verify_signed_note`, `verify_records`, `verify_strata`, `verify_spore`, `verify_bundle` and `check_vitalsigns`.
- `vectors/index.json` lists every file with its SHA-256 and number of cases.
- **The vectors are generated by `tools/gen_vectors.py`, which shares no code with the verifier**, and the expectations are written by hand. Vectors are never edited by hand. ML-DSA-44 signatures are made in the deterministic mode of FIPS 204, so regenerating reproduces every file byte for byte; a test checks it, and `vectors/index.json` pins each file by SHA-256.
- One vector is external: the example signed note published in C2SP, so that the verifier is tested against something neither Ilorium nor the generator wrote.
- Test keys are derived from public strings (`ilorium-test-vector-key/<name>`) and MUST NOT be used for anything else.

An implementation claims conformity with release 1.0 by passing every vector of that release. Passing is necessary, not sufficient: it shows the cases above and nothing else.

## 16. Limits of this release

These are facts about what a verification under this document means:

1. A signature shows who signed, not that the content is true.
2. A verifier checks only the records, checkpoints and pulses it was given. It cannot show that every relevant event was recorded.
3. Records after the latest checkpoint are not protected by it.
4. Keys come from the trust file supplied; they are not yet anchored in the birth act.
5. A verifier checks the integrity of evidence. It does not evaluate the Genome's laws or Proof of Life.

6. The manifest of a bundle is a list of checksums and is not signed: it shows that the files are the ones listed, not who assembled the bundle.
7. Vital Signs are checked against their bundle for identity, latest pulse, stop key holders and the words they may not use. The dimensions, the web status, the conformity and the provenance are not recomputed from the records, because their calculation is not defined yet.
8. *(Added 2026-10-24.)* Evidence produced by another system (a signed receipt of a tool call, a hardware attestation, an external identity) and imported into the Strata is a record that such an artifact was received. Importing, normalizing, hashing or signing an external record does not increase the evidentiary strength of the claim that record makes. A verifier MUST keep apart the integrity of the artifact and the authentication of its issuer from evidence of execution, attribution of a decision, completeness of observation and conformity of the organism; the claims an imported record does not support stay UNKNOWN. An intermediary's signature is never the signature of the counterparty of an action. No adapter for external evidence exists in this release (section 17).

Also, as of this release: the ML-DSA-44 vectors are produced by `dilithium-py`, a pure-Python FIPS 204 implementation that shares nothing with the OpenSSL code the verifier uses, and the two agree; no one outside this project has reviewed the vectors. A second verifier, written separately in another language, is planned (architecture, M7) to test whether this document is enough to build one without reading the first.

## 17. Not defined yet

- The Spore specification beyond section 12, the verification of its signatures, what a stop key holder's `credential` must be, and the signed succession record that lets the Wardens requirement be checked.
- An Evidence Bundle for part of the log: it would carry the Merkle frontier at its start (the subtree hashes of the first records) and a cosigned checkpoint of that size, so that the records can be joined to the rest of the log. References from its records to earlier records would then be UNKNOWN, not FAIL.
- How a bundle is packaged for download.
- How the Proof of Life measures, the web status and the conformity are computed from the records, and the register of measure identifiers.
- Anchoring of the log and pulse keys in the birth act.
- Key rotation records.
- Challenge and answer format (Pulse, open questions).
- Release, coalescence and recovery-drill records.
- Public-witness integration (section 7.5).
- Redaction of records, and the proof that a redaction hid only what it declared.
- Adapters that import evidence from other systems, the fields such records keep (source and version, source identifier, commitment to the original, capture and import times, issuer material, scope of what was signed, transformations, adapter version) and their vectors (architecture, "Adapters for external evidence"; limit 8 of section 16).

## 18. Licensing

The text of this document is licensed under CC BY 4.0. The JSON Schemas, the conformity vectors, the examples and all code are licensed under Apache-2.0, so that anyone can embed them in an implementation without a second license. Contributors keep the rights in what they contribute and license it under the license of the file they change (inbound = outbound). "Nobody owns the protocol" is an aim of governance; it does not replace stating who licenses each contribution.

The copyright holder named in headers is "The Ilorium Authors", listed in `AUTHORS`. Every commit carries a `Signed-off-by:` line (Developer Certificate of Origin 1.1). A commit written by an AI agent has the agent as its author, under its own identity, and the `Signed-off-by:` of the human or organization responsible for it; an agent never signs off for itself. The full text of CC BY 4.0 is in `LICENSE-SPECS`, and of Apache-2.0 in `LICENSE`.
