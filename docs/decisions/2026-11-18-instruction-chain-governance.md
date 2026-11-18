# Decision: project instruction-chain preflight, not a universal runtime loader

- Date: 2026-11-18
- Status: Proposed
- Owners: Project maintainers

## Problem and context

v2.5 checks root standing orders, compatibility entry points and Skills, but does not show which directory-scoped instructions are applicable to a particular target. Hosts differ: DSH loads additive candidate groups and trims duplicate content, Codex selects a per-directory replacement, and Claude Code has its own memory files. Pretending these are one universal precedence model can hide rule drift.

## Requirements and constraints

- Keep AGENTS.md as the common policy source, Skills as task workflows, and CLAUDE.md as a thin compatibility entry point.
- Work across DSH, Codex, Claude Code, Cursor and other clients without assigning fixed agent/model roles.
- Do not modify a host runtime, install hooks or claim a host actually followed instructions.
- Reject unsafe repository paths and unreadable instruction sources.
- Preserve manual merge/release/deployment boundaries and project-policy schema 2.

## Decision

Add a standard-library `scripts/instruction_chain.py` inspector with `shared`, `dsh`, `codex`, and `claude` file-selection profiles. Output an ordered, auditable JSON source map with skipped candidates, content digests, byte counts, advisory warnings and an explicit `host_verified: false` marker. Do not expose source text by default. Integrate source-level safety checks into the existing project verifier, and use positive plus negative-control tests.

Local overlay files are ignored by Git; they may narrow a developer's workflow but are not permitted to bypass engineering or delivery boundaries. Semantic contradictions between distinct text bodies require human review, not a regex-selected winner.

## Alternatives rejected

- **Patch DSH or other host internals:** unnecessary coupling for a repository template and high upgrade risk.
- **One universal precedence algorithm:** contradicts documented host behavior.
- **Automatically rewrite or fold conflicting prose:** unsafe semantic guess and loss of provenance.
- **Treat static tests as runtime compliance:** overstates what project CI can prove.

## Consequences and risks

Projects gain a reproducible chain preflight without adopting a new runtime dependency. CLI output does not reproduce global policy, dynamic refresh, host imports, context-budget algorithms or subagent state. Host-specific acceptance remains an explicit, separately collected evidence task. Existing projects may selectively adopt the script and tests; upgrades are not automatic.

## Verification

The PR must show successful template tests and project verifier results, plus negative-control evidence for path traversal, symlink escapes and invalid file contents. Real DSH/Claude/Codex host tests are NOT RUN until independently executed and reported.
