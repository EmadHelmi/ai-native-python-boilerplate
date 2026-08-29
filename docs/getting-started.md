# Getting Started

This guide takes a newly generated repository from the boilerplate baseline to
a verified local development environment.

## Prerequisites

Install:

- Git;
- [uv](https://docs.astral.sh/uv/);
- a supported Python version.

The project supports Python 3.13 and 3.14. The `requires-python` field in
`pyproject.toml` is the package constraint, while `.python-version` records the
preferred local interpreter.

Node.js is not a project prerequisite. pre-commit provisions the Node runtime
needed by the configured Markdown hook.

## Create the Repository

Use GitHub's **Use this template** action for an independent project. This
creates a new repository without inheriting the boilerplate's branches or
commit history.

Fork the boilerplate only when the goal is to contribute changes back to the
boilerplate itself.

## Select a Profile

Choose the profile before customizing project metadata.

### Solo

Use `solo` for a personal or internal project that does not need public GitHub
collaboration infrastructure.

Preview the exact changes:

```bash
uv run python scripts/setup_profile.py solo
```

Apply them explicitly:

```bash
uv run python scripts/setup_profile.py solo --apply
```

The command removes public collaboration files and project-level MIT metadata.
It preserves `AGENTS.md`, `.agents/`, `.cursor/`, local quality tooling, and the
boilerplate's MIT notice as `THIRD_PARTY_NOTICES.md`.

### Collaborative

Use `collaborative` for a public or multi-contributor repository. Validate that
its public layer is complete:

```bash
uv run python scripts/setup_profile.py collaborative
```

The command is non-destructive for a complete collaborative repository.

## Create the Environment

Synchronize the locked development environment:

```bash
uv sync --locked --all-groups
```

uv creates and manages `.venv`; activation is optional when commands are run
through `uv run`.

Install both configured Git hooks:

```bash
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

## Run the First Quality Check

Run the same foundations used by repository automation:

```bash
uv lock --check
uv run pre-commit run --all-files
uv run pytest --cov --cov-report=term-missing
```

See [Development Tooling](development-tooling.md) for ownership of each check
and focused commands.

## Define the New Project

Before application implementation begins:

1. follow [Customizing the Template](customizing-the-template.md);
2. replace the placeholders in `docs/project/definition.md` with confirmed
   project context;
3. record meaningful technical decisions only when they become necessary;
4. ask the agent to start or resume the project when the definition contains
   enough information for the next milestone.

The working agreement in `AGENTS.md` and the Agent Skills under `.agents/`
remain identical in both profiles.
