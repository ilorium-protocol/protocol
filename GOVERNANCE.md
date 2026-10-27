# Governance of this repository

This file is a summary. The normative text is [governance-v1.md](governance-v1.md) (release 1.0, draft). If the two disagree, governance-v1.md wins.

> No organism governs the species. Humans do, in public, with evidence.

## Status

Release 1.0, draft. No organism is running. **Interim governance** is in force (governance-v1.md, section 8): the founder is the only Genome Custodian, merges every change to `main` and publishes every release, and says so in the changelog. Public comment periods already apply.

Interim governance ends when the council of Custodians is constituted (three Custodians and two alternates in office) and can act, and at the latest **18 months** after the start date recorded in the changelog; the date never resets with a new version. The two independent Custodians and the two alternates are invited from the start. If the 18 months end and the council is incomplete, the protocol enters **restricted maintenance**: security fixes, continuity of infrastructure and the procedure to seat the council only; no IIP passes. The first external organism reaching Observed is an adoption milestone, not the end of the interim.

The rules adopted by the founder on 2026-10-22 (IIP-0004, IIP-0005, IIP-0006 and governance-v1.md section 10, the initial constitution) are **provisional** until the full council ratifies them. A Custodian is never a Warden. Approvals bound to the exact content hash are described in the documents but are **planned, not yet enforced** by any workflow here (see [governance/decisions/0004-provisional-rules-2026-10-22.md](governance/decisions/0004-provisional-rules-2026-10-22.md)).

## Who decides what

| Kind of change | Examples | Who decides | How |
| --- | --- | --- | --- |
| Editorial | Typos, clarifications, translations, examples | A maintainer | Pull request, one review by a maintainer who did not author it |
| Specification | A new section, a new optional field, a new default | Maintainers | Pull request, public comment for 14 days, one maintainer review, changelog entry |
| Method change (IIP) | The Genome, a classification rule, a record format, conformity vectors, governance-v1.md | Genome Custodians | [iips/README.md](iips/README.md) |
| Release | Publishing a protocol release; declaring it stable | Interim: the founder. Full: two Custodians | Tag `protocol/*`, release workflow |

During interim governance the founder fills every "who decides" column above.

## How governance-v1.md maps to this repository

| governance-v1.md | Where it lives in this repository | Enforced by |
| --- | --- | --- |
| Genome Custodians (sections 2, 4) | [CODEOWNERS](CODEOWNERS): every protected path points to the Custodians. Interim: `@fseldon`. Later: `@ilorium-protocol/genome-custodians`. | GitHub code owner review, required by the ruleset |
| Interim governance (section 8): only the founder merges and publishes | Org ruleset `main` (`org/rulesets/main-protection.json` in the deployment kit): no deletion, no force push, pull request required, one approval with code owner review, required status checks, signed commits. Bypass: organization admins may merge a pull request without a separate approval (`bypass_mode: pull_request`), because the only reviewer cannot approve his own pull request. Every change still goes through a pull request with every check green. | GitHub rulesets |
| End of interim governance (section 8) | The admin bypass is removed and the required approvals move to two, with code owner review by the Custodians' team. Recorded in `governance/decisions/`. Restricted maintenance (18 months, council incomplete): only security fixes and infrastructure continuity merge; the authority inventory ([governance/authority-inventory-v1.md](governance/authority-inventory-v1.md)) lists who may act alone. | GitHub rulesets, CODEOWNERS |
| IIP process (section 3.2) | [iips/](iips/): one file per proposal, template, numbering from IIP-0004. Label `iip`. Pre-IIP conversation in Discussions, category Proposals. Votes announced in Discussions, category Governance. | Labels, Discussions, pull request review |
| Method change needs an IIP (section 3.1) | Label `method-change`. A pull request that changes a protected path must reference an accepted IIP (`IIP-NNNN`) in its title or body; the security agent flags one that does not (planned until configured). | CODEOWNERS, review, security agent review (advisory) |
| Editorial change (section 3.1) | Pull request, one review by a maintainer who did not author it. Label `editorial`. Interim: the founder reviews and merges. | Ruleset (one approval) |
| Specification change (section 3.1) | Pull request, label `spec`, 14 days of public comment on the pull request, one maintainer review, changelog entry. | Ruleset, `translation-changelog` workflow |
| Releases (section 3.3) | Tags `protocol/*` and `v*` can be created, moved or deleted only by organization admins (`org/rulesets/tags-protocol.json`), must be signed, and trigger `.github/workflows/release.yml`, which needs the `release` environment (founder approval). Releases are marked prerelease while the protocol is draft. | GitHub rulesets, environment protection |
| What an AI may do (section 7) | Bots read, comment, open issues and open pull requests. No bot merges to `main`, approves a CODEOWNERS path, publishes a release or holds a production secret. Agent pull requests carry the label `agent-authored`; agent commits carry the sign-off of a responsible human or organization (`dco` workflow). The security agent's GitHub App has read permissions plus write on issues and pull request comments only. | App permissions, `dco` workflow, workflow `permissions:` blocks |
| Transparency (section 9) | [governance/](governance/README.md): decisions, votes, appointments, declarations, security reports. | Pull requests on `main` |

## The three lines

1. Anyone can propose anything: an issue, a Discussion, a pull request, an IIP.
2. Method changes go through an IIP decided by human Genome Custodians, in public, after a comment period.
3. The three locks (germline, birth gate, stop) cannot be removed. Removing one would need a new major version and a new Genome, which is a related lineage, outside the species.

## Standing decisions

- [governance/decisions/0001-interim-governance.md](governance/decisions/0001-interim-governance.md)
- External reviews and what became of them: [governance/reviews/](governance/reviews/README.md)

## Seats

See [governance/custodians/README.md](governance/custodians/README.md). Seat 1: the founder, in office. Seats 2 and 3: vacant.
