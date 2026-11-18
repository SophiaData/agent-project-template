# Decision: project-owned architecture boundary checks

- Date: 2026-11-18
- Status: Accepted
- Owners: Project maintainers

## Problem and context

Architecture documents can describe module ownership and dependency direction, but a coding assistant or contributor can still introduce forbidden imports or cycles. A stack-neutral template cannot reliably infer those rules from folder names or parse every language, build system, generated source, plugin registry and data-model graph.

## Decision

Keep project-policy.json schema version 2 and add architecture as a supported quality-check category. A consuming project records permitted and forbidden dependency edges in docs/architecture.md and configures a suitable stack-native static or test-based guard under that category.

Architecture checks remain optional until a project has meaningful module boundaries and a suitable tool. Every new or changed architecture guard must include a deliberately forbidden dependency fixture that proves the guard rejects the intended violation. An architecture check never substitutes for the required test-category check.

The template documents optional approaches for Python, TypeScript, Java and data engineering, but installs no architecture tool and does not infer dependency rules.

## Alternatives considered

- **Build a universal dependency parser:** rejected because import semantics differ across languages, build systems, reflection, dependency injection, generated code, plugins and data-model graphs.
- **Rely only on architecture prose and human review:** rejected as the sole mechanism because forbidden edges can be checked automatically in many projects.
- **Require one architecture tool for every project:** rejected because the template supports multiple stacks and some projects do not have stable module boundaries worth enforcing.

## Consequences and risks

Projects own their dependency rules, tool configuration, path selectors and negative-control fixtures. A static tool may not observe runtime-loaded dependencies; exceptions must be narrow and documented. A passing architecture command proves only the rules that the configured tool checks.

The existing test requirement remains separate. The quality runner classifies and executes architecture commands but does not interpret the architecture tool's output beyond its exit status.

## Verification

- Tests verify that the architecture category is accepted and executed through the quality runner.
- Tests verify that an architecture check alone cannot satisfy the required test-category check.
- The project verifier validates the new defensive-pattern structure and local documentation links.
- GitHub Actions runs the template contract suite and governance verifier.
