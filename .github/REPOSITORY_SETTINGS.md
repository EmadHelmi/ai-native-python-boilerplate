# Repository Settings

This document records the intended GitHub settings for
`EmadHelmi/ai-native-python-boilerplate`. The repository-local files define
automation and policy; GitHub settings must be applied and verified separately
after the initial publication.

## General

- Visibility: public.
- Default branch: `main`.
- Template repository: enabled.
- Issues: enabled.
- Wiki: disabled.
- Topics: `python`, `python-boilerplate`, `project-template`, `uv`, `ruff`,
  `pyright`, `pytest`, and `ai-agents`.
- Merge method: squash only.
- Default squash commit title: pull-request title.
- Default squash commit message: pull-request body.
- Automatically delete head branches: enabled.
- Auto-merge: disabled.

## Actions

- Allow actions created by GitHub.
- Allow `astral-sh/setup-uv@*` as the required third-party action.
- Default workflow permissions: read repository contents and packages.
- Allow GitHub Actions to create and approve pull requests: disabled.

Every third-party action used by this repository is pinned to an immutable
commit SHA in its workflow file.

## Main Branch Ruleset

Apply [the versioned ruleset blueprint](rulesets/main.json) to the default
branch. It requires:

- pull requests with one approving review;
- Code Owner review and dismissal of stale approvals;
- resolution of review conversations;
- squash merging and linear history;
- an up-to-date branch with all required status checks passing;
- protection against branch deletion and force pushes.

The required status checks are:

- `Quality gate`;
- `Compatibility gate`;
- `Review dependency changes`;
- `Validate metadata`.

Repository administrators have pull-request-only bypass. This preserves an
auditable PR trail for emergency recovery without allowing ordinary direct
pushes to `main`. Merge permission still depends on repository access granted
by the owner.

## Security and Dependencies

- Dependency graph: enabled.
- Dependabot alerts: enabled.
- Dependabot security updates: enabled.
- Private vulnerability reporting: enabled.
- Secret scanning: enabled.
- Push protection for secrets: enabled.
- CodeQL default setup: enabled for Python on this canonical public GitHub
  repository.

Scheduled version updates remain defined in `dependabot.yml`. Vulnerabilities
must be reported through the private path in the root `SECURITY.md`.

CodeQL default setup is a setting of the canonical GitHub repository. It does
not add reusable workflow files to the boilerplate and is not inherited by
repositories created from the template or hosted on GitLab.

## Publication Verification

After applying these settings:

1. confirm the repository reports itself as a public template;
2. confirm only squash merge is offered on pull requests;
3. inspect the active ruleset and its bypass list;
4. open a test pull request and confirm all four required checks run;
5. confirm an external contributor cannot merge or push to `main`;
6. confirm the security reporting form is available;
7. confirm the documented topics and CodeQL default setup are active;
8. compare the live settings with this document and the ruleset JSON.
