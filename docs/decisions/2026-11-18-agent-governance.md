# Decision: executable Agent instruction and Skill governance

- Date: 2026-11-18
- Status: Accepted
- Owners: Project maintainers

## Problem and context

A reusable engineering template can provide AGENTS.md and Skills, but drift can still create duplicate instruction sources, orphan Skills, malformed metadata or fixed model-role assumptions. DeepSeek Harness treats root and more-specific AGENTS.md files as scoped instructions and validates Skill metadata as part of its documentation gates. This template must preserve the useful engineering discipline without depending on one harness runtime.

## Decision

Use root AGENTS.md as the concise repository-wide standing-order source. Treat subtree AGENTS.md files as narrower supplements. Treat CLAUDE.md and similar host-specific files as compatibility entry points that point to the shared AGENTS.md policy rather than defining a second engineering policy.

Use .agents/skills/<name>/SKILL.md as the project Skill format. Discover Skill directories dynamically, validate kebab-case directory and frontmatter names, require a non-empty description and body, and maintain a human-readable .agents/skills/README.md registry. The verifier rejects registry drift and fixed model-role assignments.

Keep the governance model agent-neutral. The template does not assign planning, implementation or review responsibilities to GPT, Claude, Codex, DSH or another named model. Task workflows live in Skills and can be selected by any compatible Agent.

## Alternatives considered

- **Keep the hard-coded Skill allowlist:** rejected because adding a Skill would require editing a central Python list and could silently create an orphaned Skill.
- **Use only prose for instruction hierarchy:** rejected because compatibility files and Skills can drift without a structural signal.
- **Make every host-specific file a second policy source:** rejected because the same engineering rule would diverge across agents.
- **Require DSH-specific runtime behavior:** rejected because the template is intended for Claude Code, Codex, Cursor, DSH and other compatible agents.

## Consequences and risks

The verifier now owns structural governance for instruction and Skill surfaces. It cannot prove that prose is semantically complete or that a Skill performs its claimed workflow correctly; those remain review and behavior-test responsibilities.

Projects with legitimate host-specific configuration may keep it in compatibility files, but engineering rules belong in the shared policy. Projects may add subtree AGENTS.md files when a real narrower scope exists.

## Verification

- The template contract tests cover valid Skill discovery, orphan directories, registry drift, malformed or model-role Skill content, divergent CLAUDE.md and fixed model-role root instructions.
- scripts/verify_project.py discovers Skills dynamically and validates the canonical registry.
- GitHub Actions runs the contract suite and governance verifier before merge.
