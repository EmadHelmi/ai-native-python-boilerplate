---
name: verify-change
description: >-
  Verify a completed implementation batch with risk-appropriate targeted
  checks, distinguish implementation failures from pre-existing problems,
  allow only in-scope corrective fixes, assess whether an optional independent
  review would add meaningful confidence, and return control for user review
  without starting additional work or Git operations.
---

# Verify Change

Use this skill after an approved implementation batch has reached the `VERIFY` stage.

This skill determines whether the implemented change behaves as intended, whether an optional independent review would
add meaningful confidence, and whether the result is ready to return to the user.

Verification is not an opportunity to expand the project or improve unrelated code.

## Objective

Establish reasonable confidence in the completed implementation by:

1. understanding what was approved and implemented;
2. identifying the risks introduced by the change;
3. selecting the smallest meaningful verification set;
4. running the relevant checks;
5. diagnosing failures accurately;
6. correcting only failures that remain within approved scope;
7. reporting the final verification result;
8. assessing whether an optional independent review would add meaningful confidence;
9. returning control to the user after any applicable independent review.

The goal is confidence proportional to risk, not maximum test execution.

---

## 1. Establish Verification Scope

Before running checks, understand:

- the approved implementation goal;
- the files and components changed;
- any approved verification plan;
- meaningful deviations from the plan;
- the behavior expected from the change.

Use the implementation handoff when available.

Consult relevant repository context when necessary, including:

- `AGENTS.md`;
- applicable engineering rules;
- accepted ADRs;
- directly affected tests;
- relevant project requirements.

Do not restart broad project analysis.

---

## 2. Identify the Risks of the Change

Determine what could reasonably have been broken or implemented incorrectly.

Relevant risks MAY include:

- incorrect business behavior;
- regression of existing behavior;
- invalid API behavior;
- persistence errors;
- authentication or authorization failures;
- security regressions;
- invalid configuration;
- integration failures;
- incorrect error handling;
- type errors;
- formatting or lint violations;
- migration inconsistencies;
- template or UI regressions;
- deployment or runtime configuration failures.

Verification SHOULD focus on risks actually introduced or affected by the batch.

Do not create tests for hypothetical behavior unrelated to the change.

---

## 3. Choose the Smallest Meaningful Verification Set

Prefer targeted verification before broad verification.

Depending on the project and the change, appropriate checks MAY include:

- focused unit tests;
- integration tests;
- API tests;
- template or UI tests;
- security-related tests;
- static analysis;
- type checking;
- linting;
- formatting checks;
- framework-specific system checks;
- migration consistency checks;
- focused runtime validation.

The agent SHOULD select checks based on:

- affected behavior;
- changed layers;
- regression risk;
- project rules;
- existing test infrastructure;
- cost of the check.

Do not run every available check merely because it exists.

---

## 4. Respect Project Verification Standards

When repository rules define required verification commands or quality gates, follow them when applicable.

Examples may include project-standard commands for:

- tests;
- linting;
- formatting;
- type checking;
- static analysis;
- framework validation.

Do not invent alternate tooling when the project already defines an accepted toolchain.

If the required tool or command is unavailable, report the issue rather than silently substituting an unrelated tool.

---

## 5. Prefer Targeted Checks First

Start with checks closest to the changed behavior.

For example, conceptually:

```text
changed component tests
        ↓
direct integration tests
        ↓
relevant static/framework checks
        ↓
broader suite when justified
```

A broad repository-wide test suite SHOULD be run when:

- project policy requires it;
- the change has wide impact;
- targeted verification cannot provide sufficient confidence;
- the user explicitly requests it.

Avoid expensive verification that adds little confidence for the current change.

---

## 6. Verification May Include Read-only Inspection

The agent MAY inspect relevant:

- diffs;
- source files;
- tests;
- configuration;
- generated artifacts;
- logs;
- command output.

Read-only Git operations MAY be used according to `AGENTS.md`.

Inspection alone does not constitute successful verification when executable checks are reasonably available and
relevant.

---

## 7. Handle Verification Success

A verification check succeeds only when its actual result supports the expected behavior.

Do not report success merely because a command exited without obvious output if its expected result is unclear.

When all required checks pass, prepare the verification summary and assess whether an optional independent review would
add meaningful confidence before transitioning to `USER REVIEW`.

Verification success does not authorize:

- commit;
- push;
- deployment;
- another implementation batch.

---

## 8. Handle Implementation-caused Failures

When a verification failure is clearly caused by the approved implementation, the agent MAY make corrective changes when
all of the following are true:

- the fix remains within the approved intent;
- it does not introduce a new meaningful decision;
- it does not add unapproved scope;
- it does not require an unapproved dependency;
- it does not introduce an unapproved persistent-data change;
- it does not materially alter the accepted design.

After a corrective change, rerun the relevant failed checks.

Do not claim success without rerunning affected verification.

---

## 9. Corrective Fixes Are Not New Feature Work

A corrective change MAY fix:

- incorrect implementation logic;
- syntax errors;
- import errors;
- directly affected test failures;
- configuration mistakes introduced by the batch;
- formatting or lint errors introduced by the batch;
- type errors introduced by the batch.

A corrective change MUST NOT silently introduce:

- new product behavior;
- new architecture;
- additional features;
- broad refactoring;
- unrelated cleanup;
- new dependencies;
- new schema concepts.

If such work is required, stop and return to the appropriate earlier workflow state.

---

## 10. Distinguish Pre-existing Failures

When a check fails, determine whether the failure was caused by the current implementation or already existed.

Use available evidence such as:

- affected files;
- Git diff;
- test scope;
- error location;
- previous repository state when known;
- relationship between the failure and the changed behavior.

Do not automatically attribute every failing check to the current batch.

Do not silently fix unrelated pre-existing failures.

Report them separately when relevant.

---

## 11. Handle Ambiguous Failures

If it is unclear whether a failure is caused by the current implementation:

1. investigate narrowly;
2. gather enough evidence to characterize the failure;
3. avoid unrelated changes;
4. report uncertainty when it cannot be resolved reasonably.

Do not fabricate certainty.

If resolving the ambiguity requires materially broader work, return control to the user.

---

## 12. Stop When Verification Reveals a New Decision

Verification can expose architectural or technical problems that were not visible during implementation.

If resolving a failure requires a meaningful new decision affecting areas such as:

- architecture;
- security;
- authentication or authorization;
- persistent data;
- external contracts;
- dependencies;
- infrastructure;
- deployment;
- operational behavior;

stop.

Explain:

1. which verification exposed the issue;
2. what the issue is;
3. why the approved design no longer fully determines the solution;
4. what has already passed;
5. what decision is now required.

Return to `DECIDE`.

Do not choose a new design merely to make verification pass.

---

## 13. Stop When Verification Requires Expanded Scope

If successful verification requires work materially outside the approved batch:

1. stop;
2. identify the missing scope;
3. explain why it is necessary;
4. preserve valid completed work;
5. return to `PLAN` or `DISCUSS` as appropriate.

Do not silently expand the batch.

---

## 14. Security-sensitive Changes

For changes affecting security-sensitive behavior, verification SHOULD explicitly exercise relevant security properties
when practical.

Examples include:

- invalid authentication attempts;
- authorization boundaries;
- expiration behavior;
- reuse prevention;
- malformed input;
- account-enumeration behavior;
- secret exposure;
- unsafe error responses;
- CSRF behavior;
- session or token behavior;
- rate limits or attempt limits.

Do not consider only the successful path when failure behavior is security-relevant.

---

## 15. External Integrations

Verification of external integrations SHOULD avoid unnecessary reliance on live external services during ordinary
automated testing.

Prefer project-approved mechanisms such as:

- fakes;
- mocks;
- stubs;
- fixtures;
- controlled integration environments.

When live verification is genuinely required:

- identify the external side effect;
- follow approval requirements;
- protect credentials;
- avoid production mutations without explicit authorization.

Do not treat access to external credentials as permission to use them.

---

## 16. Persistent Data Verification

When the implementation affects persistent data, verification SHOULD consider relevant properties such as:

- schema consistency;
- migration generation;
- migration validity;
- constraints;
- persistence behavior;
- rollback or reversibility when relevant;
- protection of existing data.

Do not execute destructive database operations merely for verification convenience.

Production-data validation requires the appropriate explicit authorization.

---

## 17. Avoid Changing Tests to Hide Failures

Tests exist to verify intended behavior.

The agent MUST NOT make a failing test pass by weakening or removing a valid assertion merely because the implementation
currently disagrees with it.

Changing an existing test is appropriate only when:

- the approved behavior intentionally changed;
- the previous expectation is no longer valid;
- the test itself is demonstrably incorrect;
- the change remains within approved scope.

When modifying an existing test expectation materially, make the reason visible in the completion report.

---

## 18. Verification Evidence

Record enough evidence to support the final result.

For each important verification category, retain or summarize:

- what was run;
- whether it passed;
- important failure information;
- corrective work performed;
- checks that could not be completed and why.

Do not overwhelm the user with raw command output when a concise result is sufficient.

Surface detailed output when it is needed to understand a failure.

---

## 19. Verification Result

Classify the outcome as one of:

### Passed

All verification required for the batch completed successfully.

### Passed with Known External or Pre-existing Issue

The implementation-specific verification passed, but an identified unrelated or pre-existing issue remains.

The issue MUST be clearly separated from the implemented change.

### Blocked

Verification cannot complete because of an unresolved blocker, missing environment capability, unavailable dependency,
required decision, or additional scope.

### Failed

The implementation does not currently satisfy the required verification and cannot be corrected within the existing
approved scope.

Do not report a batch as passed when a relevant required verification remains unresolved.

---

## 20. Assess the Need for Optional Independent Review

After verification is complete, assess whether a separate reviewer is likely to add meaningful confidence.

Independent review is optional and is NOT a separate workflow state.

It is especially useful when the completed batch affects:

- security-sensitive behavior;
- architecture or important boundaries;
- persistent data or migrations;
- external integrations;
- public interfaces or APIs;
- business-critical behavior;
- broad regression risk;
- unusually complex or subtle implementation logic.

It SHOULD normally be skipped for trivial or very low-risk changes when it would add little engineering value.

When independent review is useful, the workflow MAY use the repository's reviewer subagent:

```text
.cursor/agents/reviewer.md
```

The reviewer is expected to inspect and report rather than silently repair the implementation.

This skill MUST NOT treat reviewer findings as automatic authorization for additional implementation.

If independent review identifies a problem that can be corrected within the already approved intent and scope, the
workflow MAY return to the appropriate corrective verification path.

If a finding requires a new meaningful decision or material scope expansion, return to `DISCUSS`, `DECIDE`, or `PLAN` as
appropriate.

---

## 21. Prepare the User Review Handoff

When verification and any applicable optional independent review are complete, transition to `USER REVIEW`.

Provide a concise report containing:

### Implemented

What behavior or capability was implemented.

### Important Files Changed

The primary files created, modified, or removed.

### Verification

List relevant checks and their outcomes.

For example:

```text
- targeted tests: passed
- type checking: passed
- linting: passed
- framework checks: passed
```

### Independent Review

When an independent review was performed, summarize:

- whether material findings were reported;
- which findings remain unresolved;
- whether any corrective verification was performed afterward.

When independent review was intentionally skipped, no review summary is required unless the reason is useful to the
user.

### Corrective Changes

Describe corrections made during verification when meaningful.

### Deviations

Describe material differences from the approved plan.

### Known Issues

Report relevant unresolved pre-existing or external issues.

### Not Included

Identify important adjacent work deliberately left outside the batch.

---

## 22. Return Control to the User

After presenting the verification result and any applicable independent-review findings, stop at:

```text
USER REVIEW
```

Do not automatically:

- commit;
- stage files;
- push;
- start the next batch;
- implement follow-up suggestions;
- deploy;
- resolve unrelated failures.

The user may review the result, ask questions, request changes, request more verification, request or skip independent
review, approve it, or reject part of it.

---

## 23. Git Boundaries

Verification approval is not Git approval.

This skill MUST NOT perform state-changing Git operations unless a separately approved plan explicitly includes them.

In particular, do not automatically:

- stage;
- commit;
- push;
- merge;
- rebase;
- reset;
- tag;
- create or modify a pull request.

Read-only Git inspection MAY be used when useful.

---

## 24. What This Skill Must Not Do

This skill MUST NOT:

- broaden project scope;
- create new product functionality;
- make an unapproved meaningful decision;
- introduce an unapproved dependency;
- use verification failures as justification for broad redesign;
- silently repair unrelated pre-existing problems;
- weaken valid tests to make them pass;
- run destructive operations without the required approval;
- treat optional independent review as mandatory for every batch;
- treat reviewer findings as implementation approval;
- continue into Git or deployment workflows automatically;
- begin the next implementation batch.

---

## 25. Completion Condition

Normal completion without independent review is:

```text
IMPLEMENT
    ↓
VERIFY
    ↓
required checks pass
    ↓
USER REVIEW
```

Normal completion when independent review adds meaningful value is:

```text
IMPLEMENT
    ↓
VERIFY
    ↓
required checks pass
    ↓
optional independent review
    ↓
USER REVIEW
```

When verification or independent review discovers a blocker:

```text
IMPLEMENT
    ↓
VERIFY
    ↓
verification failure or reviewer finding
    ↓
decision / scope / environmental blocker
    ↓
DISCUSS / DECIDE / PLAN
```

In all cases, return control at the earliest appropriate workflow boundary.
