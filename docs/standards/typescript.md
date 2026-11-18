# TypeScript and Node.js engineering standards

## Type safety

Enable strict compiler options where compatible with the project. Prefer discriminated unions, narrow interfaces and explicit return types on public APIs. Avoid any, non-null assertions and broad casts; validate data at untyped boundaries rather than weakening types throughout the codebase.

## Modules and package boundaries

Follow the package's declared module system and supported Node.js versions. Keep imports and exports explicit. Use package public entry points across package boundaries; avoid reaching into another package's private source or build output.

## Async behavior and resources

Await owned promises and handle rejection paths. Propagate cancellation and deadlines where supported. Bound concurrency and queues. Close streams, servers, database clients, workers and subprocesses through their owning lifecycle.

## Errors and diagnostics

Use typed or structured errors when consumers need to distinguish failures. Preserve cause and stable codes. Do not return success-shaped values for failures unless the API contract explicitly defines them.

## Testing and tooling

Use the repository's configured formatter, linter, compiler and test runner. Test source and built/package entry points where they differ. Where package or layer direction matters, consider dependency-cruiser or an ESLint boundary rule and register it as an architecture quality check with a forbidden-import fixture. Do not assume a particular bundler, test framework, package manager or architecture tool.
