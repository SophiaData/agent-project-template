---
name: project-implement
description: Use to implement an agreed engineering change with focused diffs, applicable defensive patterns, regression coverage, documentation and reproducible verification.
---

# Implementation workflow

1. Re-read AGENTS.md, the accepted plan and the owning module contracts.
2. Identify applicable rules in docs/defensive-patterns/ before changing a surface covered by those rules.
3. Work on a topic branch or worktree; preserve unrelated changes.
4. Keep behavior beside the capability that owns its data and lifecycle.
5. Add or update tests for observable behavior, errors, boundaries and regressions. New automated guards need a negative-control test.
6. Update API contracts, architecture, decision records and upgrade guidance when affected.
7. Run relevant checks and inspect their actual output. Report missing tools and blocked checks honestly.
8. Summarize changed files, evidence, compatibility impact and unresolved risks.
