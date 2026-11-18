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

### V2.1 to V2.2

This is an additive engineering-governance upgrade. The project-policy.json schema remains version 2; existing quality_checks entries remain valid.

Adopt the defensive-pattern catalog for the changed surfaces. The template verifier now checks that each documented pattern has its required sections, and template contract tests include negative controls that deliberately omit required content or introduce broken links. Review semantic applicability and implementation separately; the structural checks do not enforce application code behavior.

No automatic overwrite is performed. Run the project's configured checks and review the resulting diff before merging.

### V2.2 to V2.3

This is an additive quality-runner upgrade. The project-policy.json schema remains version 2; existing quality_checks entries containing only category and argv remain valid and run unconditionally.

Projects may add a relative slash-separated paths array to a quality check to select it only when a changed file matches. Checks without paths always run. Configure patterns to include the source, owning tests and relevant manifests, lockfiles or configuration files. When application source changes, at least one test check must match or the runner fails. Unknown Git bases and failed diff commands also fail closed.

CI now fetches full Git history and supplies the pull-request base or push-before commit. Local contributors should fetch the verified base and run `scripts/run_quality.py --base <base-ref>` for committed changes; omit `--base` to run all configured checks, including checks needed while validating uncommitted work. Review each project's path selectors rather than copying the example patterns blindly.

### V2.4 to V2.5

This upgrade adds executable governance for instruction files and project Skills. The project-policy.json schema remains version 2. The verifier discovers every direct child under .agents/skills, requires `<name>/SKILL.md`, validates frontmatter name and description, and checks the canonical .agents/skills/README.md registry. Root AGENTS.md is checked for the standing-order sections and concise size; CLAUDE.md is treated as a compatibility entry point that must point to the shared AGENTS.md policy. Fixed model-role assignments are rejected. Existing projects should add the registry and update their local verifier expectations through a reviewed diff.

### V2.3 to V2.4

This is an additive architecture-governance upgrade. The project-policy.json schema remains version 2. Existing quality-check entries remain valid. The runner adds the `architecture` category for stack-native module and layer dependency checks.

Projects should record permitted and forbidden dependency directions in docs/architecture.md, then configure an architecture check only when the project has enforceable module boundaries and a suitable tool. Python, TypeScript, Java and data-engineering profiles provide optional examples; no tool is installed or required automatically. Each architecture guard must include a deliberately forbidden dependency fixture and must not replace the required test-category check.
