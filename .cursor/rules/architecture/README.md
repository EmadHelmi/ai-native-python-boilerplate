<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Architecture Rules

Reusable, project-neutral design guidance for codebases where domain
boundaries, dependency direction, persistence, workflows, or concurrency
matter.

## Current Rules

| Rule | Classification | Application | Purpose |
| :--- | :------------- | :---------- | :------ |
| [`core.mdc`](core.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Specific Files | Keep architecture proportional and dependencies directed inward |
| [`domain-model.mdc`](domain-model.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Apply Intelligently | Model entities, value objects, aggregates, identity, and invariants |
| [`application.mdc`](application.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Apply Intelligently | Define use cases, services, DTOs, CQRS boundaries, and errors |
| [`persistence.mdc`](persistence.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Apply Intelligently | Keep repositories, transactions, and persistence mapping at clear seams |
| [`events-workflows.mdc`](events-workflows.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Apply Intelligently | Govern events, side effects, retries, outbox, and distributed workflows |
| [`boundaries-packages.mdc`](boundaries-packages.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Apply Intelligently | Protect package, layer, and bounded-context boundaries |
| [`concurrency.mdc`](concurrency.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Apply Intelligently | Address shared state, consistency, locks, and idempotency |
| [`construction-strategies.mdc`](construction-strategies.mdc) | GENERAL / ECOSYSTEM / PROJECT-NEUTRAL | Apply Intelligently | Guide construction, reconstitution, Strategy, and Policy designs |

## Boundaries

These rules are intentionally anti-ceremony. They do not require Clean
Architecture, DDD layers, repositories, factories, services, or CQRS for
simple code. Stronger guidance becomes relevant only after the corresponding
boundary or design problem exists.

Project-specific package maps, layer choices, and dependency exceptions do not
belong in these reusable rules.

Mechanically enforce stable import boundaries when practical. Keep behavioral
architecture constraints in tests when import contracts cannot express them.
