---
name: project-implement
description: Use to implement an agreed engineering change with focused diffs, regression coverage, documentation and reproducible verification.
---

# Implementation workflow

1. Re-read AGENTS.md, the accepted plan and the owning module contracts.
2. Work on a topic branch or worktree; preserve unrelated changes.
3. Keep behavior beside the capability that owns its data and lifecycle.
4. Add or update tests for observable behavior, errors, boundaries and regressions.
5. Update API contracts, architecture, decision records and upgrade guidance when affected.
6. Run relevant checks and inspect their actual output. Report missing tools and blocked checks honestly.
7. Summarize changed files, evidence, compatibility impact and unresolved risks.
