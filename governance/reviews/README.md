# External reviews

Outside readers (AI models) were given the protocol documents and the same prompt. Each response was checked against the text before anything was accepted: that a reader said it is not evidence; that it holds in the text is. Agreement among models points to where to look; it does not show they are right, because models share training biases.

**What this directory holds.** A summary of each review, what the reviewer received, what was verified and what happened. The unedited originals are kept in the maintainers' working project, not in this repository. Publishing them verbatim is a decision of the founder and is **pending** (see `Status` below). Nothing here changes the protocol: changes go through an IIP.

| No. | Reviewer (self-identified) | Date | Received | File |
| --- | --- | --- | --- | --- |
| 01 | DeepSeek (said twice that it was Claude; treated as DeepSeek) | 2026-10-22 | whitepaper, governance | this index |
| 02 | Qwen | 2026-10-22 | whitepaper, governance | this index |
| 03 | Gemini (Google) | 2026-10-22 | whitepaper, governance | this index |
| 04 | Grok (xAI) | 2026-10-22 | whitepaper, governance | this index |
| 05 | GPT (OpenAI) | 2026-10-22 | whitepaper, governance, the synthesis of reviews 01-04 | this index |
| 06 | ChatGPT (OpenAI) | 2026-10-24 | the 38-page final reading (revision of 2026-10-22) | [06-gpt-final-reading.md](06-gpt-final-reading.md) |

None of the reviewers ran the verifier, read the Genome or specifications (01-05), or audited the repository. Each says so.

## Main findings, 01-05 (not all accepted)

- **01 DeepSeek.** The interim-governance exit condition ("Observed") was undefined and judged by the founder; the `unwatched` state sits badly with the stop lock; appointment objections had no stated effect; governance could be changed by two of three; the mission mixed protocol and founder's conviction; a whitepaper/governance inconsistency about who decides during the interim.
- **02 Qwen.** No technical definition of "stop"; no founder-incapacity clause; no deadline for interim governance; no incident-response plan; doubts on the cost of signing every event and on witnesses without a blockchain.
- **03 Gemini.** The founder picks the first two independent Custodians; Wardens paid by the organism; the founder's conviction in the whitepaper; spam of AI-authored IIPs; privacy of the log; adoption friction. Not accepted as proposed: a blind payment pool (the protocol holds no entity to receive money).
- **04 Grok.** An objective second trigger for full governance; disputes between Wardens over a stop not yet triggered; a formal independence challenge; publication of compensation rates in advance.
- **05 GPT.** The definition of stake disqualified the Wardens themselves; the founder's power was defined two incompatible ways; no ending mechanism that could be executed; a replacement deadlock with two Wardens; the unanimity proposal was not endorsed; call for binding approvals to exact content (hash) and an inventory of who controls each account.

The founder's decisions on these are recorded in the maintainers' working project and, where they took effect, in `governance/decisions/` and in `CHANGELOG.md`.

## Status

- Review 01-05: processed; decisions of 2026-10-22 applied in the revision of that date (see `CHANGELOG.md`).
- Review 06: verified against the English texts and applied on 2026-10-24 by the founder's delegation; see the file.
- Originals not published in this repository: **pending the founder's decision.**
- Approvals bound to the content hash (raised in 05 and 06): described in the documents as planned; **not enforced by any workflow in this repository yet** (decision 0004).
