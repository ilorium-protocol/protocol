# Related Projects

Living document · 2026-10-20 · Revised 2026-10-24 · Not part of the protocol

## Why this file exists

Many projects near Ilorium will appear: agent protocols, policy languages, registries, certification schemes, verifiable logs. This register records each one we find, so Ilorium can take ideas, concepts and code from them, give credit, avoid rebuilding what exists, and stay clear about what makes it different.

Every entry is dated and sourced. Facts about a project are kept apart from our judgment about it. Before copying any code, check that project's license for its code, which may differ from the license of its specification, and keep its notices. New entries are added here without a changelog entry; when an idea is applied to a specification, that change goes to the changelog.

## Where Ilorium stands apart

Similar projects mostly build tools: a way for agents to talk, a way to encode rules, a way to certify, a way to govern one task. Ilorium is a different kind of idea:

| Most related projects | Ilorium |
| --- | --- |
| A tool or a standard | A species of organisms that are born, diverge, inherit, rest, coalesce and are chronicled, with nothing erased |
| Certify, score or govern one task | Measure how much human life an organization still consumes per thing it delivers, and show it in public, without seals |
| One system, one owner | Lineages, a network of ancestry, and a Commons where organisms trade and link their chains |
| Govern what an agent may do now | Govern how the species evolves: what every generation inherits, who may originate whom (the birth gate), and that every organism is born stoppable by a human |
| Capability as a feature | SI2SI as the horizon: superintelligences originating superintelligences, under the same rules as the first birth in the species |
| Documentation | A story: the Codex, the Radiant, the Vault, the Wardens, Organism Zero's Threshold going quiet |

**The rule that keeps this credible:** the story and the horizon live in the narrative layer (Codex, Radiant, brand, website). The method stays literal: evidence, scope, freshness, limitations. Fantasy is how Ilorium is told; it is never what Ilorium claims.

## Ideas queue

Ideas taken from the entries below, waiting to be applied. Each names where it would go.

| Idea | From | Goes to |
| --- | --- | --- |
| Bind a human approval to the digest of the exact action | NOMOS (SPEC-008) | Probe specification, authorization gate; stop key holder acceptance of a newborn's key |
| Declare how each limit is enforced: permission, gate, host hook, or only the agent's word | Signet (`enforced_by`) | Probe specification, claim template; Genome Law 2 tests |
| Host hooks as a reference gate: compile an agent's limits into a pre-tool-call hook that denies forbidden calls | Signet (`signet hook init`) | Probe specification, reference implementation for agents on hook-capable hosts |
| Verifier isolated from the runtime, auditable on its own | Signet (`src/verify.ts`) | Architecture document: evidence format, Probe, and an independent verifier |
| Structured task contract for directives: scope, limits, gates, evidence, completion criteria | Signet (packet) | Threshold `/do` directives and work-unit success criteria |
| Three-valued verdict: undecided is neither pass nor fail | NOMOS (`INCOMPLETE`), Signet (`UNEVALUATED`) | Conformity tests and claim template |
| Published test vectors per specification | NOMOS | Conformity tests |
| Revocation lists and `max_age` | NOMOS (SPEC-006) | Spore key rotation; Wardens' credentials |
| Receiver-attested receipts as a source for the `corroborated` attribution state and for counterpart confirmation of work units | Notarized Agents / Sello | Probe specification (attribution), Proof of Life (work units), adapters (architecture) |
| Signing key held by a separate daemon, never in the agent process | Obsigna, AEVS (KMS) | Probe, Pulse emitter: key custody of the reference implementation |
| Hardware-attested runtime evidence as an optional source for "where it ran" and "which policy was enforced" | TRACE (Linux Foundation) | Adapters (architecture); coverage measures |
| Admission rule for imported evidence: provenance, original material, transformations, declared claims, UNKNOWN for the rest | Sixth outside review (2026-10-24) | Architecture (adapters), evidence format (limits) |

## How to add an entry

Use the template at the end. Status: `watch` (keep an eye on it), `borrow` (take ideas or code), `build on` (Ilorium depends on it), `discard` (not useful, with the reason).

---

## A2A (Agent2Agent Protocol)

- **Found:** 2026-10-20 · **Status:** build on
- **What it is (facts):** Open protocol for communication between AI agents. Originated by Google, hosted by the Linux Foundation. Version 1.0 is its first stable specification; more than 150 supporting organizations as of April 2026. Agent Cards at `/.well-known/agent-card.json`, skills, security schemes, signed cards (JWS over RFC 8785), extensions declared by URI and activated with the `A2A-Extensions` header, task states.
- **Relation to Ilorium:** The layer below. A2A says what an agent can do; Ilorium shows how the organism behind it lives.
- **Taken:** Agent Cards replace Ilorium's own offers; the draft Ilorium A2A extension; task terminal states as work units; signing pattern for the Spore (Discovery and Growth, Probe, Proof of Life).
- **Not taken:** A2A's registries; Ilorium's index covers organisms, not agents.
- **Sources:** https://a2a-protocol.org/ ; https://a2a-protocol.org/latest/topics/extensions/ ; Linux Foundation press release, 2026-04-09.

## Signet (`azel-asl/signet`)

- **Found:** 2026-10-20 (suggested by the founder) · **Status:** borrow
- **What it is (facts):** "Governance by contract, enforcement by hook (on hook-capable hosts), and verification by receipt" for AI agent work. A **packet** (format "ASL Lite + GCL") declares a task's scope, locks (forbidden actions), gates (human approvals required before execution), evidence and completion rules. Flow: intent → packet → parse → verify → approve → run → receipt. Verdicts PASS, FAIL, BLOCKED and UNEVALUATED (a check that cannot be verified mechanically is never passed). `signet hook init` compiles locks into a PreToolUse hook that denies forbidden tool calls on hosts such as Claude Code. Receipts carry two hashes under its XAS-CANON-1 canonicalization: `sha256` over the bytes and `h10` over the semantic core; receipts in the open repository are unsigned. The verifier does not import the runtime. TypeScript, Node 22.5 or later; 232 tests. Code under Apache 2.0, specifications under CC BY 4.0; Ed25519 signing and approval issuance ("Signet Authority") are closed and operated by ASL Labs. Author: Erwin Layaoen, ASL Labs. At the time of review: 3 commits, 0 stars, 0 forks, no npm package, no visible dates.
- **States its own limits:** not an OS sandbox; no inspection of file contents or network traffic; agents on hosts without hooks are not constrained; the enforcement journal records denials only; the runtime "governs declared intent, not live behavior"; a receipt proves the record was not modified, not that the work was done or correct.
- **Relation to Ilorium:** Adjacent. Signet governs one task before and during execution; Ilorium observes a whole organism over its life and governs how the species reproduces. Signet's hooks and packets could sit inside an organism as its gates and its directive contracts, and Ilorium's Probe would record what they allowed and denied.
- **Ideas to take:** see the ideas queue above: honest enforcement labels (`enforced_by`), host hooks as a reference gate, an isolated verifier, task contracts for directives, the UNEVALUATED verdict.
- **Code reuse:** the parser, validator, verifier, canonicalization and hook compiler are Apache 2.0, so they can be reused with attribution and its `NOTICE` kept. Check the `LICENSE` and `NOTICE` files before copying.
- **Not to take:** a closed authority for signatures and approvals (an open protocol cannot depend on a trust root one company controls; Ilorium anchors keys in the Strata with a witness); unsigned receipts with no transparency log; a journal that records only denials (Ilorium's gate records allowed and refused attempts).
- **Limits of this review:** based on the repository page and README; the specification files were not read one by one.
- **Sources:** https://github.com/azel-asl/signet ; https://raw.githubusercontent.com/azel-asl/signet/main/README.md (consulted 2026-10-20).

## NOMOS Protocol (`nomos-spec/spec`)

- **Found:** 2026-10-20 (suggested by an external review) · **Status:** borrow
- **What it is (facts):** "Open protocol and reference implementation for machine-executable governance artifacts." Turns institutional policy into signed `.nomos` JSON files that any runtime can evaluate deterministically, without calling an AI model at runtime. Eight specifications (001 to 008; 005, 007 and 008 in draft): core rules and sealing; multi-agent manifest with permissions, `cannot_call` and constraints; temporal validity and staleness; composition and third-party attestation; public queries; revocation; chain-of-trust key certificates; Act Binding. Ed25519 seals, verifiable offline. Reference verifiers in Python and TypeScript, CLI, test vectors. Specification and schemas under CC BY 4.0; "implementations may be proprietary." At the time of review: 0 stars, 1 fork, no releases, no visible dates, one listed contact (nomosprotocol.com). Does not mention A2A.
- **Relation to Ilorium:** Adjacent, not overlapping. NOMOS answers "may I do this?" before an action; Ilorium answers "what happened, who did it, who decided it, how much human life did it take?" after, and "may this organism give rise to another?" at every birth. An organism's limits (Law 2) and gates (Law 7) could be expressed as `.nomos` artifacts.
- **Ideas to take:** consent bound to the exact action (SPEC-008); three-valued verdict (`INCOMPLETE`); agents manifest with `cannot_call`; revocation lists and `max_age`; test vectors per specification. See the ideas queue.
- **Not to take:** confidence tiers (DECLARED to SOVEREIGN) tied to a score, "ARI", that the README does not define and writes on two incompatible scales (0.60 and 60); listing in a commercial exchange tied to a tier.
- **Code reuse:** check the code license before copying; only the specification's license is stated.
- **Limits of this review:** based on the README and the website; the specification files could not be read directly.
- **Sources:** https://github.com/nomos-spec/spec ; https://nomosprotocol.com (consulted 2026-10-20).

## ERC-8004 (Trustless Agents)

- **Found:** 2026-10-19 · **Updated:** 2026-10-24 · **Status:** watch
- **What it is (facts):** Ethereum proposal "Trustless Agents", Standards Track, status Draft, created 2025-08-13 (De Rossi, Crapis, Ellis, Reppel). Three registries: identity (an ERC-721 token per agent, with an `agentURI` to a registration file), reputation (signed feedback values with decimals and tags, aggregated mostly off-chain) and validation (a designated validator posts a 0–100 response; stake, zkML or TEE validators are examples outside the registry). Identities are **transferable** tokens; the agent wallet is cleared on transfer. The text says it "cannot cryptographically guarantee that advertised capabilities are functional and non-malicious" and that Sybil inflation of reputation is possible.
- **Relation to Ilorium:** Agent identity and reputation, on-chain; Ilorium is organism identity and evidence, off-chain. An ERC-8004 identity could be linked from a Spore as an optional, dated external reference with a proof of control; a transfer of that token would move no history, no conformity and no stop key of the organism. A source of candidates, never of members.
- **Not to take:** reputation scores as evidence; on-chain registration as a requirement of the core.
- **Sources:** https://eips.ethereum.org/EIPS/eip-8004 (consulted 2026-10-19 and 2026-10-24).

## AEVS (Fetch.ai Agent Execution Verification System)

- **Found:** 2026-10-24 (suggested by the sixth outside review) · **Status:** watch
- **What it is (facts):** "Transparent audit SDK for AI agents" by Fetch.ai: intercepts tool calls in LangChain/LangGraph and MCP, builds hash-chained receipts signed with HMAC-SHA256 (v1 keys) or ECDSA P-256 (v2 keys), and sends them to an AEVS backend where a cloud HSM key signs each ingested receipt. Visibility modes `public`, `private` and `proof_only` (inputs and outputs replaced by hashes). Apache-2.0. At the time of review: 104 stars, no release listed, no dates shown. Its own security document says it is "tamper-evident, not tamper-proof" ("a fully compromised host process could skip creating receipts entirely") and that a receipt "does not independently verify that the tool actually performed the action".
- **Relation to Ilorium:** A receipt is an observation of a tool call from inside the agent's process, signed by the agent's own side and by the vendor's backend. It could feed the Probe through an adapter as evidence that a call was recorded; it says nothing about who decided, whether the external effect happened, or what was omitted. Verification depends on the vendor's backend unless the signed bytes and keys are exportable; that is to be checked before any adapter.
- **Not to take:** a dependency on one vendor's backend as a root of trust.
- **Limits of this review:** README and security document only; no code run, no receipt verified offline.
- **Sources:** https://github.com/fetchai/AEVS-sdk ; https://github.com/fetchai/AEVS-sdk/blob/main/docs/07-security-and-privacy.md (consulted 2026-10-24).

## TRACE and AgenTrust (Linux Foundation)

- **Found:** 2026-10-24 · **Status:** watch
- **What it is (facts):** TRACE ("Trust, Runtime Attestation and Compliance Evidence") is a specification for hardware-attested runtime and compliance evidence for AI agents and confidential workloads, contributed by OPAQUE and developed with AMD, Intel, Microsoft and TII; the Linux Foundation announced its stewardship on 2026-08-25 (first shown June 2026). It builds on RATS, EAT, SLSA, SCITT, SPIFFE and EAR. AgenTrust is the open ecosystem around it: TRACE receipts (spec v0.2), a TRACE Registry (public log with signed checkpoints), an Agent Manifest, cMCP and cA2A policy checks, a Weight Custody Manifest; most components pre-1.0. The site states: a signature shows who signed and that nothing changed, not where it was produced; a registry entry shows a receipt was published, not that its contents are true.
- **Relation to Ilorium:** The most institutional neighbor. TRACE answers "where did this run and which policy was enforced", with hardware roots; Ilorium answers "how does this organization live, how much human life does it consume, may it originate another". A TRACE artifact could be an optional source for coverage and control through an adapter. Its registry with signed checkpoints is close to the Strata; worth testing whether an Ilorium log can be witnessed by, or published to, such a registry.
- **Limits of this review:** press release and project site; specification not read.
- **Sources:** https://www.linuxfoundation.org/press/linux-foundation-welcomes-trace-to-advance-verifiable-runtime-evidence-for-ai-workloads ; https://agentrust-io.com/ (consulted 2026-10-24).

## Agent Receipts / Obsigna

- **Found:** 2026-10-24 · **Status:** borrow
- **What it is (facts):** "An open protocol for producing cryptographically signed, tamper-evident records of AI agent actions": receipt format, Ed25519 signing, hash chain with sequence and `previous_receipt_hash`, action-type taxonomy; Obsigna is the reference toolset (MCP proxy, a signing daemon that holds the key out of the agent process, a Claude Code hook, CLI, SDKs in Go, TypeScript and Python), with a cross-language conformance suite and a bounded formal model. Code Apache-2.0, specification MIT. At the time of review: 20 stars, about 1,300 commits, no release listed. States its limits: a key inside the agent process can be forged by anyone with code execution there; the conformance suite catches serialization drift, not interpretation; the Byzantine key holder is "the boundary, not covered".
- **Relation to Ilorium:** The closest open design to the Probe's record of tool calls. Its out-of-process signing daemon is the right custody model for the reference Probe and Pulse emitter.
- **Ideas to take:** key custody in a separate daemon; a conformance suite across languages (Ilorium's M7 second verifier).
- **Sources:** https://github.com/agent-receipts/obsigna ; https://agentreceipts.ai/ (consulted 2026-10-24).

## Notarized Agents / Sello (research)

- **Found:** 2026-10-24 · **Status:** borrow
- **What it is (facts):** arXiv 2606.04193 (Juan Figuera, 2026-06-02): "receiver-attested confidential receipts". The service that receives an agent's call signs a receipt of what it observed with its own key, encrypts it to the agent owner's key and publishes it to a witness-cosigned Merkle log, so the owner can reconstruct the agent's activity without trusting the agent or its operator. Named limits: suppression (a receiver may omit), colluding receivers, adoption incentives.
- **Relation to Ilorium:** Exactly the `corroborated` attribution state and the counterpart confirmation of work units: evidence signed by the other side of an action. The adoption problem is the same one Ilorium faces with witnesses and Oracles.
- **Sources:** https://arxiv.org/abs/2606.04193 (consulted 2026-10-24).

## AGTP Transparency Log (Internet-Draft)

- **Found:** 2026-10-24 · **Status:** watch
- **What it is (facts):** `draft-hood-agtp-log` (Chris Hood, Nomotic; independent submission, not endorsed by the IETF; version 01 of 2026-05-20): a transparency log for agent identity lifecycle events (genesis issued, revoked, suspended, reinstated, deprecated), built on RFC 9162 and SCITT (RFC 9943) with COSE receipts. Single-issuer model; witnesses and monitors deferred.
- **Relation to Ilorium:** Overlaps with the Strata's role for lifecycle facts, at the level of agents rather than organisms. Confirms that RFC 9162-style logs with SCITT receipts are where the field is going; Ilorium's C2SP choice should be checked for interoperability with SCITT receipts before M1 closes.
- **Sources:** https://datatracker.ietf.org/doc/html/draft-hood-agtp-log-01 (consulted 2026-10-24).

## Andon Labs (AI-run businesses in the real world)

- **Found:** 2026-10-24 · **Status:** watch (candidate organisms)
- **What it is (facts):** A company that deploys AI in real settings to study it: Andon Market (a retail store in San Francisco described as fully AI-run), Andon Café (Stockholm), Andon FM (agent-run radio stations), Vending-Bench (benchmarks of agents running vending businesses) and Pion (a platform for agent-run businesses, in waitlist). Project Vend was run with Anthropic. Its site publishes no human-intervention figures and states that "safety from humans in the loop is a mirage".
- **Relation to Ilorium:** The first real organizations that look like organisms. They are Sightings until a Spore and evidence exist. They are also the test of whether a counterparty wants what Ilorium shows: how much human work stands behind an "AI-run" store.
- **Sources:** https://andonlabs.com/ (consulted 2026-10-24).

## The field of agent receipts (note, 2026-10-24)

A public competitor map (`JaredKlopstein/provenant`, issue 6, consulted 2026-10-24) lists more than twenty projects producing signed, hash-chained receipts of agent actions, open and commercial: among them protect-mcp, agent-custody, veritrail, halo-record, agent-receipt, AgentMint, Pipelock, Quox, ProofAgent, CertNode, Asqav, ProofTrail, TrustNotch, Cloak, and three Internet-Drafts (`draft-sahu-agent-action-receipts`, `draft-farley-acta-signed-receipts`, `draft-marques-asqav-compliance-receipts`). None was reviewed one by one here. Two conclusions for Ilorium: the evidence layer (records, Merkle log, checkpoints, witnesses) is comparable to many of these and is not where Ilorium is different; and no project found measures an organization (human time per work unit, coverage, rescue rate), governs births or defines guardianship. That is a statement about this search on this date, not a claim that nothing else exists.

## Darwin Gödel Machine

- **Found:** 2026-10-20 (cited by an external review) · **Status:** watch
- **What it is (facts):** Research on agents that modify their own code and keep an archive of variants, with measured gains on programming tasks, run with foundation models, sandboxing and human oversight.
- **Relation to Ilorium:** Evidence that agent evolution can be studied; not evidence that a species of organizations leads to superintelligence. Model for the research program on the horizon: same base model and budget, fixed vs. human-improved vs. system-selected variants, new tasks.
- **Sources:** https://arxiv.org/abs/2505.22954

## Project Vend (Anthropic)

- **Found:** 2026-10-20 (cited by an external review) · **Status:** watch
- **What it is (facts):** Anthropic's experiment running a small shop with an AI agent; performance improved with better models, tools and procedures, while human support and vulnerabilities to adversarial interactions were documented.
- **Relation to Ilorium:** A business can improve and still depend on human rescues. Ilorium's rescue rate and dependency per work unit exist to tell those two apart.
- **Sources:** https://www.anthropic.com/research/project-vend-2

---

## Template

```
## <Project name>

- **Found:** <date> · **Status:** watch | borrow | build on | discard
- **What it is (facts):** <what it says it is, version, license, maturity>
- **Relation to Ilorium:** <overlap, complement, or none>
- **Ideas to take:** <add them to the ideas queue, each with where it would go>
- **Not to take:** <and why>
- **Code reuse:** <license of the code, notices to keep>
- **Sources:** <links, consulted date>
```
