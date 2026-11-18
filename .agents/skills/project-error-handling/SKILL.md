---
name: project-error-handling
description: Use when designing, implementing or reviewing exceptions, retries, cancellation, timeouts, cleanup, partial effects or operational failure reports.
---

# Error-handling workflow

1. Read docs/error-handling.md and identify the layer that owns the operation and state.
2. Enumerate expected failures, dependency failures, cancellation, timeout and partial or unknown outcomes.
3. Choose a structured error or result contract that preserves cause and required machine-readable information.
4. Define whether the caller may retry, recover, continue or must stop; prove idempotency before retry.
5. Ensure cancellation reaches owned work and cleanup runs without masking the original failure.
6. Make uncertain or degraded state visible with a safe next action; never expose secrets.
7. Add tests for failure codes, state after failure, cancellation, cleanup and retry boundaries.
