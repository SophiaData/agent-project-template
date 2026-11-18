# Instruction-chain governance

This version adds an **offline, deterministic preflight** for the project tree. It does not install a runtime injection hook in DSH, Codex, Claude Code, Cursor, or another Agent. It does not assert that an Agent actually read or obeyed the text. An ordinary CI pass proves source readability and repository structure, not prompt delivery or semantic compliance.

## Canonical policy vs. host projection

`AGENTS.md` remains the common engineering policy owner. Scoped files narrow its applicability; Skills own task workflows. Run the inspector against the actual file/directory a task will touch, rather than assuming every subtree file is in scope.

~~~sh
python scripts/instruction_chain.py --target docs/agent-governance.md --profile shared
python scripts/instruction_chain.py --target docs/agent-governance.md --profile dsh
python scripts/instruction_chain.py --target docs/agent-governance.md --profile codex
python scripts/instruction_chain.py --target docs/agent-governance.md --profile claude
~~~

The output is stable JSON. `sources` contains ordered project-relative source paths, directory scope, byte counts and SHA-256 content digests. `skipped` contains candidates omitted as duplicates or shadowed by a same-directory Codex override; `warnings` calls out local overlays, Codex policy-shadowing and advisory budget overflow. By default, the inspector does **not** print instruction text; use `--include-content` only when reviewing trusted local files. A `host_verified: false` field is always reported.

| Profile | Project-file semantics in this preflight | Important boundary |
| --- | --- | --- |
| `shared` | `AGENTS.md`, then optional `AGENTS.local.md`, at each directory from root to target | Canonical project policy; not a host-specific loader |
| `dsh` | `AGENTS.md`, `CLAUDE.md`, then `AGENTS.local.md` and `CLAUDE.local.md`; exact trimmed-content duplicates collapse per directory | DSH additionally loads user-global instructions and refreshes on filesystem touches; this CLI does neither |
| `codex` | First non-empty of `AGENTS.override.md` / `AGENTS.md` in each directory, root down | Host fallback filenames, global instructions, byte budgeting and run lifecycle are not simulated |
| `claude` | `CLAUDE.md` then `CLAUDE.local.md` per directory | `AGENTS.md` is not automatically expanded by this inspector; the project `CLAUDE.md` is a compatibility instruction entry point |

These profiles model the documented *file-selection differences* and should not be treated as an exact emulator of host prompt construction. In particular, a host may perform imports, exclude files, truncate to its own budget, dynamically refresh, or use higher-authority/global rules that this project cannot see.

Upstream references:
- [DSH instruction package](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/context/agent-instructions/README.md)
- [Codex AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Claude Code memory](https://code.claude.com/docs/en/memory)

## Scope and precedence rules

1. Resolve the target relative to the repository root. For existing directories, include that directory; for files, include the parent directory. Unknown file paths may be inspected before the file exists. Paths resolving outside the repository fail closed.
2. Walk from the project root to the target scope in ascending specificity. Unrelated sibling instruction files do not apply.
3. Discover each profile's candidate files without loading any bytes from outside the checkout. Empty files are skipped during chain resolution, but flagged as invalid by the repository audit.
4. Treat local overlays as **additions for developer convenience**, not an authorization to bypass project guardrails, tests, approval requirements or safety boundaries. They are gitignored. A local file that contradicts shared policy must be reconciled manually.
5. Keep `CLAUDE.md` files as thin compatibility entry points to the shared engineering policy. Codex's `AGENTS.override.md` is a host-specific replacement; if present, inspect both the Codex and DSH/shared profiles before review because their effective project guidance can diverge.
6. If different nonidentical instructions disagree, the verifier **cannot** determine semantic priority or compliance. Record the conflict, authoritative owner and intended resolution in the PR. Do not automatically merge or silently choose prose instructions.
7. Repository files never override system, developer, direct user or enterprise/host policy. A subtree rule can specialize the shared project rule only within its scope.

## Static checks and tests

`python scripts/verify_project.py` now scans instruction candidates under the checkout for invalid UTF-8, empty content, oversized files and instruction symlinks that escape the checkout. It preserves v2.5 Skill registry, root standing-order and compatibility-entry-point checks.

`python -m unittest discover -s tests -p 'test_template_*.py' -v` exercises nested scopes, irrelevant siblings, local overlays, DSH duplicate folding, Codex replacement, Claude entry points, directory vs. file targets, traversal/symlink escapes, invalid sources and advisory budgets. Negative controls must fail for their intended reason.

## Host acceptance checklist

For the host(s) used by the consuming project, separately demonstrate a root task and a nested task: capture the sources the host reports, verify the nested instructions appear only in the intended scope, confirm a changed or removed instruction is eventually reflected according to that host's documented refresh behavior, and check delegated/subagent behavior when relevant. Never infer these runtime outcomes from CLI JSON alone. CI is an offline structural gate; human review and real host acceptance remain required.

This is an additive v2.5-to-v2.6 upgrade. `project-policy.json` retains schema 2 and production/release boundaries stay manual.
