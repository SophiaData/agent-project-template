# Defensive patterns

Defensive patterns are requirements for recurring defect classes, not general style preferences. Apply a rule when its stated trigger matches the code being changed; do not impose unrelated rules on every module.

Each pattern records:
- **Applies when:** the code or change condition that activates the rule.
- **Required invariant:** what must remain true.
- **Failure prevented:** the concrete class of defect.
- **Evidence:** what a reviewer or test must inspect to establish compliance.
- **Boundary and exception:** what the rule does not cover and who may approve an exception.
- **Incorrect / correct examples:** contrasting implementations that make the distinction reviewable.
- **Enforcement:** whether the rule is checked automatically, by tests, or through semantic review.

## Choose the relevant patterns

| Change area | Read |
| --- | --- |
| Shared state, asynchronous work, resource ownership, cancellation, retries, error reporting and performance | [general.md](general.md) |
| SQL models, warehouse tables, batch jobs, streaming pipelines, data contracts and migrations | [data-engineering.md](data-engineering.md) |

Read the relevant patterns before implementation and again during review. A pattern is not a reason to add defensive code without a real trigger: identify the owner, observable risk and smallest evidence that proves the invariant.

## Enforcement model

The project verifier checks that every pattern has the required documentation structure and that its local Markdown links resolve. Template contract tests include deliberately invalid fixtures to prove those guards reject violations.

Those structural checks do **not** prove that a rule is semantically correct or that application code follows it. Reviewers must inspect applicability, implementation and evidence. When a new automated guard is introduced, add a negative-control test that injects the rejected condition and asserts the guard fails for the intended reason.

Exceptions must be explicit, local to the affected contract and approved by the owner responsible for the invariant. An exception does not silently become a repository-wide precedent.
