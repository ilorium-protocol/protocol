# Decision 0005: Provisional software signing key

- Date: 2026-10-27
- Decided by: the founder, as the only Genome Custodian
- Kind: standing decision; amends decision 0003 (point 1 and condition 6) for as long as it is in force
- Status: in force until the rotation in point 4

## Decision

1. **The founder's signing key is, for now, an Ed25519 key kept in software**, protected by a passphrase, on the founder's computer. Public fingerprint: `SHA256:rd2Y71cS6Vz956Qmql8w66RfAZpU6d7IqTp0RJ29E/Q`. Added on 2026-10-27 and registered as a signing key on the GitHub account `fseldon`. It signs Seldon's commits, tags and releases.
2. **It is provisional.** Decision 0003 calls for an `ed25519-sk` key on a hardware key, with an independent backup key. That is not in place yet. Until it is, every statement in this repository that depends on a hardware key or a backup key is read together with this decision.
3. **There is no independent backup key.** The only backup is an encrypted copy of the same key. If the key is lost, the copy restores it. If the key is compromised, the copy is compromised too, and the recovery rule of the authority inventory ("a message signed by the backup key names the new key") cannot be used. In that case the founder removes the key from `fseldon`, publishes a notice from the `fseldon` account and from `security@ilorium.com`, records an incident under `governance/incidents/`, and registers the new key by a governance decision. Signatures made with the old key after the date of the notice are not the founder's.
4. **Rotation to a hardware key** happens at the first of: the first release that is not a draft; the appointment of the first Genome Custodian; 2027-10-27. It is done by a rotation statement (`governance/keys/rotation-<date>.md`) naming the old and the new fingerprints, signed with the old key **and** with the new key. The new key and its backup key are registered on `fseldon`. The old key stays registered so that what it signed can still be checked, and is listed in `governance/keys/allowed_signers` with `valid-before` set to the rotation date.
5. **Why.** No hardware keys were available on 2026-10-27, and publishing the repositories did not need to wait for them. Saying so is better than a key description that is not true.

## Sources

- Decision 0003.
- `governance/authority-inventory-v1.md`, signing key row.
- `governance/security/2026-10-21-report-0001.md`, recommendation 1.
