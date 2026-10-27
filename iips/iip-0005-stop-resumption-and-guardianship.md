# IIP-0005 · Stop, resumption and guardianship

| Field | Value |
| --- | --- |
| Number | IIP-0005 |
| Title | Stop, resumption and guardianship |
| Author | The founder (Seldon), with Claude (AI, identified as such) |
| Status | In comment from 2026-10-27 to 2026-11-26 (30 days). Discussion: https://github.com/ilorium-protocol/protocol/discussions/6 |
| Kind | Method change to `governance-v1.md`, section 5, and a specification note to the Spore (`stop_key_holders`) in `specs/evidence-format-v1.md` (30 days) |
| Affects | Governance sections 2 (ties), 5.1–5.5; the Spore; Vital Signs (guardianship state) |
| Decides | The founder, as the only Custodian during interim governance, in public, after the comment period |
| Does not touch | Law 3 of the Genome, IIP-0002 or any lock. The human stop key, "any one Warden can stop" and "no organism holds a key" stay as they are |

## Motivation

The first draft of section 5 contained one contradiction and two gaps, confirmed by the outside reviews and by the text:

- The definition of "stake" (section 2) made holding a stop key a stake, while section 5.1 required Wardens to declare no stake: a Warden could not be a Warden. Corrected on 2026-10-22 with a table of incompatibilities by function.
- With exactly two Wardens, if one disappeared the other was not a majority and could not replace them; the Custodians only intervened when all Wardens were gone.
- Any Warden could stop, and nothing said who could resume, what happens with an abusive stop, or how payments behave while an organism is stopped. One reviewer named the real risk: a Warden who threatens to stop in order to extort.

## Specification

The rules below are in `governance-v1.md`, marked *provisional (IIP-0005)*.

1. **Guardianship states (section 5.4).** Complete (at least two active Wardens with a passed drill), degraded (one: the stop works; no birth under the organism is valid; an interim Warden is appointed within 14 days), absent (none: "unwatched"; birth gate closed; interim Wardens within 14 days). The denominator of every Warden vote is the Wardens active for that decision, excluding anyone recused; no Warden votes on their own removal.
2. **Stop, resumption, sanction (section 5.5).** Three decisions. A stop is recorded at once with a categorized reason and a justification for authorized reviewers, with a public explanation after. Having stopped is not a conflict and does not exclude that Warden from the resumption decision. Resumption needs the cause evaluated, compromised credentials revoked, the scope declared, a decision by the eligible Wardens and a passed drill; a passed drill does not by itself show the incident was resolved. A prudent false alarm is not bad faith. Loss of the key needs a defined cause, a right to reply, an independent reviewer and an effective replacement; withdrawing recognition and revoking access are two recorded acts. Interim Wardens break ties and fill in when recusals leave fewer than two eligible.
3. **Payments during a stop or dispute (section 5.3).** Unchanged while stopped or under review; an organism that stops paying is shown as such and that is never a ground to remove a Warden.
4. **Concentration and attention, published (section 5.2).** Each Warden publishes how many organisms they watch and the share of guardianship income from each; no fixed cap; the independence check reads it as risk. Two Wardens that share an account, device or recovery path are not independent.
5. **Spore recommendation.** The Spore specification recommends, for organisms founded by humans, at least two `stop_key_holders` independent of each other by access and recovery; Vital Signs shows when there is only one. This is a recommendation, not a requirement: requiring it would change Law 3 and is outside this IIP.
6. **What the protocol never does here.** It does not pause, isolate or operate an organism. It records the guardianship state, publishes it and withholds recognition of births.

## What it breaks

Nothing in operation. It replaces "majority of Wardens" as the only replacement rule.

## What it does not establish

- The public list of qualified volunteer Wardens: how it is kept, who vets it.
- The legal responsibility a Warden assumes by holding a key, which needs legal advice before any real Warden is recruited.
- The scale rule ("never two organisms of the same lineage"), kept and marked under review; its cost is measured in the pilot.
- An incident response procedure at protocol level, to be written before real guardianship begins.
- *(Added 2026-10-24.)* Who selects, accepts, provisions, revokes and proves the revocation of a Warden's technical access, separately from the public decision that appoints or removes them; and what happens when no eligible Warden exists on the list.
- *(Added 2026-10-24.)* A funded reserve so that "payments continue during a stop" is a mechanism, with the rule for insufficient funds; today it is a written obligation.

## Questions for commenters

1. Should a degraded organism keep any right to originate (for example, with an interim Warden), or is "no birth" right?
2. Is 14 days a workable deadline for interim Wardens before a volunteer list exists?
3. What categories of stop reason should the record allow?
4. Does keeping payments unchanged during a stop create its own incentive (to stop and keep being paid)? What would you add?
5. Who should hold and revoke a Warden's technical credentials, so that the public decision and the access control are two acts and neither is the organism's?

## Test vectors

The guardianship state will need vectors in the Vital Signs schema (`complete`, `degraded`, `absent`) when IIP-0006 settles how evidence is read; none in this IIP.
