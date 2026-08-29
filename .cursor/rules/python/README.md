<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Python Rules

Python engineering guidance for projects that use this reusable baseline.

## Current Rules

| Rule | Classification | Application | Purpose |
| :--- | :------------- | :---------- | :------ |
| [`core.mdc`](core.mdc) | HYBRID | Specific Files | Combine general change discipline with the validation stack selected by this baseline |
| [`tooling.mdc`](tooling.mdc) | BOILERPLATE / REUSABLE PROJECT BASELINE | Apply Intelligently | Define the chosen responsibilities of uv, Ruff, Pyright, and Pylance |
| [`observability.mdc`](observability.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Apply Intelligently | Guide vendor-neutral logs, metrics, tracing, telemetry, and health signals |
| [`tests.mdc`](tests.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Specific Files | Cover test quality and the appropriate unit-to-operational test portfolio |
| `conventions.mdc` | PERSONAL CONVENTION | Specific Files | Record Emad's Python implementation preferences |
| `test-conventions.mdc` | PERSONAL CONVENTION | Specific Files | Record Emad's Python test structure and style preferences |

## Boundaries

General Python behavior and the selected reusable tooling baseline belong here.
Framework-specific rules belong in their framework directory. Personal
preferences remain local-only when the recommended `*convention*.mdc` ignore
policy is used.

The tooling rule describes responsibilities, not the full executable
configuration. [`pyproject.toml`](../../../pyproject.toml), lock files, and CI
configuration remain authoritative for mechanically enforced settings.
