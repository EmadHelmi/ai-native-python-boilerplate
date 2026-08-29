# ADR-0001: Template Usage Profiles

## Status

Accepted

## Date

2026-08-26

## Context

The canonical boilerplate repository must be suitable for public release and
external contributions. It therefore needs community health files, GitHub
pull-request policies, repository automation, and a public license.

Most projects created from the boilerplate, however, are expected to be
personal or internal projects maintained by Emad. Carrying the complete public
collaboration layer into those repositories would add files and workflows that
do not serve their normal use case.

The reusable engineering baseline, repository rules, and human-agent workflow
remain valuable in both cases. A lighter project profile must not weaken or
alter those parts of the boilerplate.

---

## Decision Drivers

### Drivers

- Keep one canonical source of truth for reusable engineering configuration.
- Preserve GitHub's **Use this template** workflow.
- Make the common personal or internal setup small and predictable.
- Keep public collaboration infrastructure available when it is needed.
- Prevent profile selection from changing any agent instruction or engineering
  rule.
- Avoid maintaining duplicate repositories or long-lived branches.
- Keep profile application deterministic and testable.

---

## Options Considered

### Option 1 — One Template with Setup Profiles

Keep a complete canonical repository and provide a one-time setup mechanism
that selects either a `solo` or `collaborative` profile.

#### Advantages

- Maintains one source of truth.
- Preserves the normal GitHub template experience.
- Makes the resulting solo repository intentionally smaller.
- Allows profile behavior to be tested as part of the canonical repository.

#### Disadvantages

- Starting a derived project requires one additional setup step.
- The setup mechanism must safely remove and update files.

---

### Option 2 — Separate Full and Minimal Repositories

Maintain independent collaborative and minimal boilerplate repositories.

#### Advantages

- Each repository can be used directly without a transformation step.
- The contents of each variant are immediately visible.

#### Disadvantages

- Rules, dependencies, tooling, and fixes can drift between repositories.
- Most maintenance work must be repeated and reconciled.
- It recreates the synchronization problem this boilerplate is intended to
  avoid.

---

### Option 3 — Dedicated Template Generator

Use a conditional generator such as Copier or Cookiecutter to render only the
selected files.

#### Advantages

- Produces a clean output without first creating unwanted files.
- Can support rich interactive customization.

#### Disadvantages

- Introduces another tool and template language.
- Makes GitHub's **Use this template** action secondary or incompatible with
  the primary workflow.
- Adds disproportionate implementation and maintenance complexity for the two
  required variants.

---

## Decision

Use one canonical, collaborative boilerplate repository with a deterministic
first-use setup mechanism supporting two profiles:

- `collaborative` retains the complete public collaboration and publication
  layer, including GitHub automation, contribution infrastructure, and the MIT
  project license;
- `solo` removes the public collaboration and publication layer while
  preserving the complete reusable engineering baseline.

The following content MUST remain identical and available in both profiles:

- `AGENTS.md`;
- `.agents/` and all agent skills;
- `.cursor/` and all engineering rules;
- the repository's human-agent approval workflow;
- local quality tooling and Git hooks;
- project-definition and decision-record infrastructure;
- secure-coding, dependency-safety, and secret-handling rules.

The `solo` profile removes the repository's `.github/` directory, public
community health files, the root project `LICENSE`, MIT project metadata, and
tests that exist only for removed GitHub pull-request policy. It also removes
only the corresponding public-collaboration and project-license references
from shared documentation.

The `solo` profile does not declare the derived project to be MIT-licensed.
The canonical boilerplate's MIT notice is retained as provenance in
`THIRD_PARTY_NOTICES.md`; it is not presented as the license of the derived
project.

---

## Rationale

The selected approach gives the common solo or internal workflow a small
repository without splitting the reusable baseline into independently
maintained copies. It also keeps the public source repository fully prepared
for external contributions.

Treating public collaboration as a removable layer is a better fit than
weakening the underlying rules or agent workflow. The main accepted trade-off
is an additional initialization step when creating a derived project.

---

## Consequences

### Positive

- Engineering rules and agent behavior cannot drift between profiles.
- Public-repository infrastructure no longer burdens typical solo projects.
- The canonical repository remains ready for public contribution.
- Improvements to the shared baseline are maintained once.

### Negative

- The profile mechanism needs its own safety checks and tests.
- A generated project is not in its final form until profile setup completes.
- An unchanged rule currently contains an inert reference to
  `CONTRIBUTING.md`, which is absent from the `solo` profile.
- `THIRD_PARTY_NOTICES.md` remains in solo projects to preserve provenance even
  though the project itself is not declared MIT-licensed.

### Follow-up Implications

- Define the exact tracked-file manifest for each profile.
- Make profile application deterministic, explicit, and safe for a newly
  generated repository.
- Verify both resulting profiles independently.
- Document profile selection near the beginning of the root README.
- Do not implement profile-specific changes inside rules or agent files.

---

## References

- [The MIT License — Open Source Initiative](https://opensource.org/license/mit)
- [Licensing a repository — GitHub Docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
