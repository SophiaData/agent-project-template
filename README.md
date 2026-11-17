# PROJECT_NAME

Project type: **PROJECT_TYPE**.

This repository uses SophiaData cross-Agent engineering conventions:
- [AGENTS.md](AGENTS.md) — common rules for GPT, Claude Code, Codex and other Agents
- [docs/development.md](docs/development.md) — plan → implement → verify → review → PR
- [docs/testing.md](docs/testing.md) — actual test evidence and CI commands

## First task

When created through GitHub **Use this template**, replace the `PROJECT_NAME` and `PROJECT_TYPE` placeholders in `README.md` and `project-policy.json`. GitHub does not automatically substitute them.

1. Fill in the architecture reference and select the real stack.
2. Configure `project-policy.json` with actual quality commands, as token arrays.
3. Run `python scripts/verify_project.py` and `python scripts/run_quality.py`.
4. Add the correct runtime setup to `.github/workflows/quality.yml` for your stack (Node/Java/dbt/etc.), and use `.agents/skills/` for detailed workflows.

**Important:** this template is not an automatic DSH workflow engine. The agent must really call workers, CI and review tools; merging and publishing remain separate authorized operations.
