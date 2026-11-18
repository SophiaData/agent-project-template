# Template changelog

## 2.4.0 — 2026-11-18

- Add an architecture quality-check category for stack-native module dependency and layer-boundary guards.
- Add a defensive pattern requiring permitted dependency direction, acyclic module graphs by default and public interfaces across package boundaries.
- Extend architecture documentation with allowed/forbidden dependency rules, ownership and enforcement guidance.
- Add optional examples for Python, TypeScript, Java and data-engineering projects without imposing a parser or tool dependency.
- Require forbidden-dependency negative controls for new or changed architecture guards; architecture checks do not replace the required test category.
- Preserve project-policy.json schema 2 and all existing quality-check categories.

## 2.3.0 — 2026-11-18

- Add optional relative path-glob selectors to V2 quality-check entries without changing the policy schema.
- Add Git-diff-aware quality selection; checks without selectors continue to run unconditionally.
- Fail closed when the requested base diff cannot be resolved or changed application source selects no test check.
- Preserve both old and new paths for renames and add contract tests for path matching, Git diff handling and selection failures.
- Fetch full Git history in CI and select checks from the pull-request base or push-before commit.

## 2.2.0 — 2026-11-18

- Add a defensive-pattern catalog for shared state, asynchronous correctness, resource allocation, quiescent cleanup, retries, outcome reporting, trust boundaries and performance evidence.
- Add data-engineering patterns for grain, join cardinality, time semantics, idempotent processing, delivery guarantees and schema evolution.
- Require negative-control tests for new automated guards and add structural validation for defensive-pattern documents.
- Update implementation, review and pre-PR workflows to identify applicable patterns without applying unrelated rules mechanically.
- Clarify that the generic quality runner cannot prove a configured test command discovered or executed meaningful tests; require framework-specific fail-on-empty behavior or a project-owned discovery check.
- Keep project-policy.json schema 2 and existing argv-based quality checks compatible.

## 2.1.0 — 2026-11-17

- Reframe the template as a stack-neutral engineering standards baseline.
- Add common coding, testing, error-handling, documentation, compatibility and Git standards.
- Add technology profiles for Python, TypeScript, Java and SQL/data engineering.
- Add decision-record guidance and reusable Skills for review, pre-push checks, documentation, errors, simplification and upgrades.
- Strengthen the root AGENTS.md as a concise cross-tool engineering entry point; remove model-role framing from the PR workflow.
- Keep project-policy.json schema 2 and the existing argv-based quality runner compatible.

## 2.0.0 — 2026-11-17

- Introduce an explicit versioned project policy with typed quality checks.
- Require at least one declared test check once application code exists.
- Validate architecture/Skill links and baseline release boundaries.
- Add project metadata configuration and technology-specific CI runtime setup.
- Add regression tests for governance, failure states, and source detection.
- Document safe manual upgrades and the central template source policy.

## 1.0.0 — 2026-11-17

- Initial shared Agent instructions, four Skills and minimal Python CI.
