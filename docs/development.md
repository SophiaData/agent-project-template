# Development workflow

Use the same evidence-based workflow for human and AI-assisted changes. The workflow is task-oriented; it does not prescribe which model, editor or agent performs a task.

## 1. Understand and plan

Inspect the repository, architecture, affected modules, callers, tests and deployment path. Establish scope, non-goals, owners, acceptance criteria, compatibility impact, security risks and rollback or recovery expectations before substantive implementation.

## 2. Design the smallest complete change

Prefer existing interfaces and extension points. Trace producers and consumers before adding fields, states, configuration, dependencies or abstractions. Explain why each new public choice is needed and what owns it. Read the applicable [defensive patterns](defensive-patterns/README.md) before implementing a change that matches one of their triggers.

## 3. Implement

Work on a focused branch or worktree. Keep changes local to the owning module. Add or update tests, API contracts, documentation and migration guidance with the implementation. Do not mix unrelated cleanup into a behavior change.

## 4. Verify

Choose checks based on the changed behavior and its real execution path. Run focused tests first, then the relevant type, lint, build, integration or compatibility checks. Run python scripts/verify_project.py and the configured checks where applicable. For committed branch changes, fetch the verified base and run `python scripts/run_quality.py --base origin/main` (replace `origin/main` with the actual base); omit `--base` to run all configured checks, including checks for uncommitted work. Record the selected checks, exact commands, exit status, environment and limitations. An unresolved Git diff must fail, not be interpreted as no changed files.

For a new or changed automated guard, add a negative-control test that introduces the intended violation and proves the guard rejects it. A successful run of only valid fixtures is not sufficient evidence for a guard.

A check that was skipped, blocked by missing infrastructure or not run must be reported as NOT RUN or BLOCKED. Static checks do not prove runtime integration. Do not repeat an already passing expensive check solely because a commit or push occurred unless its inputs changed.

## 5. Review

Inspect the actual diff against the base branch and acceptance criteria. Review surrounding code, error paths, security, data integrity, compatibility, concurrency, tests and documentation. Apply relevant defensive patterns. Independent review is required for material changes; a model's self-reported PASS is not sufficient evidence.

## 6. Deliver

Open a PR with motivation, scope, design, compatibility, test evidence and remaining risks. Wait for required CI and human approval. PR creation, a green CI run or an AI review does not authorize merge, deployment, release or publication.

## Local setup and quality commands

Use the runtime and package manager declared by the actual project. Do not assume a tool exists because a stack was detected. Configure project-specific quality commands in project-policy.json and ensure CI installs the required dependencies and services.

For this template:

~~~sh
python scripts/verify_project.py
python -m unittest discover -s tests -p 'test_template_*.py' -v
python scripts/run_quality.py
~~~

## Project initialization and template upgrades

Preview project metadata before applying it:

~~~sh
python scripts/configure_project.py --name my-project --stack auto
python scripts/configure_project.py --name my-project --stack python --apply
~~~

The template version is recorded in TEMPLATE_VERSION and project-policy.json. Existing projects upgrade through a reviewed diff, never by blind overwrite. See docs/template-upgrades.md.
