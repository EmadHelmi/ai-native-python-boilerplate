# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for meaningful technical and architectural decisions made
in this project.

An ADR preserves:

- the context in which a decision became necessary;
- the important factors that influenced the decision;
- the strongest viable options that were considered;
- the decision that was accepted;
- the reasoning behind that decision;
- the important consequences of adopting it.

The purpose of ADRs is to preserve engineering reasoning, not to document every implementation detail.

---

## 1. When to Create an ADR

Create an ADR when a decision materially affects one or more of the following:

- architecture;
- application boundaries;
- public interfaces or APIs;
- authentication or authorization;
- security;
- persistent data;
- integration strategy;
- important dependencies;
- infrastructure;
- deployment;
- operational behavior;
- testing strategy;
- developer workflow;
- long-term maintainability.

An ADR SHOULD describe a decision whose reasoning would still be useful to someone reviewing the project later.

Do not create ADRs for trivial, local, or easily reversible implementation details.

Examples that normally do not require ADRs include:

- variable names;
- small private helper functions;
- minor formatting choices;
- obvious framework configuration implied by an accepted decision;
- routine implementation details inside an approved implementation batch.

---

## 2. Do Not Decide Everything Up Front

Not every unresolved question must be answered during project initialization.

When an unresolved technical question is identified, classify it conceptually as one of:

1. **Must decide now**
   - Implementation cannot safely proceed without resolving it.

2. **Decide before related implementation**
   - The decision matters, but current work does not depend on it yet.

3. **Defer until needed**
   - The decision would currently be speculative or lacks enough information.

The project SHOULD avoid both:

- excessive up-front design for problems that may never occur;
- postponing important decisions until implementation has already made them expensive to change.

Agents MUST NOT create speculative ADRs for decisions that are not required by the current or immediately upcoming work.

When a meaningful unresolved decision becomes necessary, the agent SHOULD initiate the project's Decision Protocol.

After the user explicitly accepts an ADR-worthy decision, the agent SHOULD create the corresponding ADR before
implementation that depends on that decision begins.

An unresolved question by itself is not a reason to create an ADR.

The intended approach is just-in-time architectural decision-making: make a decision late enough to have useful
context, but early enough that implementation has not already made the choice expensive to change.

---

## 3. Decision Workflow

The normal decision workflow is:

```text
current work requires a meaningful decision
        ↓
DISCUSS
        ↓
identify viable options
        ↓
compare trade-offs
        ↓
recommendation
        ↓
USER DECISION
        ↓
RECORD DECISION
        ↓
continue to ~~PLAN~~
```

The exploratory discussion may contain considerably more detail than the resulting ADR.

The ADR SHOULD preserve the information needed to understand the accepted decision without attempting to reproduce the
entire discussion.

In other words:

> Conversation is where options are explored.
> The ADR is where the resulting decision is preserved.

---

## 4. Considered Options

For a meaningful decision with multiple viable approaches, the strongest options SHOULD be considered before making the
decision.

Three options are generally a useful target when three genuinely strong alternatives exist.

Do not manufacture weak alternatives solely to reach a fixed number.

Each ADR SHOULD preserve enough information about rejected alternatives to explain why the selected approach was
preferable for this project.

Detailed comparison belongs in the decision process when needed; the ADR SHOULD contain a concise summary.

---

## 5. ADR Status

The supported ADR statuses are:

### `Proposed`

The decision has been documented but is not yet accepted.

Use this status only when keeping an unaccepted proposal in the repository provides real value.

Interactive decisions will normally not require a `Proposed` ADR.

### `Accepted`

The decision has been accepted and is currently authoritative.

Implementation SHOULD follow accepted ADRs.

### `Rejected`

The recorded proposal was explicitly rejected.

Rejected ADRs MAY remain in the repository when retaining their reasoning provides useful historical context.

### `Superseded`

The decision was previously accepted but has been replaced by a newer ADR.

A superseded ADR MUST identify the ADR that replaced it.

Example:

```text
Status: Superseded by ADR-0012
```

---

## 6. Immutability of Accepted Decisions

An accepted ADR is a historical record.

After acceptance:

- typo fixes are allowed;
- formatting fixes are allowed;
- clarifications that do not alter the meaning are allowed.

A material change to the decision MUST NOT silently rewrite the accepted ADR.

Instead:

1. create a new ADR;
2. explain the reason for changing the decision;
3. mark the previous ADR as superseded;
4. link the old and new records.

This preserves the history of architectural reasoning.

---

## 7. Naming and Numbering

ADR files use four-digit sequential numbering:

```text
0001-project-architecture.md
0002-authentication-strategy.md
0003-otp-storage.md
```

The corresponding title inside the document uses:

```text
# ADR-0001: Project Architecture
```

Numbers are permanent historical identifiers.

A number MUST NOT be reused after an ADR has been created, even if that ADR is later rejected or superseded.

File names SHOULD use short, descriptive, lowercase kebab-case names.

---

## 8. Creating a New ADR

Use `template.md` as the starting point.

When creating a new ADR:

1. determine the next unused ADR number;
2. copy `template.md`;
3. rename the copy using the ADR number and a short descriptive name;
4. remove template guidance that is no longer needed;
5. record the accepted decision accurately;
6. update the Decision Register in this file.

Example:

```text
template.md
    ↓
0004-api-authentication.md
```

Do not modify `template.md` to record an actual project decision.

---

## 9. ADR Structure

ADRs in this repository use a lightweight structure:

1. **Status**
2. **Date**
3. **Context**
4. **Decision Drivers**
5. **Options Considered**
6. **Decision**
7. **Rationale**
8. **Consequences**
9. **References**

Sections SHOULD remain concise.

Not every ADR needs extensive prose in every section.

The goal is to preserve useful reasoning without turning architectural documentation into unnecessary ceremony.

---

## 10. Relationship to Other Project Documentation

### `AGENTS.md`

Defines how humans and AI agents work together.

It does not contain project architecture decisions.

### `docs/project/definition.md`

Defines what the project must build, including product requirements and confirmed technical constraints.

It SHOULD NOT contain detailed reasoning for architectural choices.

### `docs/project/decisions/`

Defines why meaningful technical choices were made.

An ADR MUST NOT silently redefine product requirements.

If an architectural decision requires changing a product requirement or confirmed constraint, update the appropriate
project documentation through the normal review process.

### Engineering Rules

Engineering rules define reusable coding and implementation standards.

ADRs SHOULD NOT duplicate general coding conventions.

---

## 11. Conflicting Decisions

When multiple ADRs appear relevant, the most recent applicable accepted decision takes precedence only when it
explicitly supersedes or revises an earlier decision.

Do not infer supersession merely from publication date.

If two accepted ADRs appear to conflict and neither explicitly resolves the conflict, the conflict MUST be surfaced and
resolved before dependent implementation proceeds.

---

## 12. Decision Register

Keep this table limited to actual ADR files.

Do not reserve ADR numbers for decisions that have not yet been made.

|                            ADR                             | Decision                |  Status  |
| :--------------------------------------------------------: | :---------------------- | :------: |
| [ADR-0001](0001-template-usage-profiles.md) | Template Usage Profiles | Accepted |

When an ADR is added, append the new record.

Example:

|    ADR     | Decision               |   Status   |
| :--------: | :--------------------- | :--------: |
| `ADR-0001` | Project Architecture   |  Accepted  |
| `ADR-0002` | Browser Authentication |  Accepted  |
| `ADR-0003` | OTP Storage            | Superseded |

---

## 13. Guiding Principle

ADRs exist to answer:

> Why does the project work this way?

If a future engineer can understand the important reasoning behind a decision without reconstructing old conversations
or Git history, the ADR has done its job.
