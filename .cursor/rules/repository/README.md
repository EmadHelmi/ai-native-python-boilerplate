<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Repository Rules

This directory contains conventions that apply across repository artifacts,
independently of a specific language, framework, or application architecture.

## Current Rules

| Rule | Classification | Application | Purpose |
| :--- | :------------- | :---------- | :------ |
| [`file-authorship.mdc`](file-authorship.mdc) | BOILERPLATE / REUSABLE PROJECT BASELINE | Apply Intelligently (opt-in) | Offer a strict per-file authorship convention for projects that adopt it |
| [`branch-discipline.mdc`](branch-discipline.mdc) | BOILERPLATE / REUSABLE PROJECT BASELINE | Apply Intelligently (opt-in) | Offer focused commits and strict issue-numbered branches for projects that adopt them |

## Branch Discipline

The reusable strict profile treats each branch as one coherent, independently
reviewable unit of work and uses this branch-name format:

```text
<type>/<number>-<short-name>
```

This format is not required for public contributions to the boilerplate. A
derived project may explicitly adopt it when mandatory traceability is useful.
The profile uses the issue or task number when one is available and otherwise
permits a mandatory per-type incremental fallback number. See
[`branch-discipline.mdc`](branch-discipline.mdc) for allocation and validation
requirements.

The authorship profile is also optional. Without explicit adoption, Git history
and the repository license remain the authoritative provenance mechanisms.

Branch source selection is a separate, project-neutral concern governed by
[`../meta/git-workflow.mdc`](../meta/git-workflow.mdc).

## Boundaries

Keep language, framework, architecture, and rule-governance concerns in their
corresponding directories. Do not use `repository/` as miscellaneous storage.

A personal repository-wide preference may live here, but its filename must
contain `convention` so the local-only ignore policy applies. Shared rules use
semantic names such as `file-authorship.mdc`.
