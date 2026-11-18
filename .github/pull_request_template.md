## Motivation

<!-- Problem, context and why this change is needed. -->

## Scope and design

<!-- Acceptance criteria, affected modules, non-goals and key design decisions. -->

## Compatibility and operational impact

<!-- Public API, data/schema, migration, rollout, rollback or recovery implications. -->

## Verification evidence

| Command / check | Result (PASS / FAIL / NOT RUN / BLOCKED) | Environment / evidence |
| --- | --- | --- |
| python scripts/verify_project.py | NOT RUN | |
| python -m unittest discover -s tests -p 'test_template_*.py' -v | NOT RUN | |
| python scripts/run_quality.py | NOT RUN | |

## Review

<!-- Confirm actual diff review, findings resolved and remaining limitations. -->

## Risks and release boundary

<!-- Known risks, production approval requirements and next safe action. -->
