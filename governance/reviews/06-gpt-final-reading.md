# Review 06 - ChatGPT - final reading and integration with existing systems

Received 2026-10-24. Reviewer input: the 38-page Spanish PDF of the final reading (revision of 2026-10-22) and an earlier conversation about AEVS and ERC-8004. Output: a synthesis message, a working document (priorities P0-A to P0-G, a governance and measurement table, proposed English wording, 12 acceptance cases) and an architecture map. Limits it declares: a document review; it did not run the verifier, did not read the English texts that prevail, did not audit the repository.

The corrected map is `engineering/ilorium-architecture-map-v0.1.svg`.

## Verification against the English texts (2026-10-24)

| # | Finding | Confirmed? | What was done |
| --- | --- | --- | --- |
| P0-A | "If it is born inside the species it is born through the gate" is circular | Yes | Rewritten as a recognition condition: Ilorium recognizes a birth only when its evidence meets the gate; it cannot prevent births outside the registry |
| P0-B | Excluding tests, escalations and stops from dependency makes real human time disappear | Yes | New principle 6 in Proof of Life: all human effort is recorded in full, with breakdown |
| P0-C | "A floor" with a 5-minute minimum per session overestimates | Yes | Now an estimate from recorded activity, with published rule and version and known error |
| P0-D | "Full observed autonomy" can be read over a corroborated subset | Yes | Written with numerator, denominator, exclusions and unattributed actions; not shown above a threshold |
| P0-E | Presence, receipt and production are different proofs | Partly | Pulse section 6 and the architecture distinguish co-signing from challenging |
| P0-F | IIP-0004 lets the founder confirm at 30 days rules that section 10 protects with 90 days and two of three | Yes | Initial-constitution rule in Governance section 10; IIP-0004 at 90 days |
| P0-G | The conditions for "stable" differ across documents | Yes | `manifest.md` is the normative definition; others point to it |

Also applied: a Custodian is never a Warden; later compensation rates need an independent reviewer, a 12-month delay and are never retroactive; the independent-reviewer fallback is "not reviewed" after 14 days, never conformity; three denominators with names for Proof of Life; coverage range and age of the oldest component.

## Not applied, and why

- The founder's letter keeps its sentence: it is a signed personal conviction outside the protocol.
- No second published state for "operational maturity": "stable" stays one state.
- No adapters for AEVS, ERC-8004 or TRACE now: after the pilot, never before M2, and no announced compatibility without vectors.

The original text of this review is **not** reproduced here (see the index).
