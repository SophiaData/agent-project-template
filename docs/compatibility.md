# Compatibility and upgrades

Compatibility includes every contract a consumer can observe: APIs, CLI behavior, configuration, database schemas, events, files, persisted data, message formats, package exports and operational procedures.

## Before changing a contract

Identify producers, consumers and deployed versions. Determine whether the change is additive, behavior-changing or breaking. Check default values, nullability, ordering, units, error codes, serialization, data retention and rollback behavior.

Prefer additive evolution when it does not create ambiguous or unsafe states. Do not silently reinterpret persisted data or reuse a field for a different meaning.

## Schema and data migrations

State the migration owner, supported source and target versions, ordering, backfill, validation, rollback or forward-recovery strategy, and behavior during mixed-version operation. Make migrations repeatable or explicitly detect that they have already run. Test with representative old and new data.

For event and persisted formats, keep readers compatible with supported historical versions. Add a new version when old data cannot be interpreted safely; do not overwrite historical fixtures or formats merely to simplify current code.

## Deprecation and breaking changes

Document the old and new behavior, affected consumers, replacement and removal timeline. Provide a warning or compatibility period when practical. A breaking change requires an explicit migration path and an upgrade guide before it ships.

Use the project's declared versioning policy. If semantic versioning is adopted, breaking public contracts require a major version unless the published policy defines a compatible transition.

## Release boundary

Separate code readiness from release authorization. CI, review and a merged PR do not authorize production deployment, publication, database migration or production data changes. Follow the project's approval and rollback process.

## Verification

Test old-to-new compatibility, mixed-version behavior, migration idempotency and failure recovery where applicable. Keep compatibility fixtures and upgrade documentation aligned with the actual shipped contract.
