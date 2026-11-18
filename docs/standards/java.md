# Java engineering standards

## Runtime and dependencies

Declare the supported JDK and build tool versions. Keep dependency versions reproducible and review transitive dependencies. Avoid introducing libraries for behavior already provided by the supported JDK.

## Types and object design

Prefer cohesive classes, immutable value objects and narrow interfaces. Make nullability and mutability explicit. Avoid inheritance where composition expresses ownership more clearly. Keep public APIs minimal and documented.

## Resource and concurrency management

Use try-with-resources for closeable resources. Define executor ownership, thread lifecycle, cancellation and shutdown. Avoid unbounded thread pools and queues. Make shared mutable state and synchronization requirements explicit.

## Exceptions and observability

Use domain exceptions at API boundaries, preserve causes and avoid using exceptions for ordinary control flow. Do not catch and ignore failures. Use structured logging and avoid sensitive values.

## Testing and tooling

Use the project's declared build tool, static analysis and test framework. Test public contracts and integration with external services using isolated fixtures. Do not assume Maven, Gradle, JUnit or a specific JDK unless configured.
