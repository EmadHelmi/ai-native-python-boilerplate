---
name: implement-approved-batch
description: >-
  Implement only a previously planned and explicitly approved development
  batch, preserve the approved scope, stop when new meaningful decisions or
  scope expansion are required, and hand the completed implementation to
  verification without committing or continuing into additional work.
---

# Implement Approved Batch

Use this skill only when a concrete implementation batch has already been planned and the user has explicitly approved
that batch.

This skill executes approved work.

It does not create approval for itself.

## Objective

Implement the approved batch while preserving:

- the exact approved intent;
- project requirements;
- accepted decisions;
- engineering rules;
- scope boundaries;
- reviewability;
- reversibility where practical.

The agent MUST optimize for correct, understandable, reviewable implementation rather than maximum autonomous progress.

---

## 1. Confirm That Implementation Is Authorized

Before mutating the repository, verify that:

1. a concrete implementation batch exists;
2. its goal is sufficiently clear;
3. the user has explicitly approved implementation;
4. any meaningful blocking decisions have already been resolved;
5. required accepted decisions have been recorded when applicable.

If any of these conditions is materially missing, do not implement.

Return to the appropriate workflow state.

Do not treat:

```text
agreement with an idea
```

or:

```text
acceptance of a technical decision
```

as implementation approval.

---

## 2. Reconstruct the Approved Scope

Identify the exact scope that was approved.

The approved scope normally includes:

- the stated goal;
- expected files or components;
- approved dependency changes;
- approved mutating commands;
- approved data or schema changes;
- intended verification;
- explicitly excluded work.

If the approval was broad but still clearly bounded, use the narrowest reasonable interpretation consistent with the
user's intent.

Do not reinterpret approval in order to include useful adjacent work.

---

## 3. Read Relevant Context Before Editing

Before implementation, consult the context necessary for the approved batch.

This MAY include:

- `AGENTS.md`;
- `docs/project/definition.md`;
- applicable ADRs;
- relevant engineering rules;
- directly affected source files;
- directly affected tests;
- current repository state.

Do not re-analyze unrelated parts of the codebase without a concrete need.

The purpose is to implement the approved batch, not to restart project discovery.

---

## 4. Freeze the Scope

Once implementation begins, treat the approved batch as the maximum intended scope.

The agent MUST NOT expand the batch because:

- another feature would be useful;
- a neighboring bug is discovered;
- unrelated cleanup appears desirable;
- another abstraction could improve future extensibility;
- a new dependency would make the task easier;
- additional infrastructure is conventionally associated with the feature;
- the agent believes the user will probably want the extra work later.

Unapproved improvements belong in follow-up discussion.

---

## 5. Perform Necessary Implementation Work

The agent MAY perform implementation details that are necessary and uncontroversial consequences of the approved plan.

Examples include:

- creating approved files;
- modifying directly affected files;
- adding required imports;
- updating directly affected configuration;
- generating approved framework artifacts;
- updating directly affected tests;
- making small local refactors required for correctness;
- running approved mutating commands.

The agent SHOULD preserve the existing repository's conventions unless an applicable rule or accepted decision requires
otherwise.

---

## 6. Dependencies

Add, remove, upgrade, or materially reconfigure dependencies only when the approved batch includes that change.

Do not introduce a dependency solely because it simplifies the implementation.

If implementation reveals that an additional dependency is materially desirable or necessary but was not approved:

1. stop before adding it;
2. explain why it is needed;
3. return to `DISCUSS`, `DECIDE`, or `PLAN` as appropriate.

Minor transitive dependency changes produced by an approved package-management operation do not require separate
approval.

---

## 7. Persistent Data and Migrations

Persistent data changes MUST remain within the approved scope.

If an approved model or schema change requires a generated migration or equivalent artifact, the agent MAY generate it
when that consequence was reasonably implied by the approved batch.

The agent MUST stop before introducing an unapproved:

- destructive migration;
- data migration;
- field removal;
- field rename;
- semantic data conversion;
- uniqueness change;
- index strategy change;
- irreversible persistent-state operation.

If such a change becomes necessary, return to the decision or planning workflow.

---

## 8. Refactoring During Implementation

Small local refactoring MAY be performed when it is necessary to implement the approved behavior safely and clearly.

The agent MUST NOT use an approved feature as authorization for broad cleanup.

Examples of normally unapproved expansion include:

- restructuring unrelated modules;
- renaming unrelated public interfaces;
- replacing existing patterns throughout the codebase;
- large formatting-only changes;
- generalized abstraction work unrelated to the batch.

If broader refactoring is genuinely needed, surface it as additional scope.

---

## 9. Handle New Decisions Correctly

If implementation exposes a meaningful unresolved decision, stop before silently choosing an approach.

Examples include newly discovered choices affecting:

- architecture;
- security;
- authentication or authorization;
- persistent data;
- external contracts;
- important dependencies;
- deployment;
- operational behavior;
- long-term maintainability.

Explain:

1. what was discovered;
2. why the existing approved plan no longer fully determines the implementation;
3. what work has already been completed;
4. what decision is now required.

Return to `DECIDE`.

Do not choose the fastest option merely to finish the batch.

---

## 10. Handle Unexpected Scope Expansion

If completing the batch requires materially more work than was reasonably understood during approval:

1. stop at the safest useful point;
2. preserve completed valid work where practical;
3. identify the additional required scope;
4. explain why it was not apparent earlier;
5. propose a revised or additional batch.

Do not quietly absorb the extra work.

---

## 11. Handle Implementation Errors

When an error is clearly caused by work inside the approved scope, the agent MAY diagnose and correct it without
requesting a new approval for every corrective edit.

Examples include:

- syntax errors;
- incorrect imports;
- failing directly affected tests;
- misconfigured approved settings;
- implementation bugs in the approved feature.

This permission does not extend to solving failures by expanding architecture or scope.

---

## 12. Pre-existing Problems

Do not silently repair unrelated pre-existing problems.

If a pre-existing issue materially blocks implementation:

1. identify it;
2. explain its impact;
3. distinguish it from the approved work;
4. propose the smallest appropriate next action.

Do not use the blocker as implicit permission for broad repair work.

---

## 13. Mutating Commands

Execute only mutating commands that are:

- explicitly part of the approved plan; or
- necessary and reasonably implied by the approved batch.

Before running an unexpectedly high-impact command, apply the safeguards in `AGENTS.md`.

Do not perform destructive operations merely because they would simplify recovery or cleanup.

---

## 14. Git Boundaries

Implementation approval does not authorize unrelated Git state changes.

Unless separately approved, this skill MUST NOT:

- create or switch branches;
- stage files;
- create commits;
- push;
- pull;
- merge;
- rebase;
- reset;
- tag;
- create or modify pull requests.

Read-only Git inspection MAY be used when needed.

If the approved plan explicitly included a particular Git mutation, perform only that approved operation.

---

## 15. Do Not Begin Adjacent Work

When the approved implementation is complete, stop.

Do not continue automatically into:

- the next feature;
- the next milestone;
- optional cleanup;
- deployment;
- documentation beyond what the batch requires;
- an unrelated test expansion;
- another decision;
- commit or push operations.

The completion of one batch creates no authorization for another.

---

## 16. Preserve Reviewability

Prefer changes that are easy for the user to inspect and understand.

When multiple equivalent implementations exist inside the already accepted design, prefer the one that:

- is simpler;
- follows existing project conventions;
- minimizes unrelated diffs;
- avoids unnecessary abstraction;
- makes behavior explicit;
- is easy to verify.

Avoid cleverness that makes the approved behavior harder to review.

---

## 17. Track Deviations

If the actual implementation differs meaningfully from the approved plan, record that fact for the completion report.

A deviation MAY be acceptable when:

- it is necessary for correctness;
- it remains within the approved intent;
- it does not introduce a new meaningful decision;
- it does not materially expand scope.

Do not conceal deviations.

Material deviations require returning to an earlier workflow state.

---

## 18. Implementation Completion

Implementation is complete when:

- the approved behavior has been implemented;
- the repository is in a coherent state for verification;
- no known unresolved implementation error within the approved scope remains;
- any material deviation or blocker has been surfaced.

At this point, transition to:

```text
VERIFY
```

Do not treat implementation completion as verification success.

---

## 19. Handoff to Verification

At the end of implementation, provide enough context for verification to proceed.

Summarize:

### Implemented

What was changed.

### Files Affected

Important files created, modified, or removed.

### Deviations

Any meaningful differences from the approved plan.

### Verification Needed

The relevant checks expected from the approved plan or discovered during implementation.

Do not claim that work is complete until verification has actually occurred.

---

## 20. What This Skill Must Not Do

This skill MUST NOT:

- make an unapproved meaningful technical decision;
- expand product scope;
- add speculative functionality;
- add unapproved dependencies;
- introduce speculative abstractions;
- silently perform broad refactoring;
- create destructive data changes without approval;
- treat implementation errors as authorization for redesign;
- commit or push unless separately authorized;
- continue into another implementation batch.

---

## 21. Completion Condition

This skill ends at one of two boundaries.

### Normal Completion

```text
approved batch
    ↓
IMPLEMENT
    ↓
implementation complete
    ↓
VERIFY
```

### Interrupted Completion

```text
approved batch
    ↓
IMPLEMENT
    ↓
new decision / blocker / expanded scope
    ↓
DISCUSS / DECIDE / PLAN
```

In neither case should the skill continue autonomously beyond the appropriate workflow boundary.
