# Customizing the Template

Apply these changes after initializing the repository. Keep customization
focused on the new project's real requirements.

## Project Identity

Update the `[project]` table in `pyproject.toml`:

- `name`;
- `version` when the initial value is not appropriate;
- `description`;
- `authors`.

Rewrite the root `README.md` for the derived project. Remove boilerplate-only
instructions after they are no longer useful, but keep links to project-owned
development documentation that still applies.

Run `uv lock` after changing project metadata that affects the lockfile.

## Python Package Placeholder

The baseline uses `app` as an intentionally non-existent package placeholder.
Replace it with the real top-level package name in:

- `[tool.importlinter]` and its contracts in `pyproject.toml`;
- Import Linter and pytest file patterns in `.pre-commit-config.yaml`.

The initial `[tool.coverage.run]` source list measures repository automation
because no application package exists yet. Replace or extend that list with the
real package when application code is created.

The `app` placeholder keeps architecture checks dormant until application code
exists. Do not create that package merely to satisfy the example.

## Project Definition

Complete `docs/project/definition.md` with confirmed information about:

- goals and non-goals;
- user journeys and scope;
- functional requirements;
- mandatory technical constraints;
- security, testing, and deployment requirements;
- known unknowns;
- the project-level definition of done.

Keep technical option analysis in the decision workflow rather than embedding
it in the project definition. The policy is documented in
[Project Documentation](project/README.md).

## Python Version Policy

The template currently supports Python 3.13 and 3.14:

- `requires-python` defines the minimum supported version;
- `.python-version` selects the preferred local version;
- `[tool.pyright].pythonVersion` checks syntax and types against the minimum.

<!-- template-profile:collaborative:start -->

- the collaborative CI matrix verifies supported runtime versions.

<!-- template-profile:collaborative:end -->

If a derived project deliberately changes support, update every applicable
source together.

## License and Provenance

<!-- template-profile:collaborative:start -->

The `collaborative` profile keeps the root MIT `LICENSE` and corresponding
project metadata.

<!-- template-profile:collaborative:end -->

When `THIRD_PARTY_NOTICES.md` is present, it records the origin and license of
the reusable baseline; it is not a license declaration for the derived
project.

Apply any company or project license policy deliberately. Do not delete
third-party notices merely because the repository is private.

## Git Identity and Signing

A repository created from this template already has independent Git metadata,
so deleting or reinitializing `.git` is unnecessary.

Inspect the effective configuration:

```bash
git config --local --list
git remote -v
```

Set repository-local identity when it should differ from global Git settings:

```bash
git config --local user.name "Your Name"
git config --local user.email "you@example.com"
```

If signed commits are required, configure the correct key for the new project:

```bash
gpg --list-secret-keys --keyid-format LONG
git config --local user.signingkey YOUR_KEY_FINGERPRINT
git config --local commit.gpgsign true
git config --local tag.gpgsign true
```

If signing is not required, do not copy a project-local signing key from
another repository.

## Environment Lifecycle

For normal dependency synchronization, use:

```bash
uv sync --locked --all-groups
```

When a complete virtual-environment rebuild is actually needed, use uv's
cross-platform clearing behavior:

```bash
uv venv --clear
uv sync --locked --all-groups
```

Do not commit or copy `.venv` between machines.

## Rules and Personal Conventions

Keep the reusable rule directories that fit the project. The classification,
scope, and application modes are documented in
[Cursor Project Rules](../.cursor/rules/README.md).

Files matching `*convention*.mdc` are local personal conventions and are
ignored by the repository. Shared company or project rules should use semantic
names and be reviewed like other repository policy.

Project initialization MUST NOT change `AGENTS.md`, `.agents/`, or `.cursor/`.

## Completion Checklist

- Repository initialization is complete.
- Project name, description, authors, and package placeholders are updated.
- Python support declarations are internally consistent.
- `docs/project/definition.md` contains the confirmed initial context.
- License and provenance treatment matches the project policy.
- Git identity, remote, and optional signing configuration are correct.
- `uv.lock` is current.
- Git hooks are installed.
- The complete local quality gate passes.
