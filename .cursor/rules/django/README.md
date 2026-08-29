<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Django and DRF Rules

Install this directory only in projects that use Django or Django REST
Framework.

## Current Rules

| Rule | Classification | Application | Purpose |
| :--- | :------------- | :---------- | :------ |
| [`core.mdc`](core.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Specific Files | Cover framework boundaries, initialization, signals, async, configuration, and i18n |
| [`models-orm.mdc`](models-orm.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Specific Files | Guide queries, writes, managers, constraints, indexes, and relationships |
| [`transactions.mdc`](transactions.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Specific Files | Define transaction, rollback, `on_commit()`, locking, and async boundaries |
| [`migrations.mdc`](migrations.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Specific Files | Keep schema and data migrations safe, compatible, and reviewable |
| [`tests.mdc`](tests.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Specific Files | Test Django, DRF, database, transaction, async, and migration behavior |
| `conventions.mdc` | PERSONAL CONVENTION | Specific Files | Record Emad's Django and DRF implementation preferences |
| `test-conventions.mdc` | PERSONAL CONVENTION | Specific Files | Record Emad's Django and DRF test preferences |

## Boundaries

General framework correctness belongs here. Personal preferences stay in
files whose names contain `convention` and must not override repository
requirements or framework behavior.

Version-sensitive behavior is governed by
[`../meta/compatibility.mdc`](../meta/compatibility.mdc). Do not assume APIs
introduced in the reviewed Django or DRF baseline exist in an older project.
