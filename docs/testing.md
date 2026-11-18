# Testing policy

Tests are executable evidence for behavior. A passing command is meaningful only when the test exercises the intended code path, asserts the required outcome and runs in a representative environment.

## Test levels

- **Unit:** test a small unit with controlled dependencies. Cover normal behavior, boundaries, invalid input and meaningful failure paths.
- **Integration:** exercise real module boundaries such as database adapters, queues, filesystem, HTTP clients or engine connectors. Use isolated resources and representative configuration.
- **Contract:** verify compatibility between producers and consumers, API schemas, event formats, SQL interfaces and persisted data.
- **End-to-end:** exercise important user or operator journeys through the supported application entry point.
- **Performance and resilience:** measure throughput, latency, memory, scaling, backpressure, recovery and failure behavior when these are part of the system's requirements.

Choose levels based on risk. Do not create expensive end-to-end tests for every branch, and do not substitute mocks for the integration behavior that matters.

## Test design

Prefer observable assertions over implementation-shaped assertions. Test edge cases, error paths, ordering, concurrency and permanent regressions. A test that passes only in isolation has a resource or synchronization defect unless isolation is an explicit contract.

Tests must own and release temporary files, ports, databases, queues, processes and global state. Use deterministic synchronization rather than arbitrary sleeps. Set timeouts from the full operation budget and ensure teardown waits for owned work to stop. Apply relevant [defensive patterns](defensive-patterns/README.md) when tests or fixtures own asynchronous work or shared resources.

## Negative controls for quality gates

A new automated guard is incomplete until a deliberately invalid fixture proves that the guard rejects the intended violation. Add a negative-control test alongside the positive case. Assert the specific diagnostic or failure condition, not merely a non-zero result that could come from an unrelated error.

For a change to an existing guard, preserve or add a negative control for the regression it is intended to catch. Do not weaken the fixture or assertion just to make CI green. A negative control proves that a guard can detect one targeted violation; it does not prove that the guard covers every violation.

## Coverage

Coverage is a diagnostic and, where configured, a quality threshold. It proves execution, not correctness. Do not add meaningless tests to hit a percentage or delete tests to silence a failure. Set thresholds according to risk, language, generated code and project maturity; this template does not impose one universal percentage.

## Test environments

Document required runtimes, services, credentials and fixtures. CI must install the dependencies needed by the checks it claims to run. A skipped integration test or unavailable engine must be reported explicitly; a local mock does not prove a live service or production topology.

## Test discovery and quality-check limitations

The template runner executes declared argv commands and checks their exit status. It does not understand every test framework's output and cannot prove that a command discovered or executed a meaningful number of tests. Some frameworks return success for an empty test selection.

Configure the framework's fail-on-empty behavior when available. Otherwise use a project-owned wrapper or report that validates the discovered test count for that framework. Keep that validation close to the test command; do not guess test counts by parsing arbitrary output in the generic runner.

## Evidence and quality gates

Configure real commands in project-policy.json as category plus argv tokens. At least one test-category check is required once application source exists. The runner does not invoke a shell and rejects obvious no-op commands, but test discovery and assertion quality remain project responsibilities.

For each PR, report exact commands, PASS / FAIL / NOT RUN / BLOCKED status, runtime and relevant output or CI link. Distinguish static analysis, unit tests, integration tests, end-to-end tests and manual validation.
