# Ilorium Protocol Manifest

Release 1.0 · 2026-10-20 · Draft

## What this file is

This file names the documents that together make Ilorium at a given release, and which of them are the protocol itself. An implementer should be able to say "I implement Ilorium 1.0" and point here. If any other document contradicts this manifest, this manifest wins until it is corrected.

**One version of each document.** Only the current version of each document is kept. What changes between releases is recorded in `CHANGELOG.md`. When the protocol moves to its public repository, version control will keep the full history.

**Purpose.** Ilorium monitors organizations run by AI agents: it records how each one lives, measures what it has actually shown it can do, and requires that every organism carry a human stop key, tested by drills within a declared scope. Its mission is to provide laws, formats and verification for organizations run by AI agents and for the evolution of their species, setting from the first generation the conditions every birth must meet. The founder's conviction (the founder's letter, `founder-letter.md`), the project's hypotheses and what the protocol verifies today are set out, kept apart, in "Vision and evidence" in `README.md` and in the whitepaper. Those texts have no normative force; this manifest and the documents it lists do.

## Release 1.0

Release 1.0 is the **first complete version** of the protocol. It is still a **draft**: it has not been implemented end to end, its formats may change, and no organism has yet demonstrated it in operation. A release will be declared **stable** later (see Compatibility).

| Component | Document | Version | Layer |
| --- | --- | --- | --- |
| Genome | `genome/genome-v1.md` | 1.0 | Protocol |
| Governance | `governance-v1.md` | 1.0 | Protocol (who decides what, how, and how power is shared and handed over) |
| Pulse | `specs/pulse-v1.md` | 1.0 | Protocol, with reference defaults (N, T, D, K) |
| Evidence Format | `specs/evidence-format-v1.md` | 1.0 | Protocol (formats, checkpoint profile, Spore, Evidence Bundle and Vital Signs drafts, verifier behavior); machine forms in `schemas/` and `vectors/` |
| Probe | `specs/probe-v1.md` | 1.0 | Mixed; each section marked [Protocol] or [Reference] |
| Proof of Life | `specs/proof-of-life-v1.md` | 1.0 | Protocol |
| Ecosystem | `specs/ecosystem-v1.md` | 1.0 | Protocol (statuses, succession, coalescence and lineages); the web is Observatory |
| Discovery and Growth | `specs/discovery-and-growth-v1.md` | 1.0 | Spore fields and the A2A extension are protocol; the rest is Observatory and Organism Zero |
| Glossary | `glossary.md` | 1.0 | Protocol (shared language) |

**Licenses.** Normative text (these documents): CC BY 4.0. Code, JSON Schemas, conformity vectors and examples: Apache-2.0, so they can be embedded in any implementation. Contributors keep their copyright and license each contribution under the license of the file they change.

The whitepaper (`whitepaper-v1.md`) explains the whole project and has no normative force. The architecture document (`engineering/architecture-v1.md`), the related-projects register and the brand identity (`brand/brand-identity-v1.md`) are not part of the protocol. Spanish files (`.es.md`) are working translations of the same versions; if they differ, the English version prevails.

## Three layers

| Layer | What it is | Who it binds |
| --- | --- | --- |
| **Protocol** | Formats, meanings, requirements and conformity tests | Every organism and every implementation |
| **Reference implementation** | The Probe, the Pulse emitter and their defaults | No one. Replaceable by any implementation that produces conforming evidence |
| **Organism Zero** | The founder's organism: architecture, roles, tools and choices | Only Organism Zero. A declared pilot, never an independent validation of Ilorium |

### Where each item belongs

| Item | Layer | Required for conformity? |
| --- | --- | --- |
| The seven laws, conformity statuses, amendment by IIP | Protocol | Yes |
| The three locks: germline, birth gate, stop | Protocol | Yes |
| Governance: roles, the IIP process, Custodians, Wardens' qualification and payment, funding rules, what an AI may do | Protocol | Binds whoever governs the protocol; it decides no organism's conformity |
| Record types (observation with `event` and `outcome`, claim, evaluation with `work_unit`), attribution states, crossing types | Protocol | Yes |
| Four coverage measures, freshness, and the claim template | Protocol | Yes |
| Ilorium JSON (restricted RFC 8785), RFC 6962 tree with RFC 9162 proofs, C2SP signed-note checkpoints with a signed sidecar, signed every N beats or every T, a verifying witness quorum, verdicts PASS, FAIL and UNKNOWN | Protocol | Yes (Evidence Format) |
| JSON Schemas and conformity vectors | Protocol | Yes: an implementation claims conformity by passing the vectors of the release |
| Isolated reference verifier (`ilorium-verifier`, Python) | Reference implementation | No; any verifier that passes the vectors is equal |
| Spore at `/.well-known/ilorium.json` and its fields | Protocol | Yes (fields still draft) |
| Pulse format, interval pulses, challenges with deadlines, states of being, recovery axis, kin links and what passes through them | Protocol | Yes |
| Succession record, succession types (`founded`, `inherited`, `coalesced`), generation, the birth gate, and what passes and never passes to a descendant | Protocol | Yes, for any organism originated by another (record format still draft) |
| A human stop key holder for every organism; Wardens for lineages without human founders | Protocol | Yes |
| Proof of Life dimensions, work units; autogenesis and full observed autonomy shown as separate results, never as a composite status | Protocol | Yes |
| A single declared directive channel, every human message recorded, directives told apart from contacts, directives followed to their effect | Protocol | Yes |
| Agents never use a human identity and always identify as AI (Law 5) | Protocol | Yes |
| The Ilorium A2A extension (`https://ilorium.com/ext/a2a/v1`) | Protocol | Optional |
| Authorization gate | Protocol (optional) | No; ungated paths are declared in claims |
| SI2SI, SI → SI and SI + SI → SI′ | Horizon (glossary, Ecosystem, README, whitepaper) | No. Not a requirement, status or criterion |
| Threshold on Telegram, the Sentinel bot, the commands `/do`, `/approve`, `/stop`, `/governance`, `/test` | Reference implementation | No |
| Collectors for GitHub, Workspace, Gmail, a Linux server, A2A middleware; the `ilorium` command | Reference implementation | No |
| Defaults: N = 64 beats, T = 15 minutes, D = 10 minutes, K = 3 | Reference implementation | No; declared in the Spore when changed |
| Six agent roles, `OZ-…` names, temperaments | Organism Zero | No |
| Google Workspace, Organism Zero's agents and mailboxes on ilorium.com, a shared server, the Observatory as first product | Organism Zero | No |
| ilorium.com as the protocol's site and first index | Observatory | No |
| The index, the Codex, the Radiant and the web statuses as displayed | Observatory | No. Anyone can run an index or a different view on the same evidence |

**Known debt.** The evidence format is now its own document with conformity vectors, and the Probe document points to it; the Probe document still mixes protocol and reference sections, which remain marked. The Spore has a draft schema in the Evidence Format (with `stop_key_holders`), but the succession record, kin links and `partners` still need a single format in a Spore specification; the Evidence Bundle and Vital Signs are defined as drafts, and a bundle for part of the log is not. Public-witness integration is not available until an interoperability test and an agreement with a witness operator exist.

## Compatibility

- **1.0 is complete, not stable.** Until a release is declared stable, formats may still change; every change is recorded in the changelog and no compatibility is promised between drafts.
- **Stable will mean** (this is the normative definition; every other document points here): frozen formats, published conformity tests, a written compatibility policy and at least two independent Genome Custodians in office; and it is never declared during interim governance or restricted maintenance (Governance, section 8). Stable is a statement about formats and governance, not about operation: the founder's plan sequences other facts before it (Organism Zero beating, external adoption), and those are his plan, not conditions of this definition. Being stable says nothing about whether any organism can be trusted.
- **After a release is declared stable:** changes within its major version are additive; anything that breaks existing evidence or validators is a new major version.
- **Declared release.** Every Spore declares the release it implements (`"ilorium": "1.0"`).
- **Proof of openness.** The protocol is open in practice when someone builds a second implementation without the founder's help and both validators reach the same results on the same evidence.

## Who publishes this file

The governance document (`governance-v1.md`) says who. During **interim governance**, the founder alone publishes releases and says so in the changelog. Under **full governance**, two Genome Custodians. Interim governance ends when the council of Custodians is constituted; the founder's unilateral authority ends at the latest 18 months after the public repository is published, whether or not the council is complete (Governance, section 8, revised 2026-10-22 and provisional until IIP-0004 closes). No Genome Custodians have been appointed yet; the Genome and this release stay drafts until two independent Custodians are in office, and stable cannot be declared during interim governance.
