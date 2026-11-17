---
name: project-review
description: Use for independent code review against the original plan, actual Git diff, regression evidence, security and compatibility.
---

# Independent review

1. Read `AGENTS.md`, acceptance criteria and actual Git diff.
2. Inspect relevant surrounding code and tests; do not trust worker summaries as proof.
3. Assess correctness, race/error paths, security, contracts, migration and observability.
4. Verify reported checks/CI are real and separate static evidence from runtime smoke testing.
5. Return `PASS`, `CHANGES_REQUESTED` or `BLOCKED` with specific file findings.
6. AI PASS does not replace repo protection or human approval.
