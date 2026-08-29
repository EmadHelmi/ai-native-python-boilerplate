<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Cursor Project Rules

This directory contains the repository's Cursor Project Rules.

Directory names help humans find related rules. They are not a classification
system. Every rule is classified by its origin and portability, independently
of the directory in which it is stored.

## Classification Model

| Classification | Meaning |
| :------------- | :------ |
| **GENERAL / ECOSYSTEM / PROJECT-NEUTRAL** | Guidance that is independent of a project, company, and reusable baseline |
| **BOILERPLATE / REUSABLE PROJECT BASELINE** | A deliberate default selected for this reusable project base, without claiming universal authority |
| **PERSONAL CONVENTION** | Emad's preference; useful when compatible, but not a team or ecosystem requirement |
| **PROJECT-SPECIFIC / COMPANY-SPECIFIC** | Guidance whose meaning depends on one repository, product, or organization |
| **HYBRID** | A general principle delivered through a concrete implementation selected by this baseline |

Classification answers where a rule gets its authority and how safely it can
be reused. Directory placement answers only where the rule is easiest to find.

## Current Rule Directories

| Directory | Scope |
| :-------- | :---- |
| [`meta/`](meta/README.md) | Rule governance, compatibility, documentation, and workflow behavior |
| [`repository/`](repository/README.md) | Repository-wide authorship and Git conventions |
| [`python/`](python/README.md) | Python engineering, tooling, observability, and testing |
| [`architecture/`](architecture/README.md) | Architecture, boundaries, persistence, workflows, and concurrency |
| [`django/`](django/README.md) | Django and Django REST Framework engineering |

Use only the directories that match a repository's actual stack. Folder
hierarchy is organizational; each `.mdc` file's frontmatter controls when
Cursor applies it.

## Classifying a New Rule

Use the narrowest classification that accurately describes the rule:

1. If it depends on a repository, product, or organization, classify it as
   **PROJECT-SPECIFIC / COMPANY-SPECIFIC**.
2. If it expresses Emad's preferred style, classify it as
   **PERSONAL CONVENTION**.
3. If it records a reusable default chosen for this project base, classify it
   as **BOILERPLATE / REUSABLE PROJECT BASELINE**.
4. If a project-neutral principle is coupled to that chosen implementation,
   classify it as **HYBRID**.
5. Otherwise, use **GENERAL / ECOSYSTEM / PROJECT-NEUTRAL** only when the rule
   genuinely has no project, company, or baseline dependency.

Do not infer classification from a filename or directory name. Record it in
the directory README and keep the normative rule in the `.mdc` file.

## Overlap and Precedence

Rules are not ordered by filename or directory.

When applicable rules overlap:

1. follow explicit repository and organization requirements for their scope;
2. treat boilerplate and hybrid rules as selected defaults, not universal
   standards;
3. apply general rules where a more specific requirement does not specialize
   them;
4. never let a personal convention override correctness or an authoritative
   requirement;
5. surface material conflicts rather than silently choosing one.

The machine-facing policy lives in
[`meta/compliance.mdc`](meta/compliance.mdc).

## Personal Conventions

Files containing `convention` in their filename are personal conventions. The
recommended ignore policy is:

```gitignore
.cursor/**/*convention*.mdc
```

Shared rules should use semantic names that do not contain `convention`, such
as `standards.mdc` or `file-authorship.mdc`.

## Application Modes

Use the narrowest application mode that reliably provides a rule when needed:

- **Always Apply** for small policies relevant to arbitrary work;
- **Specific Files** for rules selected by file globs;
- **Apply Intelligently** for detailed guidance needed only for a described
  concern;
- **Manual** only when deliberate invocation is part of the intended workflow.

## Maintaining These READMEs

Each rule directory has a human-facing `README.md` that records:

- the directory's scope;
- every current rule and its classification;
- its application mode and concise purpose;
- important inclusion, exclusion, or maintenance boundaries.

README files summarize the inventory and must not duplicate the normative rule
text. Cursor consumes `.mdc` files as Project Rules; README files are for human
navigation and review.
