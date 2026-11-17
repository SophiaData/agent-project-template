# Testing policy

- `python scripts/verify_project.py` validates project instructions, skill metadata and local Markdown links.
- `python scripts/run_quality.py` runs configured commands in `project-policy.json` **without a shell**.
- An empty codebase can pass governance checks; when code appears, empty quality commands become an error.
- Add success, failure and relevant edge/regression cases; do not delete tests to silence failures.
- Treat `NOT RUN`, skipped tests and blocked integration tests honestly; never claim an installed runtime was validated by static checks alone.
- Record command, status, environment and evidence in every PR.

Stack examples (only use when applicable and installed): Python `python -m pytest -q`, Node `pnpm test`, Java `mvn test`, DBT `dbt test`. SQL engine tests require an appropriate isolated environment.
