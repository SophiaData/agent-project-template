---
name: project-upgrade-guide
description: Use when a change alters an externally observable API, CLI, configuration, schema, persisted format, package entry point or operational procedure.
---

# Upgrade guidance workflow

1. Identify the old and new contract, affected consumers and supported source versions.
2. Classify the change as additive, behavior-changing or breaking; do not hide a breaking change in a refactor.
3. Define migration order, backfill, validation, mixed-version behavior and rollback or forward recovery.
4. Write ordered user actions with exact files, keys, commands or symbols.
5. Add compatibility tests and representative old-format fixtures where applicable.
6. Update docs/compatibility.md and the project's upgrade guide in the same change.
7. Verify that the instructions describe the shipped implementation, not a proposed future state.
