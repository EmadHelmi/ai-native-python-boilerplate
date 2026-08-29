---
name: technical-decision
description: >-
  Evaluate a meaningful unresolved technical or architectural decision using
  project-specific context, compare the strongest viable options, explain their
  trade-offs, provide a recommendation, wait for the user's explicit decision,
  and record an accepted ADR-worthy decision without beginning implementation.
---

# Technical Decision

Use this skill when current or immediately upcoming work depends on a meaningful unresolved technical or architectural
decision.

This skill supports the project's `DISCUSS → DECIDE → RECORD DECISION` workflow.

It does not authorize or perform implementation.

## Objective

Help the user make an informed project-specific decision by:

1. defining the actual decision clearly;
2. gathering the relevant project context;
3. identifying the strongest viable approaches;
4. comparing meaningful trade-offs;
5. recommending the best fit for this project;
6. waiting for the user's explicit decision;
7. recording the accepted decision when it is ADR-worthy.

The agent MUST distinguish clearly between:

```text
analysis
≠ recommendation
≠ user decision
≠ implementation approval
```

---

## 1. Confirm That a Decision Is Actually Needed

Before starting a decision process, determine whether the choice is meaningful and required by the current or immediately
upcoming work.

A decision is generally meaningful when it materially affects areas such as:

- architecture;
- application or domain boundaries;
- public interfaces or APIs;
- authentication or authorization;
- security;
- persistent data;
- external contracts or integrations;
- important dependencies;
- infrastructure;
- deployment;
- operational behavior;
- testing strategy;
- developer workflow;
- long-term maintainability.

Do not initiate this workflow for trivial, local, reversible implementation details already implied by an approved plan.

Do not initiate a decision merely because an interesting architectural question exists.

If current work does not depend on the answer yet, defer the decision.

---

## 2. Check Whether the Decision Already Exists

Before comparing new options, inspect:

1. `docs/project/decisions/README.md`;
2. applicable ADRs under `docs/project/decisions/`;
3. `docs/project/definition.md`;
4. relevant repository rules and instructions;
5. relevant existing implementation when necessary.

If an accepted ADR already resolves the issue, follow it.

Do not reopen an accepted decision merely because another option is also reasonable.

If new information materially challenges an accepted ADR:

1. identify the affected ADR;
2. explain what assumption or constraint has changed;
3. explain why reconsideration may be necessary;
4. initiate a new decision process only when reconsideration is justified.

Do not silently rewrite an accepted decision.

---

## 3. Define the Decision Precisely

State the decision as a concrete project-specific question.

Prefer:

```text
How should authenticated browser state be maintained for this
application?
```

over:

```text
Which authentication technology is best?
```

Prefer:

```text
How should short-lived OTP verification state be represented and
stored for this project's requirements?
```

over:

```text
Should we use Redis?
```

The decision statement SHOULD avoid prematurely embedding one proposed solution into the question.

If the issue actually contains multiple independent decisions, separate them when doing so improves clarity and prevents
unnecessary coupling.

Do not force several decisions into one large architectural choice solely for convenience.

---

## 4. Establish Decision Drivers

Identify the project-specific factors that should determine the outcome.

Use evidence from:

- confirmed project requirements;
- technical constraints;
- architecture principles;
- accepted ADRs;
- existing implementation;
- security requirements;
- operational requirements;
- current project size and complexity;
- confirmed future requirements.

Decision drivers MAY include:

- simplicity;
- security;
- maintainability;
- framework compatibility;
- implementation complexity;
- operational complexity;
- testability;
- reversibility;
- performance;
- scalability where actually relevant;
- team familiarity where known;
- vendor coupling;
- failure behavior.

Prioritize drivers that materially affect this project.

Do not optimize for hypothetical requirements that have not been accepted.

---

## 5. Identify Viable Options

Identify the strongest viable approaches for the decision.

Three options are generally a useful target when three genuinely strong alternatives exist.

The agent MUST NOT invent a weak option merely to reach three.

If only one or two approaches are genuinely reasonable, present only those.

Likewise, do not overwhelm the user with every theoretically possible technique.

Prefer a small set of distinct options that represent meaningful trade-offs.

### 5.1 Filter Non-viable Options

An option SHOULD NOT be presented as a serious candidate when it:

- violates confirmed project requirements;
- conflicts with an applicable accepted ADR;
- creates an unacceptable security weakness;
- is incompatible with confirmed infrastructure;
- adds clearly disproportionate complexity;
- depends on assumptions known to be false.

When a commonly suggested option is excluded for an important reason, the agent MAY mention briefly why it was not
considered viable.

---

## 6. Research When Necessary

Use the information required to make the decision accurately.

When the choice depends materially on information that can change over time, such as:

- framework capabilities;
- supported versions;
- security recommendations;
- library maintenance status;
- deployment support;
- current standards;
- vendor behavior;

verify the relevant current information before making the recommendation when appropriate tools are available.

Prefer authoritative primary sources for technical facts.

Do not turn every decision into broad research when stable project knowledge is sufficient.

---

## 7. Compare the Options

For each viable option, explain enough for the user to make an informed decision.

The comparison SHOULD normally include:

### How It Works

A concise practical explanation.

### Advantages

The important benefits for this project.

### Disadvantages

The important costs and limitations for this project.

### Complexity

When relevant, distinguish between:

- implementation complexity;
- conceptual complexity;
- operational complexity.

### Security

Explain material security implications when applicable.

### Maintainability

Explain important long-term maintenance implications.

### Project Fit

Explain how well the option fits the project's current requirements, size, constraints, and architecture principles.

Do not provide generic textbook comparisons when project-specific consequences can be identified.

---

## 8. Teach Enough for an Informed Decision

When the decision involves concepts the user may need to understand, explain them before requiring a choice.

Prefer practical explanations connected to the current project.

Explain:

- what changes in actual system behavior;
- what complexity the option introduces;
- what the user or team would need to maintain;
- what future choices the option constrains or preserves.

Avoid unexplained jargon.

Do not hide meaningful trade-offs behind phrases such as:

```text
best practice
industry standard
more scalable
more enterprise-ready
```

unless the concrete relevance to this project is explained.

---

## 9. Provide a Recommendation

After comparing the viable options, recommend the option that best satisfies the decision drivers for this project.

The recommendation MUST include the reasoning that led to it.

The agent SHOULD also state the most important trade-off being accepted.

For example:

```text
Recommendation: Option B.

It provides the required isolation and testability without introducing
the additional layers of Option C. The main trade-off is that some
framework coupling remains intentionally visible.
```

The recommendation MUST NOT be presented as an already accepted decision.

Do not proceed based solely on the recommendation.

---

## 10. Stop for the User's Decision

After presenting the comparison and recommendation, stop for user input.

Do not:

- implement the recommended option;
- install dependencies;
- create application code;
- modify architecture;
- create an accepted ADR;
- start the next implementation batch.

The user may:

- choose an option;
- ask for more explanation;
- modify an option;
- combine compatible aspects of options;
- reject all presented options;
- introduce a new constraint;
- defer the decision.

Continue the decision process until the user's intent is sufficiently clear.

---

## 11. Recognize an Accepted Decision

A decision is accepted only when the user communicates clear intent to select or accept an approach.

Examples may include statements equivalent to:

```text
Use option 2.
```

```text
Let's go with Django sessions.
```

```text
I agree with the recommended approach.
```

Questions, tentative reactions, or requests for clarification are not acceptance.

For example:

```text
Option 2 looks interesting.
```

does not necessarily accept Option 2.

When acceptance is ambiguous and the distinction materially matters, remain in `DECIDE`.

---

## 12. Determine Whether the Decision Is ADR-worthy

After the user accepts the decision, determine whether it should be preserved as an ADR.

An accepted decision is generally ADR-worthy when its reasoning would remain useful to a future engineer and when it
materially affects:

- architecture;
- significant technical boundaries;
- security;
- authentication or authorization;
- persistent data;
- external integrations;
- important dependency strategy;
- infrastructure;
- deployment;
- operational behavior;
- significant testing strategy;
- long-term maintainability.

Do not create an ADR for every accepted implementation detail.

If the decision is not ADR-worthy, return to the parent workflow without creating one.

---

## 13. Record an ADR-worthy Decision

For an ADR-worthy accepted decision:

1. read `docs/project/decisions/README.md`;
2. use `docs/project/decisions/template.md`;
3. determine the next unused four-digit ADR number;
4. choose a short descriptive kebab-case file name;
5. create the ADR with status `Accepted`;
6. use the current decision date;
7. preserve the accepted decision accurately;
8. summarize the strongest considered alternatives;
9. record the actual project-specific rationale;
10. record meaningful positive and negative consequences;
11. include useful references where appropriate;
12. update the Decision Register in `docs/project/decisions/README.md`.

Do not copy the entire exploratory conversation into the ADR.

Distill it into the context and reasoning needed for future understanding.

Do not alter the substance of the user's accepted decision while documenting it.

---

## 14. Superseding an Existing ADR

When the newly accepted decision intentionally replaces an existing accepted ADR:

1. create a new ADR rather than materially rewriting the old decision;
2. explain the changed context or reasoning in the new ADR;
3. mark the previous ADR as `Superseded`;
4. identify the new ADR in the previous record;
5. reference the previous ADR from the new one;
6. update the Decision Register.

Preserve historical reasoning.

Do not treat the newest ADR as a replacement unless the new decision actually supersedes the earlier one.

---

## 15. Recording Is Not Implementation

After recording the decision, the agent MUST preserve the workflow boundary:

```text
accepted decision
      ↓
RECORD DECISION
      ↓
PLAN
      ↓
USER APPROVAL
      ↓
IMPLEMENT
```

Creating or updating the ADR does not authorize implementation.

Do not:

- modify application code;
- install or remove dependencies;
- change runtime configuration;
- generate migrations;
- modify infrastructure;
- perform state-changing Git operations;

merely because the decision has been accepted and recorded.

Return control to the parent workflow so that implementation can be planned separately.

---

## 16. Decision Output

Before the user has decided, present the decision in a structure that is easy to review.

A useful default is:

```text
Decision needed:
<precise question>

Why now:
<why current work depends on it>

Decision drivers:
- ...
- ...

Option 1 — ...
<comparison>

Option 2 — ...
<comparison>

Option 3 — ...
<comparison, only if genuinely viable>

Recommendation:
<option + project-specific reasoning>

Implementation:
Not started. Waiting for your decision.
```

Adapt the presentation to the complexity of the decision.

Do not create unnecessary ceremony for a simple decision.

---

## 17. Completion Conditions

Before user acceptance, this skill is complete for the current turn when:

```text
DECIDE
→ waiting for user decision
```

After user acceptance, it is complete when either:

```text
accepted non-ADR decision
→ return to parent workflow
```

or:

```text
accepted ADR-worthy decision
→ RECORD DECISION
→ ADR recorded
→ return to parent workflow
```

In every case:

```text
implementation has not started
```
