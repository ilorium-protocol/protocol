# Security policy

## Reporting a vulnerability

Report in private. Do not open a public issue.

- Email: security@ilorium.com
- GitHub: [private vulnerability reporting](https://github.com/ilorium-protocol/protocol/security/advisories/new) (a draft Security Advisory, visible only to the reporter and the maintainers)

Include what you found, how to reproduce it, and what you think it affects. A proof of concept helps; exploitation of systems you do not own does not.

## What to expect

- Acknowledgment within 72 hours.
- Coordinated disclosure: we agree on a timeline with you, fix, then publish. Default: 90 days from the report, shorter when a fix is ready.
- Public credit in the advisory, if you want it.
- No bounties for now. The protocol has no budget for them (governance-v1.md, section 6).

## Scope

- This repository: documents, schemas, conformity vectors, the reference verifier, tools, workflows.
- The site, ilorium.com, and its repository.
- The infrastructure of Organism Zero, when it exists (planned).

For the verifier and the evidence format (the only code in this repository today): a verifier that accepts evidence it should reject (a false PASS) is the highest severity; a crash, a hang or memory exhaustion on hostile input comes next; schemas or vectors that contradict the specification are reported the same way.

**Known limits of M0.** The verifier has no hashed lock file yet (its dependencies are pinned by minimum version in `verifier/pyproject.toml`); the SBOM is produced by the release workflow. The ML-DSA-44 vectors are signed by an independent implementation (dilithium-py, FIPS 204, deterministic mode) and verified by the OpenSSL-backed verifier; both agree. Where the environment cannot verify ML-DSA-44 (`cryptography` older than 48, or OpenSSL older than 3.5), the verifier reports UNKNOWN, never PASS and never an error. Public witness integration is not available until an interoperability test and an agreement with a witness operator exist.

Out of scope: organisms run by others. Report those to the organism's responsible party, named in its Spore. If an organism misuses the Ilorium name or publishes a false Spore, open an issue with the "Misuse report" template.

## The security agent

A security agent (`ilorium-security-agent[bot]`, AI, Genome Law 5) is planned to acknowledge and triage reports, review pull requests, watch dependency and code scanning alerts, and publish weekly reports under `governance/security/`. It reviews and proposes; it never decides. It never answers with vulnerability details in public. It is planned until the founder configures it; until then, a human reads security@ilorium.com.

## Keys

PGP key for encrypted reports: planned. Until it is published, use GitHub private vulnerability reporting for anything sensitive.

## Supported versions

Release 1.0, draft. Only `main` and the latest `protocol/*` tag receive fixes.
