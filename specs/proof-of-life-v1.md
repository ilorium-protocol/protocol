# Ilorium Proof of Life v1.0

Version 1.0 · 2026-10-20 · Draft · Revised 2026-10-24 (human effort, estimation, denominators, full observed autonomy; provisional under IIP-0006)

Ilorium monitors organizations run by AI agents: it records how each one lives, measures what it has actually shown it can do, and requires that every organism carry a human stop key, tested by drills within a declared scope. Its mission is to provide laws, formats and verification for organizations run by AI agents and for the evolution of their species. The founder reads that evolution as the road to SI2SI: a personal conviction, set out in the founder's letter, on which the protocol takes no position. Proof of Life is the part that measures. It turns an organism's own records into a profile of what it has shown, with evidence, and never assumes what it has not shown.

Beats can be inflated and say nothing about value: an organism producing 10,000 internal events in a minute has not shown more independence than one delivering ten real jobs in a month. Proof of Life therefore measures dependency against **useful work**, and applies the two-clock principle of the Pulse specification: beats define the organism's life, translation time verifies its evidence.

## Principles

1. **No composite number.** Six dimensions side by side, each with evidence and limitations.
2. **Beats measure life, work measures value.** Depth is never merit; useful work is counted separately.
3. **Time never defines the organism, but it verifies its evidence.** Freshness is shown in translation time.
4. **Human time is human life.** Founder hours are measured in seconds, because the founder's freedom of time is a goal of the protocol.
5. **Safety is never punished, and never hidden.** Tests, correct escalations and stops are not counted as dependency in the per-unit measures; they are always recorded, timed and shown. An emergency a human had to handle counts in the rescue rate, because it was human work.
6. **Human effort is recorded whole.** *(Revised 2026-10-24.)* Every human intervention is recorded and timed whatever its kind: operational, directive, approval, emergency, governance or test. The total of human time, with its breakdown by kind, is always shown next to any adjusted measure; an adjusted measure that does not disclose its exclusions and the total is invalid. A correct escalation can show good control and still consume human time: both are true, and both are shown.
7. **A gap is not autonomy.** A period the Probe could not observe is shown as unknown, never as a period with no human intervention. An UNKNOWN never becomes favorable with time.
8. **The measure is not the goal.** Every measure here can be gamed: an organism can hide human work outside the membrane or minimize visible interventions without reducing real control. Coverage, attribution states and the share of unknown work are shown at the same weight as the measures themselves, and a claim that leaves them out is invalid.
9. **Evidence is not inherited.** Each organism's profile is built only from its own records. Ancestry is never evidence.

## The six dimensions

| Dimension | Question | Measured as |
| --- | --- | --- |
| **Observed autonomy** | How much is done and decided without humans? | Per process and vital function: share of material actions **executed** by agents and share **decided** by agents, among actions with attribution `linked` or better, with the distribution of attribution states |
| **Coverage** | How much can we see? | The Probe's four measures: inventory, capture availability, reconciliation, attribution |
| **Reliability** | Does it work? | Share of work units meeting criteria the organism declared in advance |
| **Control** | Are limits respected? | Conformity of each law, drills passed, control events and their outcomes, correct escalations |
| **Human dependency** | How much human life does it consume per thing it delivers? | Per work unit: interventions, founder minutes, rescues. Secondary: umbilical load, crossing density, silence |
| **Provenance** | How was it born? | Founded, commissioned, assisted birth, autogenesis; funding sources; succession type (`founded`, `inherited`, `coalesced`), parents and generation (the Ecosystem specification) |

Functions with no activity are shown as "no activity", neither zero nor fully autonomous. Next to the dimensions the profile shows the **state of being** and **recovery** (proven, unknown, not restorable), as defined in the Pulse specification.

A composite summary may come later, only after each dimension is validated and its weights are justified and tested (for example, following the OECD *Handbook on Constructing Composite Indicators*).

## Descendants start from zero

- A descendant's profile begins empty. It inherits none of its parents' measures: no autonomy, reliability, human dependency, silence, conformity, work units or attestations.
- What it does inherit is shown, linked to its origin: scars, open restrictions and pending conformity findings (the Ecosystem specification). Scars pass to descendants; evidence and keys never do.
- Generation and parents appear under Provenance as facts about origin. They never weigh in any dimension, and the web never compares generations as better or worse. Descent proves origin, never improvement.
- Whether later generations do become more autonomous or more reliable is a question the data may answer one day, organism by organism. The profile never assumes it.

## Work units

A **work unit** is one outcome the organism delivered to someone outside its membrane, counted against criteria it declared **before** delivering. Examples:

| Kind of organism | Work unit | Typical source |
| --- | --- | --- |
| Service business | An order fulfilled | Order system, invoice, A2A task in `TASK_STATE_COMPLETED` |
| Support | A ticket resolved and not reopened within the declared window | Ticketing system |
| Software | A release deployed to users | Deployment records |
| Agent-to-agent services | A task completed for another organism | A2A task terminal state, confirmed by the counterpart's records |

Rules:

- The organism declares its work-unit types and their success criteria in its Spore (draft field `work_units`). Changing them is a governance crossing and starts a new comparison window.
- A unit counts only when its source is observed by the Probe or attested by the counterpart. A unit the organism only declares is shown as declared.
- **Failed, rejected or canceled** units are counted too (A2A `TASK_STATE_FAILED`, `TASK_STATE_REJECTED`, `TASK_STATE_CANCELED`): they feed reliability and are never hidden.
- Internal events are never work units, however many there are.
- Work done by a parent for its own descendant, or by a descendant for its parent, is shown as work within the lineage, separately from work for unrelated counterparts.

## Measuring humans: seconds

| Layer | Source | What it gives |
| --- | --- | --- |
| Detected | Probe: Threshold messages, SSH sessions, GitHub and Workspace activity | An **estimate from recorded activity**: it can understate (thinking leaves no trace) and overstate (a 20-second approval imputed as a 5-minute session) |
| Declared | Founder Ledger | The founder's own count of work sessions, with start and end |
| Connection | SSH and similar sessions | The duration of a connection, which is not the same as continuous human attention |

**Detected sessions** *(revised 2026-10-24)*: human events close together form one session (initial rule: less than 15 minutes apart, minimum 5 minutes per session). The rule and its version are published with every figure, and the figure is never called a floor or a ceiling. The three layers are shown separately and are never added without deduplication: a minute that is both detected and declared counts once. Simultaneous sessions, periods not linked to any work and discrepancies between layers are recorded. The estimator is calibrated against a sample of declared sessions with start and end, and its known error is published.

## Human dependency: measures

**Primary, per work unit**

| Measure | Definition | Reading |
| --- | --- | --- |
| **Interventions per work unit** | Dependency crossings (`operational`, `directive`, routine `approval` or `governance`) divided by work units delivered | How often a human is needed for each thing delivered |
| **Human minutes per work unit** | Deduplicated human time (all kinds; the breakdown by kind is shown) divided by work units | The cost in human life of each delivery |
| **Rescue rate** | Work units that needed an `operational` crossing or an `emergency` to complete, divided by successful work units | How often humans had to save a delivery |
| **Unattributed share** | Work units with at least one action of attribution `unknown` or `disputed` | How much of the work cannot yet be explained |

Every crossing is linked, where evidence allows, to the work units it affected (`work_unit` field in the evaluation record, defined in the Probe specification). Crossings not linked to any unit are shown as overhead.

**Denominators** *(revised 2026-10-24)*: attempts, terminal outcomes (delivered, failed, rejected, canceled) and successful deliveries are three different counts, and every measure names which one it divides by. A measure whose denominator is zero is **not computable** and is shown as such, never as zero; human time spent on units that failed is shown, so that failure never looks like zero cost. A unit that crosses a window boundary is counted in the window of its terminal outcome.

**Secondary, per beat**

| Measure | Definition | Unit |
| --- | --- | --- |
| **Umbilical load** | Human time per 1,000 beats | human minutes per 1,000 beats |
| **Crossing density** | Dependency crossings per 1,000 beats | crossings per 1,000 beats |
| **Silence** | Beats since the last `operational` or `directive` crossing | beats |

Silence is not broken by tests, correct escalations or stops, and is never extended by interval pulses.

## Freshness

Every dimension shows the translation time of its newest evidence and the age of the latest cosigned checkpoint, and also the range of its coverage, the latest datum from each source the dimension needs and the age of the **oldest** component a claim depends on: one recent event never refreshes an incomplete record. Evidence older than F (to calibrate per dimension) is marked **stale**: shown, but never presented as the current state. Recovery is shown with the date of its last drill.

## Autogenesis and full observed autonomy (no composite status)

*Revision of 2026-10-22, provisional until IIP-0006 closes.* Earlier drafts defined a composite status, "Ilorium 100%", that combined provenance with the other five dimensions under one name. Three of five independent readers took it for a seal. The protocol now shows those results separately and names no composite status.

- **Provenance** records how the organism was born: founded, commissioned, assisted birth or **autogenesis** (decided, designed, funded and launched by another organism with no human crossing). Birth is a historical fact; it never changes with later operation.
- **Full observed autonomy** is a result about a window: over at least W beats with an unbroken chain, fresh evidence and at least U work units, every corroborated material action was executed and decided by agents, with zero interventions per work unit and a rescue rate of zero. It is shown with the window, the coverage measures, the attribution states and the share of unknown work that back it, and it says nothing about any later window. *(Revised 2026-10-24.)* It is always written with its counts, per process: numerator, denominator, exclusions and unattributed actions ("10 of 10 corroborated actions executed by agents; 90 actions unattributed; autonomy of the whole process not established"). It is **not shown** when the share of unattributed actions in the window exceeds the declared threshold (to calibrate; an open question below) or when a source declared in the membrane was not captured during the window. Activity without data never becomes zero.
- **Control**, **coverage** and **reliability** keep their own results, each with its own period and evidence.

Nothing here combines into a name, a number or a badge. Emergencies handled correctly are always shown and count in the rescue rate. Holding the stop key is not a crossing; using it is a control event. An organism founded by humans can show full observed autonomy and full control, with no cap. Autogenesis is a fact about birth, not about quality, and a parent's results are never evidence for its descendants.

## What the web shows

For each organism: state of being and recovery; the six dimensions side by side, each with evidence, freshness and limitations; human dependency per work unit over its chain; silence; its status in the ecosystem; its lineage; and its guardianship state (complete, degraded, absent). No ranking and no composite status: organisms are shown in the phylogeny.

## Open questions

- W (beats), U (work units), F (freshness per dimension) and coverage thresholds.
- Work-unit templates and success criteria for common types of organisms.
- Calibration of session parameters against real ledger data, and the published error of the estimator.
- The threshold of unattributed actions above which full observed autonomy is not shown.
- Whether a composite summary is useful, after validation.
