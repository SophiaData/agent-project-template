# Coding and design standards

These rules apply across languages. Use the matching profile in docs/standards/ for language- and engine-specific guidance. A project may add stricter local rules when they have a clear owner and executable enforcement.

## Correctness before cleverness

Make behavior, invariants and side effects explicit. Prefer readable control flow over compressed expressions, hidden defaults or clever abstractions. Handle the expected and failure paths deliberately.

## Ownership and boundaries

Place behavior beside the data and lifecycle it owns. Keep dependency direction explicit. Avoid cyclic dependencies, cross-layer reach-through and generic services that expose methods for only one internal caller. Prefer narrow interfaces and cohesive modules.

## Simplicity and dependencies

Choose the smallest design that meets current requirements. Do not add speculative extension points, configuration switches, wrappers or state machines. Prefer a maintained dependency when it removes more code and maintenance than it adds; document the tradeoff and retain tests for project-specific behavior.

## Interfaces and types

Name inputs, outputs, units, nullability, ordering, side effects and failure behavior. Use the strongest practical type system. Avoid untyped escape hatches and broad casts. Validate at parsing, configuration, network, process, queue, model/tool and persistence boundaries; trust ordinary typed calls inside one process unless evidence says otherwise.

## State, concurrency and resources

Identify who owns mutable state, promises, locks, callbacks, timers, workers and external resources. Define initialization, cancellation, timeout, cleanup and shutdown behavior. Prevent races before publishing state. Release resources deterministically and wait for owned work to settle when required. Apply the relevant [defensive patterns](defensive-patterns/README.md) when these lifecycle risks are present.

## Errors and observability

Use structured errors appropriate to the owning domain. Preserve causes and stable machine-readable codes when callers need to act on failures. Do not swallow unexpected failures, log secrets or report success when the outcome is unknown. See docs/error-handling.md.

## Configuration

Separate deployment-varying values from code. Validate configuration at load or at the earliest point where it can be resolved. Avoid hidden defaults and duplicated sources of truth. Keep security invariants and protocol constants fixed unless the contract explicitly allows change.

## Security and privacy

Apply least privilege. Validate untrusted input, encode output for its destination, protect secrets, constrain filesystem and network access, and avoid leaking personal or business data through diagnostics and fixtures. Treat dependency and generated-code changes as supply-chain changes.

## Performance

Measure the real user or data path before optimizing. Identify throughput, latency, memory, I/O, cardinality and resource bounds. Avoid premature caches, unbounded queues, uncontrolled concurrency and repeated work. Add benchmarks only when performance is an acceptance criterion or regression risk.

## Comments and naming

Names should express domain meaning and units. Comments explain non-obvious intent, invariants, constraints and compatibility requirements; they should not restate code. Keep explanations beside the behavior they govern.

## Reviewability

Keep diffs focused and deterministic. Avoid formatting unrelated files, generated-file drift and unnecessary renames. Every new dependency, public API, configuration key, persistent field and compatibility path needs a clear reason and an owner.
