# Engineering standards

This repository is a stack-neutral engineering standards template. These rules apply to every contributor and coding assistant. This file is the concise entry point; the linked documents own the detailed standards.

## Before changing code

- Read docs/architecture.md, docs/coding-standards.md, docs/development.md and docs/testing.md. Read the relevant technology profile under docs/standards/.
- Read the applicable rules in docs/defensive-patterns/ before changing shared state, asynchronous lifecycles, resource ownership, retries, SQL/data grain, streaming guarantees or schema contracts.
- Trace the existing implementation, callers, tests, configuration and deployment path before proposing a change.
- State scope, non-goals, acceptance criteria and compatibility or data risks for substantive work.

## Engineering rules

- Preserve module ownership and dependency direction. Put behavior beside the capability that owns its data and lifecycle.
- Prefer the smallest complete change. Avoid speculative abstractions, duplicate representations and unrelated refactors.
- Make contracts explicit: types, inputs, outputs, invariants, ownership, side effects and failure behavior.
- Validate untrusted inputs at real trust boundaries. Do not add redundant validation to trusted, typed same-process calls without a demonstrated need.
- Treat asynchronous work, concurrency, cancellation, resource cleanup and shutdown as correctness requirements.
- Handle failures explicitly. Do not silently swallow errors or retry operations without proving safe repetition.
- Protect credentials and sensitive data. Never commit secrets or expose them in logs, fixtures, screenshots or PRs.
- Add or update regression tests for behavior changes. Tests must assert observable behavior, not merely repeat implementation details. For agent or automation work, verify resulting files, persisted state or external effects independently; never rely on the agent's self-report alone.
- Update the owning documentation and compatibility notes in the same change. Read docs/AGENTS.md when editing documentation. Record durable design decisions in docs/decisions/.
- Report only checks actually run. Distinguish PASS, FAIL, NOT RUN and BLOCKED; include environment and relevant evidence.

## Delivery boundaries

- Work on a focused topic branch and preserve unrelated changes.
- Review the actual diff against the intended scope before opening a PR.
- CI and AI review are evidence, not authorization to merge, deploy, release or publish.
- Do not modify production systems without explicit authorization. For DataWorks, draft SQL and permitted scheduling/dependency configuration may be prepared when authorized; never submit or publish production nodes automatically.

## Quality commands

Run python scripts/verify_project.py and the template contract tests for changes to this template. Run `python scripts/run_quality.py --base <verified-base-ref>` to select path-scoped checks from committed changes; omit `--base` to run every configured check. Fetch the base first and never treat an unresolved diff as an empty change set. Select additional checks based on the changed behavior; do not default to an unrelated full suite or claim unexecuted checks passed.

## Reusable workflows

Use the applicable Skill in .agents/skills/ for planning, implementation, review, pre-push verification, documentation, error handling, simplification or upgrade guidance. Skills describe task workflows; they do not define fixed GPT, Claude, Codex or other agent roles.
