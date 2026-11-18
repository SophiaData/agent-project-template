# Architecture

This document is the authoritative map of the consuming project. Complete it during project planning and keep it aligned with the shipped system.

## Purpose and boundaries

Describe the product or system purpose, users, externally visible behavior and explicit non-goals. Identify what this project owns and what belongs to external systems or other teams.

## System context

Describe upstream and downstream systems, trust boundaries, protocols, deployment environments and operational dependencies. Include a context diagram when it clarifies ownership or data flow.

## Modules and ownership

For each significant module or service, record its responsibility, owned state, public interface and lifecycle owner. Explain dependency direction and the permitted paths between layers. Avoid duplicating detailed API references that belong with the owning module.

## Dependency rules and enforcement

Record the permitted dependency direction between significant modules or layers. Use one row per boundary; name the public interface that consumers must use.

| Source module or layer | May depend on | Must not depend on | Public interface |
| --- | --- | --- | --- |
| <module> | <allowed modules> | <forbidden modules> | <package/API entry point> |

Treat the dependency graph as acyclic unless an explicit decision records why a cycle is necessary. Do not import private implementation paths across package boundaries. Record each exception with its owner, scope and reason; do not use broad tool exclusions to hide violations.

Enforce these rules with a stack-native static or test-based architecture check. Configure it as a quality-check entry with category `architecture`; include all relevant source modules and rule configuration in its `paths`. Every architecture guard needs an intentionally forbidden dependency fixture that proves it fails for the expected reason.

Possible tools include import-linter for Python, dependency-cruiser or ESLint boundary rules for TypeScript, ArchUnit for Java, and project-owned model-DAG checks over dbt manifests or warehouse lineage for data engineering. These are examples, not template dependencies. Select a tool that can observe the actual runtime and build graph.

## Data flow and state

Document important request, event, batch or streaming paths. Identify source of truth, consistency expectations, data grain, persistence boundaries, retention and recovery behavior where applicable.

## Runtime and deployment topology

Describe processes, workers, queues, databases, storage, scheduled jobs, network boundaries and deployment units. State supported runtimes and external service assumptions.

## Cross-cutting guarantees

Record security boundaries, authentication and authorization, availability, observability, performance constraints, concurrency and failure containment.

## Contracts and compatibility

Link to public APIs, event schemas, database contracts, persisted formats and migration procedures. The compatibility policy lives in docs/compatibility.md.

## Decisions

Keep durable decisions and rejected alternatives in docs/decisions/. This document describes the current architecture; decision records explain why it took this shape.
