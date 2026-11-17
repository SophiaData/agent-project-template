# Template versions and upgrade policy

The root `TEMPLATE_VERSION` and `project-policy.json.template_version` define the copied
project's baseline. Use them to compare versions; they are **not** automatic updates.

- New projects start with a snapshot of `SophiaData/agent-project-template`.
- Existing projects keep local modifications. Never replace `AGENTS.md`, Skills,
  policy, CI or architecture documents without inspecting the diff.
- Propose upgrades through a dedicated PR. Compare the old and new template
  versions, migrate the `project-policy.json` schema if needed, and rerun checks.
- For V1 → V2: rename `quality_commands: [[...]]` to
  `quality_checks: [{"category": "test", "argv": [...]}]` as appropriate.
  Each application source repository must declare at least one real `test` check.
- Template updates do not merge, deploy, publish or submit DataWorks nodes.
- The global `sophiadata-init-project` Skill reads this repository as the
  **single source**; it must not embed a second copy of these documents.
