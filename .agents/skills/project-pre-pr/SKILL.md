---
name: project-pre-pr
description: Use before opening a PR to verify scoped changes, real test evidence, CI policy and release boundaries.
---

# PR handoff

1. Verify branch, diff against known base, no unrelated or secret files.
2. Run `python scripts/verify_project.py` and `python scripts/run_quality.py`.
3. Review actual command outputs and note any tests not run.
4. Fill `.github/pull_request_template.md` with changes, evidence, AI roles and risks.
5. Never merge or publish automatically; PR creation is not release authorization.
