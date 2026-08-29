# Documentation

Use this directory for task-oriented project documentation. The root
`README.md` is intentionally a concise entry point rather than the complete
manual.

| Task | Document |
| :--- | :------- |
| Create and verify a repository from the template | [Getting Started](getting-started.md) |
| Turn the reusable baseline into a specific project | [Customizing the Template](customizing-the-template.md) |
| Understand local quality tools and Git hooks | [Development Tooling](development-tooling.md) |
| Define what a project must build | [Project Documentation](project/README.md) |
| Understand Agent Skills and approval boundaries | [Agent Skills](../.agents/README.md) |
| Understand Cursor rules, hooks, and integration | [Cursor Integration](../.cursor/README.md) |
| Classify and maintain engineering rules | [Cursor Project Rules](../.cursor/rules/README.md) |

## Sources of Truth

Different documents own different concerns:

- `AGENTS.md` defines how humans and AI agents work together.
- `.cursor/rules/` defines reusable engineering guidance.
- `docs/project/definition.md` defines the product and confirmed constraints.
- `docs/project/decisions/` records accepted meaningful decisions.
- `pyproject.toml`, `uv.lock`, and `.pre-commit-config.yaml` own executable
  tooling configuration.

Prefer linking to the owning source over copying facts that can drift.
