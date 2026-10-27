# Decision 0004: Provisional rules adopted on 2026-10-22

- Date: 2026-10-22
- Decided by: the founder, as the only Genome Custodian, after external reviews 01 to 05 (governance/reviews/)
- Kind: standing decision; every rule below is provisional until the council of Custodians ratifies it (governance-v1.md, section 10)
- Status: in force

## Decision

The founder adopts, as provisional rules, the governance and reading rules written in governance-v1.md (release 1.0, draft) and in IIP-0004, IIP-0005 and IIP-0006 (iips/), which are opened for public comment with the publication of this repository. The founder adopts them because no council exists to adopt them (governance-v1.md, section 10, initial constitution). They bind the founder first.

In force from the first public release, in summary (the normative text is governance-v1.md and the three IIPs; this list does not replace them):

1. **Interim governance** ends when the council is constituted (three Custodians and two alternates) and at the latest 18 months after the repository is published. If the term ends without a council, the protocol enters restricted maintenance: security and continuity only, no IIP, and the founder keeps convening without unilateral authority.
2. **Custodians** declare their independence in a verifiable way; the first two come by two routes (one invited by the founder, one from a public call); admissible objections have a suspensive effect and get a public answer with evidence.
3. **Constitutional rules** change only with 90 days, a justification, an independent reviewer, two of three Custodians without alternates, and ratification by a body once it exists. No unanimity.
4. **Wardens** (stop key holders for lineages without human founders): stopping, resuming and sanctioning are three separate decisions. A Custodian is never a Warden.
5. **AI in governance:** an AI may propose, review, maintain and operate; it never votes, holds a key, appoints or moves money. IIPs drafted by agents need a human sponsor who signs.
6. **Publication:** approvals are tied to the content (hash, voters, dates, signatures). The authority inventory (governance/authority-inventory-v1.md) states that one person can act alone on everything today.
7. **Continuity:** a continuity person (convenes the transition after 90 days without a response) and a recovery person are designated. Both are pending.

## What this decision does not do

It does not change the Genome. It does not declare any release stable. It does not appoint any Custodian or Warden.

## What the repository enforces

- `GOVERNANCE.md` maps governance-v1.md to this repository. `CODEOWNERS` names the Custodians (today `@fseldon`).
- The review-by-hash point (6) is **not yet enforced by a workflow**: it is planned. Today the interim ruleset requires a pull request, signed commits, status checks and a code owner review; the content binding is a published convention until a workflow checks it.

## Sources

- governance-v1.md, sections 4, 7, 8, 9 and 10; iips/iip-0004, iip-0005, iip-0006.
- governance/reviews/01 to 06; governance/authority-inventory-v1.md.
