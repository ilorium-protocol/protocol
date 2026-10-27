# IIP-0006 · Reading evidence, status names and publishing

| Field | Value |
| --- | --- |
| Number | IIP-0006 |
| Title | Reading evidence, status names and publishing |
| Author | The founder (Seldon), with Claude (AI, identified as such) |
| Status | In comment from 2026-10-27 to 2026-11-26 (30 days). Discussion: https://github.com/ilorium-protocol/protocol/discussions/7 |
| Kind | Method change to `specs/proof-of-life-v1.md` (the composite status), specification additions to `specs/evidence-format-v1.md` (reading rules) and to `governance-v1.md` sections 3.2.6 and 9 (approvals bound to content; authority inventory) (30 days, because governance is affected) |
| Affects | Proof of Life; Evidence Format verdicts; Vital Signs; glossary; governance 3.2.6 and 9 |
| Decides | The founder, as the only Custodian during interim governance, in public, after the comment period |

## Motivation

- Three of five outside readers took "Ilorium 100%" for a seal, although the text said it was not one. A name that combines provenance (a historical fact) with five measured dimensions under a percentage invites exactly the comparison the protocol forbids.
- The reviews asked for explicit reading rules: a gap in observation is not autonomy; an UNKNOWN does not become favorable with time; a drill has a scope and an age; emergencies are recorded even when not penalized; a hash is not by itself a privacy protection; a questioned decision keeps its record and adds the review.
- Two votes on paper do not bind an account that can publish something else. Approvals must be bound to the exact content, and the resources that control publication must be listed.

## Specification

1. **No composite status (Proof of Life, revised 2026-10-22).** "Ilorium 100%" is withdrawn. Provenance records autogenesis as a fact about birth. "Full observed autonomy" is a result about a window (every corroborated material action executed and decided by agents; zero interventions and zero rescues per work unit), shown with the window, the coverage measures, the attribution states and the share of unknown work. Nothing combines into a name, number or badge. The glossary marks "Ilorium 100%" deprecated.
2. **Reading rules (Proof of Life principles 5, 7, 8; to be mirrored in the Evidence Format's verdict section).** Safety is never punished and never hidden: stops and correct escalations are not dependency but are always shown; an emergency a human handled counts in the rescue rate. A gap is unknown, never autonomy; an UNKNOWN never turns favorable with time. The measure is not the goal: coverage, attribution states and unknown share are shown at the same weight as the measures, and a claim that leaves them out is invalid. A drill result carries its scope and date. A hash in the public log is not presumed to protect every private datum behind it. A decision later questioned keeps its original record and adds the review.
3. **No global PASS.** A verifier's result names the claim, the scope, the period, the method version, the sources and the limits. A witness cosignature attests to log consistency, nothing about governance, autonomy or work.
4. **Approvals bound to content (Governance 3.2.6).** Proposal and version, hashes of text and artifacts, voters and abstentions, dates, signatures, effective date, decisions replaced. Changed content is approved again.
5. **Authority inventory (Governance 9; `governance/authority-inventory-v1.md`).** Every resource that publishes or controls the protocol, its holders, permissions, transfer procedure and who can act alone, with no secrets; reviewed quarterly. During the interim it states that one person can act alone on everything.
6. **Honest openings.** The whitepaper and README state requirements and tests with their scope ("requires a human stop key, tested by drills within a declared scope"), not guarantees; "decentralized" and "no one owns it" are stated with the interim control that exists today.

## Revision of 2026-10-24

A sixth outside review (`governance/reviews/06`) read the final draft and found that "full observed autonomy" could still be read on a subset: ten corroborated actions by agents next to ninety unattributed ones. Four reading rules are added to the Proof of Life specification, provisional under this IIP:

- **Counts, not adjectives.** Full observed autonomy is always written with numerator, denominator, exclusions and unattributed actions, per process, and is not shown when unattributed actions exceed the declared threshold or a declared source was not captured.
- **Human effort whole.** Every intervention is timed whatever its kind; the total and its breakdown are shown next to any adjusted measure, whose exclusions are disclosed.
- **Estimate, not floor.** Detected human time is an estimate from recorded activity with a published rule, version and error; detected, declared and connection time are never added without deduplication.
- **Denominators named.** Attempts, terminal outcomes and successful deliveries are three counts; a zero denominator is "not computable", never zero; human time spent on failed units is shown.

## What it breaks

The name "Ilorium 100%" in earlier drafts, the brand's status iconography if it used it, and any site copy. No organism has displayed it.

## What it does not establish

- A replacement composite status. There is none, by design; a future one would need its own IIP with validated weights.
- Hardware attestation (TEE) or zero-knowledge proofs: noted as research, not part of this release.
- A threshold signing scheme for releases: to be evaluated (for example TUF) before any second approver exists.

## Questions for commenters

1. Is "full observed autonomy" clear enough, or does it still read as a grade?
2. Which reading rule is missing? Which one could be gamed?
3. Should the authority inventory be part of the protocol (normative) or stay a governance document?

## Test vectors

Vital Signs schema: remove any field naming a composite status; add the guardianship state. Conformity vectors for the verdict fields (claim, scope, period, method version, limits) to be added when the Evidence Format section is written.
