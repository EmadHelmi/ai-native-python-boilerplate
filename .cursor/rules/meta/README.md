<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Meta Rules

Install this directory with every rule set. It contains guidance about how
rules, documentation, compatibility, and the human-agent workflow operate.

## Current Rules

| Rule | Classification | Application | Purpose |
| :--- | :------------- | :---------- | :------ |
| [`compatibility.mdc`](compatibility.mdc) | HYBRID | Always Apply | Combine version-awareness with the concrete baselines reviewed for this rule set |
| [`compliance.mdc`](compliance.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Always Apply | Define relevance, precedence, conflicts, and intentional exceptions |
| [`git-workflow.mdc`](git-workflow.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Always Apply | Choose branch sources explicitly and avoid hidden long-lived branch chains |
| [`markdown.mdc`](markdown.mdc) | HYBRID | Specific Files | Combine general documentation quality with the selected Markdown baseline |
| [`workflow.mdc`](workflow.mdc) | BOILERPLATE / REUSABLE PROJECT BASELINE | Always Apply | Document the approval-controlled workflow selected for this project base |

## Boundaries

Keep this directory focused on the rule system and cross-cutting workflow. A
rule does not belong here merely because it applies to many files. Put
language, framework, architecture, and repository artifact guidance in their
more relevant directories.

The classification describes each rule's origin and portability; the shared
directory does not imply that every rule has the same classification.
