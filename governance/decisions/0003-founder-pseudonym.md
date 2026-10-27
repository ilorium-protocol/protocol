# Decision 0003: The founder signs with a persistent pseudonym

- Date: 2026-10-22
- Decided by: the founder, as the only Genome Custodian
- Kind: standing decision
- Status: in force

## Decision

1. **The founder signs and publishes as "Seldon"** (`user.name`; GitHub account `fseldon`). The pseudonym is tied to a signing key (`ed25519-sk`, on a hardware key, with a backup key). The signing key is the identity: whoever holds it is Seldon.
2. **Why a pseudonym.** The asymmetry. A pseudonym can later be tied to a person, verifiably, with a message signed with the same key. Starting with a legal name cannot be undone. The pseudonym is not a mask: the protocol says in public that a human and AI agents built and deployed it.
3. **Review and signing account.** Everything is signed and reviewed with `fseldon`. `CODEOWNERS` and the deployment environments name `@fseldon`. The founder's second GitHub account (second owner of the organization, for recovery) is not used in public and is **not** used to approve the founder's own pull requests: that would be an independent review in appearance only, because it is one person.

## Conditions the founder accepted

1. A pseudonym is not anonymity: privacy on the domain's WHOIS record; accounts and emails are not cross-linked with the founder's other projects; the personal account is not used in public.
2. Recovery is documented and a trusted person is named (a recovery plan; it holds no secrets in this repository).
3. The two independent Genome Custodians will be identifiable persons (governance-v1.md, section 4).
4. It is said in public that "Seldon" is a pseudonym and that a human and AI agents built the protocol (AUTHORS, GOVERNANCE.md, the site).
5. `CONTRIBUTING.md` accepts persistent pseudonyms tied to a verifiable signing key for the DCO.
6. The signing key is the identity, so a backup key is required.

## What the repository enforces

- `AUTHORS` names Seldon and points here. `CONTRIBUTING.md`, section "Sign-off and signatures", states the pseudonym rule.
- `CODEOWNERS` names `@fseldon`. The `main` ruleset requires signed commits.
- Commits by agents carry the agent's own identity and the `Signed-off-by` of the responsible human or organization (decision 0001, `CONTRIBUTING.md`).

## Sources

- governance-v1.md, sections 4, 7 and 8.
- `ilorium/founder-letter.md` (not part of the protocol).
