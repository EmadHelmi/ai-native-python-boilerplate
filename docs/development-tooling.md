# Development Tooling

The boilerplate uses a small set of tools with explicit ownership. Executable
configuration remains authoritative over prose documentation.

| Tool | Responsibility | Configuration |
| :--- | :------------- | :------------ |
| uv | Python versions, environments, dependencies, and lockfile | `pyproject.toml`, `uv.lock`, `.python-version` |
| Ruff | Python formatting, linting, and import ordering | `pyproject.toml` |
| Pyright | Reproducible static type checking | `pyproject.toml` |
| pytest and coverage.py | Behavioral tests and coverage threshold | `pyproject.toml` |
| Import Linter | Executable package-boundary contracts | `pyproject.toml` |
| pre-commit | Local Git-hook orchestration | `.pre-commit-config.yaml` |
| markdownlint-cli2 | Markdown and Cursor rule formatting | `pyproject.toml`, `.pre-commit-config.yaml` |

## Environment and Dependencies

Use uv for all project dependency changes:

```bash
uv add PACKAGE
uv add --dev PACKAGE
uv remove PACKAGE
```

Do not edit `uv.lock` by hand. After an intentional metadata or dependency
change, regenerate and validate it:

```bash
uv lock
uv lock --check
```

Synchronize all configured dependency groups with:

```bash
uv sync --locked --all-groups
```

## Local Quality Gate

Run focused tools while developing:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
```

Before review, run the integrated checks:

```bash
uv lock --check
uv run pre-commit run --all-files
uv run pre-commit run --all-files --hook-stage pre-push
uv run pytest --cov --cov-report=term-missing
```

Coverage must remain at or above the configured threshold. Tests should still
assert meaningful behavior rather than exist only to increase the percentage.

## Git Hooks

Install the configured hooks once per clone:

```bash
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

| Stage | Purpose |
| :---- | :------ |
| `pre-commit` | File hygiene, lock freshness, Ruff, Markdown, Pyright, and applicable architecture checks |
| `pre-push` | pytest with the configured branch-coverage threshold |

Hooks are a local safety net. Do not use `--no-verify` to bypass a failing
quality gate.

## Markdown and Node.js

Node.js is not a prerequisite for normal development. pre-commit installs and
manages the Node environment used by the pinned markdownlint-cli2 hook.

Run the configured Markdown check without a global npm installation:

```bash
uv run pre-commit run markdownlint-cli2 --all-files
```

A developer needs Node.js only when deliberately running markdownlint-cli2
directly through npm outside pre-commit. Keep any such CLI version aligned with
the hook revision rather than relying on an unreviewed floating version.

## Template Placeholders

Import Linter and the related hook patterns initially refer to the placeholder
package `app`. Replace those paths when the derived project creates its real
package. Initial coverage sources measure repository automation and should be
updated deliberately when application code exists.

Repository automation and safety scripts remain covered before application
code exists. The `solo` profile removes the PR-policy validator and updates
coverage sources accordingly.

## Collaborative and Solo Automation

The `collaborative` profile keeps GitHub CI, compatibility checks, dependency
review, PR policy, and Dependabot configuration.

The `solo` profile removes `.github/` but retains this complete local quality
gate. Repository visibility therefore does not change Python, Rule, or Agent
standards.

## VS Code

The repository recommends extensions through `.vscode/extensions.json` and
keeps shared editor behavior in `.vscode/settings.json`.

The Python extension supplies the core editor integration and normally offers
Pylance as its language support. Ruff remains the configured formatter and
linter, while the CLI Pyright check is the reproducible type-checking source of
truth.
