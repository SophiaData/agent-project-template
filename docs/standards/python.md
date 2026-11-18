# Python engineering standards

## Project and dependencies

Declare supported Python versions and runtime dependencies in the project's authoritative packaging file. Use a virtual environment and a lock or constraints strategy appropriate to the application. Keep development and runtime dependencies distinct. Do not rely on undeclared packages installed globally.

## Types and interfaces

Add type annotations to public functions and non-obvious data structures. Prefer concrete domain types and protocols over unbounded dictionaries or Any. Validate external JSON, configuration, files and service responses at their boundaries; avoid revalidating trusted internal values without a reason.

## Functions and resources

Keep functions focused and explicit about side effects. Use context managers for files, database sessions, locks and other owned resources. Do not leave background tasks, subprocesses or clients running after their owner exits.

## Errors and logging

Raise meaningful domain exceptions, preserve causes with exception chaining, and catch only failures the current layer can handle. Use the project's logging framework and structured context. Never log credentials or full sensitive payloads.

## Testing and tooling

Use the project's configured formatter, linter, type checker and test runner. Tests should isolate external services, use deterministic fixtures and assert behavior. Where package or layer direction matters, consider a static import-contract tool such as import-linter and register it as an architecture quality check with a forbidden-import fixture. Do not assume pytest, mypy, Ruff, import-linter or any other tool is installed unless declared by the project.
