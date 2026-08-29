# Contributing

Thank you for helping improve the AI-Native Python Project Boilerplate.
Contributions are welcome through issues, discussions, and pull requests that
keep the baseline reusable, understandable, and proportionate.

## Choose the Right Path

Use the repository in one of two distinct ways:

- To start an independent project, use GitHub's **Use this template** action.
  Customize the generated repository for that project's needs.
- To improve this boilerplate, fork this repository and open a pull request
  back to it.

A project created from the template has its own requirements and support
responsibilities. Project-specific application code normally does not belong
in this boilerplate.

## Before Opening an Issue

- Search existing issues to avoid duplicates.
- Use the matching issue form and provide enough context to reproduce or
  evaluate the request.
- Read [SUPPORT.md](SUPPORT.md) for usage questions.
- Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).
  Do not disclose suspected vulnerabilities in a public issue.

## Development Setup

Prerequisites:

- Git;
- Python 3.13 or 3.14;
- [uv](https://docs.astral.sh/uv/).

Node.js is not a project prerequisite. The configured pre-commit hook manages
the runtime needed by its Markdown tooling.

After cloning your fork:

```bash
uv sync --locked --all-groups
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

Keep `uv.lock` synchronized whenever project dependency metadata changes.
See [Development Tooling](docs/development-tooling.md) for focused commands,
hook behavior, and ownership of each quality check.

## Branches and Commits

Use a short, descriptive branch name. An issue number is welcome when one
exists, but it is not mandatory for public contributors.

Keep each branch and commit focused on one coherent change. Do not combine
unrelated cleanup with the contribution.

Commit messages should explain the change clearly. They do not have to follow
Conventional Commits because the pull-request title is the canonical squash
commit title.

## Quality Checks

Before requesting review, run:

```bash
uv lock --check
uv run pre-commit run --all-files
uv run pytest --cov --cov-report=term-missing
```

The repository requires at least 95% test coverage. New or changed behavior
should include focused tests.

## Pull Requests

Pull requests may be opened before they are complete, but they cannot be
merged until all required policies pass.

Human-authored pull requests must:

- use a Conventional Commit title such as
  `feat(scope): describe the change`;
- keep the title at or below 100 characters;
- complete the Summary, Motivation, Testing, and Checklist sections;
- pass CI, compatibility, dependency-review, and PR-policy checks;
- resolve review conversations;
- receive the required Code Owner approval.

Supported title types are `build`, `chore`, `ci`, `docs`, `feat`, `fix`,
`perf`, `refactor`, `revert`, and `test`.

Automated Dependabot pull requests must satisfy the title policy but use their
generated body instead of the human pull-request template.

Only the repository owner and explicitly authorized collaborators may merge a
pull request. Opening a contribution or receiving approval does not grant
merge access.

## Review Expectations

Review prioritizes correctness, security, maintainability, scope control, and
fit for a reusable boilerplate. A contribution may be declined when it is too
project-specific, adds speculative complexity, or conflicts with the accepted
baseline.

Maintainers may ask contributors to split broad pull requests into smaller,
reviewable changes.

## Licensing

By submitting a contribution, you agree that your contribution may be
distributed under the repository's [MIT License](LICENSE). Git history is the
primary record of contribution authorship; per-file author headers are not
required.

Participation in this project is governed by the
[Code of Conduct](CODE_OF_CONDUCT.md).
