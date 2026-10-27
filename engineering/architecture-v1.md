# Ilorium Software Architecture v1.0

Version 1.0 · 2026-10-20 · Draft

Not part of the protocol: the reference implementation.

## Purpose

Ilorium needs its own code: the reference implementation that any organization can install to produce conforming evidence, and the tools anyone can use to check it. Its repository, CLI and packages are named `ilorium` (`ilorium-*` for packages); the Spore lives at `/.well-known/ilorium.json`. This document defines how that code is organized, written, installed, secured, tested and released. It is a starting architecture, to be revised as the code is written.

Related projects (A2A, NOMOS, Signet) give ideas and, where licenses allow, code. Ilorium reuses **standards** and small, audited **libraries**; it does not build on another project's runtime or trust root.

## Principles

1. **The specification leads, the code follows.** Every behavior traces to a section of a protocol document; anything the code does that the specification does not say is a bug or an open item.
2. **Verifiable by someone who does not trust us.** The verifier is small, isolated and auditable on its own. A second verifier, in another language and written separately, is a goal before the first stable release of the code.
3. **Few dependencies, each one justified.** Every dependency is listed, pinned, license-checked and reviewed.
4. **Secure by default, fail-closed where it matters.** Least privilege, no secrets in repositories, gates that refuse when unsure.
5. **Boring technology.** Standard formats, standard tools, readable code. Operators know systemd and containers, and a single static binary installs without a runtime; the verifier is small enough for an auditor to read.
7. **The protocol does not depend on a language.** Formats, schemas and conformity vectors are shared; any implementation in any language that passes the vectors is equal. The reference code is written in Go (Probe) and Python (first verifier) for different reasons, below.
6. **Honest about limits.** Every component documents what it cannot see or prevent, as the specifications do.

## Components

| Component | What it does | Layer | Language |
| --- | --- | --- | --- |
| **Evidence format** | Defined in `specs/evidence-format-v1.md`: JSON Schemas for records, pulses, checkpoint sidecars and the trust file; the Ilorium JSON profile of RFC 8785; the C2SP checkpoint profile; the verdicts and the report. Spore and succession schemas wait for the Spore specification | Protocol | Schemas and conformity vectors (Apache-2.0). No library is normative |
| **Verifier** | Checks a log, checkpoints, consistency proofs, pulses and a Spore against the format; checks succession records against the birth gate (parents conforming, human stop key holder accepted before the act, signatures of every parent); produces a report with verdicts PASS, FAIL, UNKNOWN | Protocol tooling | Python (`ilorium-verifier`, M0); a second verifier later, in another language and written separately |
| **Probe** | Long-running service: collectors, correlator, log writer, checkpoint signer, publisher | Reference | Go |
| **Collectors** | One per source: Sentinel (Telegram), GitHub, Workspace/Gmail, system journal, A2A middleware, business systems | Reference | Go, one package each |
| **Pulse emitter** | Pulses every N beats or every T; answers challenges. Part of the Probe, and a standalone beacon for beacon mode | Reference | Go |
| **Authorization gate** | Refuses irreversible actions without a recorded authorization; hooks for hook-capable agent hosts and an HTTP gate for deploys and payments; reports allowed and refused attempts to the Probe | Reference (optional) | Go; hook scripts with no dependencies |
| **A2A extension middleware** | Adds the Ilorium extension to Agent Cards; carries pulse references; reports task states to the Probe | Reference | Go |
| **CLI (`ilorium`)** | `init`, `spore`, `verify`, `status`, `keys`, `doctor` | Reference | Go |
| **Index** | Collects Spores, follows kin links, sends challenges, publishes open data at ilorium.com | Observatory (separate repository) | To decide |

### Data flow

```
sources ──► collectors ──► local store (append-only, SQLite) ──► correlator ──► evaluations
                                   │
                                   ▼
                           log writer (Ilorium JSON + RFC 6962 tree)
                                   │
                    checkpoint signer (every N beats or every T)
                                   │
                   publisher ──► public Strata repository ──► witnesses ──► verifiers
                                   │
                           pulse emitter ──► indexes / A2A counterparts
```

### Trust boundaries

| Boundary | What crosses it | Control |
| --- | --- | --- |
| Source → collector | Events from third-party APIs | Read-only credentials per source; allowlisted fields only; content hashed, never published |
| Agents → Probe | Claims and A2A task records | Local endpoint authenticated per agent identity; claims never trusted as facts (attribution states) |
| Probe → public | Records, checkpoints, pulses | Signed with keys held only by the Probe user; nothing private leaves |
| Public → verifier | Everything published | Verifier trusts nothing it cannot recompute; keys taken from the birth act and witness-cosigned rotations |
| Agent → gate | Requests to perform irreversible actions | Fail-closed; authorization must reference a recorded command or rule |
| Stop key holder → organism | The stop | The stop key is held by a human, outside every agent and outside the Probe; the Probe records the stop, it never holds the key |

## Formats and standards

| Need | Choice | Status |
| --- | --- | --- |
| Data format | JSON, JSON Schema (draft 2020-12) | Decided |
| Canonical form | RFC 8785 (JCS), restricted to integers and strict inputs (Ilorium JSON, Evidence Format section 4). The verifier is cross-checked in its tests against the Python package `rfc8785` (0.1.4) | Decided |
| Hash | SHA-256 | Decided |
| Signatures | Ed25519 for logs, pulses and sidecars; Ed25519 and ML-DSA-44 accepted for witness cosignatures; other algorithms are reported UNKNOWN, never PASS. Python verifier: `cryptography` (pyca) | Decided |
| Log tree and proofs | RFC 6962 Merkle tree with the proof verification of RFC 9162 | Decided |
| Checkpoints and witnessing | C2SP `signed-note`, `tlog-checkpoint`, `tlog-cosignature` and `tlog-witness`, pinned at v1.1.0 (a checkpoint is a signed note, not RFC 8785 JSON; beat and translation time travel in a signed sidecar). A C2SP witness checks consistency and cosigns; it does not send Ilorium challenges. The challenge operator (Pulse, section 6) is a separate function, run by an index or a dedicated witness, even when one entity does both | **Decided** as a format. Using public witnesses is **not available** until an interoperability test and an agreement with a witness operator exist |
| Spore and Agent Card signatures | JWS over RFC 8785, as in A2A 1.0 | Proposed |
| Agent communication | A2A | Decided (Discovery and Growth) |

## Repository layout

One public monorepository for the protocol and the reference implementation, under the GitHub organization `ilorium-protocol`; the index in its own repository.

```
ilorium/
  ilorium/         protocol documents (genome/, specs/, engineering/, research/, brand/)
  schemas/         JSON Schemas (Apache-2.0)
  vectors/         conformity vectors per specification (generated, Apache-2.0)
  tools/           gen_vectors.py: independent generator, shares no code with the verifier
  verifier/        isolated verifier (Python): imports nothing from probe/
  probe/           (from M1, Go)
    core/          records, local store, log writer, checkpoint signer, publisher
    collectors/    sentinel_telegram, github, workspace, journal, a2a, business
    correlator/    attribution, crossings, work units
    pulse/         emitter, challenge responder, beacon mode
  gate/            authorization gate: host hooks, HTTP gate
  a2a/             extension middleware
  cli/             ilorium command
  deploy/          systemd units, container image, example configs
  docs/            operator and contributor guides
  LICENSE  LICENSE-SPECS  NOTICE  SECURITY.md  CONTRIBUTING.md
```

Only `ilorium/`, `schemas/`, `vectors/`, `tools/`, `verifier/` and the repository files exist today (M0).

**The verifier never imports the Probe.** It depends only on the evidence format and its pinned libraries (`cryptography`, `jsonschema`, `referencing`), so it can be audited alone (idea from Signet). A test (`tests/test_isolation.py`) fails if it imports anything else.

## Language, licenses and governance

Decided on 2026-10-20, by the founder.

**Languages.** The persistent Probe is written in **Go** from M1: distribution as executables and operation as a service are the priority. The first verifier (M0) is written in **Python**, because it is small and auditors read it easily. The protocol stays independent of both: formats and vectors are shared, and a second verifier in a third language is milestone M7.

**M1 priorities for the Go Probe**, in this order: durable persistence (a record acknowledged is a record on disk), crash recovery (restart at any point without losing or duplicating records, and write the gap), resource limits (bounded queues, disk, memory and open files, with overflow recorded as a gap, never silently dropped), and explicit signaling of gaps in the evidence (every interval in which a collector or the Probe was down becomes a `gap` observation, Evidence Format section 5.3).

**Licenses.** Code, JSON Schemas, conformity vectors and examples: **Apache-2.0**, so anyone can embed them in an implementation, with the patent grant of contributors. Normative text (the Markdown documents): **CC BY 4.0**. Each contribution is licensed by its author under the license of the file it changes (inbound = outbound); contributors keep their copyright. "Nobody owns the protocol" describes how it is governed; it does not replace stating who licenses what. The copyright holder named in headers is, for now, "The Ilorium Authors", until the founder names a legal entity.

**Governance, interim.** Until the governance document exists, the founder alone merges and publishes releases. This is declared, not hidden, and it changes when the governance document is accepted.

## Dependencies

**Policy**

- Each dependency needs a written reason, a license compatible with Apache 2.0, an active maintainer and a review before it is added.
- Pinned versions with hashes in a lock file; installs refuse unpinned packages.
- No dependency may make network calls at import time.
- Prefer the standard library and plain HTTP over vendor SDKs; a collector that needs an SDK isolates it in its own module.
- A software bill of materials (SBOM, CycloneDX or SPDX) ships with every release.
- Dependency updates arrive as pull requests with the diff reviewed by a maintainer who did not author them.

**Initial candidates**

Verifier (Python, in use):

| Library | For | Notes |
| --- | --- | --- |
| `cryptography` (pyca) | Ed25519, ML-DSA-44, SHA-256 | Widely used, audited |
| `jsonschema`, `referencing` | JSON Schema 2020-12 validation | Pinned |
| `rfc8785` | Cross-check of canonicalization | Development and tests only; the verifier has its own canonicalizer |

Probe (Go, to review at M1; none is adopted yet):

| Library | For | Notes |
| --- | --- | --- |
| Go standard library | Ed25519, SHA-256, HTTP, `database/sql` | Preferred wherever it is enough |
| `golang.org/x/mod/sumdb/note` | C2SP signed notes | To verify that it covers the pinned profile, including ML-DSA-44 |
| `github.com/transparency-dev/merkle` | RFC 6962 hashing and proofs | To verify, and to compare with our vectors |
| `modernc.org/sqlite` | Local append-only store, no cgo | To compare with plain files and a write-ahead log, for durability |

Whatever is adopted must pass the conformity vectors.

Not yet in place for the Python verifier: a lock file with hashes, a software bill of materials and continuous integration.

## Installation

| Path | For whom | How |
| --- | --- | --- |
| **Beacon** | Anyone who wants to appear as a sighting | One small binary or script: generates a pulse key, publishes a Spore, emits pulses, answers challenges |
| **Full Probe, executable** | Operators on a Linux server | Download the signed static binary (or `go install`), then `ilorium init` |
| **Full Probe, container** | Operators with container platforms | Signed image, non-root user, read-only filesystem, minimal base |
| **Gate** | Organisms that want prevention, not only detection | Hook scripts installed in the agent host; HTTP gate in front of deploy or payment endpoints |

`ilorium init` walks through step zero: separate identities, keys, Spore, membrane, Threshold, human stop key holder, collectors to enable, witness choice. `ilorium doctor` checks permissions, clock sync, collector health and key custody.

**systemd hardening** for the Probe service: dedicated `oz-probe` user, `NoNewPrivileges`, `ProtectSystem=strict`, `ProtectHome`, `PrivateTmp`, a writable path only for its store, journal access through a restricted group, credentials loaded with systemd credentials or a 0600 file owned by the service user.

## Configuration and secrets

- **Configuration** (non-secret: membrane, collectors, N, T, work-unit types) lives in the organism's repository, so changes to it are observed by the Probe itself.
- **Secrets** (source tokens, Sentinel bot token, signing keys) never live in a repository. They are readable only by the Probe user.
- **Keys, separated by purpose:** log signing key (checkpoints), pulse key (pulses and challenge answers), and the organism's identity anchored in its birth act. Each can rotate on its own; every rotation is a record signed with the old key and cosigned by a witness. The **stop key** is not among them: it belongs to the human stop key holder and never lives on the organism's machines.
- **Hardware keys** (TPM, security keys) are a later option for the signing keys.

## Security

### Threat model

| Threat | Example | Main controls | Residual risk (published) |
| --- | --- | --- | --- |
| Operator alters history | Deleting an embarrassing crossing | Append-only log, consistency proofs, verifying witnesses | Events altered before their first checkpoint (window of about T) |
| Operator stops the Probe | Silence during a human intervention | Idle checkpoints, witness alerts, challenges, degraded capture | The gap is visible, its content is not |
| Compromised agent | Agent exceeds permissions or claims false autonomy | Least privilege, gate, attribution states, disputed claims | Actions outside observed systems |
| Stolen signing key | Forged checkpoints | Keys readable only by the Probe user; rotation with old key; witnesses refuse inconsistent histories | Forgery until rotation, limited by witnesses' stored state |
| Birth outside the gate | A descendant created without a human stop key holder or by a restricted parent | Verifier rejects the succession record; undeclared lineage recorded when found | Organisms created entirely outside the protocol |
| Supply chain | Malicious dependency or tampered release | Pinned hashes, SBOM, signed releases with provenance, two-person review | Compromise of an upstream maintainer before detection |
| Malicious index or witness | Hiding or inventing organisms | Open data, multiple indexes and witnesses, verifiers recompute everything | Collusion of all witnesses an organism uses |
| Privacy leak | Message contents published | Allowlisted fields, hashes only, encrypted private store | Metadata itself can reveal patterns; documented |

### Practices

- `SECURITY.md` with a private reporting channel and coordinated disclosure.
- Fail-closed gates for irreversible actions; fail-open never without a recorded reason.
- Network egress of the Probe limited to its declared sources, the Strata repository, witnesses and indexes.
- Regular review of collector permissions against the minimum in the Probe specification.

## Build and release

- Continuous integration with every third-party action pinned to a commit.
- Releases built in CI, signed, and published with build provenance (Sigstore and SLSA provenance as the target), through trusted publishing to the package registry.
- Reproducible builds as a goal, so anyone can rebuild a release and compare.
- Signed tags; every release lists its dependencies (SBOM) and its conformity results.
- Code versioned with semantic versioning, separate from the protocol release; each code release states which protocol release it implements.

## Testing

| Level | What |
| --- | --- |
| Unit and property tests | Canonicalization, hashing, tree and proofs, attribution rules |
| **Conformity vectors** | Per specification: inputs and expected outputs, published in `vectors/` so any implementation can run them (idea from NOMOS). Generated by a tool that shares no code with the verifier, with hand-written expectations and one external vector from C2SP |
| Conformity | The verifier run against vectors and against recorded logs, including births that must be refused at the gate |
| Acceptance | The cases listed in the Probe specification (canaries, voice-note directive, idle organism, frozen Probe, A2A outcome, gate refusal), and, from 2026-10-24, the reading cases below: a collector down while the Pulse answers (presence shown, coverage degraded, no autonomy inferred); a 20-second safety approval (real or declared effort recorded, no 5-minute floor presented as proven); ten corroborated and ninety unattributed actions (no extrapolation to the whole process); an altered record, invalid signature, duplicate, truncation or incompatible root (a verdict per claim, never one PASS); a publication failure or an absent witness (local record kept, age reported); a governance decision that approves A and publishes B (B unapproved); a stop during a Probe or index outage (independent technical path checked, later record documented); zero successful deliveries with failed attempts and human hours (explicit denominators, "not computable" where due, never zero cost) |
| Cross-verification | Both verifiers must agree on every vector before the first stable release of the code |
| Failure drills | Kill collectors, cut the network, rotate keys, restore from backup (recovery drill), stop drill by the human holder |

## Build order

| Milestone | Delivers | Proves |
| --- | --- | --- |
| **M0 · Format** | Evidence Format specification, JSON Schemas (record, pulse, checkpoint sidecar, trust), canonicalization and the C2SP checkpoint profile, conformity vectors, isolated Python verifier. *Delivered as a draft on 2026-10-20; the Spore, Evidence Bundle and Vital Signs schemas, with vectors, added on 2026-10-21.* The succession schema moves to the Spore specification | The evidence can be checked by someone else |
| **M1 · Log** | In Go: local store, log writer, checkpoints every N beats or T, publisher to a public repository, first witness. Priorities: durable persistence, crash recovery, resource limits, explicit gaps | History cannot be rewritten unnoticed |
| **M2 · First collectors** | GitHub and system journal; correlator with attribution states | Organism Zero's first real beats |
| **M3 · Threshold** | Sentinel collector, commands, contacts, directives followed to effects | Human decisions are visible |
| **M4 · Pulse** | Emitter, challenges with deadlines, beacon mode, Spore | Presence without trusting the operator |
| **M5 · Work units** | Business-system and A2A collectors, work units, dependency per unit | The founder's freedom becomes measurable |
| **M6 · Gate** | Host hooks and HTTP gate; allowed and refused attempts recorded | Prevention where it matters |
| **M7 · Second verifier** | Independent verifier in another language | Openness in practice |
| **M8 · Succession** | Succession records, birth-gate checks in the verifier, stop key holder credentials | The first birth in the species can pass the gate |

## Adapters for external evidence *(added 2026-10-24; after the Organism Zero pilot, never before M2)*

Systems that produce signed receipts of agent actions, hardware-attested runtime evidence or external agent identities exist (`research/related-projects.md`). The reference implementation may, later, ingest such evidence through **optional adapters**. An adapter is a collector, and its records keep: the source system and version; the source identifier; a commitment to the original artifact and where it may be fetched; the capture time and the import time, separately; the issuer's identity and verification material; the scope of what was signed; the transformations applied and what was lost; the adapter version; the agent-to-organism relation at that time; and the source's own stated limits. Privacy policy applies before anything is published: the original may stay in the private store.

What an adapter can and cannot do is stated in the evidence format (section 16, limit 8): importing, normalizing, hashing or signing an external record never strengthens the claim that record makes. An adapter declares which claims it can support ("a tool invocation was recorded") and leaves the rest UNKNOWN ("the payment settled", "no human decided"). An invalid signature is FAIL for the cryptographic claim; insufficient material is UNKNOWN. An external identity that changes owner moves no history, no conformity and no stop key. Supporting a system endorses neither its operators nor its use by other implementations, and the core format requires no blockchain, token or service provider. No compatibility is announced before vectors and a reproducible interoperability test exist, including: a valid receipt with an uncorroborated external result (integrity may pass; delivery stays unknown); the same receipt imported twice (one action, both imports traceable); a transferred external identity (no authority or favorable history inherited); an unreachable external service (the bundle reproduces the checks it has material for; the rest UNKNOWN, with no silent remote query).

## Open decisions

- Interoperability test of an Ilorium log against a real C2SP witness, and an agreement with a witness operator, before public witnesses are declared available. Check, in the same test, whether the log can also be published to or witnessed by a SCITT-style registry (the AGTP log draft and TRACE Registry use RFC 9162 with COSE receipts; `research/related-projects.md`).
- The legal name or entity for the copyright notice (now "The Ilorium Authors").
- Decided on 2026-10-21: the contributor rule is a Developer Certificate of Origin sign-off; commits by agents carry the `Signed-off-by:` of the responsible human or organization and the agent as author under its own identity (`CONTRIBUTING.md`). "The Ilorium Authors" stays, with an `AUTHORS` file.
- Governance document; until then, the founder alone merges and publishes.
- Settled: the Spore carries `stop_key_holders`, a list; Genome and Ecosystem still speak of "the stop key holder" as a role, which stays correct. Pending: what a holder's `credential` must be.
- An Evidence Bundle for part of the log (Merkle frontier), and how a bundle is packaged, before the public repository serves bundles.
- A lock file with hashes, an SBOM and continuous integration for the verifier.
- Library for the encrypted private store.
- Key custody of the Probe and the Pulse emitter: a signing daemon separate from any agent process, as Obsigna does (`research/related-projects.md`), so that code execution inside an agent cannot forge records.
- Where the index lives and in which language.
- Package name on PyPI for `ilorium` and `ilorium-*`. The GitHub organization is `ilorium-protocol`, because the `ilorium` name on GitHub is taken.

## Sources

- C2SP specifications repository, `signed-note`, `tlog-checkpoint`, `tlog-cosignature` and `tlog-witness` at v1.1.0: https://github.com/C2SP/C2SP (consulted 2026-10-20); transparency.dev witnesses (tlog-witness v0.1.0, operated by Google's TrustFabric team; participation via witness-network.org): https://transparency.dev/witnesses (consulted 2026-10-20).
- `rfc8785` Python package, version 0.1.4, packaged by Debian and Gentoo (consulted 2026-10-20).
- Ideas from related projects: see `research/related-projects.md`.
