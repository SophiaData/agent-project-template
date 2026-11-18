## Motivation

<!-- Problem, context and why this change is needed. -->

## Scope and design

<!-- Acceptance criteria, affected modules, non-goals and key design decisions. -->

## Defensive-pattern review

- [ ] Applicable defensive patterns were identified and reviewed.
- [ ] New or changed automated guards have a negative-control test.
- [ ] Exceptions are documented with an owner and bounded scope, if applicable.

## Compatibility and operational impact

<!-- Public API, data/schema, migration, rollout, rollback or recovery implications. -->

## Test design

<!-- Explain why the selected tests cover the changed behavior. For behavior changes, use scenario × previous behavior × expected behavior × test. For performance changes, include before/after measurements and conditions. For refactors or migrations, show how unchanged behavior is verified. For documentation-only changes, state how links, examples and generated outputs are checked. -->

## Verification evidence

| Command / check | Result (PASS / FAIL / NOT RUN / BLOCKED) | Environment / evidence |
| --- | --- | --- |
| python scripts/verify_project.py | NOT RUN | |
| python -m unittest discover -s tests -p 'test_template_*.py' -v | NOT RUN | |
| python scripts/run_quality.py | NOT RUN | |

## Review

<!-- Confirm actual diff review, findings resolved and remaining limitations. -->

## AI assistance (when applicable)

<!-- Disclose material AI assistance: tools used, areas they contributed to, and how a human verified the result and made consequential decisions. Do not include private prompts, credentials or sensitive context. This is transparency, not a model-role or agent-orchestration requirement. -->

## Risks and release boundary

<!-- Known risks, production approval requirements and next safe action. -->
