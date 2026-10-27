# Authority inventory v1.0

Version 1.0 · 2026-10-22 · Draft · Provisional under IIP-0006

Updated 2026-10-27: provisional software signing key (decision 0005); second factors and repositories corrected.

Every resource through which the Ilorium protocol is published or controlled: who holds it, with what permissions, how it transfers, and who can act alone. Required by Governance, section 9. **No secrets:** no passwords, recovery codes, private keys, tokens or seed phrases appear here or anywhere in the repository. Updated whenever a holder or a permission changes; reviewed quarterly.

**Honest summary.** During interim governance one person, the founder, can act alone on every resource below. Two votes on paper do not bind a single account that can replace a binary, change the domain or publish a release. This inventory exists so that the fact is public, so that each approval can be checked against what was actually published, and so that the transition to full governance has a list of what must change hands.

| Resource | What it controls | Holder(s) today | Permissions | Can act alone? | Transfer procedure |
| --- | --- | --- | --- | --- | --- |
| GitHub organization `ilorium-protocol` | Repositories `.github`, `protocol`, `site`, `probe`, `agent-kit`; rulesets; secrets; Actions | Founder (`fseldon`) and a second, private account of the founder kept for recovery only; both owners with two-factor authentication (a passkey on `fseldon`, an authenticator app on the recovery account); hardware keys planned | Owner | Yes, the founder | Add a Custodian as owner; remove the founder's recovery account once two independent owners exist (Governance, section 8) |
| Repository rulesets (`main-protection`, `tags-protocol`) | Signed commits, PR review by CODEOWNERS, who may tag a release | Founder | Administrator bypass by pull request, recorded | Yes | Bypass is removed when two Custodians are in office |
| Domain `ilorium.com` | The site, the Lighthouse, email | Founder, at the registrar (GoDaddy), with auto-renewal and WHOIS privacy to be confirmed in the quarterly review | Registrant | Yes | Transfer of registrant to the receiving entity when it exists |
| DNS and hosting (Cloudflare: zone, DNSSEC, Pages) | Where `ilorium.com`, `llms.txt` and `/.well-known/ilorium.json` resolve | Founder (`root@ilorium.com`), two-factor authentication by authenticator app; hardware keys planned | Account owner | Yes | Add a second administrator; DS record rule: remove the DS at the registrar before any DNS move |
| Email (`@ilorium.com`, Google Workspace) | Verification mail for every other resource; the groups `hello@`, `security@`, `press@`, `agents@` | Founder (`root@`, superadmin, 2-Step Verification; hardware keys planned) | Superadmin | Yes | Second superadmin to be added (open) |
| Signing key, **provisional** (decision 0005): Ed25519 in software with a passphrase, `SHA256:rd2Y71cS6Vz956Qmql8w66RfAZpU6d7IqTp0RJ29E/Q`, since 2026-10-27; the only backup is an encrypted copy of the same key. Planned: `ed25519-sk` on a hardware key, with a backup key | The pseudonymous identity "Seldon"; every commit, tag and release | Founder | — | Yes | Planned rotation: decision 0005, point 4 (a statement signed by the old and the new key). Compromise: decision 0005, point 3 (no independent backup key exists yet). After the rotation: Governance recovery rule (a message signed by the backup key names the new key); loss of both keys: announced by the Custodians, new key, recorded as a governance decision |
| Release signing (Sigstore, build provenance) | What people install | Founder, through CI | — | Yes (one human approver) | Second approver when two Custodians are in office; evaluate a threshold scheme (for example TUF) before inventing one |
| Package registry (PyPI, planned) | The verifier people install | Founder (to be created) | — | Yes | Trusted publishing from CI; second owner with the Custodians |
| Security agent (`ilorium-security-agent`, a GitHub App) | Reads repositories, opens issues; zero write (decision 0002) | Installed by the founder | `Contents: Read` | No: it cannot write | Revoke by uninstalling the App |
| Funds | None. The founder pays from his own pocket; the protocol accepts no donations until a receiving entity exists | Founder | — | — | Receiving entity (Governance, section 6.6) |
| Account recovery | Recovery codes, backup keys, the sealed plan | Founder, in a sealed plan with a designated person who recovers access only | — | — | Recovering access confers no authority over rules (Governance, section 4.5) |
| The Project documents (Claude Project, working drafts) | Drafts before they reach the repository | Founder | — | Yes | The repository is the source of truth once published |

## Pre-authorized procedures (Governance, section 4.5)

These keep what exists running and change no rule. During interim governance the founder executes them; if he is unreachable, the person named in his recovery plan executes only these, and reports in public.

1. **Compromised credential or token:** revoke, rotate, publish a signed notice, record the incident under `governance/incidents/`.
2. **Certificate or DNSSEC key rotation:** rotate at Cloudflare, update the DS record at the registrar, confirm resolution.
3. **Domain renewal:** renew; never let the domain lapse.
4. **Deployment:** `DEPLOY_ENABLED` stays `false` by default; a deployment is a release and follows the release rules.
5. **Security fix:** a security release may be published by the founder alone and is stated as such in the changelog; under restricted maintenance (Governance, section 8) it is the only kind of release allowed.

## Approvals bound to content (Governance, section 3.2.6)

Every governance decision under `governance/decisions/` records: the proposal and version approved; the SHA-256 of the approved text and of each artifact; who voted and who abstained; the dates of the comment period and the vote; the signatures; the effective date; and the decisions it corrects or replaces. A published artifact that does not match an approved hash is unapproved, whoever published it.

## Quarterly review

- Every holder and permission above is still correct.
- Second owners, administrators and superadmins: who exists, who is missing.
- Domain expiry, auto-renewal, WHOIS privacy.
- Audit logs of GitHub, Cloudflare and Workspace read for actors, members, roles, installed Apps and license requests.
- Keys and recovery tested.
