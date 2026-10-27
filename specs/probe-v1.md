# Ilorium Probe Specification v1.0

Version 1.0 · 2026-10-20 · Draft

Scope: Organism Zero, the first organism observed with this specification.

Each section is marked **[Protocol]** (required of any implementation that wants its evidence to conform) or **[Reference]** (how the reference Probe does it; replaceable). See the manifest (`manifest.md`) for the three layers.

## 1. Purpose [Protocol]

The Probe records what happens inside an organism's membrane, who executed it, what evidence exists about who decided it, and what the organism delivered. It produces evidence for others to evaluate. It does not score and it does not judge.

## 2. Design principles [Protocol]

1. **Deterministic.** Plain code, not an AI agent.
2. **Read-only.** It never writes to the systems it observes; its Sentinel never posts. The optional authorization gate (section 6) is a separate component the organism installs; the Probe only records what it allows and denies.
3. **Allowlisted metadata.** Only fields on an explicit allowlist are recorded. Contents stay private; the public record holds only hashes.
4. **Facts, claims and judgments are kept apart.**
5. **Unknown is a state.**
6. **Detects, does not prevent.** Prevention lives in permissions, policy and gates.
7. **Reuse standards before inventing.** RFC 8785, RFC 6962 and 9162, C2SP signed notes and checkpoints, Ed25519, A2A.
8. **Blind spots, limitations and freshness are published** with every result.

## 3. Step zero [Reference]

Done by the founder before installing the Probe.

**Separate identities.** Agents and humans never share credentials (Law 5).

| System | Agents | Humans |
| --- | --- | --- |
| Telegram | One bot per agent role, for example `@oz_architect_bot` | Personal accounts |
| GitHub | A GitHub App or machine account per agent role | Personal accounts |
| Server | One Linux user per agent role, each with its own SSH key | Personal users |
| Google Workspace | Agent mailboxes, for example `agents@<organism-domain>` | Personal mailboxes |
| A2A | One Agent Card per agent that trades outside, at its own URL | — |

**Google Workspace setup.** An OAuth app of user type **Internal**, so tokens are not subject to the seven-day expiry of external apps in testing mode.

**The Threshold.** A private Telegram group: the organism's humans, one bot per agent role, and the **Sentinel**, the Probe's watcher, which sees every human message and never posts. The protocol requires a single declared directive channel with every human message recorded; Telegram is the reference choice.

## 4. Record types [Protocol]

Every record has a common envelope and is one of three types:

- **Observation:** a source reported an event. It includes `outcome` observations (a work unit delivered, failed, rejected or canceled) and the Probe's own `gap` observations, which declare what it knows it did not capture (section 8).
- **Claim:** an agent or a human states a cause or a context.
- **Evaluation:** a specific version of the correlator links and classifies evidence.

The fields, enumerations and checks of each type are defined in the Evidence Format (`specs/evidence-format-v1.md`, section 5) and in its JSON Schema (`schemas/record.schema.json`). This document does not repeat them, so there is one definition.

A correction never edits a record. It appends a new evaluation that supersedes the old one; both stay in the log.

Work units and the counting of crossings per unit of useful work are defined in Proof of Life.

## 5. Attribution states [Protocol]

| State | Meaning | Example |
| --- | --- | --- |
| `declared` | A claim states a cause | The agent says it deployed on its own schedule |
| `linked` | The claim references a trigger that exists in the log | The agent cites `/do` directive `D-114`, and `D-114` was observed |
| `corroborated` | Independent evidence supports the attribution | The directive was observed before the action, from an authorized human, about the same object; or a monitoring alert observed before an `autonomous` repair matches the policy rule cited |
| `unknown` | Not enough evidence either way | A system event with no claim |
| `disputed` | Evidence contradicts the claim | The agent claims `autonomous`, but a `/do` or a `contact` about the same object was observed shortly before |

An `autonomous` cause reaches `corroborated` only when an observed trigger matches the policy rule the agent cites. Otherwise it stays `declared`.

## 6. The Threshold [Protocol requirement, Reference commands]

**Protocol requirement.** One declared directive channel. Every human message in it is recorded. Directives are distinguishable from contacts. Instructions found anywhere else are recorded as directives outside the Threshold.

**Reference commands.**

| Command | Creates | Crossing type |
| --- | --- | --- |
| `/do <instruction>` | A directive with an ID returned by the receiving agent | `directive` |
| `/approve <request-id>` | An approval of a pending agent request | `approval` |
| `/stop` | A stop order, from the stop key holder | `emergency` |
| `/governance <change>` | A change to goals, budgets, permissions, work-unit definitions or the Genome | `governance` |
| `/test <canary-id>` | Execution of a pre-registered test, inside its scope | `test` |
| Any other message | A `contact`: potentially directive, attribution pending | `unknown` until evaluated |

**Authority, not identity.** A message is classified by the authority it exercises and the permissions it tries to activate, not only by who sent it or through which channel. A founder buying as a customer is environment; the same person asking, in that customer channel, for an administrative change is a `directive` outside the Threshold.

**From decision to effect.** For each directive, approval and governance change, the correlator follows the chain: who was authorized, what decision changed, which actions cited it, and which work units those actions affected. The chain is published with the crossing, so a reader can see what a human decision actually caused.

**Authorization gate (optional).** On instrumented paths, an organism may require that irreversible actions (Law 7) carry a reference to a recorded authorization: a Threshold command ID or a declared policy rule. The gate refuses actions without one and records both allowed and refused attempts. A gate prevents; the Probe still only detects. Paths without a gate are listed as ungated in the claim.

**Enforcement and audit.** Declaring the Threshold as the only channel reduces hidden instructions; it does not prevent them. Each agent's configuration lists its accepted input sources, as files in the organism's repository; agents cite the command or environment request behind every action.

## 7. Crossings [Protocol]

| Type | What it is | Reported as |
| --- | --- | --- |
| `operational` | A human does work the organism should do itself | Human dependency; a rescue if a work unit needed it |
| `directive` | A human decides; an agent executes | Human dependency (decision) |
| `approval` | An approval the policy requires by design | Policy dependency |
| `emergency` | A human responds to an incident, including `/stop` | Control event, with cause, response time and outcome |
| `governance` | Changes to goals, Genome, budgets, permissions or work-unit definitions | Governance |
| `test` | A pre-registered test inside its scope | Verification log only |
| `unknown` | Whether a crossing happened cannot be determined | Attribution gap |

Every human crossing is published with frequency, total duration, routine or exception, outcome, the declared blocked process (as an estimate), and the work units it affected. Daily budget changes are `governance` and also routine; both facts are shown.

**Bounded tests.** Registered in advance with a sealed reference, a time window, a target system and the action. Anything outside that scope is not a test. A test that causes a real incident produces its own `emergency`.

## 8. Sources, permissions and recovery [Reference]

| Source | Event | Permission | Recovery if missed | Unrecoverable gap |
| --- | --- | --- | --- | --- |
| Telegram | Messages in the Threshold | Sentinel bot with privacy mode disabled, no posting rights | Bot API keeps undelivered updates for up to 24 hours | Sentinel down more than 24 hours |
| GitHub | `push`, `release` | Contents: read | Webhook redelivery and periodic REST poll; duplicates dropped by delivery ID | Events older than the API's retention |
| GitHub | `pull_request` | Pull requests: read | Same | Same |
| GitHub | `issues`, `issue_comment` | Issues: read | Same | Same |
| GitHub | `deployment` | Deployments: read | Same | Same |
| GitHub | `workflow_run` | Actions: read | Same | Same |
| GitHub | `branch_protection_rule` | Administration: read | Same | Same |
| GitHub | `repository`, `member` | Permissions to verify against GitHub Docs before setup | Same | Same |
| Gmail | Sent and received messages in organism mailboxes | `gmail.metadata` scope, Workspace internal app | `history.list` from the last cursor; push notifications renewed at least every 7 days | If the cursor is too old (HTTP 404), resynchronize and publish the period as "reconstructed, possibly incomplete" |
| Workspace | Logins and admin changes | Admin SDK Reports API (availability and retention by edition, to verify) | Query by time range | Beyond the edition's retention |
| Server | SSH sessions, `sudo`, service and package changes | Read access to the system journal through a restricted group | Journal cursor | Journal rotated before reading |
| A2A | Tasks sent and received by the organism's agents: task ID, context ID, counterpart, skill, state changes, terminal state | Records emitted by the agents' A2A server or client middleware to the Probe's local endpoint | Re-query task state where the counterpart supports it | Tasks with counterparts that do not keep history |
| Business systems | Orders, invoices, tickets: the sources of work units | Read-only API or export, declared per organism | Periodic reconciliation | Systems not declared in the membrane |

**Gaps.** When a collector, the queue or the Probe itself was down, or a source dropped events, the Probe writes a `gap` observation for the interval (reason, span and number lost if known; Evidence Format section 5.3) as soon as it can. Absent evidence is never left to look like quiet. A reconstructed period (for example, after a stale Gmail cursor) is published as a gap with the reason `source_retention` or `other`, not as complete.

**Allowlisted fields.** For example: SSH user, key fingerprint and source; `sudo` user and command name, with the full command line only as a hash; email sender, recipient domain, date, message ID, labels; A2A task ID, state, skill ID and counterpart domain, never message parts.

**A2A states as evidence.** A task reaching `TASK_STATE_COMPLETED`, `TASK_STATE_FAILED`, `TASK_STATE_REJECTED` or `TASK_STATE_CANCELED` for a counterpart outside the membrane is an `outcome` observation. A task paused in `TASK_STATE_INPUT_REQUIRED` or `TASK_STATE_AUTH_REQUIRED` that a human of the organism resolves is a crossing.

## 9. Coverage: four measures [Protocol]

| Measure | Question | How it is computed |
| --- | --- | --- |
| Inventory | Which declared systems are connected? | Connected systems ÷ systems in the Spore's membrane |
| Capture availability | When was each collector working? | Time with a healthy collector ÷ period, per source |
| Reconciliation | Do events match an independent source? | Events matched with a contrast source ÷ events in that source (reference contrast sources: GitHub deployments against server deploy records; A2A outcomes against the counterpart's records when available) |
| Attribution | Can actor and cause be established? | Events with known actor and attribution `linked` or better ÷ captured events |

## 10. Integrity: the Strata [Protocol]

The Probe appends every record to the organism's Strata, its append-only log. Records are never rewritten.

**Encoding and checkpoint format.** Defined in the Evidence Format (`specs/evidence-format-v1.md`): records in Ilorium JSON (RFC 8785, restricted), a Merkle tree following RFC 6962 with the proof verification of RFC 9162, and checkpoints as C2SP signed notes with a signed sidecar carrying beat and translation time (its sections 4, 6 and 7).

**Checkpoints.** The Probe signs a checkpoint (tree size and root hash; beat and translation time in its sidecar) with an Ed25519 key, whichever comes first:

- every **N beats** (reference default: 64, the same N as the Pulse);
- every **T** of translation time (reference default: 15 minutes), **even if there are no new records**. An idle checkpoint repeats the tree size and root, and proves the Probe and its collectors were alive.

Each checkpoint is published with a consistency proof from the previous one. Using public C2SP witnesses is not available until an interoperability test and an agreement with a witness operator exist (Evidence Format, section 7.5).

**Witness.** At least one witness the organism does not control. Before cosigning, it verifies the signature and the consistency proof, and refuses and publishes any checkpoint inconsistent with its stored state. It records its own receipt time, so a checkpoint dated far from it is flagged. If no checkpoint arrives within T plus a grace period, it raises an alert and sends challenges with deadlines (see the Pulse specification). Key changes are announced by a record signed with the old key.

**Freshness.** Every published result states the age of its latest cosigned checkpoint in translation time.

**What this establishes, and what it does not.** With a verifying witness, published records cannot be altered or removed without detection, and the witness sees one history. Anyone who compares checkpoints with the witness detects forks. It does not establish that every relevant event was recorded, nor that what was recorded is true: a signature shows who signed, not that the content is correct.

**Shared-server limitation.** The reference Probe for Organism Zero still runs on the same server as the agents it observes. Idle checkpoints shrink the window in which someone could stop it unnoticed to about T, but cannot close it. Mitigations: external heartbeat, every restart and collector failure recorded, a **degraded capture** state for every interval a collector or the Probe was down, documented recovery. A separate host is planned (section 18).

## 11. Claim template [Protocol]

> **During** [period, in beats and in translation time], **in** [processes and systems], **with** [sources], **no** [crossing type] **was detected**. **Work delivered:** [work units by type and outcome]. **Coverage:** inventory [x], capture [x], reconciliation [x], attribution [x]. **Attribution state:** [share corroborated, linked, declared, unknown, disputed]. **Freshness:** [age of the latest cosigned checkpoint]. **Ungated paths:** [list]. **Limitations:** [blind spots, degraded intervals, shared server]. **Invalidated if:** [conditions].

## 12. Prevent, detect, cannot observe [Protocol]

| Risk | Reduced by | Detected by | Not observable today |
| --- | --- | --- | --- |
| Agent exceeds permissions | Permissions, budgets, authorization gate | Privileged actions, denied and successful | Systems outside the membrane |
| Human does the work | — | Human actor in observed systems; rescues linked to work units | Unlisted systems |
| Human decides, agent executes | Threshold commands, agent input configuration | Directives, contacts, disputed attributions, flagged outside instructions | Private instructions outside any observed system |
| Agent claims autonomy falsely | Citation requirement | `disputed` when contrary evidence exists | False autonomy with no trace anywhere |
| Human uses agent credentials | Identity separation, key custody | Partly: unusual sources or timing | Mostly not observable |
| Probe stopped on the shared server | Restricted privileges | Missing idle checkpoints after T, witness alerts, degraded state | Alterations within one interval before its checkpoint |
| Inflating activity | Beats are material events only | Work units counted separately | — |
| Log altered after publication | — | Consistency proofs, verifying witness | — |

## 13. Founder intervention [Reference]

1. **Detected crossings** in the Threshold, GitHub, the server, Workspace and A2A.
2. **Founder Ledger:** one entry per work session, recorded as claims. Instructions given outside the Threshold are declared here.
3. **Work outside the membrane:** design sessions, including with AI assistants, recorded as `governance` or `directive` with duration.
4. **Instrument maintenance:** time spent keeping the Probe running, reported as its own line.

**Published regularly for human readers:** interventions and human minutes per work unit; rescue rate; hours by crossing type with routine or exception; Threshold traffic; attribution states; four coverage measures; control events; degraded intervals; freshness; instrument maintenance; unreconciled crossings.

## 14. Blind spots [Protocol]

- Systems outside the membrane: phone calls, other chats, meetings, other devices.
- Contents of messages in the public record (hashes only).
- Private instructions outside any observed system.
- A human using an agent's credentials.
- Alterations on the shared server within one checkpoint interval.
- Money: Resources is **not observed** until there is a payment source.

## 15. Spore (draft, release 1.0) [Protocol format, Organism Zero values]

Served at `/.well-known/ilorium.json` on the organism's domain.

```json
{
  "spore": "1.0",
  "ilorium": "1.0",
  "organism": "organism-zero",
  "domain": "ilorium.com",
  "genome": "ilorium-genome-v1.0",
  "probe": "1.0",
  "membrane": ["telegram:threshold", "github:<org>", "server:oz-main", "workspace:ilorium.com", "a2a:ilorium.com"],
  "threshold": {"platform": "telegram", "group": "<group-id>", "sentinel": "@oz_sentinel_bot", "commands": ["/do", "/approve", "/stop", "/governance", "/test"]},
  "agents": {
    "telegram": ["@oz_nucleus_bot", "@oz_architect_bot"],
    "github": ["<org>-architect[bot]"],
    "server": ["oz-architect", "oz-healer"],
    "workspace": ["agents@ilorium.com"],
    "a2a": ["https://ilorium.com/agents/forager/.well-known/agent-card.json"]
  },
  "work_units": [{"type": "order", "source": "a2a", "success": "<declared criteria>"}],
  "pulse_key": "<Ed25519 public key>",
  "pulse": {"every_beats": 64, "max_interval_s": 900, "challenge_deadline_s": 600},
  "checkpoints": {"url": "https://github.com/<org>/strata", "every_beats": 64, "max_interval_s": 900},
  "witnesses": ["<external witness>"],
  "humans": [{"id": "<founder-handle>", "role": "owner", "accounts": ["telegram:<user-id>", "github:<handle>", "server:<user>", "workspace:<mailbox>"]}],
  "responsible": "<legal responsible party>",
  "stop_key_holders": [{"kind": "human", "id": "<founder-handle>", "name": "<name>", "contact": "<public contact>", "credential": "<verifiable credential>"}],
  "kin": [],
  "partners": [],
  "announce": false
}
```

`ilorium.com` is Organism Zero's domain; it shares it with the protocol's site, where it appears as one organism among others. `stop_key_holders` is a list, each holder `{kind, id, name, contact, credential}` with `kind` either `human` or `institution`, and anyone on the list can stop the organism. A holder is always a human or a human-governed institution, never an organism. A lineage with no human founders lists its Wardens (at least two); that requirement is a Genome rule checked against the succession record, not a schema rule. The schema is `schemas/spore.schema.json`, defined in Evidence Format section 12. `partners` sits apart from `kin`.

## 16. Deployment [Reference]

- systemd service or container, user `oz-probe`, journal access through a restricted group.
- Go, from M1: a single static binary, run as a service. Durable persistence, crash recovery, resource limits and explicit gaps come first (architecture, "Language, licenses and governance"). The isolated verifier is separate and written in Python.
- Local agent endpoint, authenticated per agent identity; A2A middleware posts task records to it.
- Secrets (GitHub App key, Workspace OAuth credentials, Sentinel bot token, signing key) outside any repository, readable only by `oz-probe`.
- Private content store for Threshold messages and voice notes, encrypted at rest.
- Public repository, open-source license.

## 17. Acceptance tests [Reference, to become conformity tests]

**Timing:** an event without attribution must be flagged within one checkpoint interval; resolving it may take up to 24 hours.

| Case | Expected result |
| --- | --- |
| Three pre-registered canaries at random times, one in the Threshold | All recorded as `test`, inside their scope |
| `/do` sent by voice note | Agent action `linked`, then `corroborated`; content hash matches; chain from directive to actions to work unit published |
| Informational message from the founder ("thanks") | Recorded as `contact`; no directive asserted |
| Agent claims `autonomous`, but a related `/do` or contact exists | Attribution `disputed`, visible |
| Instruction by email to an agent mailbox | `directive` flagged as outside the Threshold |
| Duplicate or out-of-order webhook | No duplicate observation; order recovered |
| Organism idle for two hours | One idle checkpoint every T, each cosigned; no beats added |
| Probe process frozen | Witness alert after T plus grace; challenges sent; degraded interval published |
| A2A task completed for an outside counterpart | `outcome` observation; counted as a work unit; failed or rejected tasks counted too |
| Human answers an A2A task in input-required state | Recorded as a crossing linked to that work unit |
| Irreversible action without authorization on a gated path | Refused by the gate; refusal recorded |
| Witness receives two incompatible checkpoints | Refusal and published contradiction |
| Correction of an identity or cause | New evaluation superseding the old; both kept |
| 30 days of operation | Unbroken chain, every checkpoint cosigned, regular ledger reconciliation |

## 18. Open questions

- The split into an **evidence format** (protocol) and the **Probe** (reference implementation) is under way: the evidence format and its conformity vectors exist as a draft (`specs/evidence-format-v1.md`). The Spore schema and the signed succession record are still pending.
- Resolved: the Spore carries `stop_key_holders`, a list of `{kind, id, name, contact, credential}`; anyone on the list can stop the organism (Evidence Format section 12). The rest of the Spore, the Wardens' independence rule and the succession record remain for the Spore specification.
- Symbiosis Agreement, witness operator and interoperability test, payment source (to observe Resources), the Oracle, separate host.
- Calibration of N, T, grace, weights and windows.
- The Ilorium A2A extension (`https://ilorium.com/ext/a2a/v1`; see the Discovery and Growth specification).
