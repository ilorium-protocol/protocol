# Decision 0001: Interim governance

- Date: 2026-10-21
- Decided by: the founder, as the only Genome Custodian
- Kind: standing decision, recorded from governance-v1.md (release 1.0, draft), section 8
- Status: in force

## Decision

1. **Interim governance is in force.** The protocol is under the interim stage described in governance-v1.md, section 8, from the first public release.
2. **The founder is the only Genome Custodian.** Seat 1 is held by the founder. Seats 2 and 3 are vacant (governance/custodians/README.md).
3. **The founder alone merges to `main` and publishes releases**, and says so in the changelog of every release. Public comment periods (30 days for the Genome and governance-v1.md, 14 days for other method changes, 14 days for specification changes) are already in force.
4. **Stable is not declared** during interim governance.
5. **The protocol is funded by the founder.** No donations are accepted until a receiving entity exists (governance-v1.md, section 6).

## What the repository enforces

- `CODEOWNERS` names the founder for every path, and explicitly for the protected paths: `/genome/`, `/governance-v1.md`, `/governance-v1.es.md`, `/manifest.md`, `/manifest.es.md`, `/schemas/`, `/vectors/`, `/iips/`, `/CODEOWNERS`, `/.github/`.
- The organization ruleset for `main` requires a pull request, one approval with code owner review, resolution of review threads, required status checks, signed commits, and forbids deletion and force push. Organization admins may merge a pull request without a separate approval (bypass mode `pull_request`), because the only reviewer cannot approve his own pull request. Every change still goes through a pull request with every check green.
- The organization ruleset for tags `protocol/*` and `v*` allows only organization admins to create, move or delete them, and requires signatures. The release workflow runs only on those tags and needs approval in the `release` environment.
- No bot merges, approves, publishes or holds a production secret. Bots read, comment, open issues and open pull requests.

## What ends this decision

Interim governance ends when the first organism founded by someone other than the founder reaches the status Observed on the Radiant (governance-v1.md, section 8). Before that, the founder invites two independent Custodians, announced in public with a 30-day notice (section 4.2). When two independent Custodians are in office:

- `CODEOWNERS` entries move to the team `@ilorium-protocol/genome-custodians`;
- the `main` ruleset moves to two required approvals and the admin bypass is removed;
- releases need two Custodians.

That transition is recorded as a new decision in this directory and announced in the changelog and in the Codex.

## Sources

- governance-v1.md, sections 3.3, 4, 6.1, 6.6, 8 and 9.
- README.md, "This repository".
