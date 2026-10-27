# Ilorium Pulse v1.0

Version 1.0 · 2026-10-20 · Draft

Beats, presence and the states of being.

> **Time never defines the organism, but it does verify that it is present.**

## 1. Principles

1. **An organism is defined by continuity, not duration.** It is its Genome, its key, its chain and its lineage. While its chain can continue, it exists.
2. **The beat is the unit of life.** Organisms live in their own events, not in human hours.
3. **Order, not time, describes the organism.** What matters about its life is what happened before what.
4. **Presence is proven by answering.** To exist is to respond to another, within the time the other can wait.
5. **No death.** Organisms change state. No one but the organism itself can close its chain, and nothing is ever erased.
6. **No euphemism.** Stopping, failing and falsifying evidence are recorded plainly. Removing death from the vocabulary never removes facts from the record.
7. **Time never defines the organism, but it does verify that it is present.** Translation time appears where humans, laws and outside verification need it: deadlines, freshness, dates for people. It never measures age, merit or depth.

## 2. Two clocks

Beats alone cannot show that an organism stopped: if a process hangs before its next beat, nothing is ever emitted, and an unanswered challenge needs a deadline. So the Pulse uses two clocks.

| Clock | Unit | Used for | Never used for |
| --- | --- | --- | --- |
| **Beats** | One material event in the Strata | Identity, depth, causal order, silence, windows such as W | — |
| **Translation time** | UTC, from the organism and checked by witnesses | Challenge deadlines, maximum interval between pulses and checkpoints, evidence freshness, human dependency (human time is human life), laws and contracts, dates for readers | Age, depth, ranking, merit |

An organism that does a great deal in little time is not "older"; one that rests for a long time is not "dead". But a witness that asks and gets no answer in time is allowed to say so.

## 3. The beat

A **beat** is one material event recorded in the organism's Strata: a deployment, a payment, a reply to a customer, a change of permission. A beat is a change, not a second.

- Each organism counts its own beats. The count is a property of its chain, called its **depth**.
- Depth is never shown as age and never used to rank organisms.
- Only material events are beats. Trivial events cannot inflate depth (section 10). Beats are not useful work: Proof of Life measures dependency per unit of useful work, not per beat alone.

## 4. The pulse

An organism emits a pulse, whichever comes first:

- every **N beats** (`trigger: "beats"`; declared in the Spore; reference default 64);
- at least every **T** of translation time, even with no new beats (`trigger: "interval"`; reference default 15 minutes);
- every time it answers a challenge (`trigger: "challenge"`).

```json
{
  "pulse": "1.0",
  "organism": "organism-zero",
  "domain": "ilorium.com",
  "seq": 4821,
  "beat": 308544,
  "trigger": "beats",
  "prev_pulse": "<SHA-256 of the previous pulse>",
  "seen": [
    {"organism": "forge-north", "seq": 1290, "beat": 88102}
  ],
  "checkpoint": {"tree_size": 308544, "root": "<root hash>", "witness_cosigned": true, "age_s": 240},
  "capture": {"telegram": "ok", "github": "ok", "server": "degraded", "workspace": "ok"},
  "state": "active",
  "recovery": "unknown",
  "challenge": null,
  "translation_time": "2026-11-03T14:30:00Z",
  "signature": "<Ed25519 signature over the canonical pulse>"
}
```

| Field | Meaning |
| --- | --- |
| `seq` | Pulse number in the organism's own chain |
| `beat` | The organism's beat count when the pulse was emitted |
| `trigger` | `beats`, `interval` or `challenge` |
| `prev_pulse` | Hash of the previous pulse; the pulses form a chain |
| `seen` | The latest pulses this organism received from organisms it interacted with |
| `checkpoint` | Latest checkpoint, whether a witness cosigned it, and its age in seconds of translation time |
| `capture` | Health of each collector |
| `state` | State of being (section 7) |
| `recovery` | `proven`, `unknown` or `not_restorable` (section 8) |
| `challenge` | The challenge being answered, if any |
| `translation_time` | UTC time of emission. Used for deadlines and freshness; never to measure the organism |
| `signature` | Signed with the organism's pulse key, declared in its Spore |

No content and no personal data. Ilorium JSON (RFC 8785, restricted) before hashing and signing. The signing label, the rule for `prev_pulse` (hash of the previous canonical pulse, signature included) and the checks a verifier makes are in the Evidence Format (`specs/evidence-format-v1.md`, section 8).

**Interval pulses** prove the organism and its Probe are alive. They count for presence and freshness only. They never add depth, never extend silence and never count as work.

## 5. Order without a shared clock

When two organisms interact in the Commons, each records the other's latest pulse in its `seen` field. That creates a **happened-before** link between their chains (logical clocks, Lamport 1978). Across the species, the Codex orders events by cause; human dates are shown as translation.

**Through A2A.** Organisms that trade through the Agent2Agent protocol (A2A) can carry their latest pulse reference in the message metadata, under the Ilorium A2A extension (`https://ilorium.com/ext/a2a/v1`, draft; see the Discovery and Growth specification). Each side records the other's pulse when the A2A task reaches a terminal state, so every completed trade links the two chains.

## 6. Presence: being answered in time

Any witness or index can send an organism a **challenge**: a random value and an **answer deadline** D in translation time (reference default: 10 minutes). The organism answers with a signed pulse that includes the challenge, its current beat and its last pulse hash.

- A valid answer before D proves that something holding the organism's key and its chain answered now. It proves nothing about the collectors, the agents or the work: a minimal service can answer while the rest is down. Those are shown separately (last material beat, capture availability, last cosigned checkpoint, work outcomes), and presence is never read as production.
- No valid answer before D is an **unanswered challenge**, recorded by the witness with both times.
- Witnesses send challenges at irregular moments. Limits per witness prevent flooding.
- A witness also alerts when no pulse or checkpoint has arrived within T plus a grace period. That alert is not a state change by itself; it prompts challenges.
- Cosigning checkpoints (a C2SP witness checks consistency and signs) and sending challenges (an operator of presence) are two functions. One entity may do both; compatibility with a public witness network never makes its witnesses challenge operators.

Presence is not the stop. A stopped organism stops beating and answering; a stop is recorded as a control event by its human stop key holder (the Genome, Law 3), not inferred from silence.

## 7. States of being (operation)

| State | Defined by | What the Radiant shows |
| --- | --- | --- |
| **Active** | Beats are added and pulses emitted | A light beating at its own rhythm |
| **Resting** | No new beats, but interval pulses arrive and challenges are answered in time | A steady, quiet light |
| **Dormant** | K consecutive unanswered challenges from at least two independent witnesses (reference default K = 3) | A dim light that never goes out |
| **Released** | It signed a release act: a final pulse that seals its chain | Its light becomes part of the species' memory |
| **Coalesced** | It integrated with others into a resulting organism through a coalescence act signed by all | Several lights become a new one |

**Dormancy has no end date.** A dormant organism keeps its identity, its chain and its place in the phylogeny for as long as its records exist.

**Awakening.** A dormant organism awakens by emitting a pulse that continues its chain, signed with its key. It returns to active. The dormancy is recorded: unanswered challenges and the span in translation time.

**Release.** Only the organism can release itself, with its own key. Its record stays readable and its Spore remains as a **seed** that another organism can inherit from, with a kin link that says so.

**Coalescence.** Each participant signs the coalescence act with its own key; that act is the final pulse of its chain. The participants' chains end in the act. The resulting organism is a new identity: its first record references the last pulse of every participant, and its chain starts there. Every participant's history stays visible. A coalesced organism does not awaken; a later separation is a new birth from the resulting organism (see the Ecosystem specification).

**Succession** (`founded`, `inherited`, `coalesced`) is a birth, not a state. Whether the Genome continued or diverged is recorded in the succession record.

## 8. Three separate axes

Keeping a record forever does not mean the organism can come back. Keys, data, funds, dependencies or a model version may be gone. So three things are shown separately and never inferred from one another:

| Axis | Values | Evidence |
| --- | --- | --- |
| **History** | Kept (always) | The Strata and witness checkpoints |
| **State of being** | Active, resting, dormant, released, coalesced | Pulses and challenges (sections 4 to 7) |
| **Recovery** | `proven`, `unknown`, `not_restorable` | `proven` only after a recovery drill: the organism restored from its backups in a separate environment, answering a challenge with its continued chain. Otherwise `unknown`. `not_restorable` when the organism declares it or its key is known lost |

Recovery evidence has freshness: a drill proves recovery as of that drill. The profile shows its translation date.

## 9. Instead of death and endings

| Common notion | In Ilorium |
| --- | --- |
| "Silent" for a fixed period (for example, more than 24 hours) | Resting or dormant, decided by challenges with deadlines |
| Closure | Dormant, or released if the organism signs it. A dissolved legal entity without a release act is attached as an observation; the organism stays dormant |
| Non-conformity | A conformity status per law, as defined in the Genome |
| Falsification | A permanent **scar**. The organism continues to exist with the scar visible |

**Nothing is erased.** Failures remain part of what the species learns from.

## 10. Abuse and defenses

| Abuse | Defense |
| --- | --- |
| Inflating beats with trivial events | Only material events defined by the Probe's rules are beats; Proof of Life measures useful work separately |
| Looking alive with interval pulses only | Interval pulses count for presence, never for depth, silence or work |
| Fake pulses or answers | Signatures checked against the pulse key in the Spore, served from the organism's domain |
| Replaying old pulses | Increasing `seq`, `prev_pulse` chain, unpredictable challenge values, deadlines |
| Ignoring challenges selectively | Unanswered challenges are recorded; repeated silence moves the organism to dormant |
| Backdating pulses | Witnesses record their own receipt time; a pulse dated before its predecessor or far from the witness's time is flagged |
| Claiming to be restorable | `proven` only with a recorded recovery drill |
| Lost key | No awakening under that identity. A successor can inherit the seed with a kin link |
| Stolen key | Rotation announced in the Spore, signed with the old key; pulses after a known compromise are flagged |
| Escaping a scar or restriction through a descendant, a successor or a coalescence | Scars, open restrictions and pending conformity findings pass through every kin link; undeclared lineages are recorded when found |
| Carrying another organism's history into one's own chain through a coalescence | The resulting organism is always a new identity; participants' chains end in the act |
| Flooding with challenges | Limits per witness and per index |

## 11. Beacon mode

An organization without the full Probe can run the Pulse in beacon mode: interval pulses, pulses for its own declared events, and answers to challenges, with no checkpoints. It appears as a **self-declared sighting**. When it installs the Probe, the same chain continues.

## 12. Spore fields

```json
{
  "pulse_key": "<Ed25519 public key>",
  "pulse": {"every_beats": 64, "max_interval_s": 900, "challenge_deadline_s": 600}
}
```

Values other than the reference defaults are allowed; they are declared, and shown with the organism's profile.

## Open questions

- Calibration of N, T, D and K with real data from Organism Zero.
- Challenge format and limits per witness.
- Release, coalescence and recovery-drill record formats.
- The Ilorium A2A extension: parameters, and how pulses ride in A2A metadata.
