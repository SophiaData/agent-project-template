# Error handling

Error handling is part of an API contract. For each failure, define who detects it, who owns recovery, what state may have changed and what the caller can safely do next.

## Error representation

Use domain-appropriate error types or structured result values. Preserve the original cause when translating a dependency failure. Use stable machine-readable codes when callers, retry policy, UI or analytics must distinguish failures. Keep human-readable messages actionable and free of secrets.

Do not create a separate error class for every message. Create a distinct type when callers handle it differently or it carries structured fields. Do not erase a known error's type or code while wrapping it.

## Catch and recovery

Catch an error only when the current layer can recover, add useful context or translate it into its owned contract. Logging alone is not recovery. Do not catch and continue with state whose validity is unknown.

A catch that intentionally ignores a failure must name the expected failure and explain why discarding it is safe. Keep the protected operation narrow. Unexpected failures must propagate or be reported through an independent failure path.

## Retry and timeout

Retry only when repetition is safe, the operation is idempotent or has an idempotency key, and the retry owner has a finite budget and cancellation policy. Do not retry validation, authorization or permanent failures as if they were transient. Bound queueing, backoff and total elapsed time.

Define what timeout means for the underlying operation. Returning a timeout to the caller does not prove that a remote mutation stopped. Reconcile uncertain outcomes before retrying non-idempotent work.

## Cancellation and cleanup

Propagate cancellation through owned asynchronous work. Cleanup must run on success, failure and cancellation. Do not release shared resources while other owners still use them. Await cleanup when correctness depends on completion, and report cleanup failure without hiding the original failure.

## User-facing and operational reporting

Reports should identify the failed operation, impact, whether the outcome is known, and a safe next action. Do not expose credentials, tokens, raw personal data or sensitive SQL parameters. Persistent degraded or uncertain state needs persistent visibility.

## Verification

Test expected failures, cancellation, timeout, partial effects, cleanup failure and safe retry behavior. Assert structured codes and externally observable state where those are part of the contract.
