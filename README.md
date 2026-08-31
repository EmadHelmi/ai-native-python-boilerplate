# AI-Native Python Project Boilerplate

A production-oriented Python baseline with modern quality tooling, reusable
engineering rules, and human-controlled AI-agent workflows.

Use it to start an independent Python project.

<!-- template-profile:collaborative:start -->

Contributions that improve the shared boilerplate are welcome.

## Choose Your Path

### Start an Independent Project

Create a repository with GitHub's **Use this template** action, then select the
profile that matches how the new project will be maintained.

For a personal or internal repository, preview and apply `solo`:

```bash
uv run python scripts/setup_profile.py solo
uv run python scripts/setup_profile.py solo --apply
```

`solo` removes public GitHub collaboration infrastructure and the project-level
MIT declaration. It preserves all Agent Skills, engineering Rules, local hooks,
and quality tooling.

[![CI](https://github.com/EmadHelmi/ai-native-python-boilerplate/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/EmadHelmi/ai-native-python-boilerplate/actions/workflows/ci.yml)
[![Python 3.13 and 3.14](https://img.shields.io/badge/Python-3.13%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[![Use this template](https://img.shields.io/badge/Use_this_template-2EA44F?style=for-the-badge&logo=github&logoColor=white)](https://github.com/EmadHelmi/ai-native-python-boilerplate/generate)
[![Contribute](https://img.shields.io/badge/Contribute-0969DA?style=for-the-badge&logo=github&logoColor=white)](CONTRIBUTING.md)

For a public or multi-contributor repository, validate and keep
`collaborative`:

```bash
uv run python scripts/setup_profile.py collaborative
```

`collaborative` retains GitHub automation, contribution infrastructure, and
the [MIT License](LICENSE).

To improve this boilerplate itself, read [Contributing](CONTRIBUTING.md) and
open a pull request from a fork. Usage questions belong in the channels
described by [Support](SUPPORT.md); vulnerabilities must follow the private
reporting process in [Security](SECURITY.md). Participation is governed by the
[Code of Conduct](CODE_OF_CONDUCT.md).

The detailed profile and setup flow is documented in
[Getting Started](docs/getting-started.md).

<!-- template-profile:collaborative:end -->

## Quick Start

Prerequisites are Git, [uv](https://docs.astral.sh/uv/), and Python 3.13 or
3.14. Node.js is not required for the configured hooks.

```bash
uv sync --locked --all-groups
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
uv run pytest --cov --cov-report=term-missing
```

uv manages `.venv` and runs project tools without requiring manual activation.

## What the Baseline Provides

- dependency and environment management with uv and a committed lockfile;
- Ruff formatting, linting, and import ordering;
- reproducible Pyright type checking;
- pytest with branch coverage enforcement;
- pre-commit and pre-push quality gates;
- reusable Python, Django, architecture, repository, and meta Rules;
- an explicit human-agent working agreement;
- Agent Skills for project startup, technical decisions, implementation, and
  verification;
- project-definition and Architecture Decision Record foundations;
- Cursor integration with deterministic shell-command guardrails.

<!-- template-profile:collaborative:start -->

- public contribution and repository automation in the `collaborative`
  profile.

<!-- template-profile:collaborative:end -->

The boilerplate intentionally does not prescribe application architecture,
framework dependencies, infrastructure, or product requirements before a real
project needs them.

## Repository Mental Model

| Concern              | Canonical location                                     | Question answered                        |
| :------------------- | :----------------------------------------------------- | :--------------------------------------- |
| Human-agent workflow | `AGENTS.md`                                            | How may an agent work here?              |
| Engineering Rules    | `.cursor/rules/`                                       | How should code be engineered?           |
| Agent Skills         | `.agents/skills/`                                      | How are specialized workflows performed? |
| Project definition   | `docs/project/definition.md`                           | What must this project build?            |
| Accepted decisions   | `docs/project/decisions/`                              | Why was a meaningful choice made?        |
| Executable tooling   | `pyproject.toml`, `uv.lock`, `.pre-commit-config.yaml` | What do deterministic checks enforce?    |

These responsibilities remain separate so requirements, reusable guidance,
decisions, and workflow permissions do not silently redefine one another.

## Documentation Map

- [Documentation index](docs/README.md) — task-oriented navigation;
- [Getting Started](docs/getting-started.md) — environment setup and first
  local verification;
- [Customizing the Template](docs/customizing-the-template.md) — project
  identity, package placeholders, Git, Python, and licensing;
- [Development Tooling](docs/development-tooling.md) — uv, quality checks,
  hooks, Markdown, and editor integration;
- [Project Documentation](docs/project/README.md) — project definition, known
  unknowns, and ADR policy;
- [Agent Skills](.agents/README.md) — approval boundaries and specialized
  workflows;
- [Cursor Integration](.cursor/README.md) — Rules, Skills, hooks, subagents,
  and portability;
- [Cursor Project Rules](.cursor/rules/README.md) — classification, precedence,
  profiles, and maintenance.

## Quality Gate

Run focused tools during development and the integrated gate before review:

```bash
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pre-commit run --all-files
uv run pytest --cov --cov-report=term-missing
```

The authoritative configuration is in `pyproject.toml`, `uv.lock`, and
`.pre-commit-config.yaml`. See [Development Tooling](docs/development-tooling.md)
for command ownership and hook behavior.

## Start Project Work with an Agent

Before application implementation, replace the placeholders in
`docs/project/definition.md` with confirmed project context. Then ask the agent
to start or resume the project.

The repository workflow keeps these boundaries distinct:

```text
DISCUSS → DECIDE → RECORD → PLAN → APPROVE → IMPLEMENT → VERIFY → REVIEW
```

Read `AGENTS.md` for the complete working agreement. Project initialization
never changes Agent or Rule behavior.
