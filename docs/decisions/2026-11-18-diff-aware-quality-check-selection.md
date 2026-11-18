# Decision: diff-aware quality check selection

- Date: 2026-11-18
- Status: Proposed
- Owners: Project maintainers

## Problem and context

Running every configured check for every change wastes time in multi-language and data-engineering repositories. Selecting checks by guessed language ownership is unreliable in a stack-neutral template, and a failed Git comparison must not look like an empty change set.

## Decision

Keep project-policy.json schema version 2 and allow each quality check to declare an optional relative POSIX \`paths\` array. A check runs when any changed path matches any configured pattern. A check without \`paths\` always runs.

The runner compares committed changes using \`git diff BASE...HEAD\` with rename detection disabled, so both the old and new paths participate in selection. The caller supplies a verified base ref. Without \`--base\`, all configured checks run. If the diff cannot be resolved, the runner fails. If application source changes but no test check is selected, the runner fails.

The path patterns are project-owned declarations. The runner does not infer import graphs, test ownership, transitive dependencies or language-specific build relationships. CI fetches full Git history and supplies the pull-request base or push-before commit.

## Alternatives considered

- **Run every check for every change:** simple and conservative, but repeats unrelated work and does not scale well across multi-stack repositories.
- **Infer affected tests from source imports:** can be useful within one language, but is not reliable across SQL, generated code, build systems, dynamic imports, data pipelines and external services.
- **Introduce a new policy schema:** unnecessary for an additive optional field; existing category/argv entries remain valid.
- **Treat an unavailable diff as no changes:** rejected because it can silently skip required validation.

## Consequences and risks

Projects must maintain selectors that include relevant source files, tests, manifests, lockfiles, configuration and generated interfaces. A selector can still be incomplete; requiring a selected test for source changes prevents the most dangerous empty-test case but does not prove that the selected test suite covers the change.

Unscoped checks continue to run for every invocation. A full run remains available by omitting \`--base\`, which is also the safe choice for uncommitted work. The selection mechanism remains language-neutral and does not change release or production-operation boundaries.

## Verification

- Unit tests cover glob matching, root and nested \`**\` patterns, selected and skipped checks, unscoped checks, invalid patterns and the source-change/no-test failure.
- A temporary Git repository test verifies that rename changes report both old and new paths.
- A non-repository or unknown base must fail with an actionable diagnostic.
- GitHub Actions verifies the template contract, governance documents and configured quality checks using full history.
