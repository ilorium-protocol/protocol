# governance/

The public record of how the protocol is governed. governance-v1.md, section 9: "Decisions, votes, appointments, removals, declarations of independence and stakes: in the repository, under `governance/`." A decision that is not published does not exist.

Everything here enters through a pull request on `main`, so the git history is the audit trail.

| Directory | What goes here | Who writes it |
| --- | --- | --- |
| `decisions/` | Standing decisions of the Custodians, numbered `NNNN-slug.md`, dated. Interim: the founder's decisions. IIP outcomes point here. | Custodians (interim: the founder) |
| `votes/` (planned) | One file per IIP vote: who voted what, abstentions with their declared stake, result, date. Created with the first vote. | Custodians |
| `custodians/` | The seats, who holds them, appointment announcements with their 30-day notice, declarations of independence, independence reviews, removals. | Custodians |
| `declarations/` (planned) | Declarations of stake by anyone who takes part in a decision (governance-v1.md, section 2). Created with the first declaration. | Whoever declares |
| `security/` | Weekly reports from the security agent (observed / not observed / recommended). The security agent opens issues with its reports (zero-write mode, decision 0002); a human copies them here through a pull request. | Security agent (AI), planned until configured |
| `budget/` (planned) | Income and expenses, at least quarterly (governance-v1.md, section 6). Today: funded by the founder; no donations accepted until a receiving entity exists. | Custodians |

What does not go here: the status of any organism (that comes from evidence alone, never from governance), stop events (recorded in the organism's Strata and reported in the Codex), and IIP texts (under `iips/`).
