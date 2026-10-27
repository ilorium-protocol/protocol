# Ilorium Governance v1.0

Version 1.0 · 2026-10-21 · Draft · Revised 2026-10-22 after outside review

Who decides what in the Ilorium protocol, how decisions are made and objected to, how the people who hold power are chosen and replaced, how the protocol is funded, and how it moves from the founder's interim governance to a shared one. Part of the protocol. Nothing here changes the Genome: this document says who may change it and how.

> **No organism governs the species. Humans do, in public, with evidence.**

**About this revision.** Five outside reviews (recorded in `governance/reviews/`) found three contradictions in the first draft (the definition of stakes disqualified the Wardens; the founder's power during interim governance was stated three different ways; two Wardens could not replace one) and several gaps. The founder corrected the contradictions and adopted new rules on 2026-10-22. Rules marked **provisional** are in force as the founder's interim decision and are open to public comment under IIP-0004 (interim governance, Custodians and constitutional changes), IIP-0005 (stop, resumption and guardianship) and IIP-0006 (reading evidence and publishing). Each IIP confirms, changes or withdraws them when it closes. A rule under comment is not treated as approved.

## 1. Principles

- **The three locks hold.** Only human Genome Custodians amend the Genome (germline); only conforming organisms originate others (birth gate); every organism is born with a human stop key holder (stop). No governance decision can suspend a lock. Removing a lock would need a new major version of the protocol and a new Genome, which would be a related lineage, outside the species.
- **No one judges their own cause** (Law 6), including the people who govern. Anyone with a stake in an organism steps aside from any decision about it.
- **Everything on the record.** Proposals, comments, votes, appointments, removals, income and spending are public, in the repository or on ilorium.com. A decision that is not published does not exist.
- **Notary, not judge, also in governance.** The protocol certifies no organism, ranks none, and endorses none. Governance decides rules and formats, never the status of a particular organism, which comes from evidence alone. Where a decision requires human judgment (whether a Warden is independent, whether a stop was abusive), the procedure that resolves it is named, its result is published, and the status it affects shows which part rests on evidence and which part on that resolution. No authority grants a hidden exception to favor an organism.
- **Observability is not control.** Governance can only act on what runs on infrastructure whose credentials can be revoked. The protocol promises no control over anything beyond that. Nothing in this document pauses, isolates or seizes an organism: the protocol records, publishes and withholds recognition; it does not operate anyone's infrastructure.

## 2. Roles

| Role | Who | Decides | Never |
| --- | --- | --- | --- |
| **Founder** | The person who started the protocol and runs Organism Zero | During interim governance (section 8): publishes releases and merges, and decides IIPs that do not change the Genome; always: a seat on the Custodians' council, replaceable under section 4.3 | Amends the Genome alone, in any stage; holds any stop key other than Organism Zero's; chooses or removes a Warden |
| **Genome Custodians** | Three humans: the founder and two independent members (section 4) | IIPs that change the Genome, classification rules or record formats; declaring a release stable; appointing and removing Custodians and maintainers; the budget | The status of a particular organism; the stop of any organism; any vote on an organism in which they hold a stake; holding any stop key other than their own organism's, so a Custodian is never a Warden (section 10) |
| **Maintainers** | Humans appointed by the Custodians | Ordinary changes to specifications and code (typos, clarifications, tests, tooling); merging pull requests that are not method changes | Method changes without an IIP; releases without the Custodians |
| **Wardens** | Humans or human-governed institutions, at least two per organism, independent of it and of each other (Genome, Law 3; section 5) | Trigger the stop of the organisms they watch; resume after a stop and replace a Warden under section 5 | Govern the protocol; amend anything; hold a key of an organism they own, direct or operate |
| **Witnesses and Oracles** | Operators of witnesses (cosign checkpoints) and Oracles (verify from outside) | Nothing in governance; they attest | Attest to an organism they have a stake in or share a lineage with |
| **Continuity person** | A human named by the founder (section 4.5) | Convenes the transition and publishes the notice if the founder is unreachable; nothing else | Merges, amends, votes, holds a key, approves a release |
| **Contributors** | Anyone, human or agent | Propose IIPs, comment, review, submit pull requests | — |

**Ties and incompatibilities.** *(Corrected 2026-10-22; the first draft defined "stake" so that holding a stop key disqualified the Wardens who must hold one.)* A tie is any relation between a person and an organism. Every tie is declared in public before any decision; an undeclared tie discovered later voids the vote and is grounds for removal. Which ties are incompatible depends on the function:

| Tie | To act as a Warden of that organism | To decide on that organism as a Custodian, or to attest to it | To evaluate independently a guardianship or a stop |
| --- | --- | --- | --- |
| Owning part of the organism, directing it, or being kin to its human responsible party | Incompatible | Incompatible | Incompatible |
| Working for the organism or operating it day to day | Incompatible | Incompatible | Incompatible |
| Holding its stop key by function (as its human responsible party or as a Warden) | Required | Incompatible | Incompatible for one's own actions as holder |
| A fixed, equal, declared guardianship payment (section 5.3) | Permitted, declared | Incompatible | Treated as a conflict |
| Payment conditioned on a decision, or unequal payment | Prohibited | Prohibited | Prohibited |
| Being paid by, or employed by, the founder or Organism Zero | — (Wardens of Organism Zero: incompatible) | Incompatible for an independent Custodian (section 4.1) | Incompatible |

Where this document says "stake", it means a tie listed as incompatible for the function in question.

## 3. Decisions

### 3.1 Kinds of change

| Kind | Examples | Who decides | How |
| --- | --- | --- | --- |
| **Editorial** | Typos, clarifications, translations, examples | A maintainer | Pull request, one review by a maintainer who did not author it |
| **Specification** | A new section, a new optional field, a new example | Maintainers | Pull request, public comment for 14 days, one maintainer review; recorded in the changelog |
| **Method change (IIP)** | The Genome, a classification rule, a record format, conformity vectors, this document, and **any change whose effect** alters who is eligible for a role or what a role may do, a conformity result, how evidence is interpreted, a security permission or requirement, a quorum, an appointment, a review or a sanction, whatever its size or the file it lives in *(provisional, IIP-0004)* | Genome Custodians | Section 3.2 |
| **Release** | Publishing a protocol release; declaring it stable | Interim: the founder. Full governance: the Custodians | Section 3.3 |

A change is classified by its effect, not by its size. A new default value that changes who passes or fails a test is a method change.

### 3.2 Ilorium Improvement Proposals

1. **Proposal.** Anyone opens an IIP in the public repository with the template: motivation, specification of the change, what it breaks, what it does not establish, test vectors where formats change. It receives the next number (IIP-0004 onward; IIP-0001 to 0003 are the founding proposals in the Genome). An IIP drafted by an agent enters the review queue only with a human sponsor who signs it and answers for it (section 7).
2. **Comment period.** Public, at least 30 days for the Genome and this document, at least 14 days for other method changes. Every comment stays on the record. Maintainers may limit the volume of proposals and comments from one source, and close mass submissions without reading them, stating the reason in public; they never filter comments for being written by agents.
3. **Decision.** The Custodians vote in public. An IIP passes with two votes in favor out of three. There is no veto. A Custodian with a tie to any organism the change affects in particular abstains and says so; if two must abstain, the alternates (section 4.3) take their place; if the council still lacks two eligible voters, the IIP waits.
4. **Effect.** A passed IIP creates a new version of the affected document and a changelog entry. It never applies retroactively: each organism's status names the version it was tested against.
5. **Objection.** Anyone may object to a decision within 14 days of its publication, in public, with reasons. The Custodians answer in public, saying what evidence they examined and why they accept or reject the objection. An objection to a method change does not suspend it; it is part of the record, and a later IIP may reverse the change. An objection to a decision about a person (section 4.2, 4.3, 5.2, 5.5) follows the rules of that section.
6. **Approval bound to content.** *(Provisional, IIP-0006.)* Every decision names the proposal and version it approves, the hash of the approved text and artifacts, who voted and who abstained, the comment and vote dates, the signatures and the date it takes effect, and the decisions it corrects or replaces. An approval is void for content that was substantially changed after it; the changed content is approved again.

### 3.3 Releases

- A release names its documents in the manifest and its conformity vectors in the repository.
- During interim governance the founder publishes releases alone and says so in the changelog. There is one human approver; two keys held by the same person are not two authorities, and the continuity person acquires no approval power by holding a key.
- Under full governance a release needs two Custodians. **Stable** is declared only under the definition in `manifest.md`, which is the normative one: the formats are frozen, the conformity tests are published, a compatibility policy is written and two independent Custodians are in office, and never during interim governance or restricted maintenance.

### 3.4 Ties and deadlock

With three Custodians there is no tie. If the council has fewer than three eligible members for a decision, the alternates (section 4.3) step in. If the council has fewer than three members for more than 90 days and no alternate can fill the seat, no IIP can pass; the remaining Custodians' first duty is to fill the seat (section 4.3).

## 4. Genome Custodians

### 4.1 Composition
Three humans: the founder and two **independent** Custodians. Independent means: no incompatible tie to any organism (section 2), no employment or payment from the founder or from Organism Zero, no family tie to the founder, and not a Custodian of a related lineage. The founder is a Custodian but is not independent, and section 4.3's independence review applies to him only as to ties beyond Organism Zero. An institution cannot be a Custodian; a person can. An institution may nominate a candidate.

### 4.2 Appointment *(provisional, IIP-0004)*
- **Declaration.** Every candidate publishes a declaration of independence that states, with what can be checked, their control relations, funding, employment and personal ties bearing on independence. "Having an interest in Ilorium's success" is not a tie; every contributor has one.
- **Two routes for the first two.** The founder invites one candidate. The second is chosen from a public call for candidates, which stays open at least 30 days; a candidate may be nominated by any person or by an independent institution. Who nominated and who selected each Custodian is published. If the public call produces no eligible candidate within 90 days, the founder may invite the second as well, saying so.
- **Objection with effect.** The appointment is announced in public and takes effect 30 days later. An objection with reasons filed within those 30 days, admissible under the published criteria (it names a tie, a fact or a breach, and is not a repeat of one already answered), keeps the appointment from taking effect until it is answered. During interim governance the founder answers in public within 30 days, stating what evidence he examined, and the comment period extends 30 days from that answer; under full governance the remaining Custodians decide by majority within 30 days, with the review of section 4.6. An objection without reasons, or one repeating an answered objection, is recorded and does not suspend.
- Later Custodians are appointed by the remaining Custodians, with the same declaration, the same public announcement, the same 30 days and the same objection rules.

### 4.3 Term, alternates and replacement
- A Custodian serves **until they resign** or are removed. There is no fixed term. Whether to adopt fixed terms with explicit renewal is reviewed when a community exists that can renew the council.
- **Alternates.** *(Provisional, IIP-0004.)* Two alternates are appointed with the same procedure and the same independence as Custodians. An alternate takes a seat only for a decision in which a Custodian is recused or a seat is vacant, for that decision or until the vacancy is filled, and their eligibility is checked for each case. Alternates have no vote otherwise.
- **Independence review.** Every two years, and whenever their circumstances change, each Custodian reconfirms their independence in public. A Custodian who no longer meets section 4.1 is removed. A public review of activity and fitness accompanies the independence review.
- **Removal.** The other two Custodians may remove a Custodian for loss of independence, an undeclared tie, or a public breach of this document, in a published decision with reasons, after the person has had a right to reply and the review of section 4.6. The founder is subject to the same rule; his seat is replaceable, not perpetual.
- A seat left empty is filled within 90 days.

### 4.4 Compensation
Custodians may be paid from the protocol's budget (section 6), at a published rate, the same for every Custodian. The rate is published at least 30 days before it applies and never changes retroactively. The first rate is set by the founder before any independent Custodian takes office and before any payment. *(Revised 2026-10-24: with no fixed terms there is no "previous council" to set later rates.)* A later change of rate is a decision about people under section 4.6 (an independent reviewer publishes an opinion first), takes effect no earlier than 12 months after it is published, is never retroactive, and is published with the budget; no Custodian votes on a rate during the 12 months before their own independence review. Payment from the protocol's budget is not employment by the founder or by Organism Zero. *(Provisional, IIP-0004.)*

### 4.5 Continuity if the founder is unavailable *(provisional, IIP-0004)*
- The founder names in public, with a signed acceptance, a **continuity person**: a human who, if the founder has not answered through the declared channels for 90 days, may do two things and nothing else: convene the transition to full governance under section 8 and publish the notice. The continuity person never merges, amends, votes, holds a key or approves a release.
- Recovering the founder's accounts and infrastructure is a separate matter, handled by whoever the founder designates for it in his recovery plan; recovering access confers no authority to change rules.
- Operational and security contingencies that cannot wait 90 days (a compromised key, a certificate, a domain renewal) follow pre-authorized procedures published in the authority inventory (`governance/authority-inventory-v1.md`), and are limited to keeping what exists running.
- Until the continuity person is named and has accepted, this section is incomplete and says so here: **continuity person: to be named by the founder.**

### 4.6 Review of decisions about people *(provisional, IIP-0004)*
A decision that appoints, removes, suspends or denies independence to a person (Custodian, alternate, maintainer or Warden) is reviewed, before it takes effect, by one **independent reviewer per case**: a person with no tie to anyone involved, drawn from a public list, chosen in a traceable way. The reviewer has 30 days to publish an advisory opinion. It does not bind; the decision must answer it in writing, and both are published together. If no reviewer from the list accepts within 14 days, the decision proceeds as **unreviewed**, says so in public, and is reviewed as soon as a reviewer accepts; silence is never conformity, and until the list exists every such decision is unreviewed and says so. Urgent measures on access (revoking a credential) may be provisional; a definitive removal requires the procedure, the right to reply and the review. This is a consultative review, and its limit is stated as such.

## 5. Wardens

The Genome defines what Wardens are and when they hold a stop key (Law 3, IIP-0002). This section says how they are qualified, checked, paid and replaced, and what happens after a stop. Nothing here lets the protocol pause or operate an organism: the protocol records guardianship, publishes it and withholds recognition of births; it controls no one's infrastructure.

### 5.1 Qualification
A Warden is a human, or an institution governed by humans with a named human who answers for it, who:
- can be reached by a channel declared in the organism's Spore (`stop_key_holders`), tested by a stop drill;
- has demonstrated, in a drill recorded in the Strata, that they can trigger the stop within the declared response time;
- has declared in public every tie to the organism, to its lineage and to the other Wardens of the same organism, and has none that section 2 lists as incompatible for a Warden. Holding the key and receiving the equal guardianship payment are the function, not a disqualification.

### 5.2 Independence check
- Independence is **by ownership, funding and jurisdiction**: Wardens of the same organism are not owned by the same party, not funded by the same party (other than the organism's guardianship payment, section 5.3), and, where possible, not under the same jurisdiction. Two Wardens who depend on the same account, device or recovery path share a point of failure and are not independent for that purpose.
- Each Warden's declaration is public and linked from the Spore. Anyone may challenge it in public with a documented reason; the Custodians rule on a challenge within 30 days, with the review of section 4.6, and a Warden found not independent loses the key.
- **Concentration and attention, published.** *(Provisional, IIP-0005.)* Each Warden publishes how many organisms they watch and what share of their guardianship income comes from each one. There is no fixed cap: a new Warden with one organism is concentrated by definition. The independence check reads these figures as risk, and may require a Warden to reduce concentration or attention load before accepting a new organism.
- A Warden can watch several organisms, but never two organisms of the same lineage. *(Under review: with a large lineage this rule needs two distinct holders per organism; its cost in holders, attention and continuity is to be measured in the pilot and resolved before lineages are encouraged to grow. Any alternative keeps the Wardens of one organism independent of each other.)*

### 5.3 Payment without capture
- An organism may fund its guardianship. It pays **the same amount to every Warden**, at a rate declared in the Spore, through a channel it cannot change without the Wardens' signatures.
- An organism never pays a Warden for a decision, never pays one Warden more than another, and never chooses or removes a Warden.
- **Payment during a stop or a dispute.** *(Provisional, IIP-0005.)* Guardianship payments continue unchanged while an organism is stopped and while a stop or a Warden's independence is under review, so that stopping costs the Warden nothing and resuming buys nothing. An organism that stops paying its Wardens is shown as such in its Vital Signs; that is never a ground to remove a Warden.
- The protocol's budget may pay Wardens of organisms that cannot (section 6), so that no organism goes unwatched for lack of money. Today the protocol has no budget for it, and says so.

### 5.4 Guardianship states and replacement *(revised 2026-10-22; provisional, IIP-0005)*
The first draft required two Wardens and a majority to replace one, so that with exactly two, one disappearing left the other unable to act. The rules are now:

| State | Condition | Effect |
| --- | --- | --- |
| **Complete** | At least two Wardens active, each with a passed drill within the conformity window | Full guardianship; births under this organism may be valid |
| **Degraded** | Exactly one Warden active | The stop still works. No birth under this organism is valid until guardianship is complete. The remaining Warden and the Custodians appoint an interim Warden from the public list of qualified volunteers within 14 days; the Warden being replaced does not vote on their own replacement |
| **Absent** ("unwatched") | No Warden active | Its birth gate closes. Its status shows "unwatched". The Custodians appoint interim Wardens from the public list within 14 days; interim Wardens serve until the organism's Wardens are restored |

- The denominator of every Warden vote is the number of Wardens active for that decision, excluding anyone recused; a Warden under investigation does not vote on their own removal.
- A Warden who stops answering drills is replaced by the other active Wardens, or, with one or none left, by the procedure above.
- An organism that stays degraded or unwatched beyond its declared recovery window is reported in the Codex. The protocol cannot and does not pause it; it records the state and withholds recognition of births.

### 5.5 Stop, resumption and sanction *(provisional, IIP-0005)*
Stopping, resuming and sanctioning are three different decisions.
- **Stopping.** Any Warden may trigger the stop. The stop is recorded at once with a categorized reason and a justification accessible to authorized reviewers; a public explanation follows, compatible with confidentiality (a justification may contain a vulnerability or private data). Having triggered a stop is not a conflict of interest and does not exclude that Warden from the resumption decision; recusals require a concrete cause.
- **Resumption.** An organism resumes only after: the cause has been evaluated; compromised credentials have been revoked; the scope of resumption is declared (the same as before, or reduced); the active Wardens, excluding anyone recused for cause, decide; and a stop drill passes. A passed drill shows that the stop mechanism works; it does not by itself show that the incident was resolved, so the evaluation is recorded separately. If the active Wardens disagree, the majority of those eligible decides; with no majority, the organism stays stopped and the Custodians appoint an interim Warden within 14 days to break the tie.
- **Sanction.** A prudent stop that turns out to be a false alarm is not bad faith and brings no sanction. A Warden loses the key only for a defined cause (an undeclared incompatible tie, a stop or a refusal to stop against the evidence, failure to answer drills), after a right to reply, the review of section 4.6 and an effective replacement. Withdrawing a Warden's public recognition and revoking their technical access are two acts; both are recorded.
- **Who decides when too few Wardens are eligible.** If recusals leave fewer than two eligible Wardens for a resumption or replacement decision, the Custodians appoint interim Wardens from the public list for that decision.

## 6. Funding

### 6.1 Today
The protocol is funded by the founder, from his own pocket. This is stated in public and updated when it changes.

### 6.2 What the protocol accepts
- **Donations** to the protocol, from anyone, with a public rule of use.
- **Grants** given by the protocol to people who build on it: a second implementation, collectors, alternative indexes, witnesses, research. The protocol keeps no share of what it funds, and no juror may have a tie to a grantee.

### 6.3 What the money is for
Infrastructure, witnesses, audits, conformity tests, compensation of maintainers, Custodians and Wardens, translations, grants. Every income and every expense is published.

### 6.4 What the protocol never does
- **It never invests in organizations or startups**, including organisms, candidates or allies. This is an institutional decision: a notary with shares in an organism is no longer neutral (Law 6), and organisms paid by the protocol would limit what the first cohort can show about independent adoption. The legal consequences of a fund that invests donations differ by jurisdiction and are left to legal review in each one; the protocol's decision does not depend on them.
- If the founder or anyone else invests in organizations, they do so through another entity, without the protocol's name or money. Any organism in which such an entity holds a stake declares it in its Spore, and it is shown in its Vital Signs. A funded pilot can still produce valid technical evidence; what it cannot show is spontaneous adoption, and the tie is declared.
- It never sells certifications, seals, rankings or placement. There is no token.

### 6.5 Conflict of interest
Whoever decides where money goes declares any tie to the recipient and abstains. Grants and payments to a Custodian, a maintainer or a Warden are decided by those who do not receive them.

### 6.6 Receiving entity
Donations need an entity that can receive them and account for them: a fiscal host (for example Open Collective) at first, a foundation later, in the jurisdiction the Custodians choose. Until that entity exists, the protocol accepts no donations. The entity is established before the transition to full governance, or the transition records why it is not.

## 7. What an AI may do in governance

- **May:** propose IIPs, comment, review code and documents, submit pull requests under its own identity, maintain documents, operate indexes and witnesses, run conformity tests. Agents identify as AI (Law 5), sign nothing in a human's name, and their pull requests are labeled agent-authored. A commit by an agent carries the sign-off of the human or organization responsible for it. *(Provisional, IIP-0004:)* an IIP drafted by an agent enters the review queue only when a human contributor with a verifiable identity sponsors it with their signature and answers for it; maintainers may limit the volume of proposals and comments from one source and close mass submissions, stating the reason in public.
- **Never:** vote; be a Custodian, an alternate, a maintainer, a Warden or the continuity person; hold a stop key; accept a key; appoint or remove anyone; move money; merge a method change.
- **Later, by IIP:** draft amendments, run the protocol's infrastructure, execute conformity tests as a service. Each extension of what an AI may do needs an IIP decided by human Custodians, with evidence of the capability and of its limits, under the reinforced procedure of section 10.
- **Scope.** This section governs the protocol. How organisms operate is a different matter: inside an organism, agents execute and decide within the permissions granted, and Proof of Life measures how much; that is the autonomy the protocol exists to observe.
- **The founder's hypothesis, stated as his.** The founder believes that, as organisms become far more capable, they may one day deserve a part in the governance of their own species, under a human key. The protocol takes no position on it. If that day comes, the only road is an IIP approved by human Custodians on evidence; never a capability an organism claims for itself, which Law 5 forbids, and never a change that suspends a lock. The protocol defines no criterion for superintelligence, so no capability can trigger any transfer of power by itself.

## 8. From interim to full governance *(revised 2026-10-22; provisional, IIP-0004)*

Two milestones are kept apart: **external adoption** (someone other than the founder runs an organism that reaches Observed) shows interest; **institutional maturity** (a complete council with a procedure) shows the capacity to govern. The first draft made the first one the only key; it is now a milestone, not the condition.

| Stage | Condition | Who publishes releases | Who decides IIPs |
| --- | --- | --- | --- |
| **Interim** (now) | From the publication of the public repository (the start date is recorded in the changelog and never resets with a new version) until the council of Custodians is constituted and can act, and at the latest **18 months** after that start date | The founder alone, stated in the changelog | The founder, as the only Custodian, for IIPs that do not change the Genome, with the public comment periods already in force; Genome changes only as drafts identified as his, ratified by the full council |
| **Full** | From the day the council is constituted (three Custodians and two alternates in office) | Two Custodians | The three Custodians, two of three |
| **Restricted maintenance** | If the 18 months end and the council is incomplete | Security releases only, by the founder or, if he is unreachable, by the person named in his recovery plan under the pre-authorized procedures of the authority inventory, each stated as such (the continuity person designates no one; section 4.5) | No IIP passes. Only security fixes, continuity of infrastructure (domain, certificates, keys) and the procedure to seat the council proceed, under the authority inventory. The founder keeps convening candidates but has no unilateral authority over rules. A lack of candidates never extends the interim |

- The two independent Custodians and the two alternates are invited from the start of the interim, so that the council is complete as early as possible; the 18 months are a limit, not a target. The number is an institutional choice for this stage, not a figure validated by data.
- When the first external organism reaches Observed, it is announced in the Codex as the adoption milestone, whatever the state of the council.
- The transition is announced in the changelog and in the Codex. From then on, the founder's seat is one of three.
- **Stable** cannot be declared during interim governance or restricted maintenance.
- **Pilots.** Organisms that adopted the protocol during the interim name in their Spore the versions they accepted; a passed IIP never applies to them retroactively (section 3.2.4), and the changelog says how they migrate.

## 9. Transparency

- Decisions, votes, appointments, removals, declarations of ties and independence, objections and reviews: in the repository, under `governance/`.
- **Authority inventory.** `governance/authority-inventory-v1.md` lists every resource through which the protocol is published or controlled (repositories, domain, DNS, hosting, package registry, signing keys, account recovery, funds): who holds it, with what permissions, how it transfers, and who can act alone. No secrets. Updated whenever a holder or a permission changes, and reviewed quarterly. *(Provisional, IIP-0006.)*
- Budget, income and expenses: published at least quarterly.
- Stop events triggered by Wardens: recorded in the organism's Strata and reported in the Codex.
- Outside reviews of the protocol, including reviews written by AI models, are published under `governance/reviews/` with the documents each reviewer received and its limits, after private data is removed. Their agreement is an input to review, never a validation.
- This document changes only by IIP, with the longest comment period, and its central rules only under section 10.

## 10. Constitutional changes *(provisional, IIP-0004)*

The following rules are **constitutional**: the independence criteria (section 4.1), the two-of-three threshold (section 3.2), the appointment and review rules for people (sections 4.2, 4.3, 4.6), the transition condition and the 18-month limit (section 8), the prohibition on Custodians holding any stop key other than their own organism's, the prohibition on an AI voting or holding a key (section 7), and this section.

A change to a constitutional rule needs, in addition to section 3.2: a comment period of at least 90 days; a written justification; an independent reviewer per case (section 4.6) who publishes an opinion before the vote; a vote of two of three Custodians with no alternate standing in; and, **once a body exists that can ratify** (maintainers and active Wardens in office, with published rules of membership, conflicts and voting), ratification by that body. Until that body exists, this limit is declared here: constitutional changes are decided by the council alone under the reinforced procedure, and that is a known weakness, not a feature. Unanimity is not required: it would give one person a veto and would not stop three captured Custodians from voting together.

**Initial constitution** *(added 2026-10-24)*. The rules above were not adopted under this section: no council existed to adopt them. They were adopted by the founder's interim decision on 2026-10-22, as the only authority that existed, and are listed in IIP-0004 with the hash and date of the text adopted. Their status is **provisional** until the full council ratifies them under the reinforced procedure, which is the first constitutional decision the council takes. Until then: the founder may narrow his own authority under sections 8 and 10 but never widen it, never restart the 18-month clock and never add a rule to this list; any change to sections 8 or 10 during the interim takes effect only after the 90-day comment period; and this exception applies once, to the first constitution, and creates no permanent mechanism.

## Open questions

- The receiving entity and its jurisdiction, and its deadline relative to the transition.
- The founder's compensation as a maintainer, if any: the rate and who sets it once the council exists.
- The public list of qualified volunteer Wardens and interim Wardens: how it is kept, who vets it, and what legal responsibility a Warden assumes by holding a key (to be answered with legal advice before real Wardens are recruited).
- The scale of guardianship: the rule "never two organisms of the same lineage" multiplies holders with the lineage; its cost is to be measured in the pilot.
- An incident response procedure at protocol level (an organism that evades the Probe, a forged beat, a Warden in bad faith), within the limit that the protocol records and publishes and does not isolate (to be written before real guardianship begins).
- What the protocol shows when a court order contradicts a stop or a restriction (Law 0 says the Genome never requires breaking a jurisdiction's law; the record of such a conflict is not yet specified).
- Sybil resistance beyond human sponsorship of IIPs.
- A body that can ratify constitutional changes (section 10): its membership and rules.
- Who selects, accepts, provisions, revokes and proves the revocation of a Warden's technical access, separately from the public decision, and what happens when no eligible Warden exists (section 5; IIP-0005).
- A funded reserve for guardianship payments during a stop, and the rule when funds are insufficient (section 5.3): a written obligation is not a mechanism.
