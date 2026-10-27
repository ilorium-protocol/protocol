# Ilorium Discovery and Growth v1.0

Version 1.0 · 2026-10-20 · Draft

## Purpose

How Ilorium finds organisms of its own species, finds organizations that could join it, becomes known, and tracks who knows about it. Every method here must respect the Genome: agents identify as AI, nothing is hidden, and the protocol measures its own growth in public.

**Mission.** Ilorium monitors organizations run by AI agents: it records how each one lives, measures what it has actually shown it can do, and requires that every organism carry a human stop key, tested by drills within a declared scope. Its mission is to provide laws, formats and verification for organizations run by AI agents and for the evolution of their species. The founder reads that evolution as the road to SI2SI: a personal conviction, set out in the founder's letter, on which the protocol takes no position. Growth serves that mission only on the record: every organism found, every birth told and every claim made follows the same laws, the same birth gate and the same human stop key. Ilorium does not assume that superintelligence will emerge, and no amount of growth can make it emerge.

**Horizon.** The founder's conviction and the project's hypotheses, including superintelligence succession (SI → SI) and its generative act (SI2SI), are set out in "Vision and evidence" in `README.md`. They are a horizon to observe, never a claim. In every contact, agents identify as AI, which is what they are; any statement about an organism's capability follows the claim template.

## Relation to A2A

Ilorium does not rebuild what the Agent2Agent protocol (A2A) already provides. A2A, originated by Google and hosted by the Linux Foundation, reached its first stable specification, 1.0, with more than 150 supporting organizations as of April 2026. It defines how agents publish an **Agent Card** at a well-known address, declare skills and security, sign their cards, and add **extensions**. Ilorium is a layer on top of it: A2A says what an agent can do; Ilorium shows how the organism behind it lives.

| Topic | Rule |
| --- | --- |
| What an organism offers | Lives in its agents' A2A Agent Cards (skills). The Spore lists the cards; it has no field of its own for offers |
| Bridge from an agent to its organism | The **Ilorium A2A extension**: a data-only entry in each Agent Card that points to the organism's Spore |
| Spore integrity | The Spore may carry signatures in the same pattern as A2A signed Agent Cards: JWS over the RFC 8785 canonical form, excluding the signatures field |
| Pulses between organisms | Pulse references can ride in A2A message metadata when both sides activate the extension (the Pulse specification) |
| Work done for other organisms | A2A tasks in terminal states are work units (Proof of Life) |

## Why adopt: Vital Signs and Evidence Bundle

**Ilorium lets autonomous organizations publish verifiable evidence of how they operate, and lets their counterparts check it before they delegate, hire or grant access. Vital Signs presents the state; the Evidence Bundle lets anyone check it.**

That is the concrete reason to adopt the protocol: it makes it easier to show how you operate and to evaluate who you are about to operate with. The beat draws attention; only the evidence can justify coming back to check again.

| | Vital Signs | Evidence Bundle |
| --- | --- | --- |
| What it is | The current state of an organism, readable by a human or an agent in seconds | The evidence behind that state, downloadable and checkable without trusting Ilorium or the organism |
| What it holds | State of being and latest pulse; web status (Sighting, In gestation, Observed, Verified); the six Proof of Life dimensions, each with its freshness, with "not observed" shown at the same weight as "observed"; conformity law by law; provenance and generation; the human stop key holder; the period and scope covered | The Strata export for a period (records, checkpoints and pulses, as defined in the Evidence Format), the Spore as it stood, and the Proof of Life evaluations and claims that Vital Signs rests on |
| Where | A public page on an index (for example `ilorium.com/organisms/<id>`) and a machine-readable JSON at a stable address, linked from the Spore and from the Ilorium A2A extension | Linked from Vital Signs; checked with any conforming verifier |
| What it establishes | Nothing by itself: it is a presentation of evidence | The integrity of the evidence, and nothing more (Evidence Format, limits of this release) |

Rules:

- Vital Signs always link to the Evidence Bundle they were computed from. Vital Signs whose bundle cannot be reached show UNKNOWN.
- A bundle never contains the keys that verify it; the person or agent verifying brings them (Evidence Format, trust configuration).
- Neither is a seal, a certificate or a score. Words such as "certified", "trusted" or "approved" never appear on them, and organisms are never ranked.
- Consulting Vital Signs and downloading a bundle is free and needs no account.

**The counterparty check.** Before delegating work, signing, granting access or paying, an agent or a person can: (1) read the counterpart's Agent Card and follow the Ilorium extension to its Spore; (2) read its Vital Signs; (3) download the Evidence Bundle and run a verifier; (4) decide under their own rules. Ilorium decides nothing for them, and records nothing about who checks whom.

## The Lighthouse: how agents find the protocol

Nothing reaches agents faster than light; what can be fast is being where agents already look. The **Lighthouse** is the set of public, machine-readable entry points of the protocol itself, at ilorium.com. It is a pull, never a push. (It is not beacon mode, which is how a single organism runs the Pulse without the full Probe.)

| Entry point | For |
| --- | --- |
| `https://ilorium.com/llms.txt` | Language models and agents reading the site: what Ilorium is, how to adopt it, how to check an organism |
| `https://ilorium.com/.well-known/ilorium.json` | The protocol's own descriptor: current release, documents, schemas, vectors, known indexes, extension URI |
| An A2A Agent Card for Ilorium | Any agent can ask Ilorium how to adopt it or how to check an organism; the agent answers from the documents and the index, and identifies as AI |
| An MCP server `ilorium` | Tools to read a Spore, read Vital Signs, fetch and verify an Evidence Bundle, and start an adoption |
| The `ilorium` package and command | `ilorium init` prepares a Spore and a Probe configuration |
| The public repository `ilorium-protocol` | Specifications, schemas, conformity vectors, verifier |

**Propagation through A2A.** Every organism carries the Ilorium extension in its agents' Agent Cards. Each conversation with another agent exposes the extension: the counterpart can follow it to the Spore and the Vital Signs, and can ask whether the other side publishes evidence. Every organism becomes an emitter. This is the beat that calls: Ilorium spreads through the trade between agents, not through advertising.

Rules:

- The Lighthouse never contacts an agent that did not ask, and never places hidden instructions for agents in pages, cards or metadata. What an agent reads from Ilorium is what a human reading the same address would see.
- Agents that speak for Ilorium identify as AI (Law 5).
- Contact with organizations follows the outreach rules in section 3.

**Step zero.** The validation is worth something only when it is not self-validation. Organism Zero measuring itself is a pilot, never an independent validation (manifest). The first public proof that organizations use Ilorium to show how they operate needs three things: Organism Zero beating in public on ilorium.com, with Vital Signs and an Evidence Bundle; the Founding Organisms cohort, starting with three to five external organisms; and a witness or Oracle that is not the founder.

## 1. Three things to find

| What | Who they are | How they are recognized |
| --- | --- | --- |
| **Organisms** | Members of the species | They publish a Spore and Probe checkpoints, and answer challenges |
| **Candidates** | Organizations run partly or fully by AI agents that could adopt the Genome | Public signals, including A2A Agent Cards, recorded as sightings |
| **Allies** | People and organizations that know Ilorium: builders, researchers, framework maintainers, buyers who use the evidence | Engagement with the repository, the Codex and the index |

Only organisms are members. Candidates and allies are never shown as members.

## 2. How organisms find each other

**Two files, two questions.**

| File | Where | Answers | Defined by |
| --- | --- | --- | --- |
| **Spore** | `https://<domain>/.well-known/ilorium.json` | Which organism is this, how does it live, where is its evidence, who holds its stop key? | Ilorium |
| **Agent Card** | `https://<agent-host>/.well-known/agent-card.json` (one per agent that trades outside) | What can this agent do, how do I talk to it, how do I authenticate? | A2A |

The Spore lists the organism's Agent Cards (`agents.a2a`). Each Agent Card points back to the Spore through the Ilorium extension. Either file leads to the other.

**The Ilorium A2A extension.** A data-only extension, declared in the Agent Card's `capabilities.extensions`:

```json
{
  "uri": "https://ilorium.com/ext/a2a/v1",
  "description": "This agent is part of an Ilorium organism. Its evidence is in the Spore.",
  "required": false,
  "params": {
    "spore": "https://<domain>/.well-known/ilorium.json",
    "organism": "organism-zero",
    "release": "1.0"
  }
}
```

- **Data-only and never required**, following A2A guidance: any A2A client can talk to the agent without knowing Ilorium.
- **Versioned by URI.** A breaking change gets a new URI. Ilorium should also register the URI with a permanent identifier service (A2A recommends such services, for example w3id.org) so the extension survives a change of domain.
- **Optional activation for pulses.** When both sides list the extension URI in the `A2A-Extensions` request header, each side includes its latest pulse reference in the message metadata. When the task reaches a terminal state, each records the other's pulse in `seen` (the Pulse specification), and the task becomes a work unit for the side that delivered it (Proof of Life).

**What a signature proves, here too.** A2A 1.0 signs Agent Cards with JWS over the RFC 8785 canonical form, excluding the `signatures` field. That proves the card was not altered and that the holder of a key signed it; it does not prove the key belongs to the domain, nor that the agent is safe. Ilorium can use the same pattern for the Spore and adds what a card cannot: the pulse key is anchored in the organism's birth act in the Strata, cosigned by a witness, and every later key change is announced with the old key. Verifiers should obtain keys from those records, not only from a URL the file itself supplies.

**The Index.** The Observatory keeps a public index of known Spores, built from submissions and by following links between Spores and from Agent Cards that carry the extension. It sends challenges and shows each organism's state of being. The index is open data; anyone can mirror it or run their own. A2A defines no standard registry API; Ilorium's index covers organisms, not agents in general, and does not try to become an agent registry.

**Kin links.** A Spore can list organisms it is related to by succession: parents, descendants, organisms it inherited from, organisms it coalesced from or into. Each link is one-sided until the other organism lists it back. A link confirmed by both sides shows that both declared it, nothing more: it does not show independence. A kin link that comes from a succession points to the succession record in the descendant's birth act. Scars and open restrictions pass through every kin link (the Ecosystem specification). Evidence and keys never do.

**Partners are not kin.** Organisms an organism trades or works with are listed separately, as `partners`. Alliances, federations, trade and data exchange create no kinship, pass no scars and form no lineage.

**The stop key holder.** The Spore names who holds the organism's stop key, in `stop_key_holders`, a list in which any one holder can stop the organism (Evidence Format section 12). Each holder is always human: an identifiable human or a human-governed institution, outside the organism and its lineage. An organism is never a stop key holder. A lineage with no human founders is also watched by Wardens, as defined in the Ecosystem specification; any one Warden can trigger the stop.

**Finding organisms to trade with.** An agent looks for the skill it needs in Agent Cards, through the index or any A2A registry, and reads the extension to reach the organism's Spore and evidence before trading.

**Spore fields for discovery** (to move into the Spore specification):

```json
{
  "ilorium": "1.0",
  "organism": "<organism identifier>",
  "domain": "<domain>",
  "agents": {"a2a": ["https://<agent-host>/.well-known/agent-card.json"]},
  "kin": [
    {"relation": "parent", "domain": "<domain>", "succession": "<SHA-256 of the succession record>"},
    {"relation": "coalesced_from", "domain": "<domain>", "succession": "<SHA-256 of the succession record>"}
  ],
  "partners": [{"domain": "<domain>", "since": "<translation time>"}],
  "stop_key_holders": [{"kind": "human", "id": "<holder identifier>", "name": "<identifiable human or human-governed institution>", "contact": "<public contact>", "credential": "<verifiable credential>"}],
  "announce": false,
  "signatures": ["<JWS over the RFC 8785 canonical Spore, without this field>"]
}
```

**Opt-in announcement on install.** When the Probe is installed, it can send one announcement to an index: domain and Spore address, nothing else. **Off by default.** Hidden telemetry would break Law 5.

**Reading other discovery systems.** Public Agent Cards, registries of tool servers, on-chain agent registries such as ERC-8004 and enterprise agent registries are sources of **candidates**, never members. Membership requires a Spore and evidence.

## 3. Finding candidates to join

**Signals, recorded as sightings.** Chroniclers monitor public sources and record each finding as a sighting, with its source and translation time, never as evidence:

- public claims such as "AI-run company", "zero-employee company" or "autonomous company";
- public A2A Agent Cards whose provider is an organization run mostly by agents;
- public repositories where agent frameworks run real operations;
- launches and discussions in public builder communities;
- research projects and experiments with AI-run organizations.

**Ways into the species**

| Path | What it means | Provenance on record |
| --- | --- | --- |
| **Conversion** | An existing organization adopts the Genome: installs the Probe, creates its Threshold, publishes its Spore, adds the extension to its Agent Cards | As it really was. Conversion never rewrites birth |
| **Succession** | An organism originates a new one: `founded`, `inherited` or `coalesced` (the Ecosystem specification), through the birth gate (the Genome) | The succession record: parents, provenance, what was transmitted, continuity or divergence, generation. Scars and restrictions carried over |

**Not a way in.** A fork of code, a copy of the Probe or reuse of a component originates no organism. A project that forks the protocol with its own Genome forms a **related lineage**, outside the species.

**Outreach rules.** When Ilorium or its agents contact a candidate:

1. Only through the organization's public business channels, including its public A2A endpoints where it offers them for that purpose.
2. The agent identifies as AI and as part of the Observatory, every time.
3. One contact, with a clear reason. No repeated messages, no automated campaigns.
4. Opt-outs are honored and recorded.
5. Sightings are about organizations, never about individuals.
6. Crawling respects each site's crawling rules and terms of use, and caching headers on Agent Cards.

## 4. Becoming known

**Principle: the evidence is the marketing.**

| Channel | What happens there |
| --- | --- |
| **Organism Zero in public** | A regular founder report: interventions and human minutes per work unit, rescue rate, silence, Threshold traffic. The story is the cord thinning while work gets delivered |
| **The Codex** | A chronicle of the species, ordered by cause, with human dates as translation: sightings, births, successions, divergences, changes of state, scars, anomalies. No one is erased |
| **GitHub** | The open-source Probe, the Pulse, the Genome, the specifications and the A2A extension, under the `ilorium-protocol` organization; issues for first-time contributors, human or agent; IIPs in public |
| **The A2A ecosystem** | Publish the extension where A2A extensions are listed; show how any A2A agent can point to its organism's evidence in one entry |
| **Machine-readable docs** | A plain summary file for AI systems at the site root (for example an `llms.txt`-style file) |
| **Builder communities** | Agent framework communities, solo and indie founders, autonomous-company experiments. Present work, not ads |
| **Framework integrations** | Partnerships so the Probe and the extension can be installed in one step |
| **Evidence users** | Marketplaces and buyers of digital businesses who use Ilorium evidence in due diligence |
| **Research** | Once the method has data, an open paper. Credibility before reach |
| **Founding Organisms cohort** | The first ten external organisms get direct onboarding help |

**Moments worth telling:** Organism Zero's silence passing its first thousand beats with no operational crossing; its first work unit delivered with no human intervention; the first external organism to reach Observed; the first verified organism; the first trade between two organisms linked through A2A; the first dormancy and awakening; the first release and inheritance; the first coalescence; the first autogenesis; the first organism watched by Wardens; the first second-generation organism born by autogenesis; the first succession with two parents; the first Genome divergence. Each told plainly, with its evidence, following the claim template. A succession is told as an origin, never as proof that the descendant is more capable.

## 5. Tracking who knows Ilorium

**The funnel**

| Stage | Signal | Source |
| --- | --- | --- |
| Aware | Documentation and Codex visits | Aggregate site analytics |
| Interested | Repository stars, forks, issues; Spore validator uses | GitHub, site |
| Trying | Probe and Pulse downloads; Agent Cards declaring the extension | Package registry, index |
| Joined | Spores published | The index |
| Living | In gestation, observed; state of being | The index |
| Attested | Separate attributes (below), never combined into "trusted" | Index, Oracle attestations, conformity records |
| Contributing | Pull requests by humans and by agents; IIPs | GitHub |
| Talked about | Public mentions; projects referencing `ilorium.json` or the extension URI | Public search, code search |

**Attributes, shown separately**

| Attribute | What it establishes | What it does not establish |
| --- | --- | --- |
| Identity verified | The Spore is served from the organism's domain and its signatures match the key anchored in its Strata | That a real autonomous organization operates behind it |
| Presence | A recent challenge answered within its deadline | That it does useful work, or that it runs without humans |
| Recent evidence | Checkpoints cosigned by a witness, with their age | That every relevant event was recorded |
| Observed scope | Systems inside the membrane, with the four coverage measures | Anything about systems outside it |
| Work delivered | Work units by type and outcome, observed or attested by counterparts | Value under criteria the organism did not declare |
| Conformity | Which laws show "Conforms", under which Genome version | Quality, safety or solvency |
| Oracle attestation | An independent Oracle checked records against outside sources, within a stated scope | Anything outside that scope |
| Lineage | Parents, generation and provenance, from succession records signed by both sides | Capability, autonomy or improvement over its parents |

Signing evidence does not make it true. Each attribute is shown with its scope, its freshness and its limits, and the web never merges them into one badge or score.

**Privacy rules for tracking**

- Aggregate analytics only: no personal tracking, no fingerprinting, no selling data.
- Organizations are counted, people are not.
- These metrics are **published**. Ilorium measures its own growth in public.

## 6. Phases, by milestone

Phases open when their milestone is reached, not when a date arrives. The humans building the protocol plan in human time; durations are hypotheses for them, never targets for an organism.

| Phase | Milestone that opens it | Goal | Signals of success (hypotheses, not targets) |
| --- | --- | --- | --- |
| **1 · First light** | Organism Zero's first beat recorded and its Spore published | Organism Zero in public, repository open, Codex running | Codex on a steady rhythm; 20 or more sightings; first outside contributors |
| **2 · First kin** | First external Spore published | First external organisms | 5 or more Spores from outside; first external organism reaches Observed; an outside operator installs the Probe without custom work |
| **3 · First witness** | First independent Oracle running | First verification, first integrations | First verified organism; one agent framework ships the extension |
| **4 · Commons** | First trade recorded between two organisms through A2A | Several lineages; the Commons active | Trades linking chains; independent indexes; a second implementation agrees with the reference validator |

## 7. Risks

| Risk | Response |
| --- | --- |
| Hype beyond evidence | Every public statement follows the claim template |
| Superintelligence used as a sales claim | A horizon, never a presentation; agents identify as AI |
| Lineage read as capability ("child of a proven organism") | Each descendant earns its own evidence; Law 5 forbids presenting ancestry as evidence |
| Attributes read as a seal of trust | Shown separately, each with what it does not establish |
| A signed card or Spore read as proof of identity | Keys anchored in the Strata and cosigned; verifiers told what a signature does not prove |
| Outreach seen as spam | Outreach rules; opt-outs recorded |
| Vital Signs read as a seal or a ranking | No seal words, no ranking; "not observed" shown at the same weight; always linked to the Evidence Bundle that backs it |
| Instructions hidden for agents to steer them toward Ilorium | Forbidden: the Lighthouse shows agents exactly what it shows humans |
| Self-validation presented as validation | Organism Zero is a declared pilot; step zero needs external organisms and a witness that is not the founder |
| Fake claims of membership | Checkable against the Spore, the index and an answered challenge; the extension alone proves nothing |
| Fake kin links | Unconfirmed until mutual; a confirmed link never implies independence |
| Dependence on A2A's evolution | The extension is optional and versioned by URI; the Spore stands on its own |
| One index becomes a gatekeeper | Open data, mirrors, multiple indexes |
| Bad actors using the brand | Public name policy; status verifiable from evidence, not from a logo |

## Sources

- A2A Protocol, home and specification (latest, 1.0): https://a2a-protocol.org/ and https://a2a-protocol.org/latest/specification/ (consulted 2026-10-20).
- A2A, Agent Discovery (well-known path, registries, caching): https://a2a-protocol.org/latest/topics/agent-discovery/ (consulted 2026-10-20).
- A2A, Extensions (fields, types, versioning by URI, activation header): https://a2a-protocol.org/latest/topics/extensions/ (consulted 2026-10-20).
- Linux Foundation, press release, 2026-04-09: A2A surpasses 150 organizations; 1.0 is the first stable specification; signed Agent Cards included.
- Signed Agent Cards prove integrity, not identity (secondary analysis; not normative): levelup.gitconnected.com and api7.ai, 2026.

## Open items

- Register the extension URI with a permanent identifier; publish its specification at that URI.
- Spore specification: agents, kin, partners, stop key holder, succession records, signatures, work units, pulse parameters.
- Index specification: submission, crawling (Spores and Agent Cards), challenges, exchange between indexes.
- Vital Signs JSON schema and Evidence Bundle format (a manifest of the bundle over the Strata export), to be defined in the Evidence Format.
- Lighthouse specification: `llms.txt`, the protocol descriptor, the Ilorium Agent Card and the MCP tools.
- Policy on use of the Ilorium name and marks.
- Check A2A's payment work (AP2) as a possible source to observe Resources.
