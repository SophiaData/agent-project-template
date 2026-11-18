# Documentation standards

Documentation is part of the product and must describe current behavior. Keep each fact in one authoritative location; other documents should link to its owner instead of copying the same rule.

## Document ownership

- **README:** project purpose, quick start and links to authoritative references.
- **AGENTS.md:** concise standing instructions needed during engineering work.
- **Architecture:** system context, boundaries, modules, ownership, data flow and runtime topology.
- **Development guide:** setup, development workflow and verification entry points.
- **Coding and testing standards:** reusable engineering rules and test strategy.
- **Package or module documentation:** local API, configuration, behavior, limitations and extension points.
- **Decision records:** why a durable decision was made, alternatives and consequences.
- **Compatibility and upgrade guides:** user actions required when an externally visible contract changes.
- **API reference:** generated or source-derived contract details where possible.

## Writing rules

Describe current state in present tense. Separate required behavior from examples and recommendations. Name the actor, operation, condition and outcome. Explain units, defaults, ownership, failure behavior and compatibility when they affect use.

Keep comments and API documentation close to the code they describe. Comments explain non-obvious intent or invariants; they do not narrate implementation steps or repeat the code.

Avoid duplicate inventories of packages, commands, configuration or APIs when manifests, source code or generators are authoritative. Use links to lower-level owners rather than copying their implementation details.

## Maintenance

Update the owning documentation in the same change as the behavior or interface. Check links, examples, commands, diagrams and generated references. Mark examples as illustrative when they are not executable. Do not claim that an example or command was tested unless it was.

For major architecture or policy decisions, use docs/decisions/. For externally visible breaking changes, follow docs/compatibility.md and provide an upgrade guide with the change.
