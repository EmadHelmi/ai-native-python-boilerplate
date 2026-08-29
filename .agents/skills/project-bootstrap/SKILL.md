---
name: project-bootstrap
description: >-
  Start or resume development of a project by reading its repository
  instructions, project definition, accepted decisions, and current state;
  identify the smallest useful next milestone, surface any decision or missing
  context that blocks it, and stop at the appropriate human-approval boundary
  before implementation.
---

# Project Bootstrap

Use this skill when starting development of a project, resuming work whose next implementation step is not yet
established, or when the user asks to begin or continue the project from its repository-defined workflow.

This skill bootstraps the engineering process.

It does not bootstrap the application autonomously.

## Objective

Determine the correct next step from the repository's current state while preserving:

- the project's defined requirements;
- accepted architectural and technical decisions;
- the human-agent working agreement;
- incremental development;
- just-in-time decision-making;
- explicit implementation approval.

The outcome of this skill is normally one of:

1. a meaningful decision that must be discussed;
2. a material requirement or context gap that must be clarified;
3. a small, coherent implementation plan waiting for user approval.

The outcome is not autonomous implementation.

---

## 1. Read the Repository Context

Before proposing implementation, inspect the repository context relevant to understanding what should happen next.

At minimum, look for and read:

1. `AGENTS.md`;
2. `docs/project/definition.md`;
3. `docs/project/decisions/README.md`;
4. existing ADRs under `docs/project/decisions/`;
5. relevant engineering rules;
6. the current repository structure and implementation state.

Use read-only inspection as needed to understand the repository.

Do not mutate the repository during this phase.

---

## 2. Respect Source Responsibilities

Interpret repository sources according to their defined responsibilities.

In particular:

- `AGENTS.md` defines how the agent works;
- engineering rules define reusable implementation standards;
- `docs/project/definition.md` defines what the project must build;
- accepted ADRs define decisions already made;
- `.local/` may contain reference material but is not automatically authoritative.

Do not merge these responsibilities into a new source of truth.

Do not silently override one source with another.

If relevant authoritative sources conflict, surface the conflict according to `AGENTS.md`.

---

## 3. Validate Project Readiness

Before deciding what to implement, determine whether the project definition provides enough information for the next
meaningful step.

Do not require the entire project to be fully specified before development begins.

A missing detail is blocking only when the current or immediately upcoming work materially depends on it.

If a project-definition template is still substantially unfilled, or a missing requirement prevents a meaningful next
step:

1. identify the minimum missing information;
2. explain why it blocks progress;
3. return to `DISCUSS`;
4. stop before implementation.

Do not invent product requirements to fill documentation gaps.

---

## 4. Inspect the Current State

Determine what already exists before proposing new work.

Inspect relevant information such as:

- repository structure;
- existing application or package structure;
- dependency configuration;
- existing source files;
- existing tests;
- existing configuration;
- Git status when relevant;
- accepted ADRs;
- already completed project capabilities.

Do not assume that a planned or documented capability has already been implemented.

Do not repeat completed initialization work merely because this skill is called "bootstrap."

The skill MUST work both for a new repository and for a partially implemented project.

---

## 5. Identify the Smallest Useful Next Milestone

Determine the smallest coherent milestone that meaningfully advances the project.

The next milestone SHOULD be:

- required by the project definition or an accepted decision;
- compatible with the current repository state;
- small enough for meaningful human review;
- large enough to produce useful progress;
- independently verifiable where practical;
- free of speculative adjacent scope.

Prefer prerequisite work before dependent work.

Do not create a complete long-term implementation roadmap unless the user explicitly asks for one.

The objective is to determine the next useful milestone, not to pre-plan the entire project.

---

## 6. Check for Blocking Decisions

Before planning implementation, determine whether the next milestone depends on a meaningful unresolved decision.

A decision is potentially blocking when proceeding would otherwise silently choose among materially different
approaches affecting areas such as:

- architecture;
- application boundaries;
- authentication or authorization;
- security;
- persistent data;
- external contracts;
- important dependencies;
- infrastructure;
- deployment;
- operational behavior;
- testing strategy;
- long-term maintainability.

If an applicable accepted ADR already resolves the issue, follow it.

Do not reopen an accepted decision merely because another approach appears preferable.

If no accepted decision exists and the decision is required now or for the immediately upcoming work:

1. explain why the decision is now necessary;
2. transition to the project's Decision Protocol;
3. compare viable approaches according to that protocol;
4. do not make the decision for the user;
5. stop for user input.

Do not create speculative ADRs for decisions that current work does not require.

---

## 7. Use Just-in-Time Decisions

Do not attempt to resolve all known unknowns during project startup.

For each unresolved question encountered, reason conceptually as follows:

### Must Decide Now

The next meaningful milestone cannot safely proceed without the decision.

Initiate the Decision Protocol.

### Decide Before Related Implementation

The decision matters, but current work does not yet depend on it.

Defer it.

### Defer Until Needed

The decision is currently speculative, lacks useful context, or may never become necessary.

Defer it.

Do not create placeholder ADRs or reserve ADR numbers for deferred decisions.

---

## 8. Recording an Accepted Decision

When the user explicitly accepts an ADR-worthy decision:

1. preserve exactly what was accepted;
2. follow `docs/project/decisions/README.md`;
3. use `docs/project/decisions/template.md`;
4. determine the next unused ADR number;
5. create the corresponding ADR before implementation that depends on it begins;
6. update the Decision Register when required by the ADR policy.

Do not change the substance of the accepted decision while documenting it.

If material ambiguity becomes apparent while recording the decision, return to `DECIDE`.

Recording an accepted decision does not authorize implementation.

---

## 9. Prepare the Next Implementation Batch

When no unresolved blocker remains, transition to `PLAN`.

Prepare one coherent implementation batch according to `AGENTS.md`.

Where applicable, identify:

### Goal

What this batch will accomplish.

### Expected Changes

Important files, directories, configuration, dependencies, or components expected to change.

### Mutating Commands

Important commands expected to:

- create or modify project files;
- change dependencies;
- generate framework artifacts;
- alter persistent state;
- change Git state.

Read-only inspection commands do not need to be exhaustively enumerated.

### Verification

The checks that should establish confidence in the batch.

### Explicit Exclusions

Important adjacent work that is deliberately not included.

---

## 10. Stop at the Approval Boundary

After presenting the implementation plan, stop.

Do not:

- execute mutating commands;
- create application code;
- install dependencies;
- generate framework structures;
- make migrations;
- change Git state;
- continue into adjacent milestones.

Wait for explicit implementation approval according to `AGENTS.md`.

A user's request to "start the project" authorizes this bootstrap workflow.

It does not, by itself, authorize implementation of whatever milestone the workflow discovers.

---

## 11. Progress Reporting

For a multi-stage project, follow the progress-reporting policy in `AGENTS.md`.

When bootstrapping a project, report the current meaningful stage and overall progress when that information can be
estimated reasonably.

Do not invent precise percentages when the total scope is still too uncertain.

If the number of stages changes materially as the project becomes better understood, update the estimate and explain the
change briefly.

---

## 12. What This Skill Must Not Do

This skill MUST NOT:

- autonomously choose a meaningful architecture;
- resolve product ambiguity by assumption;
- create speculative ADRs;
- design the entire project up front;
- install dependencies merely because they will probably be useful;
- create application structure before its blocking decisions are resolved;
- introduce unrequested features;
- add speculative abstractions;
- treat a recommendation as a user decision;
- treat a recorded decision as implementation approval;
- commit, push, merge, or otherwise mutate Git state without the required approval.

---

## 13. Completion Condition

This skill is complete when control has been returned to the user at the earliest appropriate boundary.

That boundary will normally be one of:

```text
DISCUSS
```

because material project information is missing;

```text
DECIDE
```

because a meaningful decision blocks the next milestone;

or:

```text
PLAN
→ USER APPROVAL
```

because the next implementation batch is sufficiently defined.

Do not continue past that boundary autonomously.
