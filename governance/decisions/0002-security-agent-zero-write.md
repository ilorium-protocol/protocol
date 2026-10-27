# Decision 0002: The security agent starts with zero write access

- Date: 2026-10-21
- Decided by: the founder, as the only Genome Custodian
- Kind: standing decision, with a stated condition for reevaluation
- Status: in force

## Decision

1. **The security agent (`ilorium-security-agent`, an AI) has no write permission on repository contents.** Its GitHub App is created with Repository · Contents: Read. It creates no commits, branches or tags.
2. **Its weekly report is an issue**, labeled `agent-authored` and `security`. A human may copy it into `governance/security/` through a normal pull request.
3. **The repository variable `AGENT_SIGNOFF` is not defined.** The weekly audit workflow does not pass it to the agent in any case.
4. The agent keeps everything else it had: it reads, comments on pull requests, and opens issues. It never approves, merges, publishes, changes a setting or holds a production secret.

## Reevaluation

The founder reevaluates this decision after the first test pull request shows that the rulesets block the App on `main` (an attempted push by the App is rejected). Any change that gives the agent write access to contents is made by a new decision in this directory, or by an IIP, before the workflow and the App permissions change. The code path that commits reports (`security-agent/audit.py`, through `createCommitOnBranch`) stays in the code, switched off.

## What the repository enforces

- `.github/workflows/security-agent-weekly-audit.yml` (organization `.github` repository) mints the App token with `permission-contents: read`.
- Without write permission on contents the agent could not commit even if the code asked it to.

## Sources

- Decision 0001 (interim governance).
- governance-v1.md, sections 7 and 9.
