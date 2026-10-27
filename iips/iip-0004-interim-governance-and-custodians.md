# IIP-0004 · Interim governance, Custodians and constitutional changes

| Field | Value |
| --- | --- |
| Number | IIP-0004 |
| Title | Interim governance, Custodians and constitutional changes |
| Author | The founder (Seldon), with Claude (AI, identified as such) |
| Status | Draft, opens for public comment when the repository is published |
| Kind | Method change to `governance-v1.md`; it touches section 10, so it takes the reinforced comment period: **90 days** *(corrected 2026-10-24; the first draft said 30)* |
| Affects | Governance sections 2, 3.1, 3.2, 3.4, 4.2–4.6, 7, 8, 10 |
| Decides | The founder, as the only Custodian during interim governance, in public, after the comment period, and only to confirm, narrow or withdraw; the constitutional rules (point 10) are ratified later by the full council |

## Motivation

Five outside reviews of the first governance draft (`governance/reviews/`) agreed on four problems, and the text confirms them:

1. The transition to full governance depended on a single event (an external organism reaching Observed) that the founder himself judges, with no deadline. The interim could last forever.
2. The founder invited both independent Custodians, and an objection to an appointment had no stated effect. Two of three could be the founder under another name.
3. Nothing said what happens if the founder disappears, is incapacitated or abuses the interim.
4. The governance document could be changed by two votes of three, including the rules that define independence and the transition.

The reviews also found that the founder's power was stated three incompatible ways (the roles table, section 3.2 and section 8). That contradiction was corrected on 2026-10-22 as an editorial fix; this IIP records the correction and asks for comment on the rules built on it.

## Specification

The rules below are already in `governance-v1.md`, marked *provisional (IIP-0004)*. This IIP asks whether to confirm, change or withdraw them.

1. **Founder and Genome (section 2, 8).** During interim governance the founder decides IIPs that do not change the Genome; Genome changes are published only as drafts identified as his and ratified by the full council. He never amends the Genome alone, in any stage. His seat is replaceable, not perpetual.
2. **Deadline (section 8).** Interim governance ends when the council is constituted (three Custodians, two alternates), and at the latest 18 months after the public repository is published; the start date is recorded in the changelog and never resets. External adoption (first external Observed organism) is a milestone, not the condition. If the 18 months end with the council incomplete, the protocol enters **restricted maintenance**: security fixes, continuity of infrastructure and the procedure to seat the council; no IIP passes; the founder keeps convening candidates and has no unilateral authority over rules. A lack of candidates never extends the interim.
3. **Appointment (section 4.2).** Checkable declarations of independence; two routes for the first two independent Custodians (one invited by the founder, one from a public call, with nominators and selectors published); an admissible objection keeps an appointment from taking effect until answered in public with the evidence examined, within 30 days, with a 30-day extension of the comment period.
4. **Alternates, review and removal (sections 4.3, 4.6).** Two alternates with the same independence, who vote only for recusals and vacancies; a periodic review of activity and fitness; removal only after a right to reply and an independent reviewer per case, whose advisory opinion is answered in writing.
5. **Compensation (section 4.4).** Rates published 30 days before they apply, never retroactive; the first rate set by the founder before any independent Custodian takes office.
6. **Continuity (section 4.5).** A continuity person, named by the founder with a signed acceptance, who after 90 days without answer may only convene the transition and publish the notice. Recovery of accounts is separate and confers no authority. Pre-authorized procedures for contingencies that cannot wait live in the authority inventory.
7. **Classification by effect (section 3.1).** Any change whose effect alters eligibility, powers, conformity results, interpretation of evidence, security requirements, quorum, appointments, reviews or sanctions is a method change, whatever its size.
8. **Human sponsorship of agent proposals (sections 3.2, 7).** An IIP drafted by an agent enters review only with a human sponsor who signs and answers for it; maintainers may limit volume and close mass submissions with public reasons; comments are never filtered for being written by agents.
9. **Constitutional changes (section 10).** The independence criteria, the two-of-three threshold, the rules on people, the transition and its deadline, the key prohibitions and section 10 itself change only with 90 days of comment, a written justification, an independent reviewer, two of three without alternates and, once a body exists that can ratify, its ratification. No unanimity.
10. **Initial constitution (section 10; added 2026-10-24).** A sixth review found that this IIP let the founder confirm, after 30 days, rules that section 10 protects with 90 days and two of three Custodians. The answer is explicit: these rules were adopted by the founder's interim decision because no council existed; they are provisional until the full council ratifies them as its first constitutional decision; this IIP takes the 90-day period; during the interim the founder may narrow his authority, never widen it, never restart the clock, never add to the list; and the exception applies once. The exact text adopted, its SHA-256 and its date are recorded in `governance/decisions/0004` when the repository is published.
11. **Compensation and review without a council (sections 4.4, 4.6; revised 2026-10-24).** Later rates are decided with an independent reviewer, take effect no earlier than 12 months after publication and are never retroactive. A decision about people that finds no reviewer within 14 days proceeds as unreviewed and says so.
12. **Custodians never hold another organism's stop key (sections 2, 10).** The open question on whether a Custodian may be a Warden is closed in the negative, consistently with section 10.

## What it breaks

Nothing already in operation: no organism has adopted the protocol. It changes the expectations of anyone who read the first draft of section 8.

## What it does not establish

- Who the Custodians, alternates or continuity person are. The continuity person is pending the founder's designation and acceptance; the IIP may close without it, and section 4.5 says so until it is filled.
- The body that can ratify constitutional changes: its membership and rules are an open question.
- Whether the 18 months are right. It is an institutional choice for this stage, not a figure validated by data; comments proposing another limit must say what it buys.

## Questions for commenters

1. Does the deadline plus restricted maintenance create a credible commitment, or a dead end? What should restricted maintenance allow that it does not?
2. Is the public call for the second Custodian workable before a community exists? What would you replace it with?
3. Should the founder's recovery account count as a second owner for anything beyond recovery?
4. Which rules are missing from the constitutional list, or should not be on it?
5. Is the initial-constitution rule (point 10) narrow enough? What else should the founder be unable to do with provisional rules?

## Test vectors

None: this IIP changes no format.
