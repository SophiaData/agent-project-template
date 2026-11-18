# General defensive patterns

Apply only the patterns whose triggers match the changed behavior. These rules complement [coding standards](../coding-standards.md), [error handling](../error-handling.md) and [testing policy](../testing.md).

## Shared mutable state has one owner

### Applies when
A change introduces or modifies state shared by multiple calls, tasks, modules, workers or processes.

### Required invariant
Name one lifecycle owner for the state. Other components access it through that owner's contract; they do not create competing caches, registries, global current selections or shadow copies that can diverge.

### Failure prevented
Split-brain state, stale caches, hidden coupling, cross-request leakage and cleanup that cannot identify who owns a resource.

### Evidence
Trace every writer, reader, initializer and disposer. Tests should exercise two independent owners or overlapping operations when isolation is part of the contract.

### Boundary and exception
Immutable constants and derived values do not need a mutable-state owner. A process-wide singleton is acceptable only when process-wide identity is an explicit requirement and its initialization and shutdown owner are clear.

### Incorrect example
~~~ts
let currentTenant: Tenant
let activeSession: Session
~~~

### Correct example
~~~ts
class RequestContext {
  constructor(
    readonly tenant: Tenant,
    readonly session: Session,
  ) {}
}
~~~

### Enforcement
Architecture and code review; add a focused regression test when ownership or isolation can be observed at runtime.

## Correctness does not depend on timing

### Applies when
A change uses timers, microtasks, event-loop ordering, polling, sleeps or callback scheduling to coordinate asynchronous work.

### Required invariant
Represent readiness, completion, ordering and cancellation with explicit state or synchronization owned by the operation. Scheduling may improve responsiveness, but it must not decide whether the result is correct.

### Failure prevented
Race conditions that pass under light load, flaky tests, missed notifications and waits that never settle because the awaited transition cannot occur.

### Evidence
Identify the exact state transition being awaited. Use promises, conditions, barriers, queues or protocol acknowledgements with explicit completion semantics. For a race regression, prove overlap with synchronization rather than repeating the test and hoping the race appears.

### Boundary and exception
A delay used for rate limiting, backoff or user-visible pacing is valid when elapsed time is itself the requirement. It is not a substitute for observing readiness or completion.

### Incorrect example
~~~ts
startWorker()
await new Promise(resolve => setTimeout(resolve, 100))
readWorkerResult()
~~~

### Correct example
~~~ts
const worker = startWorker()
await worker.ready
const result = await worker.completion
~~~

### Enforcement
Code review and deterministic regression tests. A test that relies on arbitrary sleeps to establish correctness is not sufficient evidence.

## Acquire shared resources atomically

### Applies when
Tests or application code acquire ports, filesystem paths, locks, database names, queues, sockets, sessions or other resources shared beyond one call stack.

### Required invariant
Use the resource owner's atomic allocation mechanism. Do not check that a resource appears free and claim it later. Give concurrent owners isolated identities or namespaces.

### Failure prevented
Time-of-check/time-of-use races, cross-test interference, overwritten files, port collisions and data contamination between concurrent jobs.

### Evidence
Inspect allocation and cleanup paths. When cross-process isolation matters, run independent test processes concurrently and assert their resources remain separate.

### Boundary and exception
A literal path or URL used only as parser input or an expected value is not an acquired resource. Stable identifiers required by a protocol may remain fixed if the fixture maps them to isolated live resources.

### Incorrect example
~~~ts
const port = await findUnusedPort()
const server = await listen(port)
~~~

### Correct example
~~~ts
const server = createServer()
await listen(server, 0)
const address = server.address()
~~~

### Enforcement
Review plus tests for the relevant resource boundary. Prefer allocator-provided uniqueness over a repository-wide serial test setting.

## Cleanup reaches quiescence

### Applies when
A component starts asynchronous work, owns callbacks or subscriptions, spawns processes, or exposes cancellation and disposal.

### Required invariant
After disposal reports completion, owned work can no longer mutate released state or use released resources. Propagate cancellation, detach callbacks, await owned work where required, and report cleanup failures without hiding the original failure.

### Failure prevented
Use-after-dispose races, leaked subprocesses, writes after teardown, dangling listeners and tests that pass while background work is still running.

### Evidence
Test disposal during active work. Assert externally observable state after disposal and verify that child processes, listeners, files or connections are actually gone. Include failure and cancellation paths.

### Boundary and exception
A fire-and-forget notification may intentionally outlive its caller only when another named owner takes responsibility for its lifetime and failure reporting.

### Incorrect example
~~~ts
abortController.abort()
releaseResources()
return
~~~

### Correct example
~~~ts
abortController.abort()
await ownedTasksSettled()
await releaseResources()
return
~~~

### Enforcement
Lifecycle review and regression tests. A cancellation request alone is not proof that teardown has completed.

## Retry only safe, bounded operations

### Applies when
A change adds retries, replay, reconnect, redelivery or automatic recovery after an uncertain outcome.

### Required invariant
The operation is idempotent or protected by an idempotency key; retry classification excludes permanent failures; attempts and total elapsed time are bounded; cancellation and uncertain outcomes are explicit.

### Failure prevented
Duplicate mutations, repeated charges or writes, retry storms, amplified outages and hidden partial success.

### Evidence
Test transient and permanent failures, duplicate delivery, exhausted budgets and cancellation. Verify persisted or externally visible state, not only the retry counter.

### Boundary and exception
A read-only operation may be naturally repeatable, but still needs a finite resource and time budget. Provider-specific transient retry policies belong at that provider boundary.

### Incorrect example
~~~ts
for (;;) {
  try {
    await createOrder()
    break
  } catch {
    // try again
  }
}
~~~

### Correct example
~~~ts
await createOrder({
  idempotencyKey: requestId,
  retry: { maxAttempts: 3, deadline },
})
~~~

### Enforcement
Error-path review and tests that inspect final state after duplicate or uncertain delivery.

## Report independent outcomes independently

### Applies when
A process, request, job or test can have multiple simultaneous outcome facts, such as timeout, cancellation, signal, exit code, partial effects or cleanup failure.

### Required invariant
Preserve each independently meaningful outcome. Do not hide one fact inside another fact's conditional branch or collapse an uncertain result into success.

### Failure prevented
A timed-out process that exits zero being reported as clean success, partial mutations being lost from reports, and callers making unsafe recovery decisions.

### Evidence
Test combinations that can coexist. Confirm callers can distinguish the operation result, termination cause and cleanup result from the public report.

### Boundary and exception
A deliberately mutually exclusive sum type is appropriate when the underlying contract guarantees exclusivity. Do not invent independent fields for states that cannot coexist.

### Incorrect example
~~~ts
if (timedOut) {
  report({ status: 'timed-out' })
} else {
  report({ status: exitCode === 0 ? 'passed' : 'failed' })
}
~~~

### Correct example
~~~ts
report({
  timedOut,
  signal,
  exitCode,
  cleanupError,
})
~~~

### Enforcement
Contract tests for combined outcomes and review of every consumer that makes a recovery decision.

## Validate at real trust boundaries

### Applies when
Data crosses from an untrusted or differently governed boundary, such as HTTP, files, environment variables, queues, external tools, model output or persistence.

### Required invariant
Parse and validate the boundary representation before using it as trusted domain data. Preserve useful validation errors. Inside a typed, trusted call path, do not repeat equivalent validation without evidence of a new trust boundary.

### Failure prevented
Malformed or hostile data entering domain logic, inconsistent interpretation between callers and duplicated validation that obscures ownership.

### Evidence
Test malformed, missing, oversized and unauthorized boundary inputs as relevant. Trace where raw data becomes a typed domain value and ensure downstream code relies on that contract.

### Boundary and exception
A value is not trusted merely because it is internal: persisted data, plugin boundaries and cross-process messages may be stale or independently produced. Conversely, a private typed function does not need to revalidate every invariant already guaranteed by its caller.

### Incorrect example
~~~ts
function handleTypedRequest(request: ValidatedRequest) {
  validateRequestAgain(request)
  return domainService.execute(request)
}
~~~

### Correct example
~~~ts
const request = parseAndValidate(untrustedHttpBody)
return domainService.execute(request)
~~~

### Enforcement
Trust-boundary review and malformed-input tests. Static validation is useful where the language or schema tooling can express the contract.

## Performance claims require evidence

### Applies when
A change is justified by throughput, latency, memory, cost, scaling or resource-utilization improvements, or changes a performance-sensitive path.

### Required invariant
Measure the representative workload before and after, state the environment and workload, and retain correctness checks. An optimization must not trade away correctness or an unbounded resource cost.

### Failure prevented
Optimizations that make the real workload slower, shift cost to another component, hide regressions behind synthetic inputs or introduce unbounded queues and caches.

### Evidence
Record baseline and changed measurements with workload size, concurrency, runtime and relevant resource limits. Include a correctness or output-equivalence check. Explain measurement noise and tradeoffs.

### Boundary and exception
A low-risk readability refactor does not need a benchmark merely because it changes code. Benchmark when performance is an acceptance criterion or a credible regression risk.

### Incorrect example
~~~text
The new cache should be faster because it avoids database calls.
~~~

### Correct example
~~~text
Under the same 30-minute replay and input volume, p95 latency changed from
420 ms to 280 ms; peak memory rose from 1.2 GiB to 1.3 GiB. Output
reconciliation matched across both runs.
~~~

### Enforcement
PR evidence and review. Add a repeatable benchmark gate only when the workload and threshold are stable enough to be meaningful.
