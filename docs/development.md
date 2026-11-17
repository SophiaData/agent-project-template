# Development workflow

1. **Plan**: inspect the repository and task; document scope, non-goals, risks and acceptance criteria.
2. **Implement**: change the smallest possible surface in a feature branch/worktree; add tests and docs.
3. **Verify**: run relevant checks configured in `project-policy.json`; record exact results.
4. **Review**: an independent reviewer checks actual diffs, security, compatibility and test evidence.
5. **Deliver**: use the PR template; wait for CI and authorized human review before merge.

Do not automatically publish, release, deploy or alter production services. An AI `PASS` is not an authorized merge.

For a new stack, configure real test/typecheck/lint commands in `project-policy.json` before shipping source.
