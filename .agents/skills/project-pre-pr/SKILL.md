---
name: project-pre-pr
description: Use before opening or updating a pull request to verify scope, quality evidence, defensive-pattern applicability, negative controls, documentation, compatibility and release boundaries.
---

# Pre-push and PR checks

1. Confirm the branch and compare the complete diff with the intended base.
2. Check for unrelated files, credentials, local configuration and generated-file drift.
3. Identify applicable rules in docs/defensive-patterns/ and verify the implementation and PR evidence against their triggers and invariants.
4. Run python scripts/verify_project.py and the template contract tests when changing this template.
5. When module dependencies change, verify docs/architecture.md records the permitted direction and run the configured architecture check. For each new or changed automated guard, run its negative-control test and confirm the intended violation is rejected for the expected reason.
6. Fetch and verify the live PR base. Run `python scripts/run_quality.py --base <verified-base-ref>` for committed branch changes; omit `--base` to run all configured checks or when validating uncommitted work. If the diff cannot be resolved, stop and fix the base rather than treating the scope as empty.
7. Inspect the selected and skipped checks, command output and CI evidence. Confirm that a source change selected at least one test check. Record PASS, FAIL, NOT RUN or BLOCKED accurately.
8. Check tests, documentation, decision records, compatibility and upgrade guidance.
9. Complete the PR template with scope, risks and exact evidence.
10. Do not merge, deploy, release, publish or submit production changes without separate authorization.
