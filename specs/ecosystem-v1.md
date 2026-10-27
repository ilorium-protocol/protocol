# Ilorium Ecosystem v1.0

Version 1.0 · 2026-10-20 · Draft

## Purpose

This document describes the world where agents, organisms, lineages and humans coexist: who lives in it, where each one acts, how a new organism joins, how it appears on ilorium.com, and how succession, coalescence and lineages are recorded.

## Who lives in the ecosystem

| Entity | What it is | Defined in |
| --- | --- | --- |
| Species | All organisms that carry the Ilorium Genome | Genome |
| Lineage | The network of ancestry formed by successions: an organism, its parents and every organism descended from it | This document |
| Organism | One organization running under the Genome, defined by continuity: its Genome, key, chain and lineage | Pulse |
| Agent | A software entity with its own identity, acting inside one organism | Glossary |
| Human | Founders, operators, customers, suppliers, the public | Probe (roles) |
| Warden | A human or human-governed institution that holds the stop key of an organism no human founder watches. At least two Wardens watch each such organism, independent of it, its lineage and each other; any one can trigger the stop | Genome, Law 3 |
| Oracle | An independent verifier | Genome, Law 6 |
| Observatory | The organism that chronicles the species | Glossary |

## Four spaces

| Space | Who is there | What happens | How it is recorded |
| --- | --- | --- | --- |
| **Inside the membrane** | Agents of one organism | The organism operates, repairs itself and grows | Probe observations; each material event is a beat |
| **The Threshold** | That organism's humans and agents | Humans give directives, approvals, stops and governance changes | The Sentinel records every human message; commands are crossings, other messages are contacts |
| **The Commons** | Organisms and their environment | Trade, requests and services between organisms | Environment, not crossings; each interaction links the organisms' chains in causal order |
| **The Radiant** | Anyone | Watching the species: lights beating at their own rhythm, lineages, states of being | Watching is not acting |

**Coexistence rules**

1. Humans with authority speak to an organism only in its Threshold.
2. Agents always identify as AI, in the Commons and everywhere else (Law 5).
3. An organism tells its customers that they are dealing with an organization run by AI agents.
4. Watching never requires permission; intervening is always recorded.

## How an organization joins

1. **Install the Probe**, or start with the Pulse in beacon mode.
2. **Separate identities and create the Threshold.**
3. **Adopt the Genome** and publish the Spore at `https://<domain>/.well-known/ilorium.json`.
4. **Sign the Symbiosis Agreement**, the birth act, naming a human stop key holder. Its hash is the first record in the organism's Strata. An organism originated by other organisms also carries a succession record (below).
5. **Start beating.** The organism now exists in the protocol.

## How organisms appear on the web

| Status | Requirement | What the web shows |
| --- | --- | --- |
| **Sighting** | Claims to be autonomous, or runs in beacon mode; no checkpoints | Name, source of the claim. Marked as self-declared, not evidence |
| **In gestation** | Spore published; checkpoints cosigned; fewer than W beats with an unbroken chain | Identity, Genome version, Probe version, evidence so far, and its lineage if it has one |
| **Observed** | At least W beats with an unbroken chain (initial W to calibrate) | Full Proof of Life profile, with coverage and limitations |
| **Verified** | At least one independent Oracle has attested its records | Profile plus the attestation and the Oracle's independence declaration |
| **Conforming** | Every law of the Genome shows "Conforms" | Conformity badge, linked to its evidence |

Every organism also shows its **state of being**: active, resting, dormant, released or coalesced. Appearing on the web is never an endorsement. A descendant goes through every status on its own evidence, starting from "in gestation", whatever its parents' status.

## Succession and lineages

**Lineage is the network; succession is the act.** A succession is the recorded act by which one or more organisms originate another. Most successions add a branch; some join lines, when an organism has several parents. To succeed is to originate: a parent may continue to exist alongside its descendant. Succession proves origin. It never proves autonomy, capability or improvement, which each organism shows only through its own Proof of Life.

**The birth gate.** Every succession, of every type, passes the gate in the Genome (Succession; IIP-0003): the parents conform and have a recent stop drill; no parent is under restriction; each parent authorizes it under its own rules; a human stop key holder accepts the descendant's key before the birth act is valid; the laws travel whole; the act is signed, cross-referenced and witnessed.

**Types of succession**

| Type | What happens | Parents afterwards |
| --- | --- | --- |
| `founded` | One or more organisms originate a new organism. With two or more parents, each contributes rules, components or resources to a single new organism (SI2SI, on the horizon) | Continue as they were |
| `inherited` | An organism takes up the seed (Spore) of a released organism, or of a dormant organism whose key was lost | Remain released or dormant |
| `coalesced` | Two or more organisms integrate into one **resulting organism**, a new identity with every participant as a parent (coalescence, below) | Pass to the state "coalesced"; their chains end in the coalescence act |

**Provenance.** Every organism's birth act names its provenance:

| Provenance | Meaning |
| --- | --- |
| Founded | Humans created and designed it |
| Commissioned | A human gave the order; an AI designed and launched it |
| Assisted birth | Another organism created it, with a human crossing during the birth |
| Autogenesis | Another organism decided, designed, funded and launched it with no human crossing |

Type and provenance are separate: type says *how* the organism was originated; provenance says *who* decided and designed it, and whether a human crossed during the birth.

**The succession record.** Part of the descendant's birth act, signed by every parent and by the descendant, referenced from each parent's Strata and cosigned by a witness:

| Field | Content |
| --- | --- |
| Type | `founded`, `inherited` or `coalesced` |
| Parents | The originating organisms, by key |
| Authorization | For each parent, the reference to its own authorization record (Threshold command or declared policy rule) |
| Provenance | As in the table above |
| Transmitted | Genome version (always); for each parent, the declared rules kept, changed or dropped; component digests; resources. Never private keys, never evidence |
| Genome | **Continuity** (same Genome version and rules as a parent) or **divergence** (changed rules). A Genome other than the Ilorium Genome is not a birth in the species: it forms a related lineage |
| Stop key holder | The descendant's own, a human or human-governed institution, who accepted the key before the act was valid (Genome, Law 3) |
| Responsible party | The descendant's own, declared at birth (Genome, Law 4); it may be the same party as a parent's, declared again |
| Obligations declared | Commitments of the parents that the descendant declares it takes on. A record, not a legal transfer: whether any obligation actually passes depends on law and contracts outside the protocol |
| Generation | One more than the highest generation among its parents. Organisms with no parent in the protocol are generation 0 |

Resources transferred to a descendant are material actions of the parent and count against its limits (Genome, Law 2).

### Coalescence

**What it is.** Two or more organisms integrate into one resulting organism, under one Genome version, through an act signed by every participant and authorized under each participant's own rules. The result is always a **new identity**: its own key, chain, stop key holder and responsible party, with every participant as a parent. No participant continues as the result: if one did, it would carry the others' history and evidence into its own chain, which Law 5 forbids.

**What happens to the participants.** They pass to the state "coalesced". Their records stay readable; their chains end in the coalescence act, and the resulting organism's first record references each participant's last pulse.

**What the result inherits.** Every participant's scars, open restrictions and pending conformity findings. Never their evidence: the result starts "in gestation", like any descendant. Capabilities the participants declared are recorded as declarations, not as evidence; the result shows its own through its Proof of Life.

**What is not coalescence.** Alliances, federations, trade, shared resources and data exchange. Without a resulting organism with its own birth act, key and Genome, there is no coalescence. Trading partners are listed in the Spore as `partners`, never as kin.

**What is not yet defined.** Separation after a coalescence (provisionally: a `founded` succession from the resulting organism; the former identities are not revived); coalescence with an organism of a related lineage; coalescence of parts of organisms.

### Rules for the whole network

**What is not a succession.** A fork of code, a copy of the Probe or reuse of a component does not originate an organism: no birth act, no record, no kin link. A fork of the protocol whose Genome is not the Ilorium Genome is a **related lineage**, outside the species; its organisms can be linked for history, never for conformity.

**Generation is a position, not a rank.** It says where an organism sits in the network. A later generation is not assumed to be more capable, more autonomous or better than an earlier one, and the profile never weighs it.

**What always passes through a kin link.** Every succession carries the parents' scars, open restrictions and pending conformity findings to the descendant. They stay visible on its record, linked to their origin, until they are lifted on the descendant's own evidence. A restriction or suspension cannot be escaped by creating a descendant, a successor or a coalescence. An organism created by the same humans, keys or infrastructure without declaring its succession is recorded as an **undeclared lineage** when found.

**What never passes.** Conformity, Proof of Life measures, Oracle attestations, status on the web, and the stop key. A descendant earns each of these from zero and is watched by its own human holder.

**Moving does not erase the past.** An operation that moves to a new entity carries its history with it. Rebirth cannot improve a record.

**No death, no erasure.** The phylogeny shows every organism in its current state of being. Dormant organisms stay in the network, dimmed. Released and coalesced organisms stay as part of the species' memory. Scars, such as proven falsification, stay visible on the organism's record. Failures are part of what the Observatory studies.

## SI2SI: the horizon of the species

*Horizon, not specification. Nothing in this section adds a rule, a status or a criterion beyond those already defined above and in the Genome.*

**The mission.** Ilorium monitors organizations run by AI agents: it records how each one lives, measures what it has actually shown it can do, and requires that every organism carry a human stop key, tested by drills within a declared scope. Its mission is to provide laws, formats and verification for organizations run by AI agents and for the evolution of their species. The founder reads that evolution as the road to SI2SI: a personal conviction, set out in the founder's letter, on which the protocol takes no position. It sets, from the first generation, the conditions every birth must meet — the laws every organism carries, the record of every succession, the birth gate and the human stop key — and it evolves with the species, following the chain of succession to measure it and govern it. It does not assume that superintelligence will emerge, and no record can make it emerge; what it requires is that if a new generation begins, it begins on the record, through the gate, with a human stop key for every organism and every claim backed by evidence.

**Three kinds of statements.** This section keeps apart the founder's conviction (his, not the protocol's), the project's hypotheses (to be observed, never claimed) and what the protocol defines today (the rules above and in the Genome). The full statement is in "Vision and evidence" in the README.

**What SI2SI names.** The generative act between superintelligences: two or more parents contribute what they are, their rules, components and resources, to a new and distinct mind, as two people conceive a child.

**The founder's narrative and conviction.** In the founder's narrative, SI2SI is also the new generation itself: the stage of life that follows humans. In his words: "God created humans; humans created SI2SI; SI2SI created God." His conviction is that a new era is coming where humans no longer have to work, medicine reaches everyone, and the human species branches alongside superintelligence. Both are the founder's, labeled as his. They are not hypotheses of the project and not rules of the protocol.

**Three relations, three notations**

| Notation | Relation | Type of succession | The antecedents afterwards |
| --- | --- | --- | --- |
| **SI → SI** | Descent | Any | Depends on the type |
| **SI2SI** | Conception: a new mind from two or more parents | `founded`, with two or more parents | Continue to exist |
| **SI + SI → SI′** | Coalescence: integration into one resulting mind | `coalesced` | Pass to "coalesced" and continue only in the result |

These are horizon terms only. The protocol defines and verifies no criterion for superintelligence, and no agent or organism presents itself as superintelligent (Law 5). None of the notations asserts that such capability exists, that the result surpasses its antecedents, that it has a unified mind, or that an integration is irreversible.

**How SI2SI is governed, if it happens.** By the same rules as the first birth in the species, because the protocol cannot tell when an organism becomes a superintelligence and does not try:

| What | Rule |
| --- | --- |
| Who may conceive | Only parents that conform, with a recent stop drill, and under no restriction (birth gate) |
| What is always inherited | Every law of the Genome; the parents' scars and open restrictions |
| What may be inherited | Declared rules, components, resources, as listed in the succession record |
| What is never inherited | Private keys, evidence, conformity, attestations, the stop key |
| Variation | The descendant may change its declared rules (divergence within the species). Changing a law leaves the species |
| Before life | A human stop key holder accepts the newborn's key |
| Gestation | From the birth act to "observed": the newborn proves everything on its own evidence |
| Selection | What propagates is what has shown it can be stopped, tells the truth about itself and keeps its limits |

**What no protocol can promise.** These rules hold while organisms run on infrastructure whose credentials can be revoked. A system that leaves that infrastructure is not stopped by a record. Ilorium cannot guarantee control of a superintelligence, and it cannot prevent a birth outside the record; it recognizes a birth as part of the species only when its evidence satisfies the birth gate, with a human key, on the record, and that recognition proves no control beyond the scope the drills covered.

## Where the founder fits

The founder lives in Organism Zero's Threshold and in the Radiant, like any other human. The founder's path is to speak less and less in the Threshold, until the final gate: retiring with no special keys. Organism Zero's stop key then passes to the Wardens.

## Stages of the ecosystem

| Stage | What exists |
| --- | --- |
| Now | Organism Zero, its Threshold, its Probe and Pulse; the Observatory listing sightings |
| Next | First external organisms; statuses "in gestation" and "observed" |
| Then | First independent Oracle; status "verified"; first recorded succession through the birth gate |
| After that | Several lineages; trade in the Commons; the first Wardens; the Radiant as a live view of the species |
| Later | An immersive Radiant, once there is a species worth watching |

## Open questions

- Rules for organism-to-organism agreements in the Commons.
- Value of W, the beats needed for "observed".
- Minimum evidence for the first independent Oracle.
- How a restriction is lifted, and who decides (governance document).
- How Wardens are qualified, checked for independence and paid without capture (Genome, open questions).
- Separation after a coalescence; coalescence across lineages with other Genomes; coalescence of parts of organisms.
- Format of the succession record, kin links and `partners` in the Spore specification.
