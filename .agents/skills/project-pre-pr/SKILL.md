---
name: project-pre-pr
description: Use before opening or updating a pull request to verify scope, quality evidence, documentation, compatibility and release boundaries.
---

# Pre-push and PR checks

1. Confirm the branch and compare the complete diff with the intended base.
2. Check for unrelated files, credentials, local configuration and generated-file drift.
3. Run python scripts/verify_project.py and the template contract tests when changing this template.
4. Run python scripts/run_quality.py and the focused checks required by the changed behavior.
5. Inspect command output and CI evidence. Record PASS, FAIL, NOT RUN or BLOCKED accurately.
6. Check tests, documentation, decision records, compatibility and upgrade guidance.
7. Complete the PR template with scope, risks and exact evidence.
8. Do not merge, deploy, release, publish or submit production changes without separate authorization.
