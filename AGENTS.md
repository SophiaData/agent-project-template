# SophiaData Project Agent Rules

Applies to GPT, Claude Code, Codex, DSH and other coding assistants working on this repository.

- Read `docs/architecture.md`, `docs/development.md` and `docs/testing.md` before substantive changes.
- Follow the project plan and acceptance criteria; inspect source and tests before editing.
- Prefer existing components and public interfaces. Keep changes scoped; avoid speculative refactors.
- Do not record credentials, tokens, cookies, or local environment secrets in code, logs or PRs.
- Work on a topic branch/worktree. Preserve unrelated changes.
- Add regression tests for behavior changes. Never invent results or downgrade a check to pass.
- Reviewer must inspect the actual diff and test evidence independently, not just the worker summary.
- Do not auto-merge, deploy, release, publish, or modify production without explicit authorization.
- For DataWorks and similar production systems, modify drafts only when authorized; never submit/publish production nodes automatically.
- CI is the executable quality gate; instructions and Skills alone do not enforce behavior.
- Use `.agents/skills/` instructions for planning, implementation, review and PR preparation.

This is a **new-project baseline**. Add technology-specific rules after identifying the project stack.

## V2 policy

Before shipping application code, run `python scripts/configure_project.py`
with the real project name/stack, configure non-placeholder tests in the
`quality_checks` array, and run the template contract tests. Template version
is tracked in `TEMPLATE_VERSION`; updates require a reviewed PR following
[upgrade guidance](docs/template-upgrades.md). The declared command categories
are an audit signal, not evidence that an arbitrary test command is meaningful.
