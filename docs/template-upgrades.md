# Template versions and upgrade policy

TEMPLATE_VERSION and project-policy.json.template_version define the copied project's baseline. They are not automatic updates.

## Upgrade rules

- New projects start with a snapshot of SophiaData/agent-project-template.
- Existing projects keep local modifications. Never replace AGENTS.md, Skills, policy, CI or architecture documents without inspecting the diff.
- Propose upgrades through a dedicated PR. Compare old and new versions, migrate project-policy.json only when its schema changes, preserve local decisions and rerun checks.
- Template updates do not merge, deploy, release or publish production artifacts; they do not submit or publish DataWorks nodes.
- The global sophiadata-init-project Skill reads this repository as the single source; it must not embed a second copy of these documents.

## Version history

### V1 to V2

Rename quality_commands entries to typed quality_checks entries with category and argv. The V2 runner requires at least one test-category check when application source exists.

### V2 to V2.1

This is an additive engineering-standards upgrade. The project-policy.json schema remains version 2; existing quality_checks entries remain valid.

Review and adopt the new coding, testing, error-handling, documentation, compatibility, Git and technology-profile documents. Reconcile the root AGENTS.md and reusable Skills with local project rules. Add decision records where durable choices need to be documented.

No automatic overwrite is performed. Run the project's configured checks and review the resulting diff before merging.
