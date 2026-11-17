# PROJECT_NAME

Project type: **PROJECT_TYPE**.

This repository is a reusable, stack-neutral engineering standards baseline. It provides project architecture guidance, coding and testing standards, documentation and compatibility practices, reusable engineering workflows, and executable quality checks.

## Standards map

- **AGENTS.md** — concise repository-wide engineering rules for every contributor and coding assistant.
- **docs/architecture.md** — system boundaries, module ownership, dependencies and runtime topology.
- **docs/coding-standards.md** — language-neutral coding and design principles.
- **docs/standards/** — technology-specific standards for Python, TypeScript, Java and data engineering.
- **docs/development.md** — plan, implement, verify, review and deliver workflow.
- **docs/testing.md** — test levels, reliability and evidence requirements.
- **docs/error-handling.md** — failure ownership, cancellation, retries and reporting.
- **docs/documentation.md** — documentation placement and maintenance.
- **docs/compatibility.md** — API, schema, persistence and upgrade policy.
- **docs/git-workflow.md** and **CONTRIBUTING.md** — branch, commit and pull-request conventions.
- **docs/decisions/** — durable architecture and engineering decisions.
- **.agents/skills/** — reusable task workflows; they do not assign work to a particular model or agent.
- **scripts/** and **.github/workflows/** — executable governance checks and CI.

## Initialize a repository created from this template

GitHub Template repositories copy files; they do not substitute placeholders automatically.

1. Configure the project identity and detect the stack:
   ~~~sh
   python scripts/configure_project.py --name my-project --stack auto
   ~~~
2. Review the preview. Apply only when correct:
   ~~~sh
   python scripts/configure_project.py --name my-project --stack python --apply
   ~~~
3. Complete docs/architecture.md with the actual system boundaries and module ownership.
4. Configure real quality checks in project-policy.json. Use token arrays, not shell command strings.
5. Configure the CI runtime, dependency installation, credentials and service fixtures required by the actual project.
6. Run the template checks:
   ~~~sh
   python scripts/verify_project.py
   python -m unittest discover -s tests -p 'test_template_*.py' -v
   python scripts/run_quality.py
   ~~~

Supported project classifications: generic, python, node, java, data and mixed. The classification is descriptive; use the technology-specific standards that match the code actually present.

## Quality policy

The project policy keeps the V2 schema and typed quality-check format. Once application source exists, at least one real test check is required. The runner executes argv arrays without a shell and rejects obvious no-op commands; it cannot prove that a test suite is meaningful. Review the test design and CI environment as well as the exit code.

A project may add lint, typecheck, build, SQL validation and other checks that its actual toolchain supports. Do not declare a check merely to make the policy green.

## Template updates

The template is a versioned starting point, not a remote synchronization mechanism. Existing projects keep their local decisions and customizations. Upgrade through a dedicated reviewed PR, compare the old and new versions, and preserve local changes. See docs/template-upgrades.md.

Production deployment, release, publishing, database migration and production DataWorks node submission or publication remain separately authorized operations. A passing CI run does not authorize them.
