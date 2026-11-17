# Contributing

Thank you for improving this engineering standards template.

## Before opening a pull request

1. Read AGENTS.md and the standards documents relevant to the change.
2. Open a focused branch from the current default branch.
3. Keep the change scoped; explain any new abstraction, dependency or policy requirement.
4. Add regression tests for changed behavior and update affected documentation.
5. Run the template contract tests, project verifier and configured quality checks.
6. Inspect the complete diff, including generated files, workflows and policy changes.
7. Complete the pull-request template with exact command results and remaining risks.

## Review expectations

Reviewers inspect the actual diff and surrounding implementation. Check correctness, ownership, security, compatibility, error paths, concurrency, test quality and documentation. A summary from an author or coding assistant is not a substitute for independent inspection.

A review should identify actionable findings with file and line references. If no findings remain, state the scope reviewed and checks or evidence examined. Do not imply that unrun integration, performance or platform checks passed.

## Changes to this template

Increment TEMPLATE_VERSION and update project-policy.json, CHANGELOG.md and docs/template-upgrades.md together. Preserve the existing policy schema unless a schema migration is necessary. Add tests for new governance behavior and update the required-file contract in scripts/verify_project.py.

Do not overwrite consumer-project customizations during upgrades. Do not change branch protection, merge, release, deploy or publish as part of a template update unless separately authorized.
