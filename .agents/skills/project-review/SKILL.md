---
name: project-review
description: Use for an independent review of the actual diff, architecture fit, correctness, security, compatibility, tests, defensive patterns and operational risks.
---

# Engineering code review

Review the actual diff against the base branch, accepted requirements and observable acceptance criteria. Do not treat author summaries or test names as proof.

## Review preparation

Read the relevant architecture and technology profile. For every changed surface, identify and read the applicable rules in docs/defensive-patterns/ before judging the implementation. Check the rule's trigger, required invariant, evidence and exception boundary; do not apply unrelated patterns mechanically.

## Review dimensions

- **Correctness:** normal, boundary, invalid-input and failure paths; data integrity; deterministic behavior.
- **Ownership:** module boundaries, dependency direction, state ownership, lifecycle and public API necessity. Compare changed dependency edges with docs/architecture.md and inspect the architecture check and its forbidden-dependency fixture where configured.
- **Concurrency:** races, cancellation, timeout, resource acquisition and quiescent cleanup.
- **Errors:** structured failure, cause preservation, safe retry, partial effects and visible unknown outcomes.
- **Security:** trust boundaries, authorization, secret handling, filesystem/network exposure and dependency changes.
- **Compatibility:** APIs, configuration, event and persistence formats, database migrations and supported runtimes.
- **Tests:** real execution path, meaningful assertions, regression strength, negative controls for new guards, isolation and teardown.
- **Operations:** logs, metrics, alerts, performance, rollback and recovery.
- **Documentation:** owning docs, examples, decision records and upgrade instructions match shipped behavior.
- **Scope:** speculative generality, duplicate representations, unrelated refactors and unnecessary dependencies.

## Findings

Report actionable findings with severity, file/line, impact and a concrete correction. Distinguish blocking defects from follow-up suggestions. If no blocking finding remains, state what was reviewed and which evidence was inspected. Do not claim unrun checks passed.
