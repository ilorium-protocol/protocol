# Ilorium Improvement Proposals (IIPs)

The public, numbered proposal required for a **method change**: the Genome (the laws organisms carry), a classification rule, a record format, the conformity vectors, or governance-v1.md. Normative text: [governance-v1.md](../governance-v1.md), section 3.2.

Status of this process: in force, draft, under interim governance.

## What an IIP is not

Editorial and specification changes are pull requests, not IIPs ([CONTRIBUTING.md](../CONTRIBUTING.md)). An idea that is not yet a proposal goes to Discussions, category Proposals. An IIP does not decide the status of any organism; that comes from evidence alone.

## Numbering

- IIP-0001 (Succession), IIP-0002 (Stop and the Wardens) and IIP-0003 (Birth gate and germline) are the founding proposals. They are part of Genome 1.0 (draft); their text lives in [genome/genome-v1.md](../genome/genome-v1.md). The files here are pointers.
- New proposals take the next number, from **IIP-0004** onward, assigned when the pull request that adds the file is opened. Numbers are never reused.
- File name: `iip-NNNN-slug.md`, lowercase, hyphens.

## Process

1. **Draft.** Copy [TEMPLATE.md](TEMPLATE.md) to `iip-NNNN-slug.md`, fill every section, open a pull request labeled `iip`. The author may be a human or an agent; an agent says so and carries a human's sign-off ([CONTRIBUTING.md](../CONTRIBUTING.md), "Agents"). Open a Discussion in Proposals and link it from the file.
2. **In comment.** The pull request is merged with status "In comment" so the text is on the record. The comment period is public and runs on the Discussion and on the pull request: at least **30 days** for the Genome and governance-v1.md, at least **14 days** for other method changes. Every comment stays on the record. The author may revise the text during the period; substantive revisions restart it.
3. **Voting.** The Custodians vote in public, in Discussions, category Governance, and record the vote under `governance/votes/`. An IIP passes with **two votes in favor out of three**. There is no veto. A Custodian with a stake in any organism the change affects in particular abstains and says so; if two must abstain, the IIP waits until the council is complete. Interim: the founder decides alone, as the only Custodian, after the comment period, and says so.
4. **Accepted / Rejected.** The status is updated in the file. An accepted IIP is implemented by a pull request labeled `method-change` that references `IIP-NNNN`, creates a new version of the affected document, adds the changelog entry, delivers the `.es.md` translation and updates the vectors when a format changes.
5. **Objection.** Anyone may object within **14 days** of the decision's publication, in public, with reasons. The Custodians answer in public. An objection does not suspend the decision; it is part of the record, and a later IIP may reverse the change.
6. **Withdrawn.** The author may withdraw at any time before the vote. The file stays, with status "Withdrawn".

An IIP never applies retroactively: each organism's status names the version it was tested against.

## Statuses

`Draft` → `In comment` → `Voting` → `Accepted` or `Rejected`; `Withdrawn` at any point before the vote.

## Index

| Number | Title | Kind | Status |
| --- | --- | --- | --- |
| [IIP-0001](iip-0001-succession.md) | Succession | genome | Part of Genome 1.0 (draft) |
| [IIP-0002](iip-0002-stop-and-wardens.md) | Stop and the Wardens | genome | Part of Genome 1.0 (draft) |
| [IIP-0003](iip-0003-birth-gate-and-germline.md) | Birth gate and germline | genome | Part of Genome 1.0 (draft) |
