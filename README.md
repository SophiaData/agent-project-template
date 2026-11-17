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

## V2: initialize your repository

The template carries a versioned quality policy and safe cross-Agent roles.
After creating a repository, configure its name and stack:

```bash
python scripts/configure_project.py --name my-project --stack auto
python scripts/configure_project.py --name my-project --stack python --apply
python scripts/verify_project.py
python scripts/run_quality.py
```

The first command previews only; `--apply` updates placeholder project metadata.
Supported stacks: `generic`, `python`, `node`, `java`, `data`, `mixed`.
For Python, data and mixed projects, test commands cannot be assumed from the
technology alone. Add real `quality_checks` to `project-policy.json`, e.g.:

```json
{"category": "test", "argv": ["python", "-m", "pytest", "-q"]}
```

For recognized Node `package.json` test scripts and Java Maven projects,
configuration can suggest the corresponding test command. Validate it against
actual project dependencies before claiming a test passed. CI provides runtimes
for common stacks, but projects may need additional dependency setup.

Run `python -m unittest discover -s tests -p 'test_template_*.py' -v` to verify
the template itself. See [template upgrades](docs/template-upgrades.md) for
versioned, reviewable updates. A declared test command is not a proof of good
coverage; code review and real integration evidence remain necessary.
