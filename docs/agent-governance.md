# Agent governance

This document defines the repository contract for instruction files and Skills. It is intentionally independent of any model, editor or harness.

## Instruction hierarchy

Use the nearest applicable instruction files, from broad to specific:

1. Root AGENTS.md contains repository-wide standing orders. Keep it concise and link detailed rules to their owning documents.
2. A subtree AGENTS.md supplements the root only for that subtree. It may narrow ownership, commands, interfaces or failure rules, but must not silently contradict a broader instruction.
3. Tool compatibility files such as CLAUDE.md are entry points, not a second source of engineering policy. They point to AGENTS.md and may contain only tool-specific loading guidance that does not redefine repository rules.
4. Detailed standards, architecture documents and Skills own their respective facts. Do not copy a detailed rule into multiple instruction files just to make it easier to find.

When instructions conflict, resolve the conflict by scope and ownership: the more specific applicable rule may narrow the broader rule; a tool-specific compatibility file must not override repository engineering policy.

## Root AGENTS.md standard

The root file is the always-on entry point. It should contain only high-value standing orders: what must be read, what must be preserved, what evidence is required, and what delivery boundaries apply. Put examples, rationale, long procedures and technology-specific details in their owning documents.

Do not assign fixed responsibilities to a named model, editor or harness. A project can choose different agents for different tasks without changing the engineering contract.

## Subtree AGENTS.md standard

Add a subtree AGENTS.md only when that subtree has rules that are genuinely narrower than the repository-wide rules. State the scope, link the parent instructions, and keep the local rules focused on contracts that are easy to violate in that subtree.

Do not create nested AGENTS.md files merely to repeat the root. A new instruction file creates another precedence point and must earn that maintenance cost.

## CLAUDE.md and other compatibility entry points

When a tool-specific file exists because a host discovers it automatically, make it a compatibility shim to the shared AGENTS.md. Keep the engineering rules in AGENTS.md so Claude Code, Codex, Cursor, DSH and other compatible agents consume the same policy.

If a host requires additional syntax or loading guidance, keep that guidance local to the compatibility file and link back to the shared policy. Never use the compatibility file to assign a model-specific planner, implementer or reviewer role.

## Skill contract

A project Skill lives at .agents/skills/<name>/SKILL.md. The directory name and frontmatter name are the same lowercase kebab-case identifier. The description is the routing contract: it states when the Skill applies and the outcome or workflow it provides.

Keep full instructions in the Skill body. Do not paste the same workflow into AGENTS.md. A Skill may link to references inside its own directory or to authoritative repository documents.

The Skill registry at .agents/skills/README.md is the human-readable index. It must list every project Skill exactly once and point to its SKILL.md. The verifier discovers Skill directories from the filesystem, so adding a Skill never requires editing a Python allowlist.

## Skill authoring rules

- Use one Skill for one coherent task family.
- Keep the description specific enough for routing and short enough for discovery.
- Make prerequisites, workflow, verification and failure boundaries explicit when they matter.
- Do not silently require a particular model or editor.
- Do not claim a command or external integration works unless it was verified.
- When a Skill introduces an automated guard, add both a valid case and an invalid case that proves the guard rejects the intended violation.

## Change procedure

When changing AGENTS.md, CLAUDE.md, a subtree AGENTS.md or a Skill:

1. Identify the instruction scope and authoritative owner.
2. Check for duplicate or conflicting rules before editing.
3. Update the owner and registry together when a Skill is added, renamed or removed.
4. Run scripts/verify_project.py and the template contract tests.
5. Review the complete diff and report which checks actually ran.

The durable policy decision is recorded in [docs/decisions/2026-11-18-agent-governance.md](decisions/2026-11-18-agent-governance.md). The verifier treats these rules as executable governance. A green verifier proves structural consistency; it does not prove that a prose rule is complete or that a Skill's behavior is semantically correct.
