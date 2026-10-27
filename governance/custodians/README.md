# Genome Custodians

governance-v1.md, section 4. Three humans: the founder and two independent Custodians. An institution cannot be a Custodian; a person can.

## Seats

| Seat | Holder | Since | Declaration of independence | Status |
| --- | --- | --- | --- | --- |
| 1 | The founder (pseudonym "Seldon"; GitHub: `@fseldon`) | 2026-10-21 | Not applicable: the founder's seat is the founder's (section 4.1). Stake in Organism Zero, declared. | In office |
| 2 | — | — | — | Vacant |
| 3 | — | — | — | Vacant |

Interim governance is in force while seats 2 and 3 are vacant (governance-v1.md, section 8; governance/decisions/0001-interim-governance.md).

## How a Custodian is appointed

1. The founder (for the first two) or the remaining Custodians (later) invite a person who meets section 4.1: no stake in any organism, no employment or payment from the founder or Organism Zero, no family tie to the founder, not a Custodian of a related lineage.
2. The appointment is announced in public: a pull request adds the person's declaration of independence to this directory as `YYYY-MM-DD-seat-N-<handle>.md` and a post in Discussions, category Governance, links to it.
3. **30 days** pass. Anyone may object in public, with reasons, on the Discussion or on the pull request.
4. If the appointment stands, the pull request merges, the table above is updated, and the person's GitHub login is added to the team `@ilorium-protocol/genome-custodians`. When the team has two independent members, `CODEOWNERS` and the `main` ruleset move to two approvals (GOVERNANCE.md).

A Custodian serves until they resign or are removed (section 4.3). Every two years, and whenever their circumstances change, each Custodian reconfirms independence in public with a new declaration file. A seat left empty is filled within 90 days.

## Template: declaration of independence

```markdown
# Declaration of independence — seat N

- Name: <legal name, or the name you are publicly known by>
- GitHub: @<login>
- Date: YYYY-MM-DD
- Appointment takes effect: YYYY-MM-DD (30 days after this announcement)

I declare, in public, that today:

1. I hold no stake in any organism of the species: I do not own part of one,
   am not paid by one, do not work for one, hold no stop key of one, and am
   not kin to the human responsible party of one.
2. I am not employed or paid by the founder or by Organism Zero.
3. I have no family tie to the founder.
4. I am not a Custodian of a related lineage.
5. I will declare any change to the above in public before taking part in any
   decision, and I will reconfirm this declaration every two years.

I understand that an undeclared stake discovered later voids my vote and is
grounds for removal (governance-v1.md, sections 2 and 4.3).

Signed: <name>
```

The declaration is committed by the person themselves, with their own sign-off and a signed commit.
