---
name: project-agent-governance
description: Use when adding, changing, reviewing or auditing AGENTS.md files, tool compatibility instructions or project Skills; keeps instruction ownership, Skill metadata and the registry consistent across coding agents.
---

# Agent governance workflow

1. Read AGENTS.md and docs/agent-governance.md before changing instruction files or Skills.
2. Map each rule to one authoritative owner and inspect nearby AGENTS.md files for narrower or conflicting instructions.
3. For a changed file, run `python scripts/instruction_chain.py --target <relative-path> --profile shared` and the relevant host profiles (`dsh`, `codex`, `claude`). Compare scope, skipped candidates, local overlays and Codex replacements; record semantic conflicts as unresolved until reviewed. A preflight is not host runtime evidence.
4. For Skills, verify the directory name, frontmatter name and description, workflow body, internal references and registry entry.
5. Keep compatibility files such as CLAUDE.md as thin entry points; do not create a second engineering policy or assign fixed model roles.
6. When adding or renaming a Skill, update .agents/skills/README.md in the same change and preserve one registry entry per Skill.
7. Run python scripts/verify_project.py and the template contract tests. Add an invalid fixture when changing a governance guard so the guard's failure path is demonstrated.
8. Review the complete diff and report structural PASS/FAIL separately from semantic review or unrun host-specific checks.
